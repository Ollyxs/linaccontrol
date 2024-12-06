from sqlmodel import Relationship, SQLModel, Field
from uuid import UUID, uuid4
from typing import Optional


class TestsBase(SQLModel):
    uid: UUID = Field(default_factory=uuid4, primary_key=True)
    test_name: str
    description: Optional[str]
    category_uid: UUID = Field(foreign_key="test_category.uid")


class Tests(TestsBase, table=True):
    __tablename__ = "tests"
    category: Optional["TestCategory"] = Relationship(back_populates="tests")
