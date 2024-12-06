from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas.frequency_schema import (
    FrequencyModel,
    FrequencyCreateModel,
)
from app.services.frequency_service import FrequencyService
from app.api.deps.dependencies import get_session, AccessTokenBearer, RoleChecker
from uuid import UUID
from typing import List

frequency_router = APIRouter()
frequency_service = FrequencyService()
access_token_bearer = AccessTokenBearer()
admin_role_checker = Depends(RoleChecker(["admin"]))


@frequency_router.get(
    "/",
    dependencies=[Depends(access_token_bearer)],
    response_model=List[FrequencyModel],
    summary="Get all frequencies",
)
async def get_all_frequencies(session: AsyncSession = Depends(get_session)):
    return await frequency_service.get_all_frequencies(session)


@frequency_router.get(
    "/{frequency_uid}",
    dependencies=[Depends(access_token_bearer)],
    response_model=FrequencyModel,
    summary="Get a frequency",
)
async def get_frequency(
    frequency_uid: UUID, session: AsyncSession = Depends(get_session)
):
    frequency = await frequency_service.get_frequency(frequency_uid, session)
    if frequency is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Frequency not found"
        )
    return frequency


@frequency_router.post(
    "/",
    dependencies=[admin_role_checker],
    response_model=FrequencyModel,
    status_code=status.HTTP_201_CREATED,
    summary="Create a frequency",
)
async def create_frequency(
    frequency_data: FrequencyCreateModel,
    session: AsyncSession = Depends(get_session),
):
    return await frequency_service.create_frequency(frequency_data, session)
