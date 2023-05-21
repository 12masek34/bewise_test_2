import logging
import os

from dotenv import (
    load_dotenv,
)
from pydantic import (
    AnyHttpUrl,
    BaseSettings,
)
from pydantic.fields import (
    Field,
)


load_dotenv()
logging.basicConfig(filename='logs.log', level=logging.INFO)


class Config(BaseSettings):

    POSTGRES_DB: str = Field(..., env='ASYNC_POSTGRES_URL')
    POSTGRES_USER: str = Field(..., env='POSTGRES_USER')
    POSTGRES_PASSWORD: str = Field(..., env='POSTGRES_PASSWORD')
    POSTGRES_PORT: int = Field(..., env='POSTGRES_PORT')
    POSTGRES_HOST: str = Field(..., env='POSTGRES_HOST')
    ASYNC_POSTGRES_URL: str = Field(..., env='ASYNC_POSTGRES_URL')

    SECRET: str = Field(..., env='SECRET')
    ALGORITHM: str = Field(..., env='ALGORITHM')
    BASE_DIR = os.path.abspath(os.getcwd())
    WAV_FILE_DIRECTORY = 'files_wav/'
    MP3_FILE_DIRECTORY = 'files_mp3/'

config = Config()