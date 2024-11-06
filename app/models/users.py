from sqlmodel import SQLModel, Field, Column
from sqlalchemy.dialects import mysql as my
from datetime import date
from uuid import UUID, uuid4


class UserBase(SQLModel):
    uid: UUID = Field(default_factory=uuid4, primary_key=True)
    first_name: str
    last_name: str
    username: str
    role: str = Field(default="technical")
    create_at: date = Field(sa_column=Column(my.DATE, default=date.today))
    is_active: bool = True


class User(UserBase, table=True):
    __tablename__ = "users"
    hashed_password: str
