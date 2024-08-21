from typing import List
from subprocess import Popen, PIPE
from asyncio import create_task, all_tasks
from fastapi import APIRouter
from ....services.messages.zeromq import start_zeroMQ
from ....services.tasks.scheduler import scheduler
from ....services.tasks.initialization import shutdown, initialize
from apscheduler.job import Job

system_router = APIRouter(prefix="/system")


process = None


@system_router.get("/reload")
async def reload():
    await shutdown()
    await initialize()
    return {"status": "system reload"}


@system_router.get("/build/engine")
async def build_engine():
    Popen(["./detector/scripts/clean.sh"], stdout=PIPE, stderr=PIPE)
    Popen(["./detector/scripts/build.sh"], stdout=PIPE, stderr=PIPE)
    return {"status": "Engine build"}


@system_router.get("/start/engine")
async def start_engine():
    global process
    process = Popen(["./detector/build/main"], stdout=PIPE, stderr=PIPE)
    return {"status": "Engine started"}


@system_router.get("/stop/engine")
async def stop_engine():
    global process
    if process and process.poll() is None:
        process.terminate()
        process.wait()
        return {"status": "Engine stopped"}
    else:
        return {"status": "Engine is not running"}


@system_router.get("/start/zeromq")
async def start_zeromq():
    create_task(start_zeroMQ("ipc:///tmp/zeromq-ipc"))


@system_router.get("/scheduler")
async def get_scheduler():
    jobs: List[Job] = scheduler.get_jobs("default")
    return jobs[0].name
