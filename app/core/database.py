from sqlmodel import create_engine, SQLModel, Session, select
from app.core.config import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
import pymysql


engine = create_engine(str(settings.DATABASE_URI), echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_db_if_not_exists():
    connection = pymysql.connect(
        host=settings.MYSQL_SERVER,
        user=settings.MYSQL_USER,
        password=settings.MYSQL_PASSWORD,
        port=int(settings.MYSQL_PORT)
    )

    with connection.cursor() as cursor:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {settings.MYSQL_DB}")
    connection.close()

def init_db():
    try:
        create_db_if_not_exists()
        SQLModel.metadata.create_all(engine)
    except OperationalError as e:
        print(f"Error to connect with database: {e}")

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
