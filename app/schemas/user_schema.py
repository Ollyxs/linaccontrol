from sqlmodel import Field, SQLModel
from datetime import date
from uuid import UUID
from typing import Optional


class UserModel(SQLModel):
    uid: UUID
    first_name: str
    last_name: str
    username: str
    role: str
    is_active: bool = True
    create_at: date
    hashed_password: str = Field(exclude=True)


class UserCreateModel(SQLModel):
    first_name: str
    last_name: str
    username: str = Field(max_length=12)
    password: str = Field(min_length=6)
    role: str


class UserUpdateModel(SQLModel):
    first_name: str
    last_name: str
    username: str
    role: str
    is_active: bool


class UserLoginModel(SQLModel):
    username: str = Field(max_length=12)
    password: str = Field(min_length=6)
