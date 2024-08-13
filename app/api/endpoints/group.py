from typing import List, Optional, Union
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status
from ..dependencies.session import get_session
from ...schemas.group import GroupCreate, GroupResponse
from ...core.models import Group, User, Department

gruop_router = APIRouter(prefix="/groups")


@gruop_router.post("/")
async def create_group(
    data: GroupCreate,
    session: AsyncSession = Depends(get_session),
):
    new_group = Group(**data.model_dump())
    if await new_group.exist_name(session):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This group is already registred",
        )
    tutor = User(id=data.tutor_id)
    if not await tutor.get(session):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tutor not found",
        )
    if not tutor.type in ["manager", "teacher"]:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Tutor must be manager or teacher",
        )
    department = Department(id=data.department_id)
    if not await department.get(session):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found",
        )

    saved_group = await new_group.save(session)
    return saved_group


@gruop_router.get("/", response_model=List[GroupResponse])
async def get_groups(
    query: str | None = None,
    session: AsyncSession = Depends(get_session),
):

    group = Group()
    if query:
        return await group.search_by(session, query)
    else:
        return await group.get_all_with_department_and_tutor_and_students(session)


@gruop_router.delete("/")
async def delete_group(
    id: UUID | None = None,
    session: AsyncSession = Depends(get_session),
):
    group = Group(id=id)
    return await group._delete(session)
