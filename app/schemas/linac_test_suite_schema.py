from sqlmodel import SQLModel
from uuid import UUID
from app.models.linac_test_suite import FrequencyEnum


class LinacTestSuiteModel(SQLModel):
    linac_uid: UUID
    test_suite_uid: UUID
    frequency: FrequencyEnum


class LinacTestSuiteCreateModel(SQLModel):
    linac_uid: UUID
    test_suite_uid: UUID
    frequency: FrequencyEnum


class LinacTestSuiteUpdateModel(SQLModel):
    linac_uid: UUID
    test_suite_uid: UUID
    frequency: FrequencyEnum
