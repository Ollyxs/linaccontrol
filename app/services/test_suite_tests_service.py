from typing import List
from sqlalchemy.orm import selectinload
from sqlmodel import select
from app.models import TestSuiteTests, Tests, TestSuite
from app.schemas.test_suite_tests_schema import TestSuiteTestsCreateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID


class TestSuiteTestsService:
    async def get_all_test_suite_tests(self, session: AsyncSession):
        statement = select(TestSuiteTests)
        result = await session.exec(statement)
        return result.all()

    async def get_test_suite_test(self, test_suite_uid: UUID, session: AsyncSession):
        statement = select(TestSuiteTests).where(
            TestSuiteTests.test_suite_uid == test_suite_uid
        )
        result = await session.exec(statement)
        test_suite_test = result.first()
        return test_suite_test if test_suite_test is not None else None

    async def get_test_suite_tests_by_test_suite_uid(
        self, test_suite_uid: UUID, session: AsyncSession
    ):
        statement = select(TestSuiteTests).where(
            TestSuiteTests.test_suite_uid == test_suite_uid
        )
        result = await session.exec(statement)
        test_suite_tests = result.all()
        return test_suite_tests

    async def create_test_suite_tests(
        self, test_suite_uid: UUID, test_uids: List[UUID], session: AsyncSession
    ):
        for test_uid in test_uids:
            new_test_suite_test = TestSuiteTests(
                test_suite_uid=test_suite_uid, test_uid=test_uid
            )
            session.add(new_test_suite_test)
            await session.commit()
        return new_test_suite_test

    async def create_test_suite_test(
        self, test_suite_uid: UUID, test_uid: UUID, session: AsyncSession
    ):
        new_test_suite_test = TestSuiteTests(
            test_suite_uid=test_suite_uid, test_uid=test_uid
        )
        session.add(new_test_suite_test)
        await session.commit()
        return new_test_suite_test

    async def delete_test_suite_test(
        self, test_suite_uid: UUID, test_uid: UUID, session: AsyncSession
    ):
        statement = select(TestSuiteTests).where(
            TestSuiteTests.test_suite_uid == test_suite_uid
            and TestSuiteTests.test_uid == test_uid
        )
        result = await session.exec(statement)
        test_suite_test_to_delete = result.first()
        if test_suite_test_to_delete is not None:
            await session.delete(test_suite_test_to_delete)
            await session.commit()
            return test_suite_test_to_delete
        else:
            return None
