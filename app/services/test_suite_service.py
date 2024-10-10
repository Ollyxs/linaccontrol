from sqlmodel import select
from app.models import TestSuite
from app.schemas.tests_suite_schema import TestsSuiteCreateModel, TestsSuiteUpdateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID


class TestsSuiteService:
    async def get_all_tests_suite(self, session: AsyncSession):
        statement = select(TestSuite)
        result = await session.exec(statement)
        return result.all()

    async def get_test_suite(self, test_suite_uid: UUID, session: AsyncSession):
        statement = select(TestSuite).where(TestSuite.uid == test_suite_uid)
        result = await session.exec(statement)
        test_suite = result.first()
        return test_suite if test_suite is not None else None

    async def create_test_suite(
        self, test_suite_data: TestsSuiteCreateModel, session: AsyncSession
    ):
        test_suite_data_dict = test_suite_data.model_dump()
        new_test_suite = TestSuite(**test_suite_data_dict)
        session.add(new_test_suite)
        await session.commit()
        return new_test_suite

    async def update_test_suite(
        self,
        test_suite_uid: UUID,
        update_data: TestsSuiteUpdateModel,
        session: AsyncSession,
    ):
        test_suite_to_update = await self.get_test_suite(test_suite_uid, session)
        if test_suite_to_update is not None:
            update_data_dict = update_data.model_dump()
            for k, v in update_data_dict.items():
                setattr(test_suite_to_update, k, v)
            await session.commit()
            return test_suite_to_update
        else:
            return None

    async def delete_test_suite(self, test_suite_uid: UUID, session: AsyncSession):
        test_suite_to_delete = await self.get_test_suite(test_suite_uid, session)
        if test_suite_to_delete is not None:
            await session.delete(test_suite_to_delete)
            await session.commit()
        else:
            return None
