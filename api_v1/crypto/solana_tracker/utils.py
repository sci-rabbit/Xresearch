import logging
from typing import Any

from core.exceptions import JsonParseError


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def parse_data_st(data_from_solana_tracker_dict: dict[str, Any]) -> dict[str, Any]:

    try:
        if data_from_solana_tracker_dict:
            name = data_from_solana_tracker_dict.get("token", {}).get("name", "")
            symbol = data_from_solana_tracker_dict.get("token", {}).get("symbol", "")
            image = data_from_solana_tracker_dict.get("token", {}).get("image", "")
            extensions = data_from_solana_tracker_dict.get("token", {}).get(
                "extensions", None
            )
            holders = data_from_solana_tracker_dict.get("holders", [])
            pools_list = data_from_solana_tracker_dict.get("pools", [])

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

    except TypeError as e:
        logger.error("Error parse data from SolanaTracker: %s", e)
        raise JsonParseError("Error parse data", raw_text=str(e))
