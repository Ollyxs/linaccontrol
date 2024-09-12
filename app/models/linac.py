from sqlmodel import SQLModel, Field
import uuid


class LinacBase(SQLModel):
    name: str

class Linac(LinacBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

