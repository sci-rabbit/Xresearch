import json
import logging

import aiohttp

from api_v1.crypto.axiom.config import settings

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


ACCESS_TOKEN_TYPE = "auth-access-token"
REFRESH_TOKEN_TYPE = "auth-refresh-token"


async def refresh_access_token(
    self,
    session: aiohttp.ClientSession,
    url: str = settings.refresh_access_token_url,
) -> bool:
    """
    Update access- and refresh- tokens through endpoint refresh-access-token.
    """

    try:
        async with session.post(url, headers=self.HEADERS) as response:
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

            session.cookie_jar.update_cookies(self.COOKIES)
            logger.info("Tokens successfully update.")
            return True
    except Exception as e:
        logger.exception("Error token update: %s", e)
        return False


async def fetch(
    session: aiohttp.ClientSession,
    url: str,
    allow_refresh: bool = False,
) -> dict | None:
    """
    Gross function for GET-requests with JSON parse.
    If allow_refresh=True, Exception jwt expired will try to update token and repeat request.
    """

    async def _raw_get() -> dict | None:
        try:
            async with session.get(url) as resp:
                logger.info("GET %s -> %s", url, resp.status)
                text = await resp.text()
                logger.debug("Response text for %s: %s", url, text)
                try:
                    return json.loads(text)
                except json.JSONDecodeError:
                    logger.error("Parse JSON error from %s", url)
                    return None
        except Exception as e:
            logger.exception("Error request %s: %s", url, e)
            return None

    data = await _raw_get()

    if allow_refresh and isinstance(data, dict) and data.get("error") == "jwt expired":
        logger.info("JWT expired for %s, trying update...", url)
        if await refresh_access_token(session):
            data = await _raw_get()
        else:
            logger.error("Update token failed %s", url)
            return None

    return data
