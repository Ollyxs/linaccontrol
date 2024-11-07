from sqlmodel import SQLModel
from uuid import UUID


class TestsSuiteModel(SQLModel):
    uid: UUID
    name: str
    test_type: str


class TestsSuiteCreateModel(SQLModel):
    name: str
    test_type: str


class TestsSuiteUpdateModel(SQLModel):
    name: str
    test_type: str
