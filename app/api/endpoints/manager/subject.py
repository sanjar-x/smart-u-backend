from typing import List, Optional, Union
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status

from ...dependencies.session import get_session
from ....schemas.subject import SubjectCreate, SubjectResponse
from ....core.models import Subject

subject_router = APIRouter(prefix="/subjects")


@subject_router.post("/")
async def create_subject(
    data: SubjectCreate,
    session: AsyncSession = Depends(get_session),
):
    new_subject = Subject(name=data.name)

    if await new_subject.exist_name(session):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This subject is already registred",
        )
    saved_subject = await new_subject.save(session)
    return saved_subject


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


# @room_router.get("/", response_model=Union[Optional[RoomResponse], List[RoomResponse]])
# async def get_rooms(
#     query: str | None = None,
#     session: AsyncSession = Depends(get_session),
# ):
#     room = Room()
#     if query:
#         return await room.search_by(session, query)
#     else:
#         return await room.get_all_with_cameras(session)


@subject_router.delete("/")
async def delete_subject(
    id: UUID | None = None,
    session: AsyncSession = Depends(get_session),
):
    subject = Subject(id=id)
    return await subject._delete(session)
