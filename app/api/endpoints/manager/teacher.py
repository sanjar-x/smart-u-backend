import os
from uuid import UUID
from typing import List, Optional, Union
from datetime import date

from pydantic import SecretStr
from sqlalchemy.ext.asyncio import AsyncSession
from PIL import UnidentifiedImageError, Image as PILImage
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from ...dependencies.session import get_session
from ....schemas.teacher import TeacherResponse
from ....core.models import Teacher, Image, User
from ....services.detector.face import check_face
from ....services.tasks.initialization import (
    detector_engine_start,
    detector_engine_shutdown,
)

teacher_router = APIRouter(prefix="/teachers")

UPLOAD_DIR = "static/users/"


@teacher_router.post("/")
async def create_teacher(
    pini: str = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    middle_name: Optional[str] = Form(...),
    birth_date: date = Form(...),
    phone_number: str = Form(...),
    address: str = Form(...),
    password: SecretStr = Form(...),
    specialization: str = Form(...),
    upload_image: UploadFile = File(...),
    session: AsyncSession = Depends(get_session),
):
    # Create the new Teacher instance
    new_teacher = Teacher(
        pini=pini,
        first_name=first_name,
        last_name=last_name,
        middle_name=middle_name,
        birth_date=birth_date,
        phone_number=phone_number,
        address=address,
        specialization=specialization,
    )
    await new_teacher.hach_password(password)
    saved_teacher: Teacher = await new_teacher.save(session)

    if not upload_image.filename:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="No image uploaded",
        )

    image_extension = os.path.splitext(upload_image.filename)[1]
    image_filename = f"{saved_teacher.id}{image_extension}"
    image_file_path = os.path.join(UPLOAD_DIR, image_filename)

    with open(image_file_path, "wb") as image_file:
        image_file.write(await upload_image.read())

    try:
        image = PILImage.open(image_file_path)
        image.verify()
    except UnidentifiedImageError:
        os.remove(image_file_path)
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Uploaded file is not a valid image",
        )

    await check_face(image_file_path)
    teacher_image = Image(
        id=saved_teacher.id,
        file=await upload_image.read(),
        file_name=image_filename,
        file_path=image_file_path,
    )
    await teacher_image.save(session)
    # await detector_engine_shutdown()
    # await detector_engine_start()
    return {
        "info": f"{saved_teacher.first_name}'s image saved at {teacher_image.file_path}"
    }


@teacher_router.get(
    "/",
    response_model=Union[
        Optional[TeacherResponse],
        List[TeacherResponse],
    ],
)
async def get_teacher(
    query: str | None = None,
    session: AsyncSession = Depends(get_session),
):
    teacher = Teacher()
    if query:
        return await teacher.search_by(session, query)
    else:
        return await teacher.get_all_with_image(session)


@teacher_router.delete("/")
async def delete_teacher(
    id: UUID | None = None,
    session: AsyncSession = Depends(get_session),
):
    user = User(id=id)
    await user.get_with_image(session)
    if user.image:
        os.remove(os.path.join(UPLOAD_DIR, user.image.file_name))
    await user._delete(session)
    return {"detail": "teacher deleted"}
