from typing import List, Optional, Union
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status
from ...dependencies.session import get_session
from ....schemas.room import RoomCreate, RoomResponse
from ....core.models import Room, Camera

room_router = APIRouter(prefix="/rooms")


@room_router.get("/", response_model=List[RoomResponse])
async def get_rooms(
    query: str | None = None,
    session: AsyncSession = Depends(get_session),
):
    room = Room()
    if query:
        return await room.search_by(session, query)
    else:
        return await room.get_all_with_cameras(session)
