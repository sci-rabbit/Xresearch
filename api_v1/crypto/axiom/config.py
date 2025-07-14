from pydantic_settings import BaseSettings

import env


class BaseAxiomSettings(BaseSettings):
    refresh_access_token_url: str = "https://api7.axiom.trade/refresh-access-token"

    token_info_url: str = "https://api6.axiom.trade/token-info?pairAddress="

    holder_data_url: tuple = (
        "https://api3.axiom.trade/holder-data-v2?pairAddress=",
        "&onlyTrackedWallets=false",
    )

    pair_info_url: str = "https://api8.axiom.trade/pair-info?pairAddress="

    defaults = {
        "tokenTicker": "",
        "tokenName": "",
        "website": "",
        "twitter": "",
        "telegram": "",
        "discord": "",
        "lpBurned": "",
        "twitterHandleHistory": [],
    }

    COOKIES = env.COOKIES
    HEADERS = env.HEADERS


settings = BaseAxiomSettings()
