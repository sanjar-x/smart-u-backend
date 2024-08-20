from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from ...schemas.auth import oauth2_scheme
from ...api.dependencies.session import get_session
from ...core.models import Manager, User
from .token import decode_token


async def get(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_session),
):
    current_user = User(id=await decode_token(token))

    if not await current_user.get_with_image(session):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED"
        )
    if current_user.type == "manager":
        current_manager = Manager(id=current_user.id)
        current_manager = await current_manager.get_with_image_and_role_with_permissions_with_resource(
            session
        )
        return current_manager
    else:
        return current_user
