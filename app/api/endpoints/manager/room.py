from typing import List, Optional, Union
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status
from ...dependencies.session import get_session
from ....schemas.room import RoomCreate, RoomResponse
from ....core.models import Room, Camera

room_router = APIRouter(prefix="/rooms")


@room_router.post("/")
async def create_room(
    data: RoomCreate,
    session: AsyncSession = Depends(get_session),
):
    new_room = Room(**data.model_dump(exclude={"cameras"}))
    if await new_room.exist_name(session):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This room is already registred",
        )
    saved_room = await new_room.save(session)
    for camera in data.cameras:
        new_camera = Camera(
            room_id=saved_room.id, ip=camera.ip, password=camera.password
        )
        if await new_camera.exist_camera(session):
            await saved_room._delete(session)
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This camera is already registred",
            )
        saved_camera = await new_camera.save(session)
    return saved_room


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


@room_router.delete("/")
async def delete_room(
    id: UUID,
    session: AsyncSession = Depends(get_session),
):
    room = Room(id=id)
    return await room._delete(session)
