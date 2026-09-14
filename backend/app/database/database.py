import urllib.parse
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Sanitize DATABASE_URL for asyncpg compatibility:
# 1. Automatically convert postgresql:// or postgres:// to postgresql+asyncpg://
# 2. Strip '?sslmode=...' query parameter which causes asyncpg to crash with TypeError
db_url = settings.DATABASE_URL
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql+asyncpg://", 1)
elif db_url.startswith("postgresql://") and not db_url.startswith("postgresql+asyncpg://"):
    db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

if "sslmode" in db_url:
    parsed = urllib.parse.urlparse(db_url)
    if parsed.query:
        queries = urllib.parse.parse_qsl(parsed.query)
        filtered = [(k, v) for k, v in queries if k.lower() != "sslmode"]
        new_query = urllib.parse.urlencode(filtered)
        db_url = urllib.parse.urlunparse(parsed._replace(query=new_query))

# Neon (and most managed Postgres) require SSL; asyncpg wants it passed via
# connect_args rather than a "sslmode" query param on the URL.
connect_args = {"ssl": "require"} if "postgresql" in db_url else {}

engine = create_async_engine(db_url, echo=False, connect_args=connect_args)

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
