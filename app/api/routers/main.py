from fastapi.routing import APIRouter


from app.api.endpoints.main.root import root_router
from app.api.endpoints.main.auth import auth_router
from app.api.endpoints.main.profile import profile_router
from app.api.endpoints.main.settings import settings_router
from app.api.endpoints.main.system import system_router


main_router = APIRouter()
main_router.include_router(root_router, tags=["ROOT"])
main_router.include_router(settings_router, tags=["SETTINGS"])
main_router.include_router(system_router, tags=["SYSTEM"])
main_router.include_router(auth_router, tags=["AUTH"])
main_router.include_router(profile_router, tags=["PROFILE"])
