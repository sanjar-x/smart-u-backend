"""
This module sets up the FastAPI application for the Smart U attendance system,
configures middleware, routers, static files, and lifecycle events.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers.main import main_router
from app.api.routers.manager import manager_router
from app.api.routers.teacher import teacher_router
from app.connections.socketio import sio_app
from app.services.tasks.initialization import initialize, shutdown


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Asynchronously manages the lifespan of a FastAPI application.

    This context manager initializes and shuts down the application,
    ensuring all resources are set up and torn down properly.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None: This function yields control back to the FastAPI application
        before proceeding to shut down.

    Examples:
        Use as a lifespan handler in a FastAPI app:

        app = FastAPI(lifespan=lifespan)
    """
    await initialize()
    yield
    await shutdown()


app = FastAPI(
    title="Smart U",
    description='API-documentation "Smart U" attendance system',
    version="0.0.1",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(main_router)
app.include_router(manager_router)
app.include_router(teacher_router)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/", app=sio_app)
