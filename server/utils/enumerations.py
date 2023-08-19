from enum import Enum


class ApplicationContentTypes(str, Enum):
    """Энумерация для типов контента приложения."""

    JSON = "application/json"
    XML = "application/xml"
    HTML = "text/html"
    TEXT = "text/plain"
    YAML = "application/x-yaml"
    CSV = "text/csv"
