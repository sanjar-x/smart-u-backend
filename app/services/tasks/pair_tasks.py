from typing import List
from uuid import UUID
from datetime import datetime

from ...core.models import Date, Pair
from ...api.dependencies.session import async_session
from ...connections.socketio import server
from ..cache.redis.session_manager import SessionManager


async def pair_starter(slot_id: UUID):
    session_manager = SessionManager()
    async with async_session() as session:
        date = Date(date=datetime.now().date())
        await date.get_by_date(session)
        pair = Pair(date_id=date.id, slot_id=slot_id)
        pairs: List[Pair] = await pair.get_by_slot_and_date(session)
        for pair in pairs:
            sid = await session_manager.get_user_session(str(pair.teacher_id))
            if not sid:
                continue
            for group in pair.groups:
                for student in group.students:
                    await server.enter_room(sid, str(student.id))  # type: ignore


async def pair_ender(slot_id: UUID):
    session_manager = SessionManager()
    async with async_session() as session:
        date = Date(date=datetime.now().date())
        await date.get_by_date(session)
        pair = Pair(date_id=date.id, slot_id=slot_id)
        pairs: List[Pair] = await pair.get_by_slot_and_date(session)
        for pair in pairs:
            sid = await session_manager.get_user_session(str(pair.teacher_id))
            if not sid:
                continue
            for group in pair.groups:
                for student in group.students:
                    await server.leave_room(sid, str(student.id))  # type: ignore
