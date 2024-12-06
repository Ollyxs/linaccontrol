from sqlmodel import SQLModel
from uuid import UUID


class FrequencyModel(SQLModel):
    uid: UUID
    name: str


class FrequencyCreateModel(SQLModel):
    name: str


class FrequencyUpdateModel(SQLModel):
    name: str
