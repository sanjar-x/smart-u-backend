from __future__ import annotations
from enum import Enum
from uuid import UUID
from datetime import date
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


class Subject(BaseModel):
    model_config = config
    name: str


class SubjectCreate(Subject):
    pass


class SubjectResponse(Subject):
    id: UUID = Field(title="Resource's id", description="Resource's id")
