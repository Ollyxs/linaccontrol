from sqlmodel import SQLModel, Field, Column
from app.models.linac_test_suite import FrequencyEnum
import sqlalchemy.dialects.mysql as my
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional


class ResultsBase(SQLModel):
    uid: UUID = Field(default_factory=uuid4, primary_key=True)
    linac_uid: UUID = Field(foreign_key="linac.uid")
    test_suite_uid: UUID = Field(foreign_key="test_suite.uid")
    frequency: FrequencyEnum
    result: Optional[str]
    created_at: datetime = Field(sa_column=Column(my.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(my.TIMESTAMP, default=datetime.now))
    realized_by: UUID = Field(foreign_key="users.uid")
    reviewed_by: Optional[UUID] = Field(foreign_key="users.uid")


class Results(ResultsBase, table=True):
    __tablename__ = "results"
