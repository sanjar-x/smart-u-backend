import socketio

sio_server = socketio.AsyncServer(
    client_manager=socketio.AsyncRedisManager("redis://localhost:6379/0"),
    async_mode="asgi",
    cors_allowed_origins=[],
)

sio_app = socketio.ASGIApp(socketio_server=sio_server, socketio_path="socket.io")


@sio_server.event
async def connect(sid, environ, auth):
    print(f"{sid}: connected")
    await sio_server.emit("join", {"sid": sid})


@sio_server.event
async def detect(sid, message):
    await sio_server.emit("detect", {"sid": sid, "message": message})


@sio_server.event
async def disconnect(sid):
    print(f"{sid}: disconnected")
