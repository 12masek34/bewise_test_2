
from uuid import (
    UUID,
)

from fastapi import (
    APIRouter,
    Depends,
    File,
    Request,
    UploadFile,
    status,
)
from fastapi.responses import (
    FileResponse,
)
from pydantic import (
    HttpUrl,
    PositiveInt,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from api.service import (
    convert_wav_to_mp3,
    get_file_name,
    make_url,
    save_file,
    validate_extension_file,
    validate_file,
    validate_token_user,
)
from database.base import (
    get_async_db,
)
from database.crud import (
    get_file_by_id,
)
from database.schema import (
    UserUploadFileSchema,
)



router = APIRouter(prefix='/record', tags=['Record'])


@router.post('', status_code=status.HTTP_201_CREATED)
async def add_file(
    request: Request,
    data: UserUploadFileSchema = Depends(),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_async_db),
) -> HttpUrl:
    """Adding a file for registered users."""

    user = await validate_token_user(db, data.token, data.id)
    validate_extension_file(file.filename)
    file_name = save_file(file)
    new_file = await convert_wav_to_mp3(db, file_name, user.id)
    url = make_url(user.id, new_file.uuid, request.url.hostname, request.url.port)

    return url


@router.get('', status_code=status.HTTP_302_FOUND)
async def get_file(id: UUID, user: PositiveInt, db: AsyncSession = Depends(get_async_db)) -> FileResponse:
    """Get file by file uuid and user id."""

    file = await get_file_by_id(db, id, user)
    validate_file(file)
    file_name = get_file_name(file.file_path)

    return FileResponse(file.file_path, media_type='application/octet-stream', filename=file_name)
