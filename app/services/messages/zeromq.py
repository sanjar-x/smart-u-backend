import time
import zmq
from zmq.asyncio import Context, Socket
from redis.asyncio import Redis
from ...connections.socketio import sio_server


async def start_zeroMQ(endpoint: str):
    r = Redis(host="localhost", port=6379, db=0)
    context = Context()  # type: ignore
    socket: Socket = context.socket(zmq.PAIR)
    socket.connect(endpoint)

    while True:
        string = await socket.recv_string()
        timestamp = time.time()
        data = string.split(":")
        await r.zadd(f"camera:{data[1]}:user:{data[3]}", {"time": timestamp})
        await sio_server.emit(
            "detect",
            {"camera": data[1], "user": data[3], "timestamp": timestamp},
        )
