from sqlmodel import SQLModel
from uuid import UUID


class LinacTestSuiteModel(SQLModel):
    linac_uid: UUID
    test_suite_uid: UUID
    frequency_uid: UUID


class LinacTestSuiteCreateModel(SQLModel):
    linac_uid: UUID
    test_suite_uid: UUID
    frequency_uid: UUID


class LinacTestSuiteUpdateModel(SQLModel):
    linac_uid: UUID
    test_suite_uid: UUID
    frequency_uid: UUID
