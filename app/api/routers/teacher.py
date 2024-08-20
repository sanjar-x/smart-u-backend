from fastapi.routing import APIRouter


# Teacher
from ..endpoints.teacher.group import group_router
from ..endpoints.teacher.slot import slot_router
from ..endpoints.teacher.pair import pair_router

teacher_router = APIRouter(prefix="/teacher")
teacher_router.include_router(slot_router, tags=["TEACHER SLOTS"])
teacher_router.include_router(group_router, tags=["TEACHER GROUP"])
teacher_router.include_router(pair_router, tags=["TEACHER PAIRS"])
