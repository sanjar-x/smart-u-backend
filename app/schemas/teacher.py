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
    file_path: FilePath


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
    specialization: str
    image: ImageResponse
