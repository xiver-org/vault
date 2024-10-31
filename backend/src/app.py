from os import makedirs

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from loguru import logger

from .config import config
from .database import async_session_maker
from .functions import send_error_msg
from .init_db import init_db
from .logger import init_logger
from .routes import health_check_router, programm_state

bot_turn = []

app = FastAPI(
    title='Xiver Vault',
    debug=config.debug,
    openapi_url='/openapi.json',
    docs_url='/docs',
    root_path='/api',
)

makedirs(config.static_files_path, exist_ok=True)
app.mount("/static", StaticFiles(directory=config.static_files_path))

app.include_router(
    health_check_router,
    prefix='/health',
    tags=['health'],
)


@app.on_event('startup')
async def on_startup() -> None:
    await init_logger()
    await init_db()
    
    programm_state.programm_status = 'Started'

    logger.info('App started')


@app.on_event('shutdown')
async def on_shutdown() -> None:
    await async_session_maker.begin().async_session.close_all()

    logger.info('App shut down')


@app.exception_handler(500)
async def internal_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    error_message = f'Internal server error: {request.url} | {request.method} | {request.headers} | {exc}'
    logger.error(error_message)

    await send_error_msg(exc, request, 500)

    return JSONResponse(status_code=500, content=jsonable_encoder({"code": 500, "msg": "Internal Server Error"}))
