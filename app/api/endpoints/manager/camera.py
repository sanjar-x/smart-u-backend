from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status
from ...dependencies.session import get_session
from ....core.models import Camera
from ....schemas.camera import CameraCreate


camera_router = APIRouter(prefix="/camera")


@camera_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_camera(
    data: CameraCreate,
    session: AsyncSession = Depends(get_session),
):
    new_camera = Camera(ip=data.ip)
    saved_camera = await new_camera.save(session)
    return saved_camera


@camera_router.get("/", status_code=status.HTTP_200_OK)
async def get_cameras(
    session: AsyncSession = Depends(get_session),
):
    camera = Camera()
    cameras = await camera.get_all(session)
    return cameras


@camera_router.delete("/", status_code=status.HTTP_200_OK)
async def delete_camera(
    id: str,
    session: AsyncSession = Depends(get_session),
):
    camera = Camera(id=id)
    await camera._delete(session)
    return True
