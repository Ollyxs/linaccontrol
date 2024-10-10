from sqlmodel import SQLModel, Field
from uuid import UUID


class TestsModel(SQLModel):
    uid: UUID
    test_name: str
    description: str
    category: str


class TestsCreateModel(SQLModel):
    test_name: str
    description: str
    category: str


class TestsUpdateModel(SQLModel):
    test_name: str
    description: str
    category: str
