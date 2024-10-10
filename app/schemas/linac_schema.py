from sqlmodel import SQLModel
from uuid import UUID


class LinacModel(SQLModel):
    uid: UUID
    name: str
    is_active: bool


class LinacCreateModel(SQLModel):
    name: str
    is_active: bool


class LinacUpdateModel(SQLModel):
    name: str
    is_active: bool
