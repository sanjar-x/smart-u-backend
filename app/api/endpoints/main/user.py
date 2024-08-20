from __future__ import annotations
import os
from uuid import UUID
from typing import List
from datetime import date
from pydantic import SecretStr
from sqlalchemy.ext.asyncio import AsyncSession
from PIL import UnidentifiedImageError, Image as PILImage
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from ...dependencies.session import get_session
from ....schemas.user import (
    UserResponse,
    UserRoleResponse,
    UserRolePermissionsResourceResponse,
)
from ....core.models import User, Image
from ....services.detector.face import check_face

user_router = APIRouter(prefix="/users")

UPLOAD_DIR = "static/users/"


@user_router.post("/")
async def create_user(
    role_id: UUID = Form(...),
    pini: str = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    middle_name: str = Form(...),
    birth_date: date = Form(...),
    phone_number: str = Form(...),
    address: str = Form(...),
    password: SecretStr = Form(...),
    upload_image: UploadFile = File(...),
    session: AsyncSession = Depends(get_session),
):
    new_user: User = User(
        role_id=role_id,
        pini=pini,
        first_name=first_name,
        last_name=last_name,
        middle_name=middle_name,
        birth_date=birth_date,
        phone_number=phone_number,
        address=address,
    )
    await new_user.hach_password(password)
    saved_user: User = await new_user.save(session)
    if not upload_image.filename:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Uploaded file is not a valid image",
        )
    image_filename = f"{saved_user.id}{os.path.splitext(upload_image.filename)[1]}"
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
    user_image = Image(
        id=saved_user.id,
        file=await upload_image.read(),
        file_name=image_filename,
        file_path=image_file_path,
    )
    await user_image.save(session)
    return {"info": f"{saved_user.first_name}'s image saved at {user_image.file_path}"}


@user_router.get("/")
async def get_users(
    session: AsyncSession = Depends(get_session),
):
    user = User()
    users = await user.get_all(session)
    return users
