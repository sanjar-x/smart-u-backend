from datetime import timedelta
from typing import List, Optional, Union
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status
from ...dependencies.session import get_session
from ....schemas.pair import PairCreate, DateResponse, PairResponse
from ....core.models import (
    Pair,
    Date,
    Group,
    Room,
    Slot,
    Teacher,
    Subject,
)

pair_router = APIRouter(prefix="/pairs")


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
