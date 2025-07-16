import logging

from core.exceptions import ApiError, HttpStatusError, NetworkError, JsonResponseError
from core.requests.request_model import BaseRequest


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class DexRequest(BaseRequest):

    async def fetch(self, url: str) -> list:

        try:
            data = self._raw_get(url=url)

            if not isinstance(data, list):
                raise ApiError(f"Expected {list.__name__}, got {type(data).__name__}")

            return data

        except HttpStatusError as e:
            logger.error("HTTP Status Error %s for %s", e.status, e.url)
            return []

        except NetworkError as e:
            logger.error("Network Error: ", e)
            return []

        except JsonResponseError as e:
            logger.error("Parse JSON error from %s", url, e)
            return []
