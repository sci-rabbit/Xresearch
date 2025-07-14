import json
import logging

import aiohttp

from core.requests.request_model import BaseRequest


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


ACCESS_TOKEN_TYPE = "auth-access-token"
REFRESH_TOKEN_TYPE = "auth-refresh-token"


class AxiomRequest(BaseRequest):

    def __init__(
        self,
        session: aiohttp.ClientSession,
        COOKIES: dict,
        HEADERS: dict,
    ):
        super().__init__(session)
        self.COOKIES = COOKIES
        self.HEADERS = HEADERS

    async def _refresh_access_token(self, refresh_url: str) -> bool:
        """
        Update access- and refresh- tokens through endpoint refresh-access-token.
        """
        try:
            async with self.session.post(refresh_url, headers=self.HEADERS) as response:
                logger.info("Updated token try. Status: %s", response.status)
                if response.status != 200:
                    logger.error("Error token update. Status: %s", response.status)
                    return False

                new_access = response.cookies.get(ACCESS_TOKEN_TYPE)
                new_refresh = response.cookies.get(REFRESH_TOKEN_TYPE)

                if not (new_access and new_refresh):
                    logger.error("New tokens not found in the cookie response.")
                    return False

                self.COOKIES[ACCESS_TOKEN_TYPE] = new_access.value
                self.COOKIES[REFRESH_TOKEN_TYPE] = new_refresh.value

                self.session.cookie_jar.update_cookies(self.COOKIES)
                logger.info("Tokens successfully update.")
                return True
        except Exception as e:
            logger.exception("Error token update: %s", e)
            return False

    async def _raw_get(self, url: str) -> dict | None:
        try:
            async with self.session.get(url) as resp:
                if resp.status != 200:
                    logger.error(
                        f"Error request to {self.__class__.__name__}. Status: %s",
                        resp.status,
                    )

                logger.info("GET %s -> %s", url, resp.status)
                text = await resp.text()
                logger.debug("Response text for %s: %s", url, text)

                try:
                    return json.loads(text)
                except json.JSONDecodeError:
                    logger.error("Parse JSON error from %s", url)

        except Exception as e:
            logger.error("Network error for %s: %s", url, e)

    async def fetch(
        self,
        url: str,
        refresh_url: str,
        allow_refresh: bool = False,
    ) -> dict | None:
        """
        Gross function for GET-requests with JSON parse.
        If allow_refresh=True, Exception jwt expired will try to update token and repeat request.
        """

        data = await self._raw_get(url=url)

        if data is None:
            return {}

        if allow_refresh and isinstance(data, dict):
            if data.get("error") == "jwt expired":
                logger.info("JWT expired for %s, trying update...", url)
                if await self._refresh_access_token(refresh_url=refresh_url):
                    data = await self._raw_get(url=url)
                else:
                    logger.error("Update token failed %s", url)
                    return {}

        return data
