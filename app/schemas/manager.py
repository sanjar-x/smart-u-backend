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


class ResourceResponse(BaseModel):
    name: str


class PermissionsResponse(BaseModel):
    model_config = config
    create: bool
    read: bool
    update: bool
    delete: bool


class PermissionsResourceResponse(BaseModel):
    model_config = config
    create: bool
    read: bool
    update: bool
    delete: bool
    resource: ResourceResponse = Field(title="Resource", description="Resource")


class RoleResponse(BaseModel):
    name: str = Field(
        title="Role’s name",
        description="Role’s name",
        examples=["admin", "teacher", "student"],
    )


class RolePermissionsResponse(BaseModel):
    name: str = Field(
        title="Role’s name",
        description="Role’s name",
        examples=["admin", "teacher", "student"],
    )
    permissions: List[PermissionsResponse] = Field(
        title="Role’s permissions", description="Role’s permissions"
    )


class RolePermissionsResourceResponse(BaseModel):
    name: str = Field(
        title="Role’s name",
        description="Role’s name",
        examples=["admin", "teacher", "student"],
    )
    permissions: List[PermissionsResourceResponse] = Field(
        title="Role’s permissions", description="Role’s permissions"
    )


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


class ManagerImageResponse(BaseModel):
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
    image: Optional[ImageResponse]


class ManagerRoleResponse(BaseModel):
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
    role: RoleResponse


class ManagerRolePermissionsResponse(BaseModel):
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
    role: RolePermissionsResponse


class ManagerRolePermissionsResourceResponse(BaseModel):
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
    role: RolePermissionsResourceResponse


class ManagerImageRolePermissionsResourceResponse(BaseModel):
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
    role: RolePermissionsResourceResponse
