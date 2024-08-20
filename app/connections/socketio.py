import datetime
from socketio import AsyncServer, AsyncRedisManager, ASGIApp
from ..services.cache.redis.session_manager import SessionManager
from ..services.auth.token import decode_connection_token
from ..api.dependencies.session import async_session
from ..core.models import User, Teacher, Slot, Date, Pair


server = AsyncServer(
    client_manager=AsyncRedisManager("redis://localhost:6379/1"),
    async_mode="asgi",
    cors_allowed_origins=[],
    always_connect=True,
    # logger=True,
    # engineio_logger=True,
)

sio_app = ASGIApp(socketio_server=server, socketio_path="socket.io")
session_manager = SessionManager()


@server.event
async def connect(sid, environ, auth):
    if not auth:
        await server.emit(event="error", data={"message": "Not authenticated"}, to=sid)
        await server.disconnect(sid)
        return 0
    user_id = await decode_connection_token(auth["token"])
    if not user_id:
        await server.emit(event="error", data={"message": "Not authenticated"}, to=sid)
        await server.disconnect(sid)
        return 0

    async with async_session() as session:
        user = User(id=user_id)
        if not await user.get(session):
            await server.emit(
                event="error", data={"message": "Not authenticated"}, to=sid
            )
            await server.disconnect(sid)
            return 0
        await session_manager.add_session(sid, user_id)
        if user.type == "student":
            server.enter_room(sid=sid, room=str(user.id))
        elif user.type == "teacher":
            date = Date()
            await date.get_active_date(session)
            slot = Slot()
            await slot.get_active(session)
            teacher = Teacher(id=user.id)
            await teacher.get(session)
            pair = Pair(date_id=date.id, slot_id=slot.id, teacher_id=teacher.id)
            pair = (
                await pair.get_with_groups_with_students_by_date_and_time_and_teacher(
                    session
                )
            )
            if not pair:
                return
            else:
                for group in pair.groups:
                    for student in group.students:
                        await server.enter_room(sid=sid, room=str(student.id))  # type: ignore
        else:
            user = User()
            users = await user.get_all(session)
            for user in users:
                await server.enter_room(sid=sid, room=str(user.id))  # type: ignore


@server.event
async def disconnect(sid):
    await session_manager.delete_session(sid)


@server.event
async def detect(sid, message):

    await server.emit("detect", {"sid": sid, "message": message})
