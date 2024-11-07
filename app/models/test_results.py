from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from typing import Optional


class TestResultsBase(SQLModel):
    uid: UUID = Field(default_factory=uuid4, primary_key=True)
    test_uid: UUID = Field(foreign_key="tests.uid", ondelete="CASCADE")
    result: str
    results_uid: UUID = Field(foreign_key="results.uid", ondelete="CASCADE")


class TestResults(TestResultsBase, table=True):
    __tablename__ = "test_results"
    results: Optional["Results"] = Relationship(back_populates="tests")
