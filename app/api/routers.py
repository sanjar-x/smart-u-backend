from fastapi.routing import APIRouter
from .endpoints.root import root_router
from .endpoints.auth import auth_router
from .endpoints.profile import profile_router
from .endpoints.resource import resource_router
from .endpoints.role import role_router
from .endpoints.manager import manager_router
from .endpoints.department import department_router
from .endpoints.teacher import teacher_router
from .endpoints.room import room_router
from .endpoints.camera import camera_router
from .endpoints.group import gruop_router
from .endpoints.student import student_router
from .endpoints.subject import subject_router
from .endpoints.slot import slot_router
from .endpoints.pair import pair_router


from .endpoints.settings import settings_router

from .endpoints.user import user_router

# from .endpoints.system import system_router

api_routers = APIRouter()
api_routers.include_router(root_router, tags=["ROOT"])
api_routers.include_router(auth_router, tags=["AUTH"])
api_routers.include_router(profile_router, tags=["PROFILE"])
api_routers.include_router(resource_router, tags=["RESOURCE"])
api_routers.include_router(role_router, tags=["ROLE"])
api_routers.include_router(manager_router, tags=["MANAGER"])
api_routers.include_router(department_router, tags=["DEPARTMENT"])
api_routers.include_router(teacher_router, tags=["TEACHER"])
api_routers.include_router(room_router, tags=["ROOM"])
api_routers.include_router(camera_router, tags=["CAMERA"])
api_routers.include_router(gruop_router, tags=["GROUP"])
api_routers.include_router(student_router, tags=["STUDENT"])
api_routers.include_router(subject_router, tags=["SUBJECT"])
api_routers.include_router(slot_router, tags=["SLOT"])
api_routers.include_router(pair_router, tags=["PAIRS"])

api_routers.include_router(settings_router, tags=["SETTINGS"])

api_routers.include_router(user_router, tags=["USER"])
# api_routers.include_router(system_router, tags=["SYSTEM"])

# api_routers.include_router(teacher_router, tags=["TEACHER"])
# api_routers.include_router(group_router, tags=["GROUP"])
# api_routers.include_router(student_router, tags=["STUDENT"])
