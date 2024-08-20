import time
from logging import getLogger
import zmq
from zmq.asyncio import Context, Socket
from ..cache.redis.client import client
from ...connections.socketio import server

logger = getLogger("uvicorn")


async def start_zeroMQ(endpoint: str):
    context = Context()  # type: ignore
    socket: Socket = context.socket(zmq.PAIR)
    socket.connect(endpoint)
    while True:
        message = await socket.recv_string()
        data = message.split(":")
        if float(data[2]) < 1.0:
            timestamp = time.time()
            await client.zadd(
                f"detections:camera:{data[0]}:user:{data[1]}",
                {f"{timestamp}": timestamp},
            )
            await server.emit(
                "detect", {"camera": data[0], "user": data[1]}, room=f"{data[1]}"
            )
