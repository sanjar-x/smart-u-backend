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


class Role(BaseModel):
    model_config = config
    name: str = Field(
        title="Role’s name",
        description="Role’s name",
        examples=["admin", "teacher", "student"],
    )


class PermissionsCreate(BaseModel):
    model_config = config
    create: bool = Field(
        default=False, title="Create permission", description="Create permission"
    )
    read: bool = Field(
        default=False, title="Read permission", description="Read permission"
    )
    update: bool = Field(
        default=False, title="Update permission", description="Update permission"
    )
    delete: bool = Field(
        default=False, title="Delete permission", description="Delete permission"
    )
    resource_id: UUID = Field(title="Resource's ID", description="Resource's ID")


class ProfilePermissionsCreate(BaseModel):
    model_config = config
    admin_history: bool = False
    first_name: bool = False
    last_name: bool = False
    middle_name: bool = False
    birth_date: bool = False
    pini: bool = False
    phone_number: bool = False
    address: bool = False
    image: bool = False


class RoleCreate(Role):
    permissions: List[PermissionsCreate]
    profile_permissions: ProfilePermissionsCreate


class ProfilePermissionsResponse(BaseModel):
    first_name: bool = False
    last_name: bool = False
    middle_name: bool = False
    birth_date: bool = False
    pini: bool = False
    phone_number: bool = False
    address: bool = False
    image: bool = False
    admin_history: bool = False


class ResourceResponse(BaseModel):
    model_config = config
    name: str


class PermissionsResponse(BaseModel):
    model_config = config
    create: bool
    read: bool
    update: bool
    delete: bool
    resource: ResourceResponse = Field(title="Resource", description="Resource")


class RoleProfilePermissionsResponse(Role):
    id: UUID = Field(title="Role's id", description="Role's id")
    profile_permissions: Optional[ProfilePermissionsResponse]
    permissions: List[PermissionsResponse] = Field(
        title="Role’s permissions", description="Role’s permissions"
    )


class RoleUpdate(Role):
    id: UUID = Field(title="Role's id", description="Role's id")
    permissions: List[PermissionsCreate]
    profile_permissions: ProfilePermissionsCreate
