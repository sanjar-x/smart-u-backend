from typing import List, Optional, Union
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status
from ...dependencies.session import get_session
from ....schemas.department import DepartmentCreate, DepartmentResponse
from ....core.models import Department, Manager

department_router = APIRouter(prefix="/departments")


@department_router.post("/")
async def create_department(
    data: DepartmentCreate,
    session: AsyncSession = Depends(get_session),
):
    manager = Manager(id=data.manager_id)
    if not await manager.exist(session):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Manager not found",
        )
    new_department = Department(**data.model_dump())
    if await new_department.exist_name(session):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This department name is already registred",
        )
    saved_department = await new_department.save(session)
    return saved_department


@department_router.get("/")
async def get_departments(
    id: UUID | None = None,
    session: AsyncSession = Depends(get_session),
):
    department = Department()
    if id:
        department.id = id
        return await department.get_with_manager(session)
    else:
        return await department.get_all_with_manager(session)


@department_router.delete("/")
async def delete_department(
    id: UUID | None = None,
    session: AsyncSession = Depends(get_session),
):
    department = Department(id=id)
    return await department._delete(session)
