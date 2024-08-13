from __future__ import annotations
from enum import Enum
from uuid import UUID
from datetime import date, time
from typing import Annotated, Optional, List
from pydantic import (
    BaseModel,
    Field,
    FilePath,
    IPvAnyAddress,
    ConfigDict,
    SecretStr,
    StringConstraints,
    constr,
)


config = ConfigDict(from_attributes=True)


class Pair(BaseModel):
    model_config = config


class PairCreate(Pair):
    room_id: UUID
    slot_id: UUID
    teacher_id: UUID
    subject_id: UUID
    groups: List[UUID]
    start_date: date
    end_date: date


class CameraResponse(BaseModel):
    model_config = config
    ip: IPvAnyAddress


class RoomResponse(BaseModel):
    model_config = config
    name: str
    cameras: List[CameraResponse]


class SlotResponse(BaseModel):
    model_config = config
    start_time: time
    end_time: time


class ImageResponse(BaseModel):
    model_config = config
    file_path: FilePath


class UserResponse(BaseModel):
    model_config = config
    id: UUID
    pini: str
    first_name: str
    last_name: str
    middle_name: Optional[str]
    birth_date: date
    phone_number: str
    active: bool
    address: str
    specialization: str
    image: ImageResponse


class SubjectResponse(BaseModel):
    model_config = config
    name: str


class GroupType(str, Enum):
    day = "day"
    night = "night"
    part = "part"


class GroupResponse(BaseModel):
    model_config = config
    name: str
    type: GroupType


class PairResponse(Pair):

    slot: SlotResponse
    room: RoomResponse

    teacher: UserResponse
    subject: SubjectResponse
    groups: List[GroupResponse]


class DateResponse(BaseModel):
    date: date
    pairs: List[PairResponse]
