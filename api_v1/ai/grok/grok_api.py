import asyncio
import os
import logging

from openai import AsyncOpenAI, APIError

import env
from api_v1.ai.grok.config import settings


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class OpenHandlerAI:

    def __init__(self, json_data: dict, api_key: str = None) -> None:

        if api_key is None:
            api_key = env.GROK_API
        if not api_key:
            logger.error("GROK_API not set.")
            raise ValueError("GROK_API is required")

        os.environ["GROK_API"] = api_key
        self.semaphore = asyncio.Semaphore(150)
        self.client = AsyncOpenAI(base_url=settings.base_url)
        self.json_data = json_data

    async def check_username(self) -> str:
        async with self.semaphore:
            try:
                response = await self.client.chat.completions.create(
                    model="grok-2-latest",
                    temperature=0,
                    messages=[
                        {
                            "role": "system",
                            "content": settings.system_prompt_for_find_dev,
                        },
                        {"role": "user", "content": self.json_data},
                    ],
                )
                result = (
                    response.choices[0].message.content if response.choices else "0"
                )
                logger.info("check_username response: %s", result)
                return result
            except APIError as e:
                logger.error("Error in check_username: %s", e)
                return "0"

    async def get_overview(self) -> str:

        async with self.semaphore:
            try:
                response = await self.client.chat.completions.create(
                    model="grok-2-latest",
                    messages=[
                        {
                            "role": "system",
                            "content": settings.system_prompt_for_overview,
                        },
                        {"role": "user", "content": self.json_data},
                    ],
                )
                result = response.choices[0].message.content if response.choices else ""
                logger.info("get_overview response: %s", result)
                return result
            except APIError as e:
                logger.error("Error in get_overview: %s", e)
                return ""
