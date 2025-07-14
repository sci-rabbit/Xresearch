import logging

import aiohttp

from api_v1.crypto.moralis.config import settings

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class MoralisApi:

    def __init__(
        self, ca: str, session: aiohttp.ClientSession, headers: dict = settings.headers
    ) -> None:
        self.contract_address = ca
        self.headers = headers
        self.session = session

    async def get_pa(self, url: tuple | str = settings.token_pair_url) -> str | None:
        token_pair_url = url[0] + self.contract_address + url[1]

        async with self.session.get(token_pair_url, headers=self.headers) as response:
            try:
                data = await response.json()
                logger.info("Полученные данные от Moralis API: %s", data)
                if isinstance(data, dict):
                    list_pa = data.get("pairs", [])
                    if list_pa and isinstance(list_pa, list):
                        first_pa = list_pa[0]

                        if isinstance(first_pa, dict):
                            pa = first_pa.get("pairAddress", "")
                            return pa

            except Exception as e:
                logger.exception("Ошибка при запросе к Moralis API: %s", e)
                return None
