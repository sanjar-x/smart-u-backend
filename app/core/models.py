from __future__ import annotations

import uuid
from enum import Enum
from datetime import date, time, datetime
from typing import Any, BinaryIO, List, Optional, Union

from passlib.context import CryptContext
from sqlalchemy import (
    Column,
    ForeignKey,
    Table,
    exists,
    update,
    extract,
    and_,
    or_,
    func,
)
from sqlalchemy.dialects.postgresql import (
    BOOLEAN,
    BYTEA,
    DATE,
    ENUM,
    INET,
    TEXT,
    TIME,
    UUID,
    VARCHAR,
    TIMESTAMP,
)
from sqlalchemy.ext.asyncio import AsyncSession, AsyncAttrs
from sqlalchemy.future import select
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    joinedload,
    mapped_column,
    relationship,
    selectinload,
)

from ..services.auth.password import PasswordMixin
from ..services.auth.token import TokenMixin


class Base(DeclarativeBase, AsyncAttrs):
    __abstract__ = True
    id: Any

    async def _setattr_instance(self, obj):
        if obj:
            for key, value in vars(obj).items():
                if key != "_sa_instance_state":
                    setattr(self, key, value)
        return obj

    async def _execute_search(
        self,
        session: AsyncSession,
        condition: Optional[Any] = None,
        options: Optional[List[Any]] = None,
    ):
        query = select(self.__class__)

        if condition is not None:
            query = query.filter(condition)

        if options is not None:
            query = query.options(*options)

        result = await session.execute(query)
        return result.scalars().all()

    async def save(self, session: AsyncSession):
        session.add(self)
        await session.commit()
        await session.refresh(self)
        return self

    async def exists(self, session: AsyncSession, condition) -> bool | None:
        result = await session.execute(select(exists(self.__class__).where(condition)))
        return result.scalar()

    async def exist(self, session: AsyncSession) -> bool | None:
        result = await session.execute(
            select(exists(self.__class__).where(self.__class__.id == self.id))
        )
        return result.scalar()

    async def search(self, session: AsyncSession, filter: Any):
        return await self._execute_search(session, condition=filter)

    async def search_with_options(
        self, session: AsyncSession, options: Any, condition: Any
    ):
        return await self._execute_search(
            session, condition=condition, options=[options]
        )

    async def search_with_multi_filters(
        self, session: AsyncSession, filters: List[Any]
    ):
        condition = or_(*filters)
        return await self._execute_search(session, condition=condition)

    async def search_with_multi_options(
        self, session: AsyncSession, options: List[Any], filter: Any
    ):
        return await self._execute_search(session, condition=filter, options=options)

    async def search_with_options_and_multi_filters(
        self, session: AsyncSession, options: Any, filters: List[Any]
    ):
        condition = or_(*filters)
        return await self._execute_search(
            session, condition=condition, options=[options]
        )

    async def search_with_multi_options_and_multi_filters(
        self, session: AsyncSession, options: List[Any], filters: List[Any]
    ):
        condition = or_(*filters)
        return await self._execute_search(session, condition=condition, options=options)

    async def get(self, session: AsyncSession):
        obj = await session.get(self.__class__, self.id)
        await self._setattr_instance(obj)
        return obj

    async def get_with_filter(self, session: AsyncSession, filter):
        result = await session.execute(select(self.__class__).filter(filter))
        obj = result.scalar_one_or_none()
        return await self._setattr_instance(obj)

    async def get_with_filter_with_options(
        self, session: AsyncSession, filter, options
    ):
        result = await session.execute(
            select(self.__class__).filter(filter).options(options)
        )
        obj = result.scalar_one_or_none()
        return await self._setattr_instance(obj)

    async def get_with_filter_with_multi_options(
        self, session: AsyncSession, filter, options
    ):
        result = await session.execute(
            select(self.__class__).filter(filter).options(options)
        )
        obj = result.scalar_one_or_none()
        return await self._setattr_instance(obj)

    async def get_where(self, session: AsyncSession, condition):
        result = await session.execute(select(self.__class__).where(condition))
        obj = result.scalar_one_or_none()
        return await self._setattr_instance(obj)

    async def get_where_with_options(self, session: AsyncSession, condition, options):
        result = await session.execute(
            select(self.__class__).where(condition).options(options)
        )
        obj = result.scalar_one_or_none()
        return await self._setattr_instance(obj)

    async def get_where_with_multi_options(
        self, session: AsyncSession, condition, options: List[Any]
    ):
        result = await session.execute(
            select(self.__class__).where(condition).options(*options)
        )
        obj = result.scalar_one_or_none()
        await self._setattr_instance(obj)
        return obj

    async def get_all(self, session: AsyncSession):
        result = await session.execute(select(self.__class__))
        return result.scalars().all()

    async def get_all_where(self, session: AsyncSession, condition):
        result = await session.execute(select(self.__class__).where(condition))
        return list(result.scalars().all())

    async def get_all_where_with_options(
        self, session: AsyncSession, condition, options: List[Any]
    ):
        result = await session.execute(
            select(self.__class__).where(condition).options(*options)
        )
        return list(result.scalars().all())

    async def get_all_where_with_multi_options(
        self, session: AsyncSession, condition, options: List[Any]
    ):
        result = await session.execute(
            select(self.__class__).where(condition).options(*options)
        )
        return list(result.scalars().all())

    async def get_all_with_options(self, session: AsyncSession, options):
        result = await session.execute(select(self.__class__).options(options))
        return list(result.scalars().all())

    async def get_all_with_multi_options(
        self, session: AsyncSession, options: List[Any]
    ):
        stmt = select(self.__class__).options(*options)
        result = await session.execute(stmt)
        return list(result.scalars().all())

    async def _update(self, session: AsyncSession, **kwargs):
        result = await session.execute(
            update(self.__class__).where(self.__class__.id == self.id).values(**kwargs)
        )
        await session.commit()
        return self

    async def _delete(self, session: AsyncSession) -> bool:
        instance = await session.get(self.__class__, self.id)
        if not instance:
            return False
        await session.delete(instance)
        await session.commit()
        return True


class Resource(Base):
    __tablename__ = "resources"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(VARCHAR(31))

    permissions: Mapped[List[Permissions]] = relationship(
        "Permissions", back_populates="resource"
    )

    async def exist_name(self, session: AsyncSession, name: str):
        return await self.exists(session, self.__class__.name == name)

    async def get_by_name(self, session: AsyncSession):
        return await self.get_where(session, self.__class__.name == self.name)


class Role(Base):
    __tablename__ = "roles"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(VARCHAR(31))
    permissions: Mapped[List[Permissions]] = relationship(
        "Permissions", cascade="all, delete-orphan"
    )
    profile_permissions: Mapped[ProfilePermission] = relationship(
        "ProfilePermission", cascade="all, delete-orphan"
    )
    managers: Mapped[List[Manager]] = relationship("Manager", back_populates="role")

    async def exist_name(self, session: AsyncSession):
        return await self.exists(session, self.__class__.name == self.name)

    async def get_with_profile_permissions_with_resource(self, session: AsyncSession):
        options = [
            selectinload(self.__class__.permissions).joinedload(
                self.__class__.permissions.property.mapper.class_.resource
            ),
            joinedload(self.__class__.profile_permissions),
        ]
        return await self.get_where_with_multi_options(
            session, self.__class__.id == self.id, options
        )

    async def get_all_with_managers(self, session: AsyncSession):
        return await self.get_all_with_options(
            session,
            selectinload(self.__class__.managers).joinedload(
                self.__class__.managers.property.mapper.class_.image
            ),
        )

    async def get_all_with_profile_permissions_with_resource(
        self, session: AsyncSession
    ):
        options = [
            selectinload(self.__class__.permissions).joinedload(
                self.__class__.permissions.property.mapper.class_.resource
            ),
            joinedload(self.__class__.profile_permissions),
        ]
        return await self.get_all_with_multi_options(session, options)

    async def get_all_with_permissions_with_resource(self, session: AsyncSession):
        return await self.get_all_with_options(
            session,
            selectinload(self.__class__.permissions).joinedload(
                self.__class__.permissions.property.mapper.class_.resource
            ),
        )


class Permissions(Base):
    __tablename__ = "permissions"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    resource_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("resources.id")
    )
    role_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("roles.id")
    )
    create: Mapped[bool] = mapped_column(BOOLEAN, default=False)
    read: Mapped[bool] = mapped_column(BOOLEAN, default=False)
    update: Mapped[bool] = mapped_column(BOOLEAN, default=False)
    delete: Mapped[bool] = mapped_column(BOOLEAN, default=False)
    resource: Mapped[Resource] = relationship("Resource", back_populates="permissions")

    def __eq__(self, other):
        if not isinstance(other, Permissions):
            return False
        return self.resource_id == other.resource_id and self.role_id == other.role_id

    def __hash__(self):
        return hash(
            (
                self.resource_id,
                self.role_id,
            )
        )

    async def exist_permissions(self, session: AsyncSession):
        return await self.exists(
            session,
            and_(
                self.__class__.resource_id == self.resource_id,
                self.__class__.role_id == self.role_id,
            ),
        )


class ProfilePermission(Base):
    __tablename__ = "profile_permissions"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True
    )

    first_name: Mapped[bool] = mapped_column(BOOLEAN, default=False)
    last_name: Mapped[bool] = mapped_column(BOOLEAN, default=False)
    middle_name: Mapped[bool] = mapped_column(BOOLEAN, default=False)
    birth_date: Mapped[bool] = mapped_column(BOOLEAN, default=False)
    pini: Mapped[bool] = mapped_column(BOOLEAN, default=False)
    phone_number: Mapped[bool] = mapped_column(BOOLEAN, default=False)
    address: Mapped[bool] = mapped_column(BOOLEAN, default=False)
    image: Mapped[bool] = mapped_column(BOOLEAN, default=False)
    admin_history: Mapped[bool] = mapped_column(BOOLEAN, default=False)


class User(Base, PasswordMixin, TokenMixin):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    pini: Mapped[str] = mapped_column(VARCHAR(14))
    first_name: Mapped[str] = mapped_column(VARCHAR(31))
    last_name: Mapped[str] = mapped_column(VARCHAR(31))
    middle_name: Mapped[str] = mapped_column(VARCHAR(31))
    birth_date: Mapped[date] = mapped_column(DATE)
    phone_number: Mapped[str] = mapped_column(VARCHAR(13))
    active: Mapped[bool] = mapped_column(BOOLEAN, default=True)
    address: Mapped[str] = mapped_column(TEXT)
    _password: Mapped[bytes] = mapped_column(BYTEA(60), nullable=False)
    type: Mapped[str] = mapped_column(VARCHAR(31))

    image: Mapped[Image] = relationship(
        "Image", cascade="all, delete-orphan", uselist=False
    )
    groups: Mapped[List[Group]] = relationship("Group", back_populates="tutor")
    detections: Mapped[List[Detection]] = relationship(
        "Detection", cascade="all, delete-orphan"
    )
    __mapper_args__ = {
        "polymorphic_on": type,
        "polymorphic_identity": "user",
        "with_polymorphic": "*",
    }

    async def exist_user(self, session: AsyncSession):
        return await self.exists(
            session,
            or_(
                self.__class__.pini == self.pini,
                self.__class__.pini == self.phone_number,
            ),
        )

    async def get_all_with_image(self, session: AsyncSession):
        return await self.get_all_with_options(
            session, joinedload(self.__class__.image)
        )

    async def get_with_image(self, session: AsyncSession):
        return await self.get_where_with_options(
            session, self.__class__.id == self.id, joinedload(self.__class__.image)
        )

    async def get_by_phone_number(self, session: AsyncSession):
        return await self.get_where(
            session, self.__class__.phone_number == self.phone_number
        )


class Image(Base):
    __tablename__ = "image"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    file: Mapped[BinaryIO] = mapped_column(BYTEA)
    file_name: Mapped[str] = mapped_column(VARCHAR(63))
    file_path: Mapped[str] = mapped_column(TEXT)


class Manager(User):
    __tablename__ = "managers"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    role_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("roles.id")
    )

    role: Mapped[Role] = relationship("Role", back_populates="managers")
    department: Mapped[Department] = relationship(
        "Department",
        back_populates="manager",
    )
    __mapper_args__ = {
        "polymorphic_identity": "manager",
    }

    async def search_by(self, session: AsyncSession, query: str):
        filters = [
            self.__class__.pini.ilike(f"%{query}%"),
            self.__class__.first_name.ilike(f"%{query}%"),
            self.__class__.last_name.ilike(f"%{query}%"),
            self.__class__.phone_number.ilike(f"%{query}%"),
            self.__class__.address.ilike(f"%{query}%"),
        ]
        options = [
            joinedload(self.__class__.image),
            joinedload(self.__class__.role)
            .selectinload(self.__class__.role.property.mapper.class_.permissions)
            .joinedload(
                self.__class__.role.property.mapper.class_.permissions.property.mapper.class_.resource
            ),
        ]
        return await self.search_with_multi_options_and_multi_filters(
            session, options, filters
        )

    async def get_all_with_role(self, session: AsyncSession):
        return await self.get_all_with_options(session, joinedload(self.__class__.role))

    async def get_all_with_role_with_permissions(self, session: AsyncSession):
        return await self.get_all_with_options(
            session,
            joinedload(self.__class__.role).selectinload(
                self.__class__.role.property.mapper.class_.permissions
            ),
        )

    async def get_all_with_role_with_permissions_with_resource(
        self, session: AsyncSession
    ):
        return await self.get_all_with_options(
            session,
            joinedload(self.__class__.role)
            .selectinload(self.__class__.role.property.mapper.class_.permissions)
            .joinedload(
                self.__class__.role.property.mapper.class_.permissions.property.mapper.class_.resource
            ),
        )

    async def get_all_with_image_and_role_with_permissions_with_resource(
        self, session: AsyncSession
    ):
        options = [
            joinedload(self.__class__.image),
            joinedload(self.__class__.role)
            .selectinload(self.__class__.role.property.mapper.class_.permissions)
            .joinedload(
                self.__class__.role.property.mapper.class_.permissions.property.mapper.class_.resource
            ),
        ]
        return await self.get_all_with_multi_options(session, options)

    async def get_with_role_with_permissions_with_resource(self, session: AsyncSession):
        return await self.get_where_with_options(
            session,
            self.__class__.id == self.id,
            joinedload(self.__class__.role)
            .selectinload(self.__class__.role.property.mapper.class_.permissions)
            .joinedload(
                self.__class__.role.property.mapper.class_.permissions.property.mapper.class_.resource
            ),
        )

    async def get_with_image_and_role_with_permissions_with_resource(
        self, session: AsyncSession
    ):
        options = [
            joinedload(self.__class__.image),
            joinedload(self.__class__.role)
            .selectinload(self.__class__.role.property.mapper.class_.permissions)
            .joinedload(
                self.__class__.role.property.mapper.class_.permissions.property.mapper.class_.resource
            ),
        ]
        await self.get_where_with_multi_options(
            session, self.__class__.id == self.id, options
        )

        return self


class Department(Base):
    __tablename__ = "departments"
    # Keys
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    manager_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("managers.id", ondelete="SET NULL"),
        nullable=True,
    )
    name: Mapped[str] = mapped_column(VARCHAR(255))
    manager: Mapped[Optional[Manager]] = relationship(
        "Manager", back_populates="department"
    )
    groups: Mapped[List[Group]] = relationship("Group", back_populates="department")

    async def exist_name(self, session: AsyncSession):
        return await self.exists(session, self.__class__.name == self.name)

    async def get_all_with_manager(self, session: AsyncSession):
        return await self.get_all_with_options(
            session, joinedload(self.__class__.manager)
        )

    async def get_with_manager(self, session: AsyncSession):
        return await self.get_where_with_options(
            session,
            self.__class__.id == self.id,
            joinedload(self.__class__.manager),
        )


class Teacher(User):
    __tablename__ = "teachers"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    specialization: Mapped[str] = mapped_column(TEXT)
    pairs: Mapped[List[Pair]] = relationship("Pair", back_populates="teacher")
    __mapper_args__ = {
        "polymorphic_identity": "teacher",
    }

    async def search_by(self, session: AsyncSession, query: str):
        filters = [
            self.__class__.pini.ilike(f"%{query}%"),
            self.__class__.first_name.ilike(f"%{query}%"),
            self.__class__.last_name.ilike(f"%{query}%"),
            self.__class__.phone_number.ilike(f"%{query}%"),
            self.__class__.address.ilike(f"%{query}%"),
            self.__class__.specialization.ilike(f"%{query}%"),
        ]
        return await self.search_with_options_and_multi_filters(
            session, joinedload(self.__class__.image), filters
        )

    async def get_active_pair(self, session: AsyncSession):

        current_datetime = datetime.now()
        current_time = current_datetime.time()
        current_date = current_datetime.date()
        statement = (
            select(self.__class__)
            .options(
                joinedload(self.__class__.pairs).joinedload(Pair.slot),
                joinedload(self.__class__.pairs).joinedload(Pair.date),
                joinedload(self.__class__.pairs)
                .joinedload(Pair.groups)
                .joinedload(Group.students),
                joinedload(self.__class__.pairs)
                .joinedload(Pair.room)
                .joinedload(Room.cameras),
            )
            .filter(
                Date.date == current_date,
                Slot.start_time <= current_time,
                current_time <= Slot.end_time,
            )
        )

        result = await session.execute(statement)
        return result.scalar_one_or_none()


groups_pairs_association = Table(
    "groups_pairs",
    Base.metadata,
    Column(
        "group_id", UUID(as_uuid=True), ForeignKey("groups.id", ondelete="SET NULL")
    ),
    Column("pair_id", UUID(as_uuid=True), ForeignKey("pairs.id", ondelete="SET NULL")),
)


class GroupType(str, Enum):
    day = "day"
    night = "night"
    part = "part"


class Group(Base):
    __tablename__ = "groups"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    department_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("departments.id", ondelete="SET NULL"),
        nullable=True,
    )
    tutor_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    name: Mapped[str] = mapped_column(VARCHAR(255))
    type: Mapped[Enum] = mapped_column(ENUM(GroupType), nullable=False)

    department: Mapped[Department] = relationship("Department", back_populates="groups")
    tutor: Mapped[Union[Manager, Teacher]] = relationship(
        "User", back_populates="groups"
    )

    students: Mapped[List[Student]] = relationship(
        "Student", back_populates="group", foreign_keys="[Student.group_id]"
    )
    pairs: Mapped[List[Pair]] = relationship(
        "Pair", secondary=groups_pairs_association, back_populates="groups"
    )

    async def exist_name(self, session: AsyncSession):
        return await self.exists(session, self.__class__.name == self.name)

    async def search_by(self, session: AsyncSession, query: str):
        options = [
            joinedload(self.__class__.department),
            joinedload(self.__class__.tutor).joinedload(
                self.__class__.tutor.property.mapper.class_.image
            ),
            selectinload(self.__class__.students).joinedload(
                self.__class__.students.property.mapper.class_.image
            ),
        ]
        filters = [
            self.__class__.name.ilike(f"%{query}%"),
            self.__class__.tutor.property.mapper.class_.first_name.ilike(f"%{query}%"),
            self.__class__.tutor.property.mapper.class_.last_name.ilike(f"%{query}%"),
            self.__class__.tutor.property.mapper.class_.phone_number.ilike(
                f"%{query}%"
            ),
        ]
        return await self.search_with_multi_options_and_multi_filters(
            session, options, filters
        )

    async def get_all_with_department_and_tutor_and_students(
        self, session: AsyncSession
    ):
        options = [
            joinedload(self.__class__.department),
            joinedload(self.__class__.tutor).joinedload(
                self.__class__.tutor.property.mapper.class_.image
            ),
            selectinload(self.__class__.students).joinedload(
                self.__class__.students.property.mapper.class_.image
            ),
        ]
        return await self.get_all_with_multi_options(session, options)

    async def get_with_department_and_tutor_and_students(self, session: AsyncSession):
        options = [
            joinedload(self.__class__.department),  # Eagerly load Department
            joinedload(self.__class__.tutor),  # Eagerly load Tutor (User)
            selectinload(self.__class__.students),  # Eagerly load Students
        ]
        return await self.get_where_with_multi_options(
            session, self.__class__.id == self.id, options
        )


class Student(User):
    __tablename__ = "students"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    group_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("groups.id", ondelete="SET NULL")
    )

    group: Mapped[Group] = relationship("Group", back_populates="students")

    __mapper_args__ = {
        "polymorphic_identity": "student",
    }

    async def search_by(self, session: AsyncSession, query: str):
        options = [joinedload(self.__class__.image), joinedload(self.__class__.group)]
        filters = [
            self.__class__.pini.ilike(f"%{query}%"),
            self.__class__.first_name.ilike(f"%{query}%"),
            self.__class__.last_name.ilike(f"%{query}%"),
            self.__class__.phone_number.ilike(f"%{query}%"),
            self.__class__.address.ilike(f"%{query}%"),
            self.__class__.group.property.mapper.class_.name.ilike(f"%{query}%"),
        ]

        return await self.search_with_multi_options_and_multi_filters(
            session, options, filters
        )

    async def get_all_with_image_and_group(self, session: AsyncSession):
        options = [
            joinedload(self.__class__.image),
            joinedload(self.__class__.group),
        ]
        return await self.get_all_with_multi_options(session, options)


class Subject(Base):
    __tablename__ = "subjects"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(VARCHAR(255))

    pairs: Mapped[List[Pair]] = relationship("Pair", back_populates="subject")

    async def exist_name(self, session: AsyncSession):
        return await self.exists(session, self.__class__.name == self.name)

    async def search_by(self, session: AsyncSession, query: str):
        return await self.search(
            session,
            self.__class__.name.ilike(f"%{query}%"),
        )


class Room(Base):
    __tablename__ = "rooms"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(VARCHAR(255))
    cameras: Mapped[List[Camera]] = relationship(
        "Camera", back_populates="room", cascade="all, delete-orphan"
    )
    pairs: Mapped[List[Pair]] = relationship(
        "Pair", back_populates="room", cascade="save-update, merge"
    )

    async def exist_name(self, session: AsyncSession):
        return await self.exists(session, self.__class__.name == self.name)

    async def search_by(self, session: AsyncSession, query: str):
        filters = [
            self.__class__.name.ilike(f"%{query}%"),
            self.__class__.cameras.ip.ilike(f"%{query}%"),
        ]
        return await self.search_with_options_and_multi_filters(
            session, selectinload(self.__class__.cameras), filters
        )

    async def get_all_with_cameras(self, session: AsyncSession):
        return await self.get_all_with_options(
            session,
            selectinload(self.__class__.cameras),
        )


class Camera(Base):
    __tablename__ = "cameras"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    room_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("rooms.id", ondelete="CASCADE")
    )
    ip: Mapped[str] = mapped_column(INET)
    password: Mapped[str] = mapped_column(VARCHAR(255))
    room: Mapped[Room] = relationship("Room", back_populates="cameras")

    async def exist_camera(self, session: AsyncSession):
        return await self.exists(session, self.__class__.ip == self.ip)

    async def get_all_with_rooms(self, session: AsyncSession):
        return await self.get_all_with_options(
            session,
            joinedload(self.__class__.room),
        )


class Slot(Base):
    __tablename__ = "slots"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    start_time: Mapped[time] = mapped_column(TIME, nullable=False)
    end_time: Mapped[time] = mapped_column(TIME, nullable=False)

    async def get_active(self, session: AsyncSession):
        active_time = datetime.now().time()
        await self.get_where(
            session=session,
            condition=and_(
                self.__class__.start_time < active_time,
                active_time < self.__class__.end_time,
            ),
        )

    async def exist_time(self, session: AsyncSession):
        return await self.exists(
            session,
            and_(
                self.__class__.start_time == self.start_time,
                self.__class__.end_time == self.end_time,
            ),
        )


class Date(Base):
    __tablename__ = "dates"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    date: Mapped[date] = mapped_column(DATE, nullable=False)
    pairs: Mapped[List[Pair]] = relationship("Pair", back_populates="date")

    def __eq__(self, other):
        if not isinstance(other, Date):
            return False
        return self.date == other.date

    async def exist_date(self, session: AsyncSession):
        return await self.exists(session, self.__class__.date == self.date)

    async def get_by_date(self, session: AsyncSession):
        return await self.get_where(session, self.__class__.date == self.date)

    async def get_active_date(self, session: AsyncSession):
        active_date = datetime.now().date()
        return await self.get_where(session, self.__class__.date == active_date)

    async def get_by_year_and_month(
        self,
        session: AsyncSession,
        group_id: uuid.UUID,
        year: int | None = None,
        month: int | None = None,
    ):
        options = [
            selectinload(self.__class__.pairs).joinedload(
                self.__class__.pairs.property.mapper.class_.slot
            ),
            selectinload(self.__class__.pairs)
            .joinedload(self.__class__.pairs.property.mapper.class_.room)
            .selectinload(
                self.__class__.pairs.property.mapper.class_.room.property.mapper.class_.cameras
            ),
            selectinload(self.__class__.pairs)
            .joinedload(self.__class__.pairs.property.mapper.class_.teacher)
            .joinedload(
                self.__class__.pairs.property.mapper.class_.teacher.property.mapper.class_.image
            ),
            selectinload(self.__class__.pairs).joinedload(
                self.__class__.pairs.property.mapper.class_.subject
            ),
            selectinload(self.__class__.pairs).selectinload(
                self.__class__.pairs.property.mapper.class_.groups
            ),
        ]
        filters = [self.__class__.pairs.property.mapper.class_.groups.any(id=group_id)]
        if year and month:
            filters.append(extract("YEAR", self.__class__.date) == year)
            filters.append(extract("MONTH", self.__class__.date) == month)

        return await self.get_all_where_with_multi_options(
            session,
            and_(*filters),
            options,
        )


class Pair(Base):
    __tablename__ = "pairs"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    date_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("dates.id", ondelete="SET NULL")
    )
    slot_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("slots.id", ondelete="SET NULL")
    )
    room_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("rooms.id", ondelete="SET NULL")
    )

    teacher_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("teachers.id", ondelete="SET NULL")
    )
    subject_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("subjects.id", ondelete="SET NULL")
    )
    date: Mapped[Date] = relationship("Date", back_populates="pairs")
    slot: Mapped[Slot] = relationship("Slot")
    room: Mapped[Room] = relationship("Room", back_populates="pairs")
    teacher: Mapped[Teacher] = relationship("Teacher", back_populates="pairs")
    subject: Mapped[Subject] = relationship("Subject", back_populates="pairs")
    groups: Mapped[List[Group]] = relationship(
        "Group", secondary=groups_pairs_association, back_populates="pairs"
    )

    async def add_groups(self, session: AsyncSession, groups: List[Group]):
        for group in groups:
            await session.execute(
                groups_pairs_association.insert().values(
                    group_id=group.id, pair_id=self.id
                )
            )

    async def get_all_by_teacher(
        self,
        session: AsyncSession,
    ):
        options = [
            joinedload(self.__class__.date),
            joinedload(self.__class__.slot),
            joinedload(self.__class__.room).selectinload(
                self.__class__.room.property.mapper.class_.cameras
            ),
            joinedload(self.__class__.subject),
            selectinload(self.__class__.groups)
            .selectinload(self.__class__.groups.property.mapper.class_.students)
            .joinedload(
                self.__class__.groups.property.mapper.class_.students.property.mapper.class_.image
            ),
        ]
        return await self.get_all_where_with_multi_options(
            session,
            and_(
                self.__class__.teacher_id == self.teacher_id,
                self.__class__.date_id == self.date_id,
            ),
            options,
        )

    async def get_with_groups_with_students_by_date_and_time_and_teacher(
        self,
        session: AsyncSession,
    ):
        options = [
            selectinload(self.__class__.groups).selectinload(
                self.__class__.groups.property.mapper.class_.students
            )
        ]
        return await self.get_where_with_multi_options(
            session,
            and_(
                self.__class__.teacher_id == self.teacher_id,
                self.__class__.date_id == self.date_id,
                self.__class__.slot_id == self.slot_id,
            ),
            options,
        )

    async def get_by_year_and_month(
        self,
        session: AsyncSession,
        group_id: uuid.UUID,
        year: int | None = None,
        month: int | None = None,
    ):
        options = [
            # joinedload(self.__class__.date),
            joinedload(self.__class__.slot),
            joinedload(self.__class__.room).selectinload(
                self.__class__.room.property.mapper.class_.cameras
            ),
            joinedload(self.__class__.teacher).joinedload(
                self.__class__.teacher.property.mapper.class_.image
            ),
            joinedload(self.__class__.subject),
            selectinload(self.__class__.groups),
        ]
        filters = [self.__class__.groups.any(id=group_id)]
        if year and month:
            filters.append(extract("YEAR", self.__class__.date) == year)
            filters.append(extract("MONTH", self.__class__.date) == month)

        return await self.get_all_where_with_multi_options(
            session,
            and_(*filters),
            options,
        )

    async def get_by_slot_and_date(self, session: AsyncSession):
        options = [
            joinedload(self.__class__.date),
            joinedload(self.__class__.slot),
            joinedload(self.__class__.room).selectinload(
                self.__class__.room.property.mapper.class_.cameras
            ),
            joinedload(self.__class__.teacher),
            joinedload(self.__class__.subject),
            selectinload(self.__class__.groups).selectinload(
                self.__class__.groups.property.mapper.class_.students
            ),
        ]
        filters = [
            self.__class__.slot_id == self.slot_id,
            self.__class__.date_id == self.date_id,
        ]
        return await self.get_all_where_with_multi_options(
            session,
            and_(*filters),
            options,
        )

    async def search_by(self, session: AsyncSession, query: str):
        options = [
            joinedload(self.__class__.room).selectinload(
                self.__class__.room.property.mapper.class_.cameras
            ),
            joinedload(self.__class__.slot),
            joinedload(self.__class__.teacher),
            joinedload(self.__class__.subject),
            selectinload(self.__class__.groups),
        ]
        filters = [
            self.__class__.room.name.ilike(f"%{query}%"),
            self.__class__.room.property.mapper.class_.cameras.ip.ilike(f"%{query}%"),
            self.__class__.slot.ilike(f"%{query}%"),
            self.__class__.teacher.ilike(f"%{query}%"),
            self.__class__.subject.ilike(f"%{query}%"),
            self.__class__.room.ilike(f"%{query}%"),
            self.__class__.groups.property.mapper.class_.name.ilike(f"%{query}%"),
        ]

        return await self.search_with_multi_options_and_multi_filters(
            session, options, filters
        )


class Detection(Base):
    __tablename__ = "detections"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    camera_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("cameras.id", ondelete="SET NULL")
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE")
    )
    time: Mapped[datetime] = mapped_column(TIMESTAMP, unique=True)

    async def get_last(self, session: AsyncSession):
        result = await session.execute(
            select(func.max(self.__class__.time)).where(
                and_(
                    self.__class__.camera_id == self.camera_id,
                    self.__class__.user_id == self.user_id,
                )
            )
        )
        return result.scalar_one_or_none()

    async def get_range(
        self, session: AsyncSession, start_time: float, end_time: float
    ):
        stmt = select(self.__class__).where(
            self.__class__.time.between(start_time, end_time)
        )
        result = await session.execute(stmt)
        return result.scalars().all()
