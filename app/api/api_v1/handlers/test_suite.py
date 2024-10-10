from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from app.services import test_suite_tests_service
from app.services.tests_service import TestsService
from app.services.test_suite_service import TestsSuiteService
from app.services.test_suite_tests_service import TestSuiteTestsService
from app.services.linac_test_suite_service import LinacTestSuiteService
from app.core.database import get_session
from app.schemas.tests_suite_schema import (
    TestsSuiteModel,
    TestsSuiteCreateModel,
    TestsSuiteUpdateModel,
)
from app.schemas.test_suite_tests_schema import (
    TestSuiteTestsModel,
    TestSuiteTestsCreateModel,
)
from app.schemas.linac_test_suite_schema import (
    LinacTestSuiteCreateModel,
    LinacTestSuiteModel,
)
from app.api.deps.dependencies import AccessTokenBearer, RoleChecker
from typing import List
from uuid import UUID
from logging import log


test_suite_router = APIRouter()
tests_service = TestsService()
test_suite_service = TestsSuiteService()
test_suite_tests_service = TestSuiteTestsService()
linac_test_suite_service = LinacTestSuiteService()
access_token_bearer = AccessTokenBearer()
admin_role_checker = Depends(RoleChecker(["admin"]))
user_role_checker = Depends(RoleChecker(["admin", "fisico", "tecnico"]))


@test_suite_router.get(
    "/",
    response_model=List[TestsSuiteModel],
    dependencies=[user_role_checker],
    summary="Get all test suites",
)
async def get_all_tests_suite(
    session: AsyncSession = Depends(get_session),
):
    test_suites = await test_suite_service.get_all_tests_suite(session)
    return test_suites


@test_suite_router.get(
    "/{test_suite_uid}",
    dependencies=[user_role_checker],
    summary="Get test suite by uid",
)
async def get_test_suite(
    test_suite_uid: UUID, session: AsyncSession = Depends(get_session)
):
    test_suite = await test_suite_service.get_test_suite(test_suite_uid, session)
    test_suite_tests = (
        await test_suite_tests_service.get_test_suite_tests_by_test_suite_uid(
            test_suite_uid, session
        )
    )
    tests = []
    for test in test_suite_tests:
        result = await tests_service.get_test(test.test_uid, session)
        tests.append(result)
    tests.sort(key=lambda x: x.category)
    if test_suite:
        return {"test_suite": test_suite, "test_suite_tests": tests}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Test suite not found"
        )


@test_suite_router.post(
    "/", dependencies=[admin_role_checker], summary="Create new test suite"
)
async def create_test_suite(
    test_suite_data: TestsSuiteCreateModel,
    test_suite_tests_data: TestSuiteTestsCreateModel,
    session: AsyncSession = Depends(get_session),
):
    new_test_suite = await test_suite_service.create_test_suite(
        test_suite_data, session
    )
    await test_suite_tests_service.create_test_suite_tests(
        new_test_suite.uid, test_suite_tests_data.test_uid, session
    )
    # for test_uid in test_suite_tests_data.test_uid:
    #     test_data = TestSuiteTestsCreateModel(
    #         test_uid=test_uid, test_suite_uid=new_test_suite.uid
    #     )
    #     await test_suite_tests_service.create_test_suite_test(test_data, session)
    created_test_suite = await test_suite_service.get_test_suite(
        new_test_suite.uid, session
    )
    return created_test_suite


@test_suite_router.post(
    "/assing",
    response_model=LinacTestSuiteModel,
    dependencies=[admin_role_checker],
    summary="Assing test suite to linac",
    status_code=status.HTTP_201_CREATED,
)
async def add_linac_to_test_suite(
    linac_test_suite_data: LinacTestSuiteCreateModel,
    session: AsyncSession = Depends(get_session),
):

    new_linac_test_suite = await linac_test_suite_service.create_linac_test_suite(
        linac_test_suite_data, session
    )
    return new_linac_test_suite
