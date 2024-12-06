from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4


class FrequencyBase(SQLModel):
    uid: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str


class Frequency(FrequencyBase, table=True):
    __tablename__ = "frequency"
