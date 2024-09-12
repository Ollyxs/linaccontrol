from sqlmodel import SQLModel, Field


class LinacBase(SQLModel):
    name: str

class Linac(LinacBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

