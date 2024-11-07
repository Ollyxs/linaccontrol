from sqlmodel import SQLModel, Field
from uuid import UUID
from typing import Optional


class TestsModel(SQLModel):
    uid: UUID
    test_name: str
    description: Optional[str] = None
    category: str


class TestsCreateModel(SQLModel):
    test_name: str
    description: Optional[str] = None
    category: str


class TestsUpdateModel(SQLModel):
    test_name: str
    description: Optional[str] = None
    category: str
