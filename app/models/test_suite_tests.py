from sqlmodel import SQLModel, Field
from uuid import UUID
from . import TestSuite, Tests


class TestSuiteTestsBase(SQLModel):
    test_suite_uid: UUID = Field(
        foreign_key="test_suite.uid", primary_key=True, ondelete="CASCADE"
    )
    test_uid: UUID = Field(
        foreign_key="tests.uid", primary_key=True, ondelete="CASCADE"
    )


class TestSuiteTests(TestSuiteTestsBase, table=True):
    __tablename__ = "test_suite_tests"
