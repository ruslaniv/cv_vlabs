import os
from typing import Generator

import cv2
import numpy as np
from face_recognition import face_locations
from fastapi import APIRouter, HTTPException, Request
from starlette.responses import FileResponse, JSONResponse, StreamingResponse

from config.config import settings as app_settings

router = APIRouter()

SAVED_IMAGES_DIR = "saved_images"
if not os.path.exists(SAVED_IMAGES_DIR):
    os.makedirs(SAVED_IMAGES_DIR)


@router.post("/upload/")
async def upload_image(request: Request) -> StreamingResponse:
    """Маршрут для загрузки изображения и определение лица на изображении

    Parameters
    ----------
    request : Request
        Запрос, содержащий изображение в бинарном формате

    Returns
    -------
    StreamingResponse
        Изображение с выделенным лицом субъекта

    Raises
    ------
    HTTPException
        Если в запросе отсутствует содержимое
    """

    contents: bytes = await request.body()

    if not contents:
        raise HTTPException(status_code=400, detail="File not found")

    image: np.ndarray = np.asarray(bytearray(contents), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    image_rgb: np.ndarray = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    face_boundaries: list = face_locations(image_rgb)

    for face in face_boundaries:
        top, right, bottom, left = face
        cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)

    # ToDo Надо выделить в отдельный класс обработчика изображений с интерфейсами и тд
    image_name = f"detected_{os.urandom(8).hex()}.jpg"
    image_path = os.path.join(SAVED_IMAGES_DIR, image_name)
    cv2.imwrite(image_path, image)

    _, image_encoded = cv2.imencode(".jpg", image)

    return StreamingResponse(
        content=_image_stream(image_encoded), media_type="image/jpeg"
    )


@router.get("/view-images/")
async def view_images() -> JSONResponse:
    """Маршрут для вывода всех сохраненных изображений

    Returns
    -------
    JSONResponse
        Список сохраненных изображений
    """

    image_files: list[str] = os.listdir(SAVED_IMAGES_DIR)
    image_urls: list[str] = [
        f"{app_settings.API_PREFIX}/get-image/{image_file}"
        for image_file in image_files
    ]

    return JSONResponse(content={"image_urls": image_urls})


@router.get("/get-image/{image_name}")
async def get_image(image_name: str) -> FileResponse:
    """Маршрут для вывода сохраненного изображения

    Parameters
    ----------
    image_name : str
        Имя файла изображения

    Returns
    -------
    FileResponse
        Файл с изображением
    """

    image_path: str = os.path.join(SAVED_IMAGES_DIR, image_name)
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found")

    return FileResponse(image_path, media_type="image/jpeg")


def _image_stream(image_encoded: np.ndarray) -> Generator[bytes, None, None]:
    """Генерирует поток байтов из закодированного изображения

    Parameters
    ----------
    image_encoded : np.ndarray
        Закодированные данные изображения

    Yields
    ------
    bytes
        Потом байтов закодированного изображения
    """
    yield image_encoded.tobytes()
