from enum import Enum
from uuid import UUID, uuid4
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
    IPvAnyAddress,
)


config = ConfigDict(from_attributes=True)


class Camera(BaseModel):
    model_config = config
    ip: IPvAnyAddress


class CameraCreate(Camera):
    pass


# class TeacherResponse(Teacher):
#     id: UUID = Field(title="Teacher’s id", description="Teacher’s id")
#     admin: bool = Field(
#         title="Checkbox",
#         description="Admin status",
#         examples=[True, False],
#     )


# class TeacherUpdate(BaseModel):
#     model_config = config
#     teacher_id: UUID = Field(title="Teacher’s id", description="Teacher’s id")
#     email: EmailStr = Field(
#         title="Teacher’s email",
#         description="Teacher’s email address",
#         examples=["example@example.com"],
#     )

#     fullname: Optional[str] = Field(
#         title="Teacher’s fullname",
#         description="Teacher’s fullname",
#         examples=["Yusupov Jahongir"],
#         default=None,
#     )
#     admin: Optional[bool] = Field(
#         title="Checkbox",
#         description="Admin status",
#         examples=[True, False],
#         default=None,
#     )
