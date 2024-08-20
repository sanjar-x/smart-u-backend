from .client import client, Redis


class SessionManager:
    def __init__(self):
        self._client: Redis = client

    async def add_session(self, sid: str, user_id: str):
        existing_sid = await self.get_user_session(user_id)
        if existing_sid:
            await self.delete_session(existing_sid)
        async with self._client.pipeline() as pipeline:
            await pipeline.hset(name="session:user", key=sid, value=user_id)  # type: ignore
            await pipeline.hset(name="user:session", key=user_id, value=sid)  # type: ignore
            await pipeline.execute()

    async def get_user_session(self, user_id: str) -> str | None:
        return await self._client.hget("user:session", user_id)  # type: ignore

    async def get_session_user(self, sid: str) -> str | None:
        return await self._client.hget("session:user", sid)  # type: ignore

    async def _delete_session(self, sid: str) -> str | None:
        return await self._client.hdel("session:user", sid)  # type: ignore

    async def _delete_user(self, user_id: str):
        await self._client.hdel("user:session", user_id)  # type: ignore

    async def delete_session(self, sid: str):
        user_id = await self.get_session_user(sid)
        if user_id:
            await self._delete_session(sid)
            await self._delete_user(user_id)

    async def delete_user(self, user_id: str):
        sid = await self.get_user_session(user_id)
        if sid:
            await self._delete_user(user_id)
            await self._delete_session(sid)
