from fastapi import APIRouter, status
from sentry_sdk import capture_exception
from starlette.responses import JSONResponse

from server.utils.device import get_compute_device
from server.utils.enumerations import ApplicationContentTypes

router = APIRouter()


@router.get(
    "/healthcheck",
    tags=["healthcheck"],
    description="Проверка работоспособности сервера",
    responses={
        "200": {
            "description": "Сервер работает",
            "content": {
                "application/json": {
                    "example": {
                        "message": "AI/ML сервис распознавания лиц готов к работе!"
                    }
                }
            },
        },
        "500": {
            "description": "Сервер не работает",
        },
    },
)
def healthcheck() -> JSONResponse:
    """Маршрут для проверки работоспособности сервера.

    Returns
    -------
    JSONResponse
        Сообщение об успешном запуске
    """
    message = {"message": "AI/ML сервис распознавания лиц готов к работе!"}
    return JSONResponse(
        content=message,
        media_type=ApplicationContentTypes.JSON,
        status_code=status.HTTP_200_OK,
    )


@router.get(
    "/sentrycheck/unhandled",
    tags=["sentry"],
    description="Проверка работоспособности сервиса Сентри для необработанных ошибок",
    response_class=JSONResponse,
    responses={
        "500": {
            "description": "Internal Server Error",
        },
    },
)
def sentrycheck_unhandled() -> float:
    """Маршрут для проверки работоспособности сервиса Сентри.

    Маршрут проверяет возникновение необработанной ошибки и вызывает ошибку деления на ноль.

    Returns
    -------
    int:
        Возвращает результат деления 42 на 0
    """
    _ = 42 / 0
    return _


@router.get(
    "/sentrycheck/handled",
    tags=["sentry"],
    description="Проверка работоспособности сервиса Сентри для обработанных ошибок",
    response_class=JSONResponse,
    responses={
        "400": {
            "description": "Обработанная ошибка",
            "content": {
                "application/json": {
                    "example": {"message": "Вызвана ошибка: division by zero"}
                }
            },
        }
    },
)
def sentrycheck_handled() -> JSONResponse:
    """Маршрут для проверки работоспособности сервиса Сентри для обработанных ошибок.

    Обрабатывает ошибку деления на ноль.

    Returns
    -------
    JSONResponse
        Сообщение о генерации ошибки
    """
    try:
        _ = 42 / 0
        message = {"message": f"Результат деления '42/0 = ' {_}"}
        return JSONResponse(
            content=message,
            media_type=ApplicationContentTypes.JSON,
            status_code=status.HTTP_200_OK,
        )
    except ZeroDivisionError as error:
        capture_exception(error)
        message = {"message": f"Вызвана ошибка: {error}"}
        return JSONResponse(
            content=message,
            media_type=ApplicationContentTypes.JSON,
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@router.get(
    "/healthcheck/device",
    tags=["healthcheck"],
    description="Определение типа устройства для векторизации",
    response_class=JSONResponse,
    responses={
        "200": {
            "description": "Используемое устройство",
            "content": {
                "application/json": {
                    "example": {
                        "message": [
                            {"device": "Используемое устройство: CPU"},
                            {"device_name": "Имя устройства: I386"},
                        ]
                    }
                }
            },
        }
    },
)
def get_device() -> JSONResponse:
    """Получение информации об устройстве для векторизации.

    Returns
    -------
    JSONResponse
        Информация об устройстве для векторизации.
    """

    compute = get_compute_device()
    message = {
        "message": [
            {"device": f"Тип устройства: {compute.device.upper()}"},
            {"device_name": f"Наименование устройства: {compute.device_name.upper()}"},
        ]
    }
    return JSONResponse(
        content=message,
        media_type=ApplicationContentTypes.JSON,
        status_code=status.HTTP_200_OK,
    )
