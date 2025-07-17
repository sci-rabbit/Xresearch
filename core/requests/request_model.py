import asyncio
import json
import logging

import aiohttp
from aiohttp import ClientResponseError, ClientError, ContentTypeError

from core.exceptions import (
    NetworkError,
    HttpStatusError,
    JsonResponseError,
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class BaseRequest:

    def __init__(
        self,
        session: aiohttp.ClientSession,
    ):
        self.session = session

    async def _raw_get(
        self,
        url: str,
        headers: dict = None,
        cookies: dict = None,
        params: dict = None,
    ) -> dict:
        try:
            async with self.session.get(
                url=url, headers=headers, cookies=cookies, params=params
            ) as response:

                response.raise_for_status()
                logger.info("GET %s -> %s", url, response.status)
                return await response.json()

        except asyncio.TimeoutError:
            logger.error("Request to %s timed out", url)
            raise NetworkError("Timeout")

        except ContentTypeError as e:
            logger.error("Invalid content type from %s: %s", url, e)
            raise JsonResponseError(f"Invalid content type: {e}")

        except json.JSONDecodeError as e:
            logger.error("Invalid JSON from %s: %s…", url, await response.text()[:200])
            raise JsonResponseError(f"JSON decode error: {e}")

        except ClientResponseError as e:
            logger.error("HTTP error %s for %s", e.status, url)
            raise HttpStatusError(e.status, url)

        except ClientError as e:
            logger.error("Network error for %s: %s", url, e)
            raise NetworkError(f"{e}")
