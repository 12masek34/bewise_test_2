
from fastapi import (
    Depends,
    status,
)
from fastapi.routing import (
    APIRouter,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from api.service import (
    encode_token,
)
from database.base import (
    get_async_db,
)
from database.crud import (
    create_new_user,
)
from database.schema import (
    UserResponseSchema,
    UserSchema,
)

router = APIRouter(prefix='/user', tags=['User'])


@router.post('', status_code=status.HTTP_201_CREATED)
async def create_user(data: UserSchema = Depends(), db: AsyncSession = Depends(get_async_db)) -> UserResponseSchema:
    """Creates and saves a new user to the database."""

    user = await create_new_user(db, data.name)
    token = encode_token(user.id, user.name)
    user.token = token

    return user
