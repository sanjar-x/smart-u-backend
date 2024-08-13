from __future__ import annotations
from enum import Enum
from uuid import UUID
from datetime import date, time
from typing import Annotated, Optional, List
from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    ConfigDict,
    SecretStr,
    StringConstraints,
    constr,
)


config = ConfigDict(from_attributes=True)


class Slot(BaseModel):
    model_config = config
    start_time: time
    end_time: time


class SlotCreate(Slot):
    pass


class SlotResponse:
    id: UUID = Field(title="Slot's id", description="Slot's id")
