import logging

from aiohttp import ClientSession

from api_v1.twitter.tweets.config import twitter_settings
from core.exceptions import ApiError
from core.requests.TwitterRequest import TwitterRequest

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TwitterApi:
    def __init__(
        self,
        session: ClientSession,
        contract_address: str,
        twitter_url: str = None,
        headers: dict = twitter_settings.headers,
    ) -> None:
        self.client = TwitterRequest(session=session)
        self.querystring_for_last_tweets = {"userName": twitter_url}
        self.querystring_for_advanced_search = {
            "query": contract_address,
            "queryType": "Top",
        }
        self.headers = headers

    async def _get_tweets(
        self,
        url: str,
        querystring: dict,
    ) -> dict:
        try:
            return await self.client.fetch(
                url=url,
                headers=self.headers,
                params=querystring,
            )
        except ApiError as e:
            logger.error("ApiError fetch_token_info Axiom: ", e)
            return {}

    async def get_user_tweets(
        self, url: str = twitter_settings.url_last_tweets
    ) -> dict:
        last_tweets_url = url
        querystring = self.querystring_for_last_tweets

        tweets = await self._get_tweets(url=last_tweets_url, querystring=querystring)
        logger.info("Tweets get successfully")
        return tweets

    async def get_top_tweets(
        self, url: str = twitter_settings.url_advanced_search
    ) -> dict:
        advanced_search_url = url
        querystring = self.querystring_for_advanced_search

        tweets = await self._get_tweets(
            url=advanced_search_url,
            querystring=querystring,
        )

        logger.info("Tweets from top get successfully")
        return tweets
