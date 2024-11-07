from sqlmodel import SQLModel, Field, Relationship
from enum import Enum
from uuid import UUID
from typing import Optional


class FrequencyEnum(str, Enum):
    daily = "daily"
    weekly = "weekly"
    quarterly = "quarterly"
    semiannually = "semiannually"
    monthly = "monthly"


class LinacTestSuiteBase(SQLModel):
    linac_uid: UUID = Field(
        foreign_key="linac.uid", primary_key=True, ondelete="CASCADE"
    )
    test_suite_uid: UUID = Field(
        foreign_key="test_suite.uid", primary_key=True, ondelete="CASCADE"
    )
    frequency: FrequencyEnum = Field(default=FrequencyEnum.daily, primary_key=True)


class LinacTestSuite(LinacTestSuiteBase, table=True):
    __tablename__ = "linac_test_suite"
    linac: list["Linac"] = Relationship(back_populates="linac_test_suite")
