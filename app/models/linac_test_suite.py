from sqlmodel import SQLModel, Field
from enum import Enum
from uuid import UUID


class FrequencyEnum(str, Enum):
    daily = "daily"
    weekly = "weekly"
    quarterly = "quarterly"
    semiannually = "semiannually"
    monthly = "monthly"


class LinacTestSuiteBase(SQLModel):
    linac_uid: UUID = Field(foreign_key="linac.uid", primary_key=True)
    test_suite_uid: UUID = Field(foreign_key="test_suite.uid", primary_key=True)
    frequency: FrequencyEnum = Field(default=FrequencyEnum.daily, primary_key=True)


class LinacTestSuite(LinacTestSuiteBase, table=True):
    __tablename__ = "linac_test_suite"
