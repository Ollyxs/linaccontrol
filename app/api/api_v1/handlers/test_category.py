from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas.test_category_schema import (
    TestCategoryModel,
    TestCategoryCreateModel,
)
from app.services.test_category_service import TestCategoryService
from app.api.deps.dependencies import get_session, AccessTokenBearer, RoleChecker
from uuid import UUID
from typing import List

test_category_router = APIRouter()
test_category_service = TestCategoryService()
access_token_bearer = AccessTokenBearer()
admin_role_checker = Depends(RoleChecker(["admin"]))


@test_category_router.get(
    "/",
    dependencies=[Depends(access_token_bearer)],
    response_model=List[TestCategoryModel],
    summary="Get all test categories",
)
async def get_all_test_categories(session: AsyncSession = Depends(get_session)):
    return await test_category_service.get_all_test_categories(session)


@test_category_router.get(
    "/{test_category_uid}",
    dependencies=[Depends(access_token_bearer)],
    response_model=TestCategoryModel,
    summary="Get a test category",
)
async def get_test_category(
    test_category_uid: UUID, session: AsyncSession = Depends(get_session)
):
    test_category = await test_category_service.get_test_category(
        test_category_uid, session
    )
    if test_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Test category not found"
        )
    return test_category


@test_category_router.post(
    "/",
    dependencies=[admin_role_checker],
    response_model=TestCategoryModel,
    status_code=status.HTTP_201_CREATED,
    summary="Create a test category",
)
async def create_test_category(
    test_category_data: TestCategoryCreateModel,
    session: AsyncSession = Depends(get_session),
):
    return await test_category_service.create_test_category(test_category_data, session)
