from sqlmodel import SQLModel, Field
from uuid import UUID


class TestSuiteTestsBase(SQLModel):
    test_suite_uid: UUID = Field(foreign_key="test_suite.uid", primary_key=True)
    test_uid: UUID = Field(foreign_key="tests.uid", primary_key=True)


class TestSuiteTests(TestSuiteTestsBase, table=True):
    __tablename__ = "test_suite_tests"
