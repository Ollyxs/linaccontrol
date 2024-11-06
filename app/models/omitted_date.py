from sqlmodel import SQLModel, Field, Relationship
from datetime import date
from uuid import UUID, uuid4
from typing import Optional
from . import Linac


class OmittedDateBase(SQLModel):
    uid: UUID = Field(default_factory=uuid4, primary_key=True)
    date: date
    reason: str
    linac_uid: Optional[UUID] = Field(
        default=None, foreign_key="linac.uid", ondelete="CASCADE"
    )


class OmittedDate(OmittedDateBase, table=True):
    __tablename__ = "omitted_dates"
    linac: Optional[Linac] = Relationship(back_populates="omitted_dates")
