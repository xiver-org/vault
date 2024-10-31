from fastapi.responses import JSONResponse
from loguru import logger

from .router import health_check_router
from .env import programm_state

__all__ = ("readiness_health_handler",)

@health_check_router.post("/readiness")
async def readiness_health_handler() -> JSONResponse:
    logger.debug(f'Getting readiness health check.')
    
    if programm_state.programm_status == "Started":
        return JSONResponse(status_code=200, content={"message": "All good"})
    
    else:
        return JSONResponse(status_code=500, content={"message": "Error"})