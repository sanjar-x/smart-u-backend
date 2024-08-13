from typing import Annotated
from pydantic import SecretStr
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import SecretStr
from ...services.auth.current_user import get
from ..dependencies.session import get_session
from ...schemas.auth import Token
from ...schemas.user import (
    UserResponse,
    UserRoleResponse,
    UserImageAndRolePermissionsResourceResponse,
)
from ...core.models import User

profile_router = APIRouter(prefix="/profile")


@profile_router.get("/me/", response_model=UserImageAndRolePermissionsResourceResponse)
async def me(
    current_user=Depends(get),
):
    return current_user
