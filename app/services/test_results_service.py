from sqlmodel import select
from app.models import TestResults
from app.schemas.test_results_schema import TestResultsCreateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from uuid import UUID


class TestResultsService:
    async def get_all_test_results(self, session: AsyncSession):
        statement = select(TestResults)
        result = await session.exec(statement)
        return result.all()

    async def get_test_result(self, test_result_uid: UUID, session: AsyncSession):
        statement = select(TestResults).where(TestResults.uid == test_result_uid)
        result = await session.exec(statement)
        test_result = result.first()
        return test_result if test_result is not None else None

    async def get_test_results_by_result_uid(
        self, results_uid: UUID, session: AsyncSession
    ):
        statement = select(TestResults).where(TestResults.results_uid == results_uid)
        result = await session.exec(statement)
        test_results = result.all()
        return test_results

    async def create_test_results(
        self,
        result_uid: UUID,
        test_results_data: List[TestResultsCreateModel],
        session: AsyncSession,
    ):
        for test_result_data in test_results_data:
            test_result_data_dict = test_result_data.model_dump()
            new_test_results = TestResults(
                test_uid=test_result_data_dict["test_uid"],
                result=test_result_data_dict["result"],
                results_uid=result_uid,
            )
            session.add(new_test_results)
        await session.commit()
        return new_test_results

    # async def create_test_result(
    #     self, test_result_data: TestResultsCreateModel, session: AsyncSession
    # ):
    #     test_result_data_dict = test_result_data.model_dump()
    #     new_test_result = TestResults(**test_result_data_dict)
    #     session.add(new_test_result)
    #     await session.commit()
    #     return new_test_result
