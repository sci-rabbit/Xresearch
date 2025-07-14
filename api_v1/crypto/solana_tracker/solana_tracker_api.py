import logging

import aiohttp

from api_v1.crypto.solana_tracker.config import settings

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class SolanaTrackerApi:

    def __init__(
        self,
        token_address: str,
        session: aiohttp.ClientSession,
        header: dict = settings.header,
    ) -> None:
        self.tokenAddress = token_address
        self.header = header
        self.session = session

    async def get_info_about_token(
        self, url: str = settings.token_pair_url
    ) -> dict | None:

        try:
            async with self.session.get(
                url=url, headers=self.header
            ) as response_from_solana_tracker:
                if response_from_solana_tracker.status != 200:
                    logger.error(
                        "Ошибка запроса к Solana Tracker API. Статус: %s",
                        response_from_solana_tracker.status,
                    )
                    return None

                data = await response_from_solana_tracker.json()

                if data:
                    name = data.get("token", {}).get("name", None)
                    symbol = data.get("token", {}).get("symbol", None)
                    image = data.get("token", {}).get("image", None)
                    extensions = data.get("token", {}).get("extensions", None)
                    holders = data.get("holders", None)
                    pools_list = data.get("pools", None)

                poolId = ""
                token_supply = None

                if pools_list and isinstance(token_supply, list):
                    poolId = pools_list[0].get("poolId", None)
                    token_supply = pools_list[0].get("tokenSupply", None)

                return {
                    "name": name,
                    "symbol": symbol,
                    "image": image,
                    "extensions": extensions,
                    "holders": holders,
                    "poolId": poolId,
                    "token_supply": token_supply,
                }

        except Exception as e:
            logger.exception("Ошибка при получение Json объекта ", e)

            return settings.defaults
