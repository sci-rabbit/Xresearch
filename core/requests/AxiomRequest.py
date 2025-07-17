import asyncio
import json
import logging
from typing import Type, Union

from aiohttp import (
    ClientError,
    ClientResponseError,
    ContentTypeError,
)

from core.exceptions import (
    HttpStatusError,
    NetworkError,
    ApiError,
    JsonResponseError,
)
from core.requests.request_model import BaseRequest


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


ACCESS_TOKEN_TYPE = "auth-access-token"
REFRESH_TOKEN_TYPE = "auth-refresh-token"


class AxiomRequest(BaseRequest):

    async def _refresh_access_token(
        self,
        refresh_url: str,
        headers: dict,
        cookies: dict,
    ) -> bool:
        """
        Update access- and refresh- tokens through endpoint refresh-access-token.
        """
        try:
            async with self.session.post(refresh_url, headers=headers) as response:
                logger.info("Updated token try. Status: %s", response.status)
                if response.status != 200:
                    logger.error("Error token update. Status: %s", response.status)
                    return False

                new_access = response.cookies.get(ACCESS_TOKEN_TYPE)
                new_refresh = response.cookies.get(REFRESH_TOKEN_TYPE)

                if not (new_access and new_refresh):
                    logger.error("New tokens not found in the cookie response.")
                    return False

                cookies[ACCESS_TOKEN_TYPE] = new_access.value
                cookies[REFRESH_TOKEN_TYPE] = new_refresh.value

                self.session.cookie_jar.update_cookies(cookies)
                logger.info("Tokens successfully update.")
                return True

        except asyncio.TimeoutError:
            logger.error("Request to %s timed out", refresh_url)
            return False

        except ClientError as e:
            logger.error("Error token update: %s", e)
            return False

    async def _raw_get(
        self,
        url: str,
        headers: dict = None,
        cookies: dict = None,
        params: dict = None,
    ) -> dict:
        try:
            async with self.session.get(url) as resp:

                resp.raise_for_status()

                logger.info("GET %s -> %s", url, resp.status)
                text = await resp.text()
                logger.debug("Response text for %s: %s", url, text)

                return json.loads(text)

        except asyncio.TimeoutError:
            logger.error("Request to %s timed out", url)
            raise NetworkError("Timeout")

        except ContentTypeError as e:
            logger.error("Invalid content type from %s: %s", url, e)
            raise JsonResponseError(f"Invalid content type: {e}")

        except json.JSONDecodeError as e:
            body = await resp.text()
            logger.error("JSON decode error from %s: %s…", url, body[:200])
            raise JsonResponseError(f"JSON decode error: {e}")

        except ClientResponseError as e:
            logger.error("HTTP error %s for %s", e.status, url)
            raise HttpStatusError(e.status, url)

        except ClientError as e:
            logger.error("Network error for %s: %s", url, e)
            raise NetworkError(f"{e}")

    async def fetch(
        self,
        url: str,
        refresh_url: str,
        headers: dict,
        cookies: dict,
        allow_refresh: bool = False,
        expected_type: Type[Union[dict, list]] = dict,
    ) -> list | dict:
        """
        Common function for GET-requests with JSON parse.
        If allow_refresh=True, Exception jwt expired will try to update token and repeat request.
        """
        try:
            data = await self._raw_get(url=url)

            if allow_refresh and isinstance(data, dict):
                if data.get("error") == "jwt expired":
                    logger.info("JWT expired for %s, trying update...", url)
                    if await self._refresh_access_token(
                        refresh_url=refresh_url,
                        headers=headers,
                        cookies=cookies,
                    ):
                        data = await self._raw_get(url=url)
                    else:
                        logger.error("Update token failed %s", url)
                        return [] if expected_type is list else {}

            if not isinstance(data, expected_type):
                raise ApiError(
                    f"Expected {expected_type.__name__}, got {type(data).__name__}"
                )

            return data

        except HttpStatusError as e:
            logger.error("HTTP Status Error %s for %s", e.status, e.url)
            return [] if expected_type is list else {}

        except NetworkError as e:
            logger.error("Network Error: ", e)
            return [] if expected_type is list else {}

        except JsonResponseError as e:
            logger.error("Parse JSON error from %s", url, e)
            return [] if expected_type is list else {}
