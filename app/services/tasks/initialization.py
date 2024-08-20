from logging import getLogger
from asyncio import create_task
from subprocess import Popen, PIPE
from ...services.cache.redis.client import client
from ...services.tasks.scheduler import jobstore, scheduler
from ...services.messages.zeromq import start_zeroMQ
from ...services.tasks.pair_tasks import pair_starter, pair_ender

from ...core.database import engine
from ...core.models import Base, Slot
from ...api.dependencies.session import async_session

logger = getLogger("uvicorn")

detector_process = None


async def init_database():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    logger.info("Database initialized successfully.")


async def initialize_redis():
    await client.flushall()
    logger.info("Redis cache flushed successfully.")


async def init_pairs():
    scheduler.remove_all_jobs(jobstore)
    async with async_session() as session:
        slots = await Slot().get_all(session)
        for slot in slots:
            scheduler.add_job(
                pair_starter,
                "cron",
                hour=slot.start_time.hour,
                minute=slot.start_time.minute,
                second=slot.start_time.second,
                args=[slot.id],
            )  # type: ignore
            logger.info(
                f"Pair starter job scheduled to: {slot.start_time.hour}:{slot.start_time.minute}"
            )
            scheduler.add_job(
                pair_ender,
                "cron",
                hour=slot.end_time.hour,
                minute=slot.end_time.minute,
                second=slot.end_time.second,
                args=[slot.id],
            )  # type: ignore
            logger.info(
                f"Pair ender job scheduled to: {slot.end_time.hour}:{slot.end_time.minute}"
            )


async def detector_engine_start():
    global detector_process
    detector_process = Popen(["./detector/build/main"], stdout=PIPE, stderr=PIPE)
    logger.info("Detector engine started successfully.")


async def initialize():
    await init_database()
    await initialize_redis()
    await init_pairs()
    scheduler.start()  # type: ignore
    await detector_engine_start()
    create_task(start_zeroMQ("ipc:///tmp/zeromq-ipc"))
    logger.info("System initialization complete.")


async def detector_engine_shutdown():
    global detector_process
    if detector_process and detector_process.poll() is None:
        detector_process.terminate()
        detector_process.wait()
        logger.info("Detector engine stopped successfully.")
        return {"status": "Engine stopped"}
    else:
        logger.info("Detector engine is not running.")
        return {"status": "Engine is not running"}


async def shutdown():
    await detector_engine_shutdown()
    await client.close(close_connection_pool=True)
    scheduler.shutdown(wait=True)
    logger.info("System shutdown complete.")
