import asyncio
import logging

import aiohttp

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class BaseRequest:

    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def _raw_get(self, url: str) -> dict | None:
        try:
            async with self.session.get(url=url) as response:

                if response.status != 200:
                    logger.error(
                        f"Error request to {self.__class__.__name__}. Status: %s",
                        response.status,
                    )

                logger.info("GET %s -> %s", url, response.status)
                data = await response.json()
                logger.debug("Response data for %s: %s", url, data)

                return data
        except Exception as e:
            logger.error("Network error for %s: %s", url, e)
