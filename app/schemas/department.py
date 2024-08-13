from __future__ import annotations
from enum import Enum
from uuid import UUID
from datetime import date
from typing import Annotated, Optional, List
from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    FilePath,
    ConfigDict,
    SecretStr,
    StringConstraints,
    constr,
)

config = ConfigDict(from_attributes=True)


class Department(BaseModel):
    model_config = config
    name: str


class DepartmentCreate(Department):
    model_config = config
    manager_id: UUID
    name: str


class ImageResponse(BaseModel):
    model_config = config
    file_path: FilePath


class ManagerResponse(BaseModel):
    model_config = config
    id: UUID = Field(title="Manager’s id", description="Manager’s id")
    pini: str = Field(
        title="Manager’s pini",
        description="Manager’s pini",
        examples=["12345678901234"],
    )
    first_name: str = Field(
        title="Manager’s first name",
        description="Manager’s first name",
        examples=["Anvar"],
    )
    last_name: str = Field(
        title="Manager’s last name",
        description="Manager’s last name",
        examples=["Anvarov"],
    )
    middle_name: Optional[str] = Field(
        title="Manager’s middle name",
        description="Manager’s middle name",
        examples=["Anvarovich"],
    )
    birth_date: date
    phone_number: str = Field(
        title="Manager’s phone number",
        description="Manager’s phone number",
        examples=["+998901234567"],
    )
    active: bool = Field(
        title="Checkbox",
        description="Manager status",
        examples=[True, False],
    )
    address: str = Field(
        title="Manager’s address",
        description="Manager’s address",
        examples=[
            "Namangan viloyati, Turaqo'rg'on tumani, Sharq MFY, Bog' ko'cha 18-uy"
        ],
    )
    image: ImageResponse | None


class TeacherResponse(BaseModel):
    model_config = config
    id: UUID = Field(title="Teacher’s id", description="Teacher’s id")
    pini: str = Field(
        title="Teacher’s pini",
        description="Teacher’s pini",
        examples=["12345678901234"],
    )
    first_name: str = Field(
        title="Teacher’s first name",
        description="Teacher’s first name",
        examples=["Anvar"],
    )
    last_name: str = Field(
        title="Teacher’s last name",
        description="Teacher’s last name",
        examples=["Anvarov"],
    )
    middle_name: Optional[str] = Field(
        title="Teacher’s middle name",
        description="Teacher’s middle name",
        examples=["Anvarovich"],
    )
    birth_date: date
    phone_number: str = Field(
        title="Teacher’s phone number",
        description="Teacher’s phone number",
        examples=["+998901234567"],
    )
    active: bool = Field(
        title="Checkbox",
        description="Teacher status",
        examples=[True, False],
    )
    address: str = Field(
        title="Teacher’s address",
        description="Teacher’s address",
        examples=[
            "Namangan viloyati, Turaqo'rg'on tumani, Sharq MFY, Bog' ko'cha 18-uy"
        ],
    )
    image: ImageResponse | None


class GroupType(str, Enum):
    day = "day"
    night = "night"
    part = "part"


class GroupResponse(BaseModel):
    model_config = config
    name: str = Field(
        title="Group's name", description="Group's name", examples=["B1234"]
    )
    type: GroupType = Field(
        title="Group's type",
        description="Group's type",
        examples=["day", "night", "part"],
    )


class DepartmentResponse(BaseModel):
    id: UUID
    name: str
    manager: Optional[ManagerResponse] = None
    teachers: List[TeacherResponse] = []
    groups: List[GroupResponse] = []
