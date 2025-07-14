from pydantic_settings import BaseSettings


class BaseDexSettings(BaseSettings):

    token_pair_url: str = "https://api.dexscreener.com/token-pairs/v1/solana/"

    defaults = {
        "twitter_url": "",
        "tg_link": "",
        "discord_link": "",
        "pools": [],
        "images": [],
        "web_links": [],
        "name": "",
        "symbol": "",
    }


settings = BaseDexSettings()
