from typing import List, Optional, Union
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status
from ...dependencies.session import get_session
from ....schemas.group import GroupCreate, GroupResponse
from ....core.models import Group, User, Department

group_router = APIRouter(prefix="/groups")


@group_router.get("/", response_model=List[GroupResponse])
async def get_groups(
    query: str | None = None,
    session: AsyncSession = Depends(get_session),
):

    group = Group()
    if query:
        return await group.search_by(session, query)
    else:
        return await group.get_all_with_department_and_tutor_and_students(session)
