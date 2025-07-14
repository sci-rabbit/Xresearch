from pydantic_settings import BaseSettings

from env import X_API_KEY_FOR_ST


class BaseSTSettings(BaseSettings):

    token_pair_url: str = "https://data.solanatracker.io/tokens/"

    header = {
        "x-api-key": X_API_KEY_FOR_ST,
    }

    defaults = {
        "name": None,
        "symbol": None,
        "image": None,
        "extensions": None,
        "holders": None,
        "poolId": None,
        "token_supply": None,
    }


settings = BaseSTSettings()
