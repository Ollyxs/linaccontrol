from sqlmodel import select
from app.models import TestResults
from app.schemas.test_results_schema import (
    TestResultsCreateModel,
    TestResultsUpdateModel,
)
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

    async def update_test_results(
        self,
        result_uid: UUID,
        test_results_data: List[TestResultsUpdateModel],
        session: AsyncSession,
    ):
        existing_test_results = await self.get_test_results_by_result_uid(
            result_uid, session
        )
        existing_test_results_dict = {tr.test_uid: tr for tr in existing_test_results}

        for test_result_data in test_results_data:
            test_result_data_dict = test_result_data.model_dump()
            test_uid = test_result_data_dict["test_uid"]
            if test_uid in existing_test_results_dict:
                existing_test_result = existing_test_results_dict[test_uid]
                existing_test_result.result = test_result_data_dict["result"]
            else:
                new_test_results = TestResults(
                    test_uid=test_result_data_dict["test_uid"],
                    result=test_result_data_dict["result"],
                    results_uid=result_uid,
                )
                session.add(new_test_results)

        await session.commit()
        test_results_data_updated = await self.get_test_results_by_result_uid(
            result_uid, session
        )
        return test_results_data_updated
