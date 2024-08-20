import os
from uuid import UUID
from typing import List, Optional, Union
from datetime import date
from pydantic import SecretStr
from sqlalchemy.ext.asyncio import AsyncSession
from PIL import UnidentifiedImageError, Image as PILImage
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from ...dependencies.session import get_session
from ....schemas.student import StudentResponse
from ....core.models import Student, Image, User, Group
from ....services.detector.face import check_face

student_router = APIRouter(prefix="/students")

UPLOAD_DIR = "static/users/"


@student_router.get(
    "/",
    response_model=Union[
        StudentResponse,
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
