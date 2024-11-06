from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.users import User
from app.schemas.test_results_schema import (
    TestResultsCreateModel,
    TestResultsModel,
    TestResultsUpdateModel,
)
from app.services.results_service import ResultsService
from app.services.test_results_service import TestResultsService
from app.core.database import get_session
from app.schemas.results_schema import (
    ResultsModel,
    ResultsCreateModel,
    ResultsUpdateModel,
)
from app.api.deps.dependencies import AccessTokenBearer, RoleChecker, get_current_user
from typing import List
from uuid import UUID


results_router = APIRouter()
results_service = ResultsService()
test_results_service = TestResultsService()
access_token_bearer = AccessTokenBearer()
admin_role_checker = Depends(RoleChecker(["admin"]))
fisico_role_checker = Depends(RoleChecker(["admin", "fisico"]))
tecnico_role_checker = Depends(RoleChecker(["admin", "tecnico"]))
user_role_checker = Depends(RoleChecker(["admin", "fisico", "tecnico"]))


@results_router.get("/", dependencies=[user_role_checker], summary="Get all results")
async def get_all_results(
    session: AsyncSession = Depends(get_session),
    user_details=Depends(access_token_bearer),
):
    results = await results_service.get_all_results(session)
    return results


@results_router.get(
    "/{result_uid}", dependencies=[user_role_checker], summary="Get a result"
)
async def get_result(
    result_uid: UUID,
    session: AsyncSession = Depends(get_session),
    user_details=Depends(access_token_bearer),
):
    result = await results_service.get_result(result_uid, session)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Result not found"
        )
    return result


@results_router.post(
    "/",
    dependencies=[user_role_checker],
    status_code=status.HTTP_201_CREATED,
    summary="Create a result",
)
async def create_result(
    result_data: ResultsCreateModel,
    test_results_data: List[TestResultsCreateModel],
    session: AsyncSession = Depends(get_session),
    user_details=Depends(access_token_bearer),
    current_user: User = Depends(get_current_user),
):
    new_result = await results_service.create_result(
        result_data, current_user.uid, session
    )
    await test_results_service.create_test_results(
        new_result.uid, test_results_data, session
    )
    test_results = await test_results_service.get_test_results_by_result_uid(
        new_result.uid, session
    )

    return {"result": new_result, "test_results": test_results}


@results_router.patch(
    "/review/{result_uid}",
    dependencies=[fisico_role_checker],
    response_model=ResultsModel,
    summary="Review a result",
)
async def review_result(
    result_uid: UUID,
    session: AsyncSession = Depends(get_session),
    user_details=Depends(access_token_bearer),
    current_user: User = Depends(get_current_user),
):
    updated_result = await results_service.update_result(
        result_uid, current_user.uid, session
    )
    if updated_result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Result not found"
        )
    return updated_result


@results_router.patch(
    "/{result_uid}",
    dependencies=[fisico_role_checker],
    # response_model=ResultsModel,
    summary="Update a result",
)
async def update_result(
    result_uid: UUID,
    result_update_data: ResultsUpdateModel,
    test_results_data: List[TestResultsUpdateModel],
    session: AsyncSession = Depends(get_session),
    user_details=Depends(access_token_bearer),
):
    updated_result = await results_service.update_result(
        result_uid, result_update_data, session
    )
    if updated_result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Result not found"
        )

    updated_test_results = await test_results_service.update_test_results(
        result_uid, test_results_data, session
    )
    return {"result": updated_result, "test_results": updated_test_results}


@results_router.delete(
    "/{result_uid}",
    dependencies=[admin_role_checker],
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a result",
)
async def delete_result(
    result_uid: UUID,
    session: AsyncSession = Depends(get_session),
    user_details=Depends(access_token_bearer),
):
    result_to_delete = await results_service.delete_result(result_uid, session)
    if result_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Result not found"
        )
    else:
        return None
