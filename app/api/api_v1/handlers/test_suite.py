from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from app.services import test_suite_tests_service
from app.services.linac_service import LinacService
from app.services.tests_service import TestsService
from app.services.test_suite_service import TestsSuiteService
from app.services.test_suite_tests_service import TestSuiteTestsService
from app.services.linac_test_suite_service import LinacTestSuiteService
from app.services.frequency_service import FrequencyService
from app.services.test_category_service import TestCategoryService
from app.services.results_service import ResultsService
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
from typing import List, Optional
from uuid import UUID
from datetime import datetime
import logging


logger = logging.getLogger(__name__)
test_suite_router = APIRouter()
linac_service = LinacService()
tests_service = TestsService()
test_suite_service = TestsSuiteService()
test_suite_tests_service = TestSuiteTestsService()
linac_test_suite_service = LinacTestSuiteService()
frequency_service = FrequencyService()
test_category_service = TestCategoryService()
results_service = ResultsService()
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
        category_name = await test_category_service.get_test_category_by_name(
            result.category_uid, session
        )
        result.category_name = category_name
        tests.append(result)
    tests.sort(key=lambda x: x.category_name)
    if test_suite:
        return {"test_suite": test_suite, "test_suite_tests": tests}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Test suite not found"
        )


@test_suite_router.get(
    "/{linac_uid}/{frequency}",
    dependencies=[user_role_checker],
    summary="Get test suite by linac uid and frequency",
)
async def get_test_suite_by_linac_uid_and_frequency(
    linac_uid: UUID,
    frequency: str,
    date: Optional[datetime] = None,
    session: AsyncSession = Depends(get_session),
):

    frequency_uid = await frequency_service.get_frequency_by_name(frequency, session)
    if not frequency_uid:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Frequency not found"
        )

    frequency_dict = {"uid": frequency_uid, "name": frequency}

    linac_test_suite = (
        await linac_test_suite_service.get_linac_test_suite_for_linac_uid_and_frequency(
            linac_uid, frequency_uid, session
        )
    )
    if linac_test_suite:
        linac = await linac_service.get_linac(linac_uid, session)
        test_suite = await test_suite_service.get_test_suite(
            linac_test_suite.test_suite_uid, session
        )
        test_suite_tests = (
            await test_suite_tests_service.get_test_suite_tests_by_test_suite_uid(
                linac_test_suite.test_suite_uid, session
            )
        )
        tests = []
        for test in test_suite_tests:
            result = await tests_service.get_test(test.test_uid, session)
            tests.append(result)
        tests.sort(
            key=lambda x: (x["category_name"], -ord(x["test_name"][0])), reverse=True
        )

        # Verficar si ya existe un resultado para la fecha especificada
        current_date = date or datetime.now()
        if await results_service.results_exist_for_date(
            linac_uid,
            linac_test_suite.test_suite_uid,
            frequency_uid,
            current_date,
            session,
        ):
            if frequency == "mensual":
                existing_result = (
                    await results_service.get_result_by_linac_test_suite_and_frequency(
                        linac_uid,
                        linac_test_suite.test_suite_uid,
                        frequency_uid,
                        session,
                    )
                )

                if existing_result:
                    for test in tests:
                        for test_result in existing_result["tests"]:
                            if str(test_result["test_uid"]) == str(test["uid"]):
                                test["result"] = test_result["result"]
                return {
                    "linac": linac,
                    "frequency": frequency_dict,
                    "test_suite": test_suite,
                    "test_suite_tests": tests,
                    "result_uid": existing_result["uid"],
                    "result": existing_result["result"],
                }
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Results already exist for this date",
                )

        # Verificar si faltan resultados para días anteriores
        missing_dates = await results_service.missing_results_for_previous_days(
            linac_uid,
            linac_test_suite.test_suite_uid,
            frequency_uid,
            current_date,
            session,
        )
        if missing_dates:
            missing_dates_str = [date.strftime("%Y-%m-%d") for date in missing_dates]
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Missing results for dates: {missing_dates_str}",
            )

        if test_suite:
            return {
                "linac": linac,
                "frequency": frequency_dict,
                "test_suite": test_suite,
                "test_suite_tests": tests,
            }
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


@test_suite_router.post(
    "/{test_suite_uid}/add_test/{test_uid}",
    dependencies=[admin_role_checker],
    summary="Add test to test suite",
    status_code=status.HTTP_201_CREATED,
)
async def add_test_to_test_suite(
    test_suite_uid: UUID,
    test_uid: UUID,
    session: AsyncSession = Depends(get_session),
):
    new_test_suite_test = await test_suite_tests_service.create_test_suite_test(
        test_suite_uid, test_uid, session
    )
    return new_test_suite_test


@test_suite_router.delete(
    "/{test_suite_uid}/remove_test/{test_uid}",
    dependencies=[admin_role_checker],
    summary="Remove test from test suite",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_test_from_test_suite(
    test_suite_uid: UUID,
    test_uid: UUID,
    session: AsyncSession = Depends(get_session),
):
    test_suite_test_to_delete = await test_suite_tests_service.delete_test_suite_test(
        test_suite_uid, test_uid, session
    )
    if test_suite_test_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Test suite test not found"
        )
    return {}
