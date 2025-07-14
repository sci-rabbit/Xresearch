import aiohttp


from pydantic_settings import BaseSettings


class TimeOutSettings(BaseSettings):

    timeout = aiohttp.ClientTimeout(
        total=15,  # максимум 15 секунд на весь запрос
        connect=2,  # не более 2 секунд на установление TCP‑соединения
        sock_read=8,  # не более 8 секунд на чтение данных
    )


timeout_settings = TimeOutSettings()
