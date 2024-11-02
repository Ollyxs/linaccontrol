from sqlmodel import SQLModel
from uuid import UUID
from typing import Optional


class LinacModel(SQLModel):
    uid: UUID
    name: str
    location: str
    # image: Optional[bytes] = None
    is_active: bool


class LinacCreateModel(SQLModel):
    name: str
    location: str
    # image: Optional[bytes] = None
    is_active: bool


class LinacUpdateModel(SQLModel):
    name: Optional[str] = None
    location: Optional[str] = None
    # image: Optional[bytes] = None
    is_active: Optional[bool] = None
