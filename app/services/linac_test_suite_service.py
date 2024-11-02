from sqlmodel import select
from app.models import LinacTestSuite
from app.schemas.linac_test_suite_schema import (
    LinacTestSuiteCreateModel,
    LinacTestSuiteUpdateModel,
)
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID
import logging

logger = logging.getLogger(__name__)


class LinacTestSuiteService:
    async def get_all_linac_test_suites(self, session: AsyncSession):
        statement = select(LinacTestSuite)
        result = await session.exec(statement)
        return result.all()

    async def get_test_suites_for_linac(self, linac_uid: UUID, session: AsyncSession):
        statement = select(LinacTestSuite).where(LinacTestSuite.linac_uid == linac_uid)
        result = await session.exec(statement)
        return result.all()

    async def get_test_suites_for_test_suite(
        self, test_suite_uid: UUID, session: AsyncSession
    ):
        statement = select(LinacTestSuite).where(
            LinacTestSuite.test_suite_uid == test_suite_uid
        )
        result = await session.exec(statement)
        return result.all()

    async def get_linac_test_suite_for_linac_and_test_suite(
        self, linac_uid, test_suite_uid, session: AsyncSession
    ):
        statement = select(LinacTestSuite).where(
            LinacTestSuite.linac_uid == linac_uid
            and LinacTestSuite.test_suite_uid == test_suite_uid
        )
        result = await session.exec(statement)
        result = result.first()
        return result

    async def get_linac_test_suite_for_linac_uid_and_frequency(
        self, linac_uid: UUID, frequency: str, session: AsyncSession
    ):
        statement = select(LinacTestSuite).where(
            LinacTestSuite.linac_uid == linac_uid, LinacTestSuite.frequency == frequency
        )
        result = await session.exec(statement)
        result = result.first()
        return result

    async def create_linac_test_suite(
        self, linac_test_suite_data: LinacTestSuiteCreateModel, session: AsyncSession
    ):
        linac_test_suite_data_dict = linac_test_suite_data.model_dump()
        new_linac_test_suite = LinacTestSuite(**linac_test_suite_data_dict)
        session.add(new_linac_test_suite)
        await session.commit()
        return new_linac_test_suite

    async def update_linac_test_suite(
        self,
        linac_uid: UUID,
        test_suite_uid: UUID,
        update_data: LinacTestSuiteUpdateModel,
        session: AsyncSession,
    ):
        linac_test_suite_to_update = (
            await self.get_linac_test_suite_for_linac_and_test_suite(
                linac_uid, test_suite_uid, session
            )
        )
        if linac_test_suite_to_update is not None:
            update_data_dict = update_data.model_dump()
            for key, value in update_data_dict.items():
                setattr(linac_test_suite_to_update, key, value)
            await session.commit()
            return linac_test_suite_to_update
        else:
            return None

    async def delete_linac_test_suite(
        self, linac_uid: UUID, test_suite_uid: UUID, session: AsyncSession
    ):
        linac_test_suite_to_delete = (
            await self.get_linac_test_suite_for_linac_and_test_suite(
                linac_uid, test_suite_uid, session
            )
        )
        if linac_test_suite_to_delete is not None:
            await session.delete(linac_test_suite_to_delete)
            await session.commit()
        else:
            return None

    # async def assign_test_suite_to_linac(self, test_suite_uid: UUID, linac_test_suite_data)
