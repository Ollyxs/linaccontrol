from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    name: str
    last_name: str
    username: str
    is_active: bool = True

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)

class UserRegister(UserBase):
    username: str = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    name: str = Field(default=None, max_length=255)
    last_name: str = Field(default=None, max_length=255)

