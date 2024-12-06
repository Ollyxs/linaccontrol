from sqlmodel import SQLModel, Field, Relationship, UniqueConstraint
from uuid import UUID


class LinacTestSuiteBase(SQLModel):
    linac_uid: UUID = Field(
        foreign_key="linac.uid", primary_key=True, ondelete="CASCADE"
    )
    test_suite_uid: UUID = Field(
        foreign_key="test_suite.uid", primary_key=True, ondelete="CASCADE"
    )
    frequency_uid: UUID = Field(
        foreign_key="frequency.uid", primary_key=True, ondelete="CASCADE"
    )


class LinacTestSuite(LinacTestSuiteBase, table=True):
    __tablename__ = "linac_test_suite"
    __table_args__ = (
        UniqueConstraint("linac_uid", "frequency_uid", name="uix_linac_frequency"),
    )
    linac: list["Linac"] = Relationship(back_populates="linac_test_suite")
    frequency: "Frequency" = Relationship()
