import logging
from collections.abc import (
    AsyncGenerator,
)

from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.ext.asyncio.session import (
    AsyncSession,
)

from config import (
    config,
)
from database.models import (
    Base,
)


async_engine = create_async_engine(config.ASYNC_POSTGRES_URL)
async_session = async_sessionmaker(
    async_engine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


async def async_init_db() -> None:
    """Create all tables."""

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """Connect to db."""

    async with async_session() as db:
        try:
            yield db
            await db.commit()
        except Exception as e:
            logging.error(e, exc_info=True)
            await db.rollback()
        finally:
            await db.close()
