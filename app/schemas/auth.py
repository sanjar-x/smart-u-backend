from fastapi.security import OAuth2PasswordBearer
from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    ConfigDict,
    SecretStr,
    StringConstraints,
    constr,
    IPvAnyAddress,
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login/")


class Token(BaseModel):
    access_token: str
    token_type: str
