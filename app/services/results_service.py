from sqlalchemy.ext.asyncio import result
from sqlmodel import select
from app.models import Results
from app.schemas.results_schema import ResultsCreateModel, ResultsUpdateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID


class ResultsService:
    async def get_all_results(self, session):
        statement = select(Results)
        results = await session.exec(statement)
        return results.all()

    async def get_result(self, result_uid: UUID, session: AsyncSession):
        statement = select(Results).where(Results.uid == result_uid)
        result = await session.exec(statement)
        result = result.first()
        return result if result is not None else None

    async def create_result(
        self, result_data: ResultsCreateModel, realized_by: UUID, session: AsyncSession
    ):
        result_data_dict = result_data.model_dump()
        result_data_dict["realized_by"] = realized_by
        new_result = Results(**result_data_dict)
        session.add(new_result)
        await session.commit()
        return new_result

    async def update_result(self, result_uid: UUID, re, session: AsyncSession):
        result_to_update = await self.get_result(result_uid, session)
        if result_to_update is not None:
            update_data_dict = update_data.model_dump()
            for k, v in update_data_dict.items():
                setattr(result_to_update, k, v)
            await session.commit()
            return result_to_update
        else:
            return None

    async def delete_result(self, result_uid: UUID, session: AsyncSession):
        result_to_delete = await self.get_result(result_uid, session)
        if result_to_delete is not None:
            await session.delete(result_to_delete)
            await session.commit()
        else:
            return None
