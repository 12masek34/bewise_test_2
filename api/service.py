import logging
import os
from collections import (
    namedtuple,
)
from urllib.parse import (
    urlencode,
    urlunparse,
)

import jwt
from fastapi import (
    HTTPException,
    UploadFile,
    status,
)
from pydub import (
    AudioSegment,
)
from sqlalchemy import (
    UUID,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from config import (
    config,
)
from database.crud import (
    creat_new_file,
    get_user,
    update_file,
)
from database.models import (
    File,
    User,
)


def encode_token(id: int, name: str) -> str:
    """Create token by name and id."""

    token = jwt.encode({'id': id, 'name': name}, config.SECRET, algorithm=config.ALGORITHM)

    return token


def decode_token(token: str) -> dict[str, int | str]:
    """Decode token."""

    user = jwt.decode(token, config.SECRET, algorithms=[config.ALGORITHM])

    return user


async def validate_token_user(db: AsyncSession, token: str, id_: int) -> User:
    """Token verification.

    Decodes the token, and checks whether there is such a user in the database.
    """

    user_data = decode_token(token)
    user = await get_user(db, user_data)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found, invalid id or token.')

    elif user.id != id_:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token or user id.')


    return user


def validate_extension_file(file_name: str) -> None:
    """Checks that the file extension is wav."""

    if not file_name.endswith('.wav'):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='File format must be wav.')


def save_file(file: UploadFile)-> str:
    """Save new file."""

    file_path = os.path.join(config.WAV_FILE_DIRECTORY, file.filename)

    try:
        contents = file.file.read()
        with open(file_path, 'wb') as f:
            f.write(contents)
    except Exception as e:
        logging.error(e, exc_info=True)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='There was an error uploading the file')
    finally:
        file.file.close()

    return file.filename


async def convert_wav_to_mp3(db: AsyncSession, file_name: str, user_id: int) -> File:
    """Converts a file with the wav extension to mp3 and saves the path to the file to the database."""

    file = await creat_new_file(db, user_id)
    new_file_name = make_file_name(file.uuid, file_name)
    full_file_path = os.path.join(config.BASE_DIR, config.WAV_FILE_DIRECTORY, file_name)
    sound = AudioSegment.from_wav(full_file_path)
    new_file_path = os.path.join(config.BASE_DIR, config.MP3_FILE_DIRECTORY, new_file_name)
    sound.export(new_file_path, format='mp3')
    file.file_path = new_file_path
    await update_file(db, file)

    return file


def make_file_name(uuid: UUID, file_name: str) -> str:
    """Create unique file name."""

    new_file_name = str(uuid) + file_name
    new_file_name = new_file_name.replace('.wav', '.mp3')

    return new_file_name


def make_url(id_: int, uuid: UUID, host: str, port: int) -> str:
    """Creates an url for the response."""

    Components = namedtuple(
        typename='Components',
        field_names=['scheme', 'netloc', 'url', 'path', 'query', 'fragment']
    )

    query_params = {
        'id': str(uuid),
        'user': id_
    }

    url = urlunparse(
        Components(
            scheme='http',
            netloc=f'{host}:{port}/record',
            query=urlencode(query_params),
            path='',
            url='/',
            fragment=''
        )
    )

    return url


def validate_file(file: File | None) -> None:
    """Checks whether the file is in the database."""

    if file is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid file id or user id.')


def get_file_name(file_path: str) -> str:
    """Get file name from path."""

    file_name = file_path.split('/')[-1]

    return file_name
