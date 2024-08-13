from os import getenv

from datetime import datetime, timedelta
from typing import Any, Optional


from jose import jwt, ExpiredSignatureError
from fastapi import HTTPException, status

SECRET_KEY = "4a8b30b3dd4a6a2e8b5c6a76e39c20c1f0f38d56c2ea24a7d52f6d1a5423e3bf"


class TokenMixin:
    id: Any

    async def generate_token(self) -> str:
        # "exp": datetime.now() + timedelta(seconds=expires_in),
        payload = {
            "sub": str(self.id),
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")  # type: ignore
        return token


async def decode_token(token: str) -> Optional[bool]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])  # type: ignore
        return payload["sub"]
    except ExpiredSignatureError:
        raise HTTPException(
            detail="Qaytadan kiring", status_code=status.HTTP_401_UNAUTHORIZED
        )
