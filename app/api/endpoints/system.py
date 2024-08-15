from subprocess import Popen, PIPE
from asyncio import create_task
from fastapi import APIRouter
from ...services.messages.zeromq import start_zeroMQ


system_router = APIRouter(prefix="/system")


process = None


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
