from sqlmodel import SQLModel, Field
import uuid


class UUIDModel(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
