from typing import List, Optional
from sqlmodel import SQLModel
from datetime import date
from uuid import UUID
from app.schemas.test_results_schema import TestResultsModel


class ResultsModel(SQLModel):
    uid: UUID
    linac_uid: UUID
    test_suite_uid: UUID
    frequency_uid: UUID
    result: Optional[str]
    realized_by: UUID
    reviewed_by: Optional[UUID]
    created_at: date
    updated_at: date
    tests: List[TestResultsModel]


class ResultsCreateModel(SQLModel):
    linac_uid: UUID
    test_suite_uid: UUID
    frequency_uid: UUID
    result: str
    created_at: Optional[date] = None


class ResultsUpdateModel(SQLModel):
    result: Optional[str]
    reviewed_by: Optional[UUID]
    updated_at: Optional[date]


class ResultsReviewModel(SQLModel):
    reviewed_by: UUID
    updated_at: date
