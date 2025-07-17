import logging

from core import BaseRequest
from core.exceptions import JsonResponseError, NetworkError, HttpStatusError, ApiError

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class MoralisRequest(BaseRequest):

    async def fetch(self, url: str, headers: dict) -> str:
        try:
            data = await self._raw_get(url=url, headers=headers)

            if not isinstance(data, dict):
                raise ApiError(f"Expected {dict.__name__}, got {type(data).__name__}")

            list_pa = data.get("pairs", [])

            if list_pa and isinstance(list_pa, list):
                first_pa = list_pa[0]

                if isinstance(first_pa, dict):
                    pa = first_pa.get("pairAddress", "")
                    return pa

            return ""

        except HttpStatusError as e:
            logger.error("HTTP Status Error %s for %s", e.status, e.url)
            return ""

        except NetworkError as e:
            logger.error(
                "Network Error: ",
                url,
                e,
            )
            return ""

        except JsonResponseError as e:
            logger.error("Parse JSON error from %s", url, e)
            return ""
