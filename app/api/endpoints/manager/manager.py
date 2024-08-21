import os
from uuid import UUID
from typing import List, Optional, Union
from datetime import datetime, date
from pydantic import SecretStr
from sqlalchemy.ext.asyncio import AsyncSession
from PIL import UnidentifiedImageError, Image as PILImage
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from ...dependencies.session import get_session
from ....schemas.manager import (
    ManagerResponse,
    ManagerImageResponse,
    ManagerRoleResponse,
    ManagerRolePermissionsResourceResponse,
    ManagerImageRolePermissionsResourceResponse,
)
from ....services.auth.user import get
from ....core.models import (
    Resource,
    Permissions,
    Image,
    User,
    Manager,
    Camera,
    Detection,
)
from ....services.detector.face import check_face
from ....services.tasks.initialization import (
    detector_engine_start,
    detector_engine_shutdown,
)
from ....services.cache.redis.client import client

managers_router = APIRouter(prefix="/managers")

UPLOAD_DIR = "static/users/"


@managers_router.post("/")
async def create_manager(
    role_id: UUID = Form(...),
    pini: str = Form(..., min_length=14, max_length=14),
    first_name: str = Form(...),
    last_name: str = Form(...),
    middle_name: Optional[str] = Form(...),
    birth_date: date = Form(...),
    phone_number: str = Form(..., min_length=13, max_length=13),
    address: str = Form(...),
    password: SecretStr = Form(..., min_length=6),
    upload_image: UploadFile = File(...),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get),
):
    # requered_resource = Resource(name="managment")
    # await requered_resource.get_by_name(session)
    # requered_permissions = Permissions(
    #     resource_id=requered_resource.id, role_id=current_user.role_id
    # )
    # if not requered_permissions in current_user.role.permissions:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="You don't have permision for this resource",
    #     )
    new_manager: Manager = Manager(
        role_id=role_id,
        pini=pini,
        first_name=first_name,
        last_name=last_name,
        middle_name=middle_name,
        birth_date=birth_date,
        phone_number=phone_number,
        address=address,
    )
    if await new_manager.exist_user(session):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This hone number or pini is already registred for another user",
        )
    await new_manager.hach_password(password)
    saved_manager: Manager = await new_manager.save(session)
    if not upload_image.filename:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Uploaded file is not a valid image",
        )
    image_filename = f"{saved_manager.id}{os.path.splitext(upload_image.filename)[1]}"
    image_file_path = f"{UPLOAD_DIR}{image_filename}"

    with open(image_file_path, "wb") as image_file:
        image_file.write(await upload_image.read())
    try:
        image = PILImage.open(image_file_path)
        image.verify()
    except UnidentifiedImageError:
        os.remove(image_file_path)
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Uploaded file is not a valid image",
        )
    await check_face(image_file_path)
    manager_image = Image(
        id=saved_manager.id,
        file=await upload_image.read(),
        file_name=image_filename,
        file_path=image_file_path,
    )
    await manager_image.save(session)
    await detector_engine_shutdown()
    await detector_engine_start()
    return {
        "info": f"{saved_manager.first_name}'s image saved at {manager_image.file_path}"
    }


from logging import getLogger

logger = getLogger("uvicorn")


@managers_router.get(
    "/",
    response_model=List[ManagerImageRolePermissionsResourceResponse],
)
async def get_managers(
    query: str | None = None,
    session: AsyncSession = Depends(get_session),
):
    manager = Manager()
    camera = Camera()
    cameras = await camera.get_all_with_rooms(session)
    if query:
        managers = await manager.search_by(session, query)
    else:
        managers = (
            await manager.get_all_with_image_and_role_with_permissions_with_resource(
                session
            )
        )
    for camera in cameras:
        for manager in managers:
            detection = Detection(camera_id=camera.id, user_id=manager.id)
            key = f"detections:camera:{camera.id}:user:{manager.id}"
            last_time = await detection.get_last(session)
            if last_time:
                results = await client.zrangebyscore(key, last_time.timestamp(), "+inf")
            else:
                results = await client.zrangebyscore(key, "-inf", "+inf")
            for result in results:
                new_detection = Detection(
                    camera_id=camera.id,
                    user_id=manager.id,
                    time=datetime.fromtimestamp(float(result)),
                )
                await new_detection.save(session)
                await client.zrem(key, result)

    return managers


@managers_router.delete("/")
async def delete_manager(
    id: UUID | None = None,
    session: AsyncSession = Depends(get_session),
):
    user = User(id=id)
    manager = Manager(id=id)
    await user.get_with_image(session)
    if user.image:
        await user.image._delete(session)
        # os.remove(os.path.join(UPLOAD_DIR, user.image.file_name))
    await user._delete(session)
    await manager._delete(session)

    return {"detail": "manager deleted"}
