from sqlmodel import SQLModel
from datetime import date
from uuid import UUID
from typing import Optional


class OmittedDateModel(SQLModel):
    uid: UUID
    date: date
    reason: str
    linac_uid: Optional[UUID] = None


class OmittedDateCreateModel(SQLModel):
    date: date
    reason: str
    linac_uid: Optional[UUID] = None


class OmittedDateUpdateModel(SQLModel):
    date: date
    reason: str
    linac_uid: Optional[UUID] = None
