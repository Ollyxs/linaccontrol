from sqlmodel import SQLModel
from uuid import UUID
from typing import List


class TestSuiteTestsModel(SQLModel):
    test_suite_uid: UUID
    test_uid: List[UUID]


class TestSuiteTestsCreateModel(SQLModel):
    test_uid: List[UUID]
