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
    dependencies=[admin_role_checker],
    summary="Get all users",
)
async def get_all_users(
    session: AsyncSession = Depends(get_session),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(
        10, ge=1, le=100, description="Maximum number of records to return"
    ),
):
    users = await user_service.get_all_users(session, is_active, skip, limit)
    return users


@user_router.get(
    "/{user_uid}",
    response_model=UserModel,
    dependencies=[user_role_checker],
    summary="Get user by uid",
)
async def get_user(user_uid: UUID, session: AsyncSession = Depends(get_session)):
    user = await user_service.get_user(user_uid, session)
    if user:
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


@user_router.patch(
    "/update/{user_uid}",
    response_model=UserModel,
    dependencies=[admin_role_checker],
    summary="Update user by uid",
)
async def update_user(
    user_uid: UUID,
    user_update_data: UserUpdateModel,
    session: AsyncSession = Depends(get_session),
):
    updated_user = await user_service.update_user(user_uid, user_update_data, session)
    if updated_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    else:
        return updated_user


@user_router.delete(
    "/delete/{user_uid}",
    dependencies=[admin_role_checker],
    summary="Delete user by uid",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(user_uid: UUID, session: AsyncSession = Depends(get_session)):
    user_to_delete = await user_service.delete_user(user_uid, session)
    if user_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    else:
        return {}
