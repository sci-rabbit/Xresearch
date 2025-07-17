import logging
from typing import Any

import aiohttp

from api_v1.crypto.dex.config import settings
from api_v1.crypto.dex.utils import parse_data_from_dex
from core.exceptions import ApiError, JsonParseError
from core.requests.DexRequest import DexRequest

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class DexApi:

    def __init__(
        self,
        contract_address: str,
        session: aiohttp.ClientSession,
    ) -> None:
        self.contract_address = contract_address
        self.client = DexRequest(session=session)

    async def fetch_token_pair(
        self,
        url: str = settings.token_pair_url,
    ) -> list:
        token_pair_url = url + self.contract_address
        try:
            return await self.client.fetch(url=token_pair_url)
        except ApiError as e:
            logger.error("ApiError fetch_token_pair DEX: ", e)
            return []

    async def get_info_about_token(self) -> dict[str, Any]:
        dex_data = await self.fetch_token_pair()

        try:
            parsed_data = parse_data_from_dex(dex_data)

            if parsed_data:
                return parsed_data
        except JsonParseError as e:
            logger.error("Error parse json data from DEX: ", e)
            return settings.defaults
