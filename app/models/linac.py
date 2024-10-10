from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4


class LinacBase(SQLModel):
    uid: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    is_active: bool = True


class Linac(LinacBase, table=True):
    __tablename__ = "linac"
