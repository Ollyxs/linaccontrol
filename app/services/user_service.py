from sqlmodel import select
from app.models import User
from app.schemas.user_schema import UserCreateModel, UserUpdateModel
from app.core.security import generate_password_hash
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID


class UserService:
    async def get_user_by_username(self, username: str, session: AsyncSession):
        statement = select(User).where(User.username == username)
        result = await session.exec(statement)
        user = result.first()
        return user

    async def get_all_users(
        self,
        session: AsyncSession,
        is_active: bool = None,
        skip: int = 0,
        limit: int = 10,
    ):
        statement = select(User)
        if is_active is not None:
            statement = statement.where(User.is_active == is_active)
        statement = statement.offset(skip).limit(limit)
        result = await session.exec(statement)
        return result.all()

    async def get_user(self, user_uid: UUID, session: AsyncSession):
        statement = select(User).where(User.uid == user_uid)
        result = await session.exec(statement)
        user = result.first()
        return user if user is not None else None

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

    async def update_user(
        self, user_uid: UUID, update_data: UserUpdateModel, session: AsyncSession
    ):
        user_to_update = await self.get_user(user_uid, session)
        if user_to_update is not None:
            update_data_dict = update_data.model_dump(exclude_unset=True)
            for k, v in update_data_dict.items():
                setattr(user_to_update, k, v)
            await session.commit()
            return user_to_update
        else:
            return None

    async def delete_user(self, user_uid: UUID, session: AsyncSession):
        user_to_delete = await self.get_user(user_uid, session)
        if user_to_delete is not None:
            await session.delete(user_to_delete)
            await session.commit()
        else:
            return None
