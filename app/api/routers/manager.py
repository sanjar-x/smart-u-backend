from fastapi.routing import APIRouter

from ..endpoints.manager.resource import resource_router
from ..endpoints.manager.role import role_router
from ..endpoints.manager.manager import managers_router
from ..endpoints.manager.department import department_router
from ..endpoints.manager.teacher import teacher_router
from ..endpoints.manager.room import room_router
from ..endpoints.manager.camera import camera_router
from ..endpoints.manager.group import group_router
from ..endpoints.manager.student import student_router
from ..endpoints.manager.subject import subject_router
from ..endpoints.manager.slot import slot_router
from ..endpoints.manager.pair import pair_router


manager_router = APIRouter(prefix="/manager")
manager_router.include_router(resource_router, tags=["MANAGER RESOURCE"])
manager_router.include_router(role_router, tags=["MANAGER ROLE"])
manager_router.include_router(managers_router, tags=["MANAGER MANAGERS"])
manager_router.include_router(department_router, tags=["MANAGER DEPARTMENTS"])
manager_router.include_router(teacher_router, tags=["MANAGER TEACHER"])
manager_router.include_router(room_router, tags=["MANAGER ROOMS"])
manager_router.include_router(camera_router, tags=["MANAGER CAMERAS"])
manager_router.include_router(group_router, tags=["MANAGER GROUPS"])
manager_router.include_router(student_router, tags=["MANAGER STUDENT"])
manager_router.include_router(subject_router, tags=["MANAGER SUBJECT"])
manager_router.include_router(slot_router, tags=["MANAGER SLOT"])
manager_router.include_router(pair_router, tags=["MANAGER PAIRS"])
