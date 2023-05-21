import logging
from uuid import (
    UUID,
)

from asyncpg.exceptions import (
    UniqueViolationError,
)
from fastapi import (
    HTTPException,
    status,
)
from sqlalchemy import (
    and_,
    select,
)
from sqlalchemy.exc import (
    IntegrityError,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from database.models import (
    File,
    User,
)


async def create_new_user(db: AsyncSession, name:str) -> User:
    """Creates new user."""

    new_user = User(name=name)
    db.add(new_user)
    try:
        await db.flush()
    except IntegrityError as e:
        logging.error(e, exc_info=True)
        if isinstance(e.orig.__cause__, UniqueViolationError):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User name alredy exists.')
        else:
            raise e

    return new_user


async def get_user(db: AsyncSession, user_data: dict[str, int | str]) -> User | None:
    """Get ueser from db."""

    query = select(User).where(and_(User.id == user_data['id'], User.name == user_data['name']))
    user = (await db.execute(query)).scalar()

    return user


async def creat_new_file(db: AsyncSession, user_id: int) -> File:
    """Create new file."""

    file = File(user_id=user_id)
    db.add(file)
    await db.flush()

    return file


async def update_file(db: AsyncSession, file: File) -> File:
    """Update existing file."""

    await db.merge(file)

    return file


async def get_file_by_id(db: AsyncSession, uuid: UUID, user_id: int) -> File | None:
    """Get file by filter uuid and user_id."""

    query = select(File).where(and_(File.uuid == uuid, File.user_id == user_id))
    file = (await db.execute(query)).scalar()

    return file
