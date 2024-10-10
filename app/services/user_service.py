from sqlmodel import select
from app.models import User
from app.schemas.user_schema import UserCreateModel
from app.core.security import generate_password_hash
from sqlmodel.ext.asyncio.session import AsyncSession


class UserService:
    async def get_user_by_username(self, username: str, session: AsyncSession):
        statement = select(User).where(User.username == username)
        result = await session.exec(statement)
        user = result.first()
        return user

    async def user_exists(self, username, session: AsyncSession):
        user = await self.get_user_by_username(username, session)
        return True if user is not None else False

    async def user_admin_exists(self, session: AsyncSession):
        statement = select(User).where(User.role == "admin")
        result = await session.exec(statement)
        user = result.first()
        return True if user is not None else False

    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        user_data_dict = user_data.model_dump()
        new_user = User(**user_data_dict)
        new_user.hashed_password = generate_password_hash(user_data_dict["password"])
        session.add(new_user)
        await session.commit()
        return new_user

    # @staticmethod
    # async def create_user(user: UserAuth):
    #     user_in = User(
    #         name=user.name,
    #         last_name=user.last_name,
    #         username=user.username,
    #         hashed_password=get_password(user.password),
    #    )
