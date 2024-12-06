from sqlmodel import SQLModel
from uuid import UUID
from typing import Optional


class TestsModel(SQLModel):
    uid: UUID
    test_name: str
    description: Optional[str] = None
    category_uid: UUID


class TestsCreateModel(SQLModel):
    test_name: str
    description: Optional[str] = None
    category_uid: UUID


class TestsUpdateModel(SQLModel):
    test_name: str
    description: Optional[str] = None
    category_uid: UUID
