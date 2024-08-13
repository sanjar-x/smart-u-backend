# from fastapi import APIRouter, status
# from ...services.messages.zeromq import start_zmq_thread

# system_router = APIRouter(prefix="/system")


# @system_router.get(
#     "/startzero",
#     status_code=status.HTTP_200_OK,
# )
# async def start_zeromq():
#     start_zmq_thread()
