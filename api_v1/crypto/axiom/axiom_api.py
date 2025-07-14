import asyncio
import logging
from typing import Any

import aiohttp

import config
from api_v1.crypto.axiom.config import settings
from core.requests.AxiomRequest import AxiomRequest

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
        cookies: dict[str, str] = settings.COOKIES,
        headers: dict[str, str] = settings.HEADERS,
    ) -> None:
        self.pair_address = pair_address
        self.COOKIES = dict(cookies)
        self.HEADERS = dict(headers)

    async def fetch_token_info(
        self,
        client: AxiomRequest,
        url: str = settings.token_info_url,
        refresh_url: str = settings.refresh_access_token_url,
    ) -> dict | None:
        token_info_url = url + self.pair_address
        return await client.fetch(
            token_info_url,
            refresh_url,
            allow_refresh=True,
        )

    async def fetch_holder_data(
        self,
        client: AxiomRequest,
        url: str | tuple = settings.holder_data_url,
        refresh_url: str = settings.refresh_access_token_url,
    ) -> dict | None:
        holder_data_url = url[0] + self.pair_address + url[1]
        data = await client.fetch(
            holder_data_url,
            refresh_url,
            allow_refresh=True,
        )

        if isinstance(data, list) and data:
            data.sort(key=lambda x: x.get("tokenBalance", 0), reverse=True)
            return data[0]

        return None

    async def fetch_pair_info(
        self,
        client: AxiomRequest,
        url: str = settings.pair_info_url,
        refresh_url: str = settings.refresh_access_token_url,
    ) -> dict | None:
        pair_info_url = url + self.pair_address
        return await client.fetch(
            pair_info_url,
            refresh_url,
            allow_refresh=True,
        )

    async def get_info_about_token(self) -> dict[str, Any]:
        """
        Gather data from endpoints:
        - token_info: from fetch_token_info
        - top_holder: from fetch_holder_data
        - another data from fetch_pair_info
        """

        async with aiohttp.ClientSession(
            cookies=self.COOKIES,
            headers=self.HEADERS,
            timeout=config.timeout_settings.timeout,
        ) as session:
            client = AxiomRequest(
                session=session,
                COOKIES=self.COOKIES,
                HEADERS=self.HEADERS,
            )

            token_info_task = asyncio.create_task(self.fetch_token_info(client))
            top_holder_task = asyncio.create_task(self.fetch_holder_data(client))
            pair_info_task = asyncio.create_task(self.fetch_pair_info(client))

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
                "token_info": None,
                "top_holder": None,
            }

            result.update(settings.defaults)

            result["token_info"] = token_info
            result["top_holder"] = top_holder

            for key, default in settings.defaults.items():
                result[key] = pair_info.get(key, default)

            return result
