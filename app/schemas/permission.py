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

from .resource import ResourceResponse

config = ConfigDict(from_attributes=True)


class Permissions(BaseModel):
    model_config = config
    create: bool
    read: bool
    update: bool
    delete: bool


class PermissionsCreate(Permissions):
    resource_id: UUID = Field(title="Resource's id", description="Resource's id")


class PermissionsResponse(Permissions):
    resource: ResourceResponse = Field(title="Resource", description="Resource")


class Role(BaseModel):
    model_config = config
    name: str = Field(
        title="Role’s name",
        description="Role’s name",
        examples=["admin", "teacher", "student"],
    )


class RoleCreate(Role):
    permissions: List[Permissions] = Field(
        title="Role’s permissions", description="Role’s permissions"
    )


class RoleResponse(Role):
    permissions: List[PermissionsResponse] = Field(
        title="Role’s permissions", description="Role’s permissions"
    )


class User(BaseModel):
    model_config = config
    first_name: str = Field(
        title="User’s first name", description="User’s first name", examples=["Anvar"]
    )
    last_name: str = Field(
        title="User’s last name", description="User’s last name", examples=["Anvarov"]
    )
    middle_name: Optional[str] = Field(
        title="User’s last name", description="User’s last name", examples=["Anvarov"]
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


class UserResponse(User):
    id: UUID = Field(title="User’s id", description="User’s id")
    role: RoleResponse


class GroupType(str, Enum):
    day_time = "daytime"
    night_time = "night_time"
    part_time = "part_time"


class Group(BaseModel):
    model_config = config
    name: str = Field(
        title="Group's name", description="Group's name", examples=["B1234"]
    )
    type: GroupType = Field(
        title="Group's type",
        description="Group's type",
        examples=["daytime", "night_time", "part_time"],
    )

    active: bool = Field(
        title="Checkbox",
        description="Group's status",
        examples=[True, False],
    )


class GroupCreate(Group):
    id: UUID = Field(title="User’s id", description="User’s id")
    tutor_id: UUID
    department_id: UUID


class GroupResponse(Group):
    id: UUID = Field(title="User’s id", description="User’s id")
    student: List[UserResponse]
    tutor: UserResponse
    department: Department


class Department(BaseModel):
    name: str = Field(
        title="Department's name",
        description="Department's name",
        examples=["Information Technology"],
    )

    active: bool = Field(
        title="Checkbox",
        description="Group's status",
        examples=[True, False],
    )


class DepartmenCreate(Department):
    head_master_id: UUID


class DepartmenResponse(Department):
    head_master: UserResponse
    groups: List[GroupResponse]
