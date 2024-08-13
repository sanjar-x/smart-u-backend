from enum import Enum
from uuid import UUID
from datetime import date
from typing import Annotated, Optional, List
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


class GroupCreate(Group):
    tutor_id: UUID
    department_id: UUID


class ImageResponse(BaseModel):
    model_config = config
    file_path: FilePath


class UserResponse(BaseModel):
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


class DepartmentResponse(BaseModel):
    name: str


class GroupResponse(Group):
    id: UUID = Field(title="User’s id", description="User’s id")
    students: List[UserResponse]
    tutor: UserResponse
    department: DepartmentResponse
