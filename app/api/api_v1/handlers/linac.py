from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from app.services.linac_service import LinacService
from app.core.database import get_session
from app.schemas.linac_schema import LinacModel, LinacCreateModel, LinacUpdateModel
from app.api.deps.dependencies import AccessTokenBearer, RoleChecker, get_current_user
from typing import List
from uuid import UUID


linac_router = APIRouter()
linac_service = LinacService()
access_token_bearer = AccessTokenBearer()
admin_role_checker = Depends(RoleChecker(["admin"]))
user_role_checker = Depends(RoleChecker(["admin", "fisico", "tecnico"]))


@linac_router.get(
    "/",
    response_model=List[LinacModel],
    dependencies=[user_role_checker],
    summary="Get all linacs",
)
async def get_all_linacs(
    session: AsyncSession = Depends(get_session),
):
    linacs = await linac_service.get_all_linacs(session)
    return linacs


@linac_router.get(
    "/{linac_uid}",
    response_model=LinacModel,
    dependencies=[user_role_checker],
    summary="Get linac by uid",
)
async def get_linac(linac_uid: UUID, session: AsyncSession = Depends(get_session)):
    linac = await linac_service.get_linac(linac_uid, session)
    if linac:
        return linac
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Linac not found"
        )


@linac_router.post(
    "/create",
    summary="Create new linac",
    response_model=LinacModel,
    dependencies=[admin_role_checker],
    status_code=status.HTTP_201_CREATED,
)
async def create_linac(
    linac_data: LinacCreateModel, session: AsyncSession = Depends(get_session)
):
    new_linac = await linac_service.create_linac(linac_data, session)
    return new_linac


@linac_router.patch(
    "/update/{linac_uid}",
    dependencies=[admin_role_checker],
    summary="Update linac by uid",
)
async def update_linac(
    linac_uid: UUID,
    linac_update_data: LinacUpdateModel,
    session: AsyncSession = Depends(get_session),
):
    updated_linac = await linac_service.update_linac(
        linac_uid, linac_update_data, session
    )
    if updated_linac is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Linac not found"
        )
    else:
        return updated_linac


@linac_router.delete(
    "/delete/{linac_uid}",
    dependencies=[admin_role_checker],
    summary="Delete linac by uid",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_linac(linac_uid: UUID, session: AsyncSession = Depends(get_session)):
    linac_to_delete = await linac_service.delete_linac(linac_uid, session)
    if linac_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Linac not found"
        )
    else:
        return {}
