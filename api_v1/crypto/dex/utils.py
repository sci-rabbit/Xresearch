import logging
from typing import Any


from api_v1.crypto.dex.config import settings
from core.exceptions import ApiError, JsonParseError

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def parse_data(dex_data: list):

    pools = []

    twitter_url = ""
    tg_link = ""
    discord_link = ""
    web_links = []
    images = []
    name = ""
    symbol = ""

    try:
        baseToken = dex_data[0].get("baseToken", {})

        if baseToken:
            name = baseToken.get("name", "")
            symbol = baseToken.get("symbol", "")

        for el in dex_data:
            if isinstance(el, dict):
                pair_address = el.get("pairAddress", "")
                if pair_address:
                    pools.append(pair_address)

        socials = dex_data[0].get("info", {}).get("socials", [])
        websites = dex_data[0].get("info", {}).get("websites", [])

        if dex_data[0].get("info", {}).get("image_Url", ""):
            images.append(dex_data[0].get("info", {}).get("image_Url", ""))

        if dex_data[0].get("info", {}).get("header", ""):
            images.append(dex_data[0].get("info", {}).get("header", ""))

        if dex_data[0].get("info", {}).get("openGraph", ""):
            images.append(dex_data[0].get("info", {}).get("openGraph", ""))

        if socials:
            for social in socials:
                if social.get("type", "") == "twitter":
                    twitter_url = social.get("url", "")

                if social.get("type", "") == "telegram":
                    tg_link = social.get("url", "")

                if social.get("type", "") == "discord":
                    discord_link = social.get("url", "")

        if websites:
            for website in websites:
                link = website.get("url", "")

                if link:
                    web_links.append(link)

        args = [
            twitter_url,
            tg_link,
            discord_link,
            pools,
            images,
            web_links,
            name,
            symbol,
        ]

        result: dict[str, Any] = {key: arg for key, arg in zip(settings.defaults, args)}

        return result

    except AttributeError as e:
        logger.error("Error parse data from DEX: %s", e)
        raise JsonParseError("Error parse data", raw_text=str(e))
