from typing import List
from .client import client, Redis


class Notifier:
    def __init__(self):
        self._client: Redis = client

    async def check_notify(self, user_id: str):
        return await self._client.exists(f"notify:{user_id}")

    async def add_receiver(self, user_id: str, receivers: List[str]):
        return await self._client.sadd(f"notify:{user_id}", *receivers)  # type: ignore

    async def get_receivers(self, user_id: str):
        return await self._client.smembers(f"notify:{user_id}")  # type: ignore

    async def delete_receiver(self, user_id: str, receive_id: str):
        result = await self._client.srem(f"notify:{user_id}", receive_id)  # type: ignore
        print(result)
        return result

    async def delete_notify(self, user_id: str):
        return await self._client.delete(f"notify:{user_id}")
