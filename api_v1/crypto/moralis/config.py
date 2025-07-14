from pydantic_settings import BaseSettings

from env import X_API_KEY


class BaseMoralisSettings(BaseSettings):

    token_pair_url: tuple = (
        "https://solana-gateway.moralis.io/token/mainnet/",
        "/pairs",
    )
    headers = {"X-API-Key": X_API_KEY}


settings = BaseMoralisSettings()
