from typing import List, Optional, Union
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status
from ..dependencies.session import get_session
from ...schemas.role import RoleCreate, RoleProfilePermissionsResponse, RoleUpdate
from ...core.models import Role, Permissions, ProfilePermission

role_router = APIRouter(prefix="/roles")


@role_router.post("/")
async def create_role(
    role: RoleCreate,
    session: AsyncSession = Depends(get_session),
):
    new_role: Role = Role(name=role.name)
    if await new_role.exist_name(session):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This role name is already registred",
        )
    saved_role = await new_role.save(session)
    for permissions in role.permissions:
        new_permissions = Permissions(role_id=saved_role.id, **permissions.model_dump())
        if await new_permissions.exist_permissions(session):
            pass
        else:
            await new_permissions.save(session)
    new_profile_permissions = ProfilePermission(
        id=saved_role.id, **role.profile_permissions.model_dump()
    )
    await new_profile_permissions.save(session)
    return saved_role


@role_router.get(
    "/",
    response_model=Union[
        RoleProfilePermissionsResponse, List[RoleProfilePermissionsResponse]
    ],
)
async def get_roles(
    id: UUID | None = None,
    session: AsyncSession = Depends(get_session),
):
    role = Role()
    if id:
        role.id = id
        return await role.get_with_profile_permissions_with_resource(session)
    else:
        return await role.get_all_with_profile_permissions_with_resource(session)


@role_router.delete(
    "/",
)
async def delete_role(
    id: UUID | None = None,
    session: AsyncSession = Depends(get_session),
):
    role = Role(id=id)
    await role.get(session)
    if role.name == "superuser":
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="You cant delete superuser role",
        )
    return await role._delete(session)
