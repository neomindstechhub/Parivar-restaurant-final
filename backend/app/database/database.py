from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Neon (and most managed Postgres) require SSL; asyncpg wants it passed via
# connect_args rather than a "sslmode"/"ssl" query param on the URL.
connect_args = {"ssl": "require"} if settings.DATABASE_URL.startswith("postgresql") else {}

engine = create_async_engine(settings.DATABASE_URL, echo=False, connect_args=connect_args)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
