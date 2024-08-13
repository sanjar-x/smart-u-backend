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


class Resource(BaseModel):
    model_config = config
    name: str


class ResourceCreate(Resource):
    pass


class ResourceResponse(Resource):
    id: UUID = Field(title="Resource's id", description="Resource's id")
