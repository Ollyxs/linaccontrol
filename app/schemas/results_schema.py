from typing import Optional
from sqlmodel import SQLModel
from datetime import datetime
from uuid import UUID
from app.models.linac_test_suite import FrequencyEnum


class ResultsModel(SQLModel):
    uid: UUID
    linac_uid: UUID
    test_suite_uid: UUID
    frequency: FrequencyEnum
    result: str
    realized_by: UUID
    reviewed_by: UUID


class ResultsCreateModel(SQLModel):
    linac_uid: UUID
    test_suite_uid: UUID
    frequency: FrequencyEnum
    result: str
    created_at: Optional[datetime] = None
    # realized_by: UUID


class ResultsUpdateModel(SQLModel):
    result: str
    reviewed_by: UUID
