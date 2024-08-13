from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status
from ..dependencies.session import get_session
from ...core.models import (
    Resource,
    Role,
    Permissions,
    ProfilePermission,
    Manager,
    Image,
)
from datetime import date
from pydantic import SecretStr

# class Permissions(Base):
#     __tablename__ = "permissions"
#     id: Mapped[uuid.UUID] = mapped_column(
#         UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
#     )
#     resource_id: Mapped[uuid.UUID] = mapped_column(
#         UUID(as_uuid=True), ForeignKey("resources.id")
#     )
#     role_id: Mapped[uuid.UUID] = mapped_column(
#         UUID(as_uuid=True), ForeignKey("role.id")
#     )
#     create: Mapped[bool] = mapped_column(BOOLEAN, default=False)
#     read: Mapped[bool] = mapped_column(BOOLEAN, default=False)
#     update: Mapped[bool] = mapped_column(BOOLEAN, default=False)
#     delete: Mapped[bool] = mapped_column(BOOLEAN, default=False)


settings_router = APIRouter(prefix="/settings")


@settings_router.get(
    "/init-db",
    status_code=status.HTTP_200_OK,
)
async def reset_database():
    from ...core.database import engine
    from ...core.models import Base

    async with engine.begin() as connection:
        await connection.exec_driver_sql("DROP SCHEMA public CASCADE")
        await connection.exec_driver_sql("CREATE SCHEMA public")
        await connection.run_sync(Base.metadata.create_all)
    return {"message": "Database schema was successfully reset."}


@settings_router.get("/default-db", status_code=status.HTTP_200_OK)
async def default_database(
    session: AsyncSession = Depends(get_session),
):
    super_user = Role(name="superuser")
    saved_super_user = await super_user.save(session)
    for resource in [
        "role",
        "managment",
        "teacher",
        "group",
        "student",
        "department",
        "timetable",
        "subject",
        "room",
        "attendance-student",
        "attendance-employee",
        "psychology-student",
        "psychology-employee",
    ]:
        new_resource = Resource(name=resource)
        saved_resource = await new_resource.save(session)
        new_permissions = Permissions(
            resource_id=saved_resource.id,
            role_id=saved_super_user.id,
            create=True,
            read=True,
            update=True,
            delete=True,
        )
        await new_permissions.save(session)
    new_profile_permissions = ProfilePermission(
        id=saved_super_user.id,
        first_name=True,
        last_name=True,
        middle_name=True,
        birth_date=True,
        pini=True,
        phone_number=True,
        address=True,
        image=True,
        admin_history=True,
    )
    await new_profile_permissions.save(session)
    jahongir = Manager(
        id="7204ba59-6bea-435e-8751-5b8c2df57208",
        role_id=saved_super_user.id,
        pini="30110942150039",
        first_name="Jahongir",
        last_name="Yusupov",
        middle_name="Solijon og'li",
        birth_date=date(1994, 10, 1),
        phone_number="+998990019437",
        active=True,
        address="Namangan viloyati, Uchqo‘rg‘on tumani, Chek MFY, Hamza ko'chasi, 2-tupik 13-uy",
    )
    await jahongir.hach_password(SecretStr("iam3489495"))
    await jahongir.save(session)
    azimjon = Manager(
        id="848db225-2723-42e8-94f4-307ba727bddc",
        role_id=saved_super_user.id,
        pini="12345678901234",
        first_name="Azimjon",
        last_name="Jalilov",
        middle_name="Abduhalil og'li",
        birth_date=date(1999, 1, 13),
        phone_number="+998999777955",
        active=True,
        address="Namangan viloyati, Namangan shaxar",
    )
    await azimjon.hach_password(SecretStr("13011999"))
    await azimjon.save(session)

    jahongir_image = Image(
        id="7204ba59-6bea-435e-8751-5b8c2df57208",
        file_name="7204ba59-6bea-435e-8751-5b8c2df57208.jpg",
        file_path="static/users/7204ba59-6bea-435e-8751-5b8c2df57208.jpg",
        file="exmple".encode(),
    )
    await jahongir_image.save(session)
    #
    # azimjon_image = Image(
    #     id="848db225-2723-42e8-94f4-307ba727bddc",
    #     file_name="848db225-2723-42e8-94f4-307ba727bddc.jpg",
    #     file_path="static/users/848db225-2723-42e8-94f4-307ba727bddc.jpg",
    #     file="exmple".encode(),
    # )
    # await azimjon_image.save(session)
