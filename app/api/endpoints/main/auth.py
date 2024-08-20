from typing import Annotated
from pydantic import SecretStr
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import SecretStr
from ....services.auth.user import get
from ...dependencies.session import get_session
from ....schemas.auth import Token
from ....schemas.user import (
    UserResponse,
    UserRoleResponse,
    ManagerImageAndRolePermissionsResourceResponse,
)
from ....core.models import User

auth_router = APIRouter(prefix="/auth")


@auth_router.post("/login/")
async def login(
    login_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_session),
):
    user = User(phone_number=login_data.username)
    if not await user.get_by_phone_number(session):
        raise HTTPException(
            detail="Incorrect phone number", status_code=status.HTTP_401_UNAUTHORIZED
        )
    if not await user.check_password(SecretStr(login_data.password)):
        raise HTTPException(
            detail="Incorrect password", status_code=status.HTTP_401_UNAUTHORIZED
        )
    return Token(access_token=await user.generate_token(), token_type="Bearer")
