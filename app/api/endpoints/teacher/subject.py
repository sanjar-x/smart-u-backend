from typing import List, Optional, Union
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status

from ...dependencies.session import get_session
from ....schemas.subject import SubjectCreate, SubjectResponse
from ....core.models import Subject

subject_router = APIRouter(prefix="/subjects")


@subject_router.get("/")
async def get_subjects(
    query: str | None = None,
    session: AsyncSession = Depends(get_session),
):
    subject = Subject()
    if query:
        return await subject.search_by(session, query)
    else:
        return await subject.get_all(session)
