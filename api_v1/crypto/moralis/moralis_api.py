import logging

import aiohttp

from api_v1.crypto.moralis.config import settings
from core.exceptions import ApiError
from core.requests.MoralisRequest import MoralisRequest

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class MoralisApi:

    def __init__(
        self, ca: str, session: aiohttp.ClientSession, headers: dict = settings.headers
    ) -> None:
        self.contract_address = ca
        self.headers = headers
        self.session = session

    async def fetch_token_pair(
        self,
        client: MoralisRequest,
        url: tuple = settings.token_pair_url,
    ) -> str:
        token_pair_url = url[0] + self.contract_address + url[1]
        try:
            return await client.fetch(url=token_pair_url)
        except ApiError as e:
            logger.error("ApiError fetch_token_pair Moralis: ", e)
            return ""

    async def get_pair_address(self) -> str:
        client = MoralisRequest(session=self.session, headers=self.headers)

        moralis_data = await self.fetch_token_pair(client=client)

        if moralis_data:
            return moralis_data

        return ""
