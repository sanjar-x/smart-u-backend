import os
from uuid import UUID
from typing import List, Optional, Union
from datetime import datetime, date
from pydantic import SecretStr
from sqlalchemy.ext.asyncio import AsyncSession
from PIL import UnidentifiedImageError, Image as PILImage
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from ...dependencies.session import get_session
from ....schemas.student import StudentResponse
from ....core.models import (
    Resource,
    Permissions,
    Image,
    User,
    Group,
    Student,
    Camera,
    Detection,
)
from ....services.detector.face import check_face
from ....services.tasks.initialization import (
    detector_engine_start,
    detector_engine_shutdown,
)
from ....services.cache.redis.client import client

student_router = APIRouter(prefix="/students")

UPLOAD_DIR = "static/users/"


@student_router.post("/")
async def create_student(
    pini: str = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    middle_name: Optional[str] = Form(...),
    birth_date: date = Form(...),
    phone_number: str = Form(...),
    address: str = Form(...),
    password: SecretStr = Form(...),
    upload_image: UploadFile = File(...),
    group_id: UUID = Form(...),
    session: AsyncSession = Depends(get_session),
):
    group = Group(id=group_id)
    if not await group.exist(session):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found",
        )
    new_student = Student(
        group_id=group_id,
        pini=pini,
        first_name=first_name,
        last_name=last_name,
        middle_name=middle_name,
        birth_date=birth_date,
        phone_number=phone_number,
        address=address,
    )
    await new_student.hach_password(password)
    saved_student: Student = await new_student.save(session)
    if not upload_image.filename:
        await new_student._delete(session)
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Uploaded file is not a valid image",
        )
    image_filename = f"{saved_student.id}{os.path.splitext(upload_image.filename)[1]}"
    image_file_path = f"{UPLOAD_DIR}{image_filename}"

    with open(image_file_path, "wb") as image_file:
        image_file.write(await upload_image.read())
    try:
        image = PILImage.open(image_file_path)
        image.verify()
    except UnidentifiedImageError:
        os.remove(image_file_path)
        await new_student._delete(session)
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Uploaded file is not a valid image",
        )
    await check_face(image_file_path)
    student_image = Image(
        id=saved_student.id,
        file=await upload_image.read(),
        file_name=image_filename,
        file_path=image_file_path,
    )
    await student_image.save(session)
    await detector_engine_shutdown()
    await detector_engine_start()
    return {
        "info": f"{saved_student.first_name}'s image saved at {student_image.file_path}"
    }


@student_router.get(
    "/",
    response_model=List[StudentResponse],
)
async def get_students(
    query: str | None = None,
    session: AsyncSession = Depends(get_session),
):
    camera = Camera()
    cameras = await camera.get_all_with_rooms(session)
    student = Student()
    if query:
        students = await student.search_by(session, query)
    else:
        students = await student.get_all_with_image_and_group(session)
    for camera in cameras:
        for student in students:
            detection = Detection(camera_id=camera.id, user_id=student.id)
            key = f"detections:camera:{camera.id}:user:{student.id}"
            last_time = await detection.get_last(session)
            if last_time:
                results = await client.zrangebyscore(key, last_time.timestamp(), "+inf")
            else:
                results = await client.zrangebyscore(key, "-inf", "+inf")
            for result in results:
                new_detection = Detection(
                    camera_id=camera.id,
                    user_id=student.id,
                    time=datetime.fromtimestamp(float(result)),
                )
                await new_detection.save(session)
                await client.zrem(key, result)
    return students


@student_router.delete("/")
async def delete_student(
    id: UUID | None = None,
    session: AsyncSession = Depends(get_session),
):
    user = User(id=id)
    student = Student(id=id)
    await user.get_with_image(session)
    if user.image:
        await user.image._delete(session)
        # os.remove(os.path.join(UPLOAD_DIR, user.image.file_name))
    await user._delete(session)
    await student._delete(session)

    return {"detail": "student deleted"}
