from fastapi import APIRouter, Depends, Query, status
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from app.services.user_service import UserService
from app.core.database import get_session
from app.schemas.user_schema import UserModel, UserCreateModel, UserUpdateModel
from app.api.deps.dependencies import AccessTokenBearer, RoleChecker, get_current_user
from typing import List, Optional
from uuid import UUID
import logging


logger = logging.getLogger(__name__)
user_router = APIRouter()
user_service = UserService()
access_token_bearer = AccessTokenBearer()
admin_role_checker = Depends(RoleChecker(["admin"]))
user_role_checker = Depends(RoleChecker(["admin", "fisico", "tecnico"]))


@user_router.get(
    "/",
    response_model=List[UserModel],
    dependencies=[user_role_checker],
    summary="Get all users",
)
async def get_all_linacs(
    session: AsyncSession = Depends(get_session),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(
        10, ge=1, le=10, description="Meximum Number of records to return"
    ),
):
    linacs = await user_service.get_all_users(session, is_active, skip, limit)
    return linacs


@user_router.get(
    "/{user_uid}",
    response_model=UserModel,
    dependencies=[user_role_checker],
    summary="Get user by uid",
)
async def get_linac(user_uid: UUID, session: AsyncSession = Depends(get_session)):
    linac = await user_service.get_user(user_uid, session)
    if linac:
        return linac
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


@user_router.patch(
    "/update/{linac_uid}",
    dependencies=[admin_role_checker],
    summary="Update linac by uid",
)
async def update_user(
    user_uid: UUID,
    user_update_data: UserUpdateModel,
    session: AsyncSession = Depends(get_session),
):
    logger.info(f"linac_uid: {linac_uid}, linac_update_data: {linac_update_data}")
    updated_linac = await user_service.update_linac(
        linac_uid, linac_update_data, session
    )
    if updated_linac is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Linac not found"
        )
    else:
        return updated_linac


@user_router.delete(
    "/delete/{linac_uid}",
    dependencies=[admin_role_checker],
    summary="Delete linac by uid",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_linac(linac_uid: UUID, session: AsyncSession = Depends(get_session)):
    linac_to_delete = await user_service.delete_linac(linac_uid, session)
    if linac_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Linac not found"
        )
    else:
        return {}
