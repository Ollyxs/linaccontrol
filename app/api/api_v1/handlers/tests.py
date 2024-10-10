from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from app.services.tests_service import TestsService
from app.core.database import get_session
from app.schemas.tests_schema import TestsModel, TestsCreateModel, TestsUpdateModel
from app.api.deps.dependencies import AccessTokenBearer, RoleChecker
from typing import List
from uuid import UUID


test_router = APIRouter()
tets_service = TestsService()
access_token_bearer = AccessTokenBearer()
admin_role_checker = Depends(RoleChecker(["admin"]))
user_role_checker = Depends(RoleChecker(["admin", "fisico", "tecnico"]))


@test_router.get(
    "/",
    response_model=List[TestsModel],
    dependencies=[user_role_checker],
    summary="Get all tests",
)
async def get_all_tests(
    session: AsyncSession = Depends(get_session),
):
    tests = await tets_service.get_all_tests(session)
    return tests


@test_router.get(
    "/{test_uid}",
    response_model=TestsModel,
    dependencies=[user_role_checker],
    summary="Get test by uid",
)
async def get_test(test_uid: UUID, session: AsyncSession = Depends(get_session)):
    test = await tets_service.get_test(test_uid, session)
    if test:
        return test
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Test not found"
        )


@test_router.post(
    "/create",
    summary="Create new test",
    response_model=TestsModel,
    dependencies=[admin_role_checker],
    status_code=status.HTTP_201_CREATED,
)
async def create_test(
    test_data: TestsCreateModel, session: AsyncSession = Depends(get_session)
):
    new_test = await tets_service.create_test(test_data, session)
    return new_test


@test_router.patch(
    "/update/{test_uid}",
    dependencies=[admin_role_checker],
    summary="Update test by uid",
)
async def update_test(
    test_uid: UUID,
    test_update_data: TestsUpdateModel,
    session: AsyncSession = Depends(get_session),
):
    updated_test = await tets_service.update_test(test_uid, test_update_data, session)
    if updated_test is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Test not found"
        )
    else:
        return updated_test


@test_router.delete(
    "/delete/{test_uid}",
    summary="Delete test by uid",
    dependencies=[admin_role_checker],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_test(test_uid: UUID, session: AsyncSession = Depends(get_session)):
    test_to_delete = await tets_service.delete_test(test_uid, session)
    if test_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Test not found"
        )
    else:
        return {}
