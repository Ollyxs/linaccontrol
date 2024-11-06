from sqlmodel import SQLModel, Field, Column, Relationship
from sqlalchemy.dialects import mysql as my
from uuid import UUID, uuid4
from datetime import date
from typing import List, Optional
from . import OmittedDate, TestResults, LinacTestSuite


class LinacBase(SQLModel):
    uid: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    location: str
    image: Optional[bytes] = Field(sa_column_kwargs={"nullable": True})
    create_at: date = Field(sa_column=Column(my.DATE, default=date.today))
    is_active: bool = True


class Linac(LinacBase, table=True):
    __tablename__ = "linac"
    ommited_dates: List["OmittedDate"] = Relationship(
        back_populates="linac", cascade_delete=True
    )
    results: List["TestResults"] = Relationship(
        back_populates="linac", cascade_delete=True
    )
    linac_test_suite: List["LinacTestSuite"] = Relationship(
        back_populates="linac", cascade_delete=True
    )
