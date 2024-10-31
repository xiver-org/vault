from fastapi.responses import JSONResponse
from loguru import logger

from .router import health_check_router

__all__ = ("liveness_health_handler",)

@health_check_router.post("/liveness")
async def liveness_health_handler() -> JSONResponse:
    logger.debug('Getting liveness health check.')

    return JSONResponse(status_code=200, content={"message": "All good"})
