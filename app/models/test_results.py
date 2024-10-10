from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4


class TestResultsBase(SQLModel):
    uid: UUID = Field(default_factory=uuid4, primary_key=True)
    test_uid: UUID = Field(foreign_key="tests.uid")
    result: str
    results_uid: UUID = Field(foreign_key="results.uid")


class TestResults(TestResultsBase, table=True):
    __tablename__ = "test_results"
