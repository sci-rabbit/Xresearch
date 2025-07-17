import logging

from core import BaseRequest
from core.exceptions import HttpStatusError, NetworkError, JsonResponseError, ApiError

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class TwitterRequest(BaseRequest):

    async def fetch(
        self,
        url: str,
        headers: dict,
        params: dict,
    ):
        try:
            data = self._raw_get(url=url, headers=headers, params=params)

            if not isinstance(data, dict):
                raise ApiError(f"Expected {dict.__name__}, got {type(data).__name__}")

            return data

        except HttpStatusError as e:
            logger.error("HTTP Status Error %s for %s", e.status, e.url)
            return {}

        except NetworkError as e:
            logger.error("Network Error: ", e)
            return {}

        except JsonResponseError as e:
            logger.error("Parse JSON error from %s", url, e)
            return {}
