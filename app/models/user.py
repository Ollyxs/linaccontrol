from sqlalchemy.sql.schema import default_is_scalar
from sqlmodel import SQLModel, Field
import uuid


class UserBase(SQLModel):
    name: str
    last_name: str
    username: str
    is_active: bool = True

class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)

class UserRegister(UserBase):
    username: str = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    name: str = Field(default=None, max_length=255)
    last_name: str = Field(default=None, max_length=255)

