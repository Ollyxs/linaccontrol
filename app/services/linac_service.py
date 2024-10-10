from sqlmodel import select
from app.models import Linac
from app.schemas.linac_schema import LinacCreateModel, LinacUpdateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID


class LinacService:
    async def get_all_linacs(self, session: AsyncSession):
        statement = select(Linac)
        result = await session.exec(statement)
        return result.all()

    async def get_linac(self, linac_uid: UUID, session: AsyncSession):
        statement = select(Linac).where(Linac.uid == linac_uid)
        result = await session.exec(statement)
        linac = result.first()
        return linac if linac is not None else None

    async def create_linac(self, linac_data: LinacCreateModel, session: AsyncSession):
        linac_data_dict = linac_data.model_dump()
        new_linac = Linac(**linac_data_dict)
        session.add(new_linac)
        await session.commit()
        return new_linac

    async def update_linac(
        self, linac_uid: UUID, update_data: LinacUpdateModel, session: AsyncSession
    ):
        linac_to_update = await self.get_linac(linac_uid, session)
        if linac_to_update is not None:
            update_data_dict = update_data.model_dump()
            for k, v in update_data_dict.items():
                setattr(linac_to_update, k, v)
            await session.commit()
            return linac_to_update
        else:
            return None

    async def delete_linac(self, linac_uid: UUID, session: AsyncSession):
        linac_to_delete = await self.get_linac(linac_uid, session)
        if linac_to_delete is not None:
            await session.delete(linac_to_delete)
            await session.commit()
        else:
            return None
