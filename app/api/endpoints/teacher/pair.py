from datetime import date
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from ....services.auth.user import get
from ...dependencies.session import get_session
from ....schemas.pair import PairResponse
from ....core.models import (
    Slot,
    Date,
    Pair,
    Teacher,
)

pair_router = APIRouter(prefix="/pairs")


@pair_router.get("/", response_model=List[PairResponse])
async def get_pairs(
    date: date,
    current_teacher: Teacher = Depends(get),
    session: AsyncSession = Depends(get_session),
):
    pair_date = Date(date=date)
    await pair_date.get_by_date(session)
    pair = Pair(date_id=pair_date.id, teacher_id=current_teacher.id)
    date_pairs = await pair.get_all_by_teacher(session)
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
