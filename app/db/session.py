from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI,
                             pool_pre_ping=True,
                             echo=True,
                             pool_size=settings.POSTGRES_POOL_SIZE,
                             max_overflow=settings.POSTGRES_MAX_OVERFLOW,
                             pool_timeout=settings.POSTGRES_POOL_TIMEOUT,
                             connect_args={"server_settings": {"application_name": settings.PROJECT_NAME}})
async_session = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
