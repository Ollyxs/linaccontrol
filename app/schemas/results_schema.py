from sqlmodel import SQLModel
from datetime import datetime
from uuid import UUID


class ResultsModel(SQLModel):
    uid: UUID
    test_suite_uid: UUID
    result: str
    realized_by: UUID
    reviewed_by: UUID


class ResultsCreateModel(SQLModel):
    linac_uid: UUID
    test_suite_uid: UUID
    result: str
    # realized_by: UUID


class ResultsUpdateModel(SQLModel):
    result: str
    reviewed_by: UUID
