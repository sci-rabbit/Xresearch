from pydantic_settings import BaseSettings

from env import TWITTER_API_KEY


class TwitterSettings(BaseSettings):
    headers = {"X-API-Key": TWITTER_API_KEY}

    url_last_tweets: str = "https://api.twitterapi.io/twitter/user/last_tweets"

    url_advanced_search: str = "https://api.twitterapi.io/twitter/tweet/advanced_search"


twitter_settings = TwitterSettings()
