from sqlmodel import select
from app.models.omitted_date import OmittedDate
from app.schemas.omitted_date_schema import (
    OmittedDateCreateModel,
    OmittedDateUpdateModel,
)
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID


class OmittedDateService:
    async def get_all_omitted_dates(
        self,
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100,
    ):
        statement = select(OmittedDate).offset(skip).limit(limit)
        result = await session.exec(statement)
        return result.all()

    async def get_omitted_date(self, omitted_date_uid: UUID, session: AsyncSession):
        statement = select(OmittedDate).where(OmittedDate.uid == omitted_date_uid)
        result = await session.exec(statement)
        omitted_date = result.first()
        return omitted_date if omitted_date is not None else None

    async def create_omitted_date(
        self, omitted_date_data: OmittedDateCreateModel, session: AsyncSession
    ):
        omitted_date_data_dict = omitted_date_data.model_dump()
        new_omitted_date = OmittedDate(**omitted_date_data_dict)
        session.add(new_omitted_date)
        await session.commit()
        return new_omitted_date

    async def update_omitted_date(
        self,
        omitted_date_uid: UUID,
        update_data: OmittedDateUpdateModel,
        session: AsyncSession,
    ):
        omitted_date_to_update = await self.get_omitted_date(omitted_date_uid, session)
        if omitted_date_to_update is not None:
            update_data_dict = update_data.model_dump()
            for k, v in update_data_dict.items():
                setattr(omitted_date_to_update, k, v)
            await session.commit()
            return omitted_date_to_update
        else:
            return None

    async def delete_omitted_date(self, omitted_date_uid: UUID, session: AsyncSession):
        omitted_date_to_delete = await self.get_omitted_date(omitted_date_uid, session)
        if omitted_date_to_delete is not None:
            await session.delete(omitted_date_to_delete)
            await session.commit()
        else:
            return None
