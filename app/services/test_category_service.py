from sqlmodel import select
from app.models import TestCategory
from app.schemas.test_category_schema import TestCategoryCreateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID


class TestCategoryService:
    async def get_all_test_categories(self, session: AsyncSession):
        statement = select(TestCategory)
        result = await session.exec(statement)
        return result.all()

    async def get_test_category(self, test_category_uid: UUID, session: AsyncSession):
        statement = select(TestCategory).where(TestCategory.uid == test_category_uid)
        result = await session.exec(statement)
        return result.first()

    async def get_test_category_by_name(self, uid: UUID, session: AsyncSession):
        statement = select(TestCategory).where(TestCategory.uid == uid)
        result = await session.exec(statement)
        category = result.first()
        return category.name if category is not None else None

    async def create_test_category(
        self, test_category_data: TestCategoryCreateModel, session: AsyncSession
    ):
        test_category_data_dict = test_category_data.model_dump()
        new_test_category = TestCategory(**test_category_data_dict)
        session.add(new_test_category)
        await session.commit()
        return new_test_category
