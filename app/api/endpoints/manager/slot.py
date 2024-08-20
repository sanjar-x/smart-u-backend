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


@slot_router.post("/")
async def create_slot(
    data: SlotCreate,
    session: AsyncSession = Depends(get_session),
):
    new_slot = Slot(start_time=data.start_time, end_time=data.end_time)

    if await new_slot.exist_time(session):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This time is already registred",
        )
    saved_slot = await new_slot.save(session)

    scheduler.add_job(
        pair_starter,
        "cron",
        hour=saved_slot.start_time.hour,
        minute=saved_slot.start_time.minute,
        second=saved_slot.start_time.second,
        args=[saved_slot.id],
    )
    logger.info(
        f"Pair starter job scheduled to: {saved_slot.start_time.hour}:{saved_slot.start_time.minute}"
    )
    scheduler.add_job(
        pair_ender,
        "cron",
        hour=saved_slot.end_time.hour,
        minute=saved_slot.end_time.minute,
        second=saved_slot.end_time.second,
        args=[saved_slot.id],
    )
    logger.info(
        f"Pair ender job scheduled to: {saved_slot.end_time.hour}:{saved_slot.end_time.minute}"
    )

    return saved_slot


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


@slot_router.delete("/")
async def delete_slot(
    id: UUID | None = None,
    session: AsyncSession = Depends(get_session),
):
    subject = Slot(id=id)
    return await subject._delete(session)
