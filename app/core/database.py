from sqlmodel import create_engine, SQLModel, Session, select
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.config import settings
from app.services.user_service import UserService
from app.schemas.user_schema import UserCreateModel
import asyncmy


async_engine = AsyncEngine(create_engine(str(settings.DATABASE_URI), echo=True))
user_service = UserService()


async def create_db_if_not_exists() -> None:
    connection = await asyncmy.connect(
        host=settings.DATABASE_SERVER,
        user=settings.DATABASE_USER,
        password=settings.DATABASE_PASSWORD,
        port=int(settings.DATABASE_PORT),
    )

    async with connection.cursor() as cursor:
        await cursor.execute(f"CREATE DATABASE IF NOT EXISTS {settings.DATABASE_NAME}")
    await connection.ensure_closed()


async def create_admin_if_not_exists(session: AsyncSession) -> None:
    admin_exists = await user_service.user_admin_exists(session)
    if not admin_exists:
        admin_data = UserCreateModel(
            first_name=settings.ADMIN_FIRST_NAME,
            last_name=settings.ADMIN_LAST_NAME,
            username=settings.ADMIN_USERNAME,
            password=settings.ADMIN_PASSWORD,
            role="admin",
        )
        await user_service.create_user(admin_data, session)


async def init_db() -> None:
    await create_db_if_not_exists()
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    async with AsyncSession(async_engine) as session:
        await create_admin_if_not_exists(session)


async def get_session() -> AsyncSession:
    Session = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with Session() as session:
        yield session
