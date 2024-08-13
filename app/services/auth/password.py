from typing import Any
from bcrypt import hashpw, gensalt, checkpw


from pydantic import SecretStr


class PasswordMixin:
    _password: Any
    password: SecretStr

    async def hach_password(self, password: SecretStr):
        self._password = hashpw(password.get_secret_value().encode("utf-8"), gensalt())

    async def check_password(self, password: SecretStr) -> bool:
        return checkpw(password.get_secret_value().encode("utf-8"), self._password)
