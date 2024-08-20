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

teacher_router = APIRouter(prefix="/teachers")

UPLOAD_DIR = "static/users/"


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
