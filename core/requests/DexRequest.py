from core.requests.request_model import BaseRequest


class DexRequest(BaseRequest):
    async def fetch(self, url: str):
        data = self._raw_get(url=url)

        if isinstance(data, list):
            return data

        return []
