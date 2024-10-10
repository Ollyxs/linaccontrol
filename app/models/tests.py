from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from typing import Optional


class TestsBase(SQLModel):
    uid: UUID = Field(default_factory=uuid4, primary_key=True)
    test_name: str
    description: Optional[str]
    category: str


class Tests(TestsBase, table=True):
    __tablename__ = "tests"
