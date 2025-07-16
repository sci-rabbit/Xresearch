import asyncio
import logging
from typing import Any

import aiohttp

import config
from api_v1.crypto.axiom.config import settings
from core.exceptions import ApiError
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
    ) -> dict:
        token_info_url = url + self.pair_address
        try:
            return await client.fetch(
                token_info_url,
                refresh_url,
                allow_refresh=True,
            )
        except ApiError as e:
            logger.error("ApiError fetch_token_info Axiom: ", e)
            return {}

    async def fetch_holder_data(
        self,
        client: AxiomRequest,
        url: str | tuple = settings.holder_data_url,
        refresh_url: str = settings.refresh_access_token_url,
    ) -> dict:
        holder_data_url = url[0] + self.pair_address + url[1]

        try:
            axiom_data = await client.fetch(
                holder_data_url,
                refresh_url,
                allow_refresh=True,
                expected_type=list,
            )
        except ApiError as e:
            logger.error("ApiError fetch_holder_data Axiom: ", e)
            return {}

        if isinstance(axiom_data, list) and axiom_data:
            axiom_data.sort(key=lambda x: x.get("tokenBalance", 0), reverse=True)
            return axiom_data[0]

        return {}

    async def fetch_pair_info(
        self,
        client: AxiomRequest,
        url: str = settings.pair_info_url,
        refresh_url: str = settings.refresh_access_token_url,
    ) -> dict:
        pair_info_url = url + self.pair_address
        try:
            return await client.fetch(
                pair_info_url,
                refresh_url,
                allow_refresh=True,
            )
        except ApiError as e:
            logger.error("ApiError fetch_pair_info Axiom: ", e)
            return {}

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
                cookies=self.COOKIES,
                headers=self.HEADERS,
            )

            token_info_task = asyncio.create_task(self.fetch_token_info(client))
            top_holder_task = asyncio.create_task(self.fetch_holder_data(client))
            pair_info_task = asyncio.create_task(self.fetch_pair_info(client))

            token_info, top_holder, pair_info = await asyncio.gather(
                token_info_task,
                top_holder_task,
                pair_info_task,
            )

            # Gathering results
            result: dict[str, Any] = {
                "token_info": {},
                "top_holder": {},
            }

            result.update(settings.defaults)

            result["token_info"] = token_info
            result["top_holder"] = top_holder
            for key, default in settings.defaults.items():
                result[key] = pair_info.get(key, default)

            return result
