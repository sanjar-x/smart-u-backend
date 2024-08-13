from datetime import timedelta
from typing import List, Optional, Union
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status
from ..dependencies.session import get_session
from ...schemas.pair import PairCreate, DateResponse, PairResponse
from ...core.models import (
    Pair,
    Date,
    Group,
    Room,
    Slot,
    Teacher,
    Subject,
)

pair_router = APIRouter(prefix="/pairs")


@pair_router.post("/")
async def create_pairs(
    data: PairCreate,
    session: AsyncSession = Depends(get_session),
):

    room = Room(id=data.room_id)
    if not await room.exist(session):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Room not found"
        )
    slot = Slot(id=data.slot_id)
    if not await slot.exist(session):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Slot not found"
        )
    teacher = Teacher(id=data.teacher_id)
    if not await teacher.exist(session):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found"
        )
    subject = Subject(id=data.subject_id)
    if not await subject.exist(session):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Subject not found"
        )
    groups = []
    for group_id in data.groups:
        group_obj = Group(id=group_id)
        if await group_obj.exist(session):
            groups.append(group_obj)

    weekday = data.start_date.weekday()
    current_date = data.start_date
    while current_date <= data.end_date:
        if current_date.weekday() == weekday:
            date = Date(date=current_date)
            if not await date.get_by_date(session):
                date = await date.save(session)
            print(date.id)
            new_pair = Pair(
                date_id=date.id,
                room_id=data.room_id,
                slot_id=data.slot_id,
                teacher_id=data.teacher_id,
                subject_id=data.subject_id,
            )
            saved_pair = await new_pair.save(session)
            await saved_pair.add_groups(session, groups)
        current_date += timedelta(days=1)

    return {"detail": "You have successfully created pair"}


@pair_router.get("/", response_model=List[DateResponse])
async def get_pairs(
    group_id: UUID,
    year: int | None = None,
    month: int | None = None,
    session: AsyncSession = Depends(get_session),
):
    date = Date()
    date_pairs = await date.get_by_year_and_month(session, group_id, year, month)
    return date_pairs


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


@pair_router.delete("/")
async def delete_pair(
    id: UUID | None = None,
    session: AsyncSession = Depends(get_session),
):
    pair = Pair(id=id)
    return await pair._delete(session)
