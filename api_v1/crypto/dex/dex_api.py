import logging

import aiohttp

from api_v1.crypto.dex.config import settings
from api_v1.crypto.dex.utils import parse_data
from core.requests.DexRequest import DexRequest

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class DexApi:

    def __init__(
        self,
        contract_address: str,
        session: aiohttp.ClientSession,
    ) -> None:
        self.contract_address = contract_address
        self.session = session

    async def fetch_token_pair(
        self,
        client: DexRequest,
        url: str = settings.token_pair_url,
    ):
        token_pair_url = url + self.contract_address
        return await client.fetch(url=token_pair_url)

    async def get_info_about_token(self) -> dict | None:
        client = DexRequest(session=self.session)
        dex_data = await self.fetch_token_pair(client)

        if dex_data:
            parsed_data = parse_data(dex_data)

            if parsed_data:
                return parsed_data
