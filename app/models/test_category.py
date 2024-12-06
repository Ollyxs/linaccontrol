from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4


class TestCategoryBase(SQLModel):
    uid: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str


class TestCategory(TestCategoryBase, table=True):
    __tablename__ = "test_category"
    tests: list["Tests"] = Relationship(back_populates="category")
