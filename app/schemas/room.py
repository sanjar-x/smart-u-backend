from enum import Enum
from uuid import UUID, uuid4
from datetime import date
from typing import Annotated, List, Optional

from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    ConfigDict,
    SecretStr,
    StringConstraints,
    constr,
    IPvAnyAddress,
)


config = ConfigDict(from_attributes=True)


class Camera(BaseModel):
    model_config = config
    ip: IPvAnyAddress


class CameraCreate(Camera):
    password: str


class CameraResponse(Camera):
    id: UUID = Field(title="Camera’s id", description="Camera’s id")


class Room(BaseModel):
    model_config = config
    name: str


class RoomCreate(Room):
    cameras: List[CameraCreate]


class RoomResponse(Room):
    id: UUID = Field(title="Room’s id", description="Room’s id")
    cameras: List[CameraResponse]
