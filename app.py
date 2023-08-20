import sentry_sdk
import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from loguru import logger

from config.config import settings as app_settings
from config.tags_metadata import tags_metadata
from server.routes.v1 import detection, healthcheck

app = FastAPI(
    title="AI/ML сервис распознавания лиц",
    description="API для сервиса распознавания лиц на фотографиях",
    version="0.0.1",
    openapi_tags=tags_metadata,
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(healthcheck.router, prefix=app_settings.API_PREFIX)
app.include_router(detection.router, prefix=app_settings.API_PREFIX)

sentry_sdk.init(
    dsn=app_settings.SENTRY_DSN,
    send_default_pii=app_settings.SEND_DEFAULT_PII,
    release=app_settings.VERSION,
    debug=app_settings.SENTRY_DEBUG,
    environment=app_settings.PROJECT_MODE,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=app_settings.TRACES_SAMPLE_RATE,
)


@app.get("/favicon.ico", include_in_schema=False)
async def favicon() -> FileResponse:
    """Загрузка фавиконки.

    Returns
    -------
    fastapi.responses.FileResponse
        Ссылка на фавиконку

    Notes
    -----
    favicon attribution:
    <a href="https://www.flaticon.com/free-icons/case-study" title="case study icons">Case study icons created by Circlon Tech - Flaticon</a>
    """
    return FileResponse("static/favicon.png")


if __name__ == "__main__":
    logger.info("starting")
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8189,
        reload=True,
    )
