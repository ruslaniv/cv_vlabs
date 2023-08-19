from os import getenv
from pathlib import Path
from typing import Any, Union

import rtoml
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).parent.parent


def read_pyproject_toml(path: Path = Path(ROOT / "pyproject.toml")) -> dict[str, Any]:
    """
    Чтение файла pyproject.toml

    Parameters
    ----------
    path : Path, optional, default=Path("../pyproject.toml")
        Путь к файлу pyproject.toml

    Returns
    -------
    dict[str, Any]
        Содержимое файла pyproject.toml
    """
    return rtoml.load(path)


class Settings(BaseSettings):
    """
    Класс хранения настроек приложения
    """

    # Project wide settings
    PROJECT_MODE: str = getenv("PROJECT_MODE", "production")
    VERSION: str = Field(read_pyproject_toml()["tool"]["poetry"]["version"])

    match PROJECT_MODE:
        case "sandbox":
            DEBUG: bool = True
            model_config = SettingsConfigDict(
                env_file=(ROOT / "settings/.env_all", ROOT / "settings/.env_sandbox"),
                env_file_encoding="utf-8",
            )
        case "production":
            DEBUG: bool = False
            model_config = SettingsConfigDict(
                env_file=(
                    ROOT / "settings/.env_all",
                    ROOT / "settings/.env_production",
                ),
                env_file_encoding="utf-8",
            )

    # Database settings
    DATABASE_HOST: str = getenv("DATABASE_HOST", "localhost")
    DATABASE_PORT: Union[int, str] = getenv("DATABASE_PORT", 5432)
    DATABASE_PASSWORD: str = getenv("DATABASE_PASSWORD", "password")

    # Sentry settings
    SENTRY_DSN: str = getenv("SENTRY_DSN", "")
    SEND_DEFAULT_PII: bool = getenv("SEND_DEFAULT_PII", False)
    SENTRY_DEBUG: bool = getenv("SENTRY_DEBUG", False)
    TRACES_SAMPLE_RATE: float = getenv("TRACES_SAMPLE_RATE", 0.0)

    # Общие настройки приложения
    COMPUTE: str = getenv("COMPUTE", "cpu")
    API_PREFIX: str = getenv("API_PREFIX", "/api/v1")


settings = Settings()
