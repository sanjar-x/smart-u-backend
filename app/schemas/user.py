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


class UserResponse(BaseModel):
    model_config = config
    id: UUID = Field(title="User’s id", description="User’s id")
    pini: str = Field(
        title="User’s pini",
        description="User’s pini",
        examples=["12345678901234"],
    )
    first_name: str = Field(
        title="User’s first name",
        description="User’s first name",
        examples=["Anvar"],
    )
    last_name: str = Field(
        title="User’s last name",
        description="User’s last name",
        examples=["Anvarov"],
    )
    middle_name: Optional[str] = Field(
        title="User’s middle name",
        description="User’s middle name",
        examples=["Anvarovich"],
    )
    birth_date: date
    phone_number: str = Field(
        title="User’s phone number",
        description="User’s phone number",
        examples=["+998901234567"],
    )
    active: bool = Field(
        title="Checkbox",
        description="User status",
        examples=[True, False],
    )
    address: str = Field(
        title="User’s address",
        description="User’s address",
        examples=[
            "Namangan viloyati, Turaqo'rg'on tumani, Sharq MFY, Bog' ko'cha 18-uy"
        ],
    )
    type: str


class UserImageResponse(BaseModel):
    model_config = config
    id: UUID = Field(title="User’s id", description="User’s id")
    pini: str = Field(
        title="User’s pini",
        description="User’s pini",
        examples=["12345678901234"],
    )
    first_name: str = Field(
        title="User’s first name",
        description="User’s first name",
        examples=["Anvar"],
    )
    last_name: str = Field(
        title="User’s last name",
        description="User’s last name",
        examples=["Anvarov"],
    )
    middle_name: Optional[str] = Field(
        title="User’s middle name",
        description="User’s middle name",
        examples=["Anvarovich"],
    )
    birth_date: date
    phone_number: str = Field(
        title="User’s phone number",
        description="User’s phone number",
        examples=["+998901234567"],
    )
    active: bool = Field(
        title="Checkbox",
        description="User status",
        examples=[True, False],
    )
    address: str = Field(
        title="User’s address",
        description="User’s address",
        examples=[
            "Namangan viloyati, Turaqo'rg'on tumani, Sharq MFY, Bog' ko'cha 18-uy"
        ],
    )
    type: str
    image: Optional[ImageResponse]


class UserRoleResponse(BaseModel):
    model_config = config
    id: UUID = Field(title="User’s id", description="User’s id")
    pini: str = Field(
        title="User’s pini",
        description="User’s pini",
        examples=["12345678901234"],
    )
    first_name: str = Field(
        title="User’s first name",
        description="User’s first name",
        examples=["Anvar"],
    )
    last_name: str = Field(
        title="User’s last name",
        description="User’s last name",
        examples=["Anvarov"],
    )
    middle_name: Optional[str] = Field(
        title="User’s middle name",
        description="User’s middle name",
        examples=["Anvarovich"],
    )
    birth_date: date
    phone_number: str = Field(
        title="User’s phone number",
        description="User’s phone number",
        examples=["+998901234567"],
    )
    active: bool = Field(
        title="Checkbox",
        description="User status",
        examples=[True, False],
    )
    address: str = Field(
        title="User’s address",
        description="User’s address",
        examples=[
            "Namangan viloyati, Turaqo'rg'on tumani, Sharq MFY, Bog' ko'cha 18-uy"
        ],
    )
    role: RoleResponse


class UserRolePermissionsResourceResponse(BaseModel):
    model_config = config
    id: UUID = Field(title="User’s id", description="User’s id")
    pini: str = Field(
        title="User’s pini",
        description="User’s pini",
        examples=["12345678901234"],
    )
    first_name: str = Field(
        title="User’s first name",
        description="User’s first name",
        examples=["Anvar"],
    )
    last_name: str = Field(
        title="User’s last name",
        description="User’s last name",
        examples=["Anvarov"],
    )
    middle_name: Optional[str] = Field(
        title="User’s middle name",
        description="User’s middle name",
        examples=["Anvarovich"],
    )
    birth_date: date
    phone_number: str = Field(
        title="User’s phone number",
        description="User’s phone number",
        examples=["+998901234567"],
    )
    active: bool = Field(
        title="Checkbox",
        description="User status",
        examples=[True, False],
    )
    address: str = Field(
        title="User’s address",
        description="User’s address",
        examples=[
            "Namangan viloyati, Turaqo'rg'on tumani, Sharq MFY, Bog' ko'cha 18-uy"
        ],
    )
    role: RolePermissionsResourceResponse


class ManagerImageAndRolePermissionsResourceResponse(BaseModel):
    model_config = config
    id: UUID = Field(title="User’s id", description="User’s id")
    pini: str = Field(
        title="User’s pini",
        description="User’s pini",
        examples=["12345678901234"],
    )
    first_name: str = Field(
        title="User’s first name",
        description="User’s first name",
        examples=["Anvar"],
    )
    last_name: str = Field(
        title="User’s last name",
        description="User’s last name",
        examples=["Anvarov"],
    )
    middle_name: Optional[str] = Field(
        title="User’s middle name",
        description="User’s middle name",
        examples=["Anvarovich"],
    )
    birth_date: date
    phone_number: str = Field(
        title="User’s phone number",
        description="User’s phone number",
        examples=["+998901234567"],
    )
    active: bool = Field(
        title="Checkbox",
        description="User status",
        examples=[True, False],
    )
    address: str = Field(
        title="User’s address",
        description="User’s address",
        examples=[
            "Namangan viloyati, Turaqo'rg'on tumani, Sharq MFY, Bog' ko'cha 18-uy"
        ],
    )
    type: str
    image: Optional[ImageResponse]
    role: Optional[RolePermissionsResourceResponse]
