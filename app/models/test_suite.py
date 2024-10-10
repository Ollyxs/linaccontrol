from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4


class TestSuiteBase(SQLModel):
    uid: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    test_type: str


class TestSuite(TestSuiteBase, table=True):
    __tablename__ = "test_suite"
