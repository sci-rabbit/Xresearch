from pydantic_settings import BaseSettings

from env import X_API_KEY_FOR_ST


class BaseSTSettings(BaseSettings):

    token_info_url: str = "https://data.solanatracker.io/tokens/"

    headers = {
        "x-api-key": X_API_KEY_FOR_ST,
    }

    defaults = {
        "name": "",
        "symbol": "",
        "image": "",
        "extensions": None,
        "holders": [],
        "poolId": "",
        "token_supply": None,
    }


settings = BaseSTSettings()
