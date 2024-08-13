from enum import Enum
from uuid import UUID
from datetime import date
from typing import Annotated, List, Optional

from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    ConfigDict,
    SecretStr,
    StringConstraints,
    constr,
    FilePath,
)


config = ConfigDict(from_attributes=True)


class Image(BaseModel):
    model_config = config
    file_path: FilePath
