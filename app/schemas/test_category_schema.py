from sqlmodel import SQLModel
from uuid import UUID


class TestCategoryModel(SQLModel):
    uid: UUID
    name: str


class TestCategoryCreateModel(SQLModel):
    name: str


class TestCategoryUpdateModel(SQLModel):
    name: str
