import logging
from typing import Any

import aiohttp

from api_v1.crypto.solana_tracker.config import settings
from api_v1.crypto.solana_tracker.utils import parse_data_st
from core.exceptions import ApiError, JsonParseError
from core.requests import STRequest

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class SolanaTrackerApi:

    def __init__(
        self,
        token_address: str,
        session: aiohttp.ClientSession,
        headers: dict = settings.headers,
    ) -> None:
        self.contract_address = token_address
        self.headers = headers
        self.client = STRequest(session=session)

    async def fetch_token_info(
        self,
        url: str = settings.token_info_url,
    ) -> dict:
        token_info_url = url + self.contract_address
        try:
            return await self.client.fetch(url=token_info_url, headers=self.headers)
        except ApiError as e:
            logger.error("ApiError fetch_token_info SolanaTracker: ", e)
            return {}

    async def get_info_about_token(self) -> dict[str, Any]:
        st_data = await self.fetch_token_info()

        try:
            parsed_data = parse_data_st(st_data)

            if parsed_data:
                return parsed_data
        except JsonParseError as e:
            logger.error("Error parse json data from SolanaTracker: ", e)
            return settings.defaults
