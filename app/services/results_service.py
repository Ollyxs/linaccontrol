from sqlalchemy import func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import result
from sqlmodel import select
from app.models import Results
from app.models.linac_test_suite import FrequencyEnum
from app.models.omitted_date import OmittedDate
from app.schemas.results_schema import ResultsCreateModel, ResultsUpdateModel
from app.schemas.test_results_schema import (
    TestResultsModel,
    TestResultsCreateModel,
    TestResultsUpdateModel,
)
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime, timedelta
from uuid import UUID
import logging

logger = logging.getLogger(__name__)


class ResultsService:
    async def get_all_results(
        self,
        session: AsyncSession,
        skip: int = 0,
        limit: int = 10,
    ):
        statement = (
            select(Results).order_by(Results.created_at).offset(skip).limit(limit)
        )
        results = await session.exec(statement)
        return results.all()

    async def get_result(self, result_uid: UUID, session: AsyncSession):
        statement = (
            select(Results)
            .where(Results.uid == result_uid)
            .options(selectinload(Results.tests))
        )
        result = await session.exec(statement)
        result = result.first()
        return result if result is not None else None

    async def create_result(
        self,
        result_data: ResultsCreateModel,
        realized_by: UUID,
        session: AsyncSession,
    ):
        result_data_dict = result_data.model_dump()
        result_data_dict["realized_by"] = realized_by
        if result_data_dict["created_at"] is None:
            result_data_dict["created_at"] = datetime.now()

        if await self.results_exist_for_date(
            result_data_dict["linac_uid"],
            result_data_dict["test_suite_uid"],
            result_data_dict["frequency"],
            result_data_dict["created_at"],
            session,
        ):
            return None, "Results already exist for this date."

        missing_dates = await self.missing_results_for_previous_days(
            result_data_dict["linac_uid"],
            result_data_dict["test_suite_uid"],
            result_data_dict["frequency"],
            result_data_dict["created_at"],
            session,
        )

        if missing_dates:
            missing_dates_str = [date.strftime("%Y-%m-%d") for date in missing_dates]
            return None, f"Missing results for dates: {missing_dates_str}"

        new_result = Results(**result_data_dict)
        session.add(new_result)
        await session.commit()
        return new_result

    async def update_result(
        self, result_uid: UUID, update_data: ResultsUpdateModel, session: AsyncSession
    ):
        result_to_update = await self.get_result(result_uid, session)
        if result_to_update is not None:
            if result_to_update.frequency == FrequencyEnum.monthly:
                current_date = datetime.now()
                if (
                    current_date.day > 20
                    or current_date.month != result_to_update.created_at.month
                ):
                    return (
                        None,
                        "Monthly results can only be update within the first 20 days of the month.",
                    )

            update_data_dict = update_data.model_dump()
            for k, v in update_data_dict.items():
                setattr(result_to_update, k, v)
            await session.commit()
            return result_to_update, None
        else:
            return None, "Result not found."

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
        if frequency == FrequencyEnum.monthly:
            start_of_month = datetime(date.year, date.month, 1)
            end_of_month = (
                datetime(date.year, date.month + 1, 1)
                if date.month < 12
                else datetime(date.year + 1, 1, 1)
            )
            statement = select(Results).where(
                Results.linac_uid == linac_uid,
                Results.test_suite_uid == test_suite_uid,
                Results.frequency == frequency,
                Results.created_at >= start_of_month,
                Results.created_at < end_of_month,
            )
        elif frequency == FrequencyEnum.daily:
            start_of_date = datetime(date.year, date.month, date.day)
            end_of_date = start_of_date + timedelta(days=1)
            statement = select(Results).where(
                Results.linac_uid == linac_uid,
                Results.test_suite_uid == test_suite_uid,
                Results.frequency == frequency,
                Results.created_at >= start_of_date,
                Results.created_at < end_of_date,
            )
        else:
            return None

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
        if frequency != FrequencyEnum.daily:
            return []

        statement_count = select(func.count()).where(
            Results.linac_uid == linac_uid,
            Results.test_suite_uid == test_suite_uid,
            Results.frequency == frequency,
        )
        result_count = await session.exec(statement_count)
        count = result_count.one()
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
        results_dates = {result.created_at for result in results_list}

        omitted_dates_statement = select(OmittedDate).where(
            (OmittedDate.linac_uid == None) | (OmittedDate.linac_uid == linac_uid)
        )
        omitted_dates_result = await session.exec(omitted_dates_statement)
        omitted_dates = {
            omitted_date.date for omitted_date in omitted_dates_result.all()
        }

        missing_dates = [
            start_date + timedelta(days=i)
            for i in range((end_date - start_date).days)
            if (start_date + timedelta(days=i)).weekday() not in [5, 6]
            and (start_date + timedelta(days=i)) not in results_dates
            and (start_date + timedelta(days=i)) not in omitted_dates
        ]
        return missing_dates
