import asyncio
from typing import List
from uuid import UUID
from datetime import datetime
from app.api.dependencies.session import async_session
from app.core.models import Pair, Date


async def test(slot_id: UUID):
    print(datetime.now())
    async with async_session() as session:
        date = Date(date=datetime.now().date())
        await date.get_by_date(session)
        pair = Pair(date_id=date.id, slot_id=slot_id)
        pairs: List[Pair] = await pair.get_by_slot_and_date(session)
        for pair in pairs:
            print(pair.teacher.first_name)
            for student in pair.groups[0].students:
                print(student.first_name)


# # UUID слота, который вы хотите передать
# slot_id = UUID("db20dd79-1fed-40cc-ae85-a06876b78c38")

# # Запуск асинхронной функции с помощью asyncio.run
# if __name__ == "__main__":
#     asyncio.run(pair_starter(slot_id))
# import asyncio
# from app.services.cache.redis.notify_manager import Notifier

# import redis

# # Подключение к Redis
# r = redis.Redis(host="localhost", port=6379, db=0)


# # # Получение данных
# # print(r.hget("camera:001", "user:001"))
# # print(r.zrange("camera:001:user:001", 0, -1))
# import logging

# # Конфигурация логгера
# logging.basicConfig(
#     level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
# )

# # Использование логгера в коде
# logging.debug("Это сообщение для отладки")
# logging.info("Приложение успешно запущено")
# logging.warning("Это предупреждение о возможной проблеме")
# logging.error("Ошибка: что-то пошло не так")
# logging.critical("Критическая ошибка: приложение не может продолжить работу")
