from sqlmodel import select
from app.models import Frequency
from app.schemas.frequency_schema import FrequencyCreateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID


class FrequencyService:
    async def get_all_frequencies(self, session: AsyncSession):
        statement = select(Frequency)
        result = await session.exec(statement)
        return result.all()

    async def get_frequency(self, frequency_uid: UUID, session: AsyncSession):
        statement = select(Frequency).where(Frequency.uid == frequency_uid)
        result = await session.exec(statement)
        frequency = result.first()
        return frequency if frequency is not None else None

    async def get_frequency_by_name(self, name: str, session: AsyncSession):
        statement = select(Frequency).where(Frequency.name == name)
        result = await session.exec(statement)
        frequency = result.first()
        return frequency.uid if frequency is not None else None

    async def create_frequency(
        self, frequency_data: FrequencyCreateModel, session: AsyncSession
    ):
        frequency_data_dict = frequency_data.model_dump()
        new_frequency = Frequency(**frequency_data_dict)
        session.add(new_frequency)
        await session.commit()
        return new_frequency
