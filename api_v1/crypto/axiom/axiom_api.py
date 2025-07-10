import asyncio
import logging
from typing import Any

import aiohttp

from api_v1.crypto.axiom.config import settings
from api_v1.crypto.axiom.utils import fetch

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class AxiomApi:
    """
    Class for getting information about token from Axiom API.
    Execute requests to endpoints: token-info, holder-data-v2 и pair-info.
    """

    def __init__(
        self,
        pair_address: str,
        cookies: dict[str, str],
        headers: dict[str, str],
    ) -> None:
        self.pair_address = pair_address
        self.COOKIES = cookies
        self.HEADERS = headers

    async def fetch_token_info(
        self,
        session: aiohttp.ClientSession,
        url: str = settings.token_info_url,
    ) -> dict | None:
        token_info_url = url + self.pair_address
        return await fetch(session, token_info_url, allow_refresh=True)

    async def fetch_holder_data(
        self,
        session: aiohttp.ClientSession,
        url: str | tuple = settings.holder_data_url,
    ) -> dict | None:
        holder_data_url = url[0] + self.pair_address + url[1]
        data = await fetch(session, holder_data_url, allow_refresh=True)

        if isinstance(data, list) and data:
            data.sort(key=lambda x: x.get("tokenBalance", 0), reverse=True)
            return data[0]

        return None

    async def fetch_pair_info(
        self,
        session: aiohttp.ClientSession,
        url: str = settings.pair_info_url,
    ) -> dict | None:
        pair_info_url = url + self.pair_address
        return await fetch(session, pair_info_url, allow_refresh=True)

    async def get_info_about_token(self) -> dict[str, Any]:
        """
        Gather data from endpoinst:
        - token_info: from fetch_token_info
        - top_holder: from fetch_holder_data
        - another data from fetch_pair_info
        """
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

        async with aiohttp.ClientSession(
            cookies=self.COOKIES, headers=self.HEADERS
        ) as session:

            token_info_task = asyncio.create_task(self.fetch_token_info(session))
            top_holder_task = asyncio.create_task(self.fetch_holder_data(session))
            pair_info_task = asyncio.create_task(self.fetch_pair_info(session))

            token_info, top_holder, pair_info = await asyncio.gather(
                token_info_task,
                top_holder_task,
                pair_info_task,
                return_exceptions=True,
            )

            for var in (token_info, top_holder, pair_info):
                if isinstance(var, Exception):
                    logger.warning("Received exception in basic info gather: %s", var)

            # Gathering results
            result: dict[str, Any] = {
                "token_info": token_info,
                "top_holder": top_holder,
                **{
                    key: pair_info.get(key, default)
                    for key, default in defaults.items()
                },
            }

            return result
