import zmq
from zmq.asyncio import Context, Socket
from ...utils.logger import logger


async def start_zeromq():
    context = Context()  # type: ignore
    socket: Socket = context.socket(zmq.PULL)
    socket.bind("tcp://*:5555")
    logger.info("ZeroMQ started")
    while True:
        message = await socket.recv_string()
        print(f"Received message: {message}")
