class ApiError(Exception):
    """Базовый класс для всех ошибок API."""


class NetworkError(ApiError):
    """Проблемы в сетевом взаимодействии (таймаут, DNS и т.п.)."""


class HttpStatusError(ApiError):
    """Неожиданный HTTP-статус."""

    def __init__(self, status: int, url: str):
        super().__init__(f"HTTP {status} at {url}")
        self.status = status
        self.url = url


class JsonResponseError(ApiError):
    """Сервер вернул не JSON"""


class JsonParseError(ApiError):
    """Сервер вернул невалидный JSON."""

    def __init__(self, url: str, raw_text: str):
        super().__init__(f"JSON parse error at {url}: {raw_text!r}")
        self.url = url
        self.raw = raw_text


class AuthError(ApiError):
    """Ошибка авторизации или истёкший токен."""
