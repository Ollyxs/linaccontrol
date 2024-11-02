from sqlalchemy import func
from sqlalchemy.ext.asyncio import result
from sqlmodel import select
from app.models import Results
from app.models.linac_test_suite import FrequencyEnum
from app.schemas.results_schema import ResultsCreateModel, ResultsUpdateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime, timedelta
from uuid import UUID
import logging

logger = logging.getLogger(__name__)


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
        self,
        # linac_uid: UUID,
        # test_suite_uid: UUID,
        # frequency: FrequencyEnum,
        result_data: ResultsCreateModel,
        realized_by: UUID,
        session: AsyncSession,
        # date: datetime = None
    ):
        result_data_dict = result_data.model_dump()
        result_data_dict["realized_by"] = realized_by
        if result_data_dict["created_at"] is None:
            result_data_dict["created_at"] = datetime.now()
        # else:
        # date = date.date()

        if await self.results_exist_for_date(
            result_data_dict["linac_uid"],
            result_data_dict["test_suite_uid"],
            result_data_dict["frequency"],
            result_data_dict["created_at"],
            session,
        ):
            logger.error("Results already exist for this date")
            raise ValueError("Results already exist for this date")

        missing_dates = await self.missing_results_for_previous_days(
            result_data_dict["linac_uid"],
            result_data_dict["test_suite_uid"],
            result_data_dict["frequency"],
            result_data_dict["created_at"],
            session,
            # linac_uid, test_suite_uid, frequency, date, session
        )
        if missing_dates:
            logger.error(f"Missing results for dates: {missing_dates}")
            raise ValueError(f"Missing results for dates: {missing_dates}")
        new_result = Results(**result_data_dict)
        session.add(new_result)
        await session.commit()
        return new_result

    async def update_result(
        self, result_uid: UUID, update_data: ResultsUpdateModel, session: AsyncSession
    ):
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

    async def results_exist_for_date(
        self,
        linac_uid: UUID,
        test_suite_uid: UUID,
        frequency: FrequencyEnum,
        date: datetime,
        session: AsyncSession,
    ):
        start_of_date = datetime(date.year, date.month, date.day)
        end_of_date = start_of_date + timedelta(days=1)
        statement = select(Results).where(
            Results.linac_uid == linac_uid,
            Results.test_suite_uid == test_suite_uid,
            Results.frequency == frequency,
            Results.created_at >= start_of_date,
            Results.created_at < end_of_date,
        )
        results = await session.exec(statement)
        return results.first() is not None

    async def missing_results_for_previous_days(
        self,
        linac_uid: UUID,
        test_suite_uid: UUID,
        frequency: FrequencyEnum,
        date: datetime,
        session: AsyncSession,
    ):
        statement_count = select(func.count()).where(
            Results.linac_uid == linac_uid,
            Results.test_suite_uid == test_suite_uid,
            Results.frequency == frequency,
        )
        result_count = await session.exec(statement_count)
        logger.info(f"\n##########\nResult Count: {result_count}\n##########")
        count = result_count.one()
        logger.info(f"\n##########\nCount: {count}\n##########")
        if count == 0:
            return []

        start_date = (
            datetime(date.year, date.month, date.day) - timedelta(days=count)
        ).date()
        end_date = datetime(date.year, date.month, date.day).date()
        statement = select(Results).where(
            Results.linac_uid == linac_uid,
            Results.test_suite_uid == test_suite_uid,
            Results.frequency == frequency,
            Results.created_at >= start_date,
            Results.created_at < end_date,
        )
        results = await session.exec(statement)
        results_list = results.all()
        logger.info(f"\n##########\nResults: {results_list}\n##########")
        results_dates = {result.created_at.date() for result in results_list}
        logger.info(f"\n##########\nResults Dates: {results_dates}\n##########")
        missing_dates = [
            start_date + timedelta(days=i)
            for i in range((end_date - start_date).days)
            if (start_date + timedelta(days=i)) not in results_dates
        ]
        logger.info(f"\n##########\nMissing Dates: {missing_dates}\n##########")
        return missing_dates
