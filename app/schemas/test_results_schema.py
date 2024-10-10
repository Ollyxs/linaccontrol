from sqlmodel import SQLModel
from uuid import UUID


class TestResultsModel(SQLModel):
    uid: UUID
    test_uid: UUID
    result: str
    results_uid: UUID


class TestResultsCreateModel(SQLModel):
    test_uid: UUID
    result: str
    # results_uid: UUID
