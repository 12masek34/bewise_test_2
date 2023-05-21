import os
import uvicorn
from fastapi import (
    FastAPI,
)

from api.routes import (
    record,
    user,
)
from config import (
    config,
)
from database.base import (
    async_init_db,
)


app = FastAPI()
app.include_router(user.router)
app.include_router(record.router)


@app.on_event('startup')
async def startup() -> None:
    await async_init_db()
    os.makedirs(os.path.dirname(config.MP3_FILE_DIRECTORY), exist_ok=True)
    os.makedirs(os.path.dirname(config.WAV_FILE_DIRECTORY), exist_ok=True)


if __name__ == '__main__':
    uvicorn.run(app=app, host='0.0.0.0', port=8000)
