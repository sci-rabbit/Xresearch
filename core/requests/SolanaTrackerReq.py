import logging

from core.exceptions import ApiError, HttpStatusError, NetworkError, JsonResponseError
from core.requests.request_model import BaseRequest


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class STRequest(BaseRequest):

    async def fetch(self, url: str, headers: dict) -> dict:
        try:
            data = self._raw_get(url=url, headers=headers)

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
