from enum import Enum
from uuid import UUID
from datetime import date
from typing import Annotated, List, Optional

from pydantic import (
    BaseModel,
    Field,
    FilePath,
    EmailStr,
    ConfigDict,
    SecretStr,
    StringConstraints,
    constr,
)


config = ConfigDict(from_attributes=True)


class ImageResponse(BaseModel):
    model_config = config
    file_path: str


class GroupType(str, Enum):
    day = "day"
    night = "night"
    part = "part"


class Group(BaseModel):
    model_config = config
    name: str = Field(
        title="Group's name", description="Group's name", examples=["B1234"]
    )
    type: GroupType = Field(
        title="Group's type",
        description="Group's type",
        examples=["day", "night", "part"],
    )


class GroupResponse(Group):
    id: UUID = Field(title="User’s id", description="User’s id")


class StudentResponse(BaseModel):
    model_config = config
    id: UUID = Field(title="Student’s id", description="Student’s id")
    pini: str = Field(
        title="Student’s pini",
        description="Student’s pini",
        examples=["12345678901234"],
    )
    first_name: str = Field(
        title="Student’s first name",
        description="Student’s first name",
        examples=["Anvar"],
    )
    last_name: str = Field(
        title="Student’s last name",
        description="Student’s last name",
        examples=["Anvarov"],
    )
    middle_name: Optional[str] = Field(
        title="Student’s middle name",
        description="Student’s middle name",
        examples=["Anvarovich"],
    )
    birth_date: date
    phone_number: str = Field(
        title="Student’s phone number",
        description="Student’s phone number",
        examples=["+998901234567"],
    )
    active: bool = Field(
        title="Checkbox",
        description="Student status",
        examples=[True, False],
    )
    address: str = Field(
        title="Student’s address",
        description="Student’s address",
        examples=[
            "Namangan viloyati, Turaqo'rg'on tumani, Sharq MFY, Bog' ko'cha 18-uy"
        ],
    )
    image: ImageResponse | None
    group: Optional[GroupResponse]
