from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

# from fastapi.responses import ORJSONResponse
from ..dependencies.session import get_session
from ...schemas.resource import ResourceResponse
from ...core.models import Resource

resource_router = APIRouter(prefix="/resources")


@resource_router.get("/", response_model=List[ResourceResponse])
async def get_resourses(
    session: AsyncSession = Depends(get_session),
):
    resource: Resource = Resource()
    resources = await resource.get_all(session)
    return resources
