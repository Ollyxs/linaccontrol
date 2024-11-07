from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas.omitted_date_schema import (
    OmittedDateModel,
    OmittedDateCreateModel,
    OmittedDateUpdateModel,
)
from app.services.omitted_date_service import OmittedDateService
from app.api.deps.dependencies import (
    AccessTokenBearer,
    RoleChecker,
    get_current_user,
    get_session,
)
from uuid import UUID
from typing import List

omitted_date_router = APIRouter()
omitted_date_service = OmittedDateService()
access_token_bearer = AccessTokenBearer()
admin_role_checker = Depends(RoleChecker(["admin"]))
user_role_checker = Depends(RoleChecker(["admin", "fisico", "tecnico"]))


@omitted_date_router.get(
    "/",
    dependencies=[user_role_checker],
    response_model=List[OmittedDateModel],
    summary="Get all omitted dates",
)
async def get_all_omitted_dates(session: AsyncSession = Depends(get_session)):
    return await omitted_date_service.get_all_omitted_dates(session)


@omitted_date_router.post(
    "/",
    dependencies=[admin_role_checker],
    response_model=OmittedDateModel,
    status_code=status.HTTP_201_CREATED,
    summary="Create new omitted date",
)
async def create_omitted_date(
    omitted_date_data: OmittedDateCreateModel,
    session: AsyncSession = Depends(get_session),
):
    return await omitted_date_service.create_omitted_date(omitted_date_data, session)


@omitted_date_router.patch(
    "/{omitted_date_uid}",
    dependencies=[admin_role_checker],
    response_model=OmittedDateModel,
    summary="Update omitted date",
)
async def update_omitted_date(
    omitted_date_uid: UUID,
    update_data: OmittedDateUpdateModel,
    session: AsyncSession = Depends(get_session),
):
    omitted_date = await omitted_date_service.update_omitted_date(
        omitted_date_uid, update_data, session
    )
    if omitted_date is None:
        raise HTTPException(status_code=404, detail="Omitted date not found")
    return omitted_date


@omitted_date_router.delete(
    "/{omitted_date_uid}",
    dependencies=[admin_role_checker],
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete omitted date",
)
async def delete_omitted_date(
    omitted_date_uid: UUID, session: AsyncSession = Depends(get_session)
):
    omitted_date = await omitted_date_service.delete_omitted_date(
        omitted_date_uid, session
    )
    if omitted_date:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Omitted date not found"
        )
    return {}
