from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from app.api.deps.dependencies import RefreshTokenBearer, RoleChecker
from app.schemas.user_schema import (
    UserCreateModel,
    UserLoginModel,
    UserModel,
    UserUpdateModel,
)
from app.services.user_service import UserService
from app.core.config import settings
from app.core.database import get_session
from app.core.security import create_access_token, decode_token, verify_password
from sqlmodel.ext.asyncio.session import AsyncSession


auth_router = APIRouter()
user_service = UserService()
admin_role_checker = Depends(RoleChecker(["admin"]))
user_role_checker = Depends(RoleChecker(["admin", "fisico", "tecnico"]))


@auth_router.post(
    "/create",
    response_model=UserModel,
    status_code=status.HTTP_201_CREATED,
    dependencies=[admin_role_checker],
    summary="Create new user",
)
async def create_user(
    user_data: UserCreateModel, session: AsyncSession = Depends(get_session)
):
    username = user_data.username
    user_exists = await user_service.user_exists(username, session)

    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User already exists"
        )
    else:
        new_user = await user_service.create_user(user_data, session)
        return new_user


@auth_router.post("/login", summary="User login")
async def login_user(
    login_data: UserLoginModel, session: AsyncSession = Depends(get_session)
):
    username = login_data.username
    password = login_data.password
    user = await user_service.get_user_by_username(username, session)
    if user is not None:
        password_valid = verify_password(password, user.hashed_password)
        if password_valid:
            access_token = create_access_token(
                user_data={
                    "uid": str(user.uid),
                    "username": user.username,
                    "role": user.role,
                }
            )

            refresh_token = create_access_token(
                user_data={
                    "uid": str(user.uid),
                    "username": user.username,
                    "role": user.role,
                },
                expiry=timedelta(minutes=settings.REFRESH_EXPIRE_TOKEN_DAYS),
                refresh=True,
            )
            return JSONResponse(
                content={
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {
                        "uid": str(user.uid),
                        "username": user.username,
                        "role": user.role,
                    },
                }
            )
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials"
    )


@auth_router.get(
    "/refresh_token", dependencies=[user_role_checker], summary="Refresh access token"
)
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details["exp"]

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_details["user"])
        return JSONResponse(content={"access_token": new_access_token})

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token"
    )
