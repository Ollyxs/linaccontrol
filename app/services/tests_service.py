from sqlmodel import select
from app.models import Tests
from app.models.test_category import TestCategory
from app.schemas.tests_schema import TestsCreateModel, TestsUpdateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID
import logging

logger = logging.getLogger(__name__)


class TestsService:
    async def get_all_tests(self, session: AsyncSession):
        statement = select(Tests).order_by(Tests.category_uid)
        result = await session.exec(statement)
        return result.all()

    async def get_test(self, test_uid: UUID, session: AsyncSession):
        statement = (
            select(Tests, TestCategory)
            .join(TestCategory, Tests.category_uid == TestCategory.uid)
            .where(Tests.uid == test_uid)
        )
        result = await session.exec(statement)
        test, category = result.first()
        if test:
            test_dict = test.model_dump()
            test_dict["category_name"] = category.name
            return test_dict
        return None
        # return test if test is not None else None

    async def create_test(self, test_data: TestsCreateModel, session: AsyncSession):
        test_data_dict = test_data.model_dump()
        new_test = Tests(**test_data_dict)
        session.add(new_test)
        await session.commit()
        return new_test

    async def update_test(
        self, test_uid: UUID, update_data: TestsUpdateModel, session: AsyncSession
    ):
        test_to_update = await self.get_test(test_uid, session)
        if test_to_update is not None:
            update_data_dict = update_data.model_dump()
            for k, v in update_data_dict.items():
                setattr(test_to_update, k, v)
            await session.commit()
            return test_to_update
        else:
            return None

    async def delete_test(self, test_uid: UUID, session: AsyncSession):
        test_to_delete = await self.get_test(test_uid, session)
        if test_to_delete is not None:
            await session.delete(test_to_delete)
            await session.commit()
        else:
            return None
