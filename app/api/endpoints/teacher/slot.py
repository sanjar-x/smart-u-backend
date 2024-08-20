from logging import getLogger

logger = getLogger("uvicorn")
from typing import List, Optional, Union
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, HTTPException, status
from ...dependencies.session import get_session
from ....schemas.slot import SlotCreate
from ....core.models import Slot
from ....services.tasks.scheduler import scheduler
from ....services.tasks.pair_tasks import pair_starter, pair_ender

slot_router = APIRouter(prefix="/slots")


@slot_router.get("/")
async def get_slots(
    session: AsyncSession = Depends(get_session),
):
    subject = Slot()
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
