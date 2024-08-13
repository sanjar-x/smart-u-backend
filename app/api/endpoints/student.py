import os
from uuid import UUID
from typing import List, Optional, Union
from datetime import date
from pydantic import SecretStr
from sqlalchemy.ext.asyncio import AsyncSession
from PIL import UnidentifiedImageError, Image as PILImage
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from ..dependencies.session import get_session
from ...schemas.student import StudentResponse
from ...core.models import Student, Image, User
from ...services.detector.face import check_face

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
    return {
        "info": f"{saved_student.first_name}'s image saved at {student_image.file_path}"
    }


@student_router.get(
    "/",
    response_model=Union[
        Optional[StudentResponse],
        List[StudentResponse],
    ],
)
async def get_students(
    query: str | None = None,
    session: AsyncSession = Depends(get_session),
):
    student = Student()
    if query:
        return await student.search_by(session, query)
    else:
        return await student.get_all_with_image_and_group(session)


@student_router.delete("/")
async def delete_student(
    id: UUID | None = None,
    session: AsyncSession = Depends(get_session),
):
    user = User(id=id)
    await user.get_with_image(session)
    os.remove(os.path.join(UPLOAD_DIR, user.image.file_name))
    await user._delete(session)
    return {"detail": "teacher deleted"}
