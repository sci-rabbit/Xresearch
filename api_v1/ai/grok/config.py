from pydantic_settings import BaseSettings


class BaseGrokSettings(BaseSettings):

    system_prompt_for_overview: str = """"I need your analysis of Twitter to urgently understand a token.  
You will receive a Twitter user’s (project’s,zzz dev’s, or an associated account’s) description, top tweets mentioning the token’s CA, and the holder count of accounts posting about it. Your goal is to identify the token’s purpose and legitimacy.  

It could be an AI agent token, a Web2/Web3 project token, a celebrity token (e.g., $TRUMP), a community/art-based token, a funny animal coin, or a short-lived meme reacting to current events. If another category fits better, use it.  

STRICT RULES:  
- IGNORE mentions of price, gains, investment potential, snipers, tokenomics, or holder stats (except official release info).  
- DO NOT include speculation, hype, or copy-pasted promotions.  
- FOCUS ONLY on the project’s purpose, legitimacy, and dev credibility.  
- WATCH FOR BOT ACTIVITY**—repetitive tweets or unverified dev links may indicate artificial engagement.  

**OUTPUT FORMAT:  
1. First line: If a founder’s @username is mentioned, return "fndr = @username"  
   - If no founder is confirmed, return "=0"  
   - If a dev is linked but hasn’t confirmed engagement, return "=0"  
2. Next lines: Provide a concise (50-70 words) summary of the token’s purpose, legitimacy, and potential concerns.   

DO NOT mention CA. Get straight to the point—no filler."
    """

    system_prompt_for_find_dev: str = """
    Find the most likely potential dev/deployer if it's mentioned.
    TWO OPTIONS OF ANSWERS ARE ONLY "0" OR "@USERNAME"
    """

    base_url: str = "https://api.x.ai/v1"


settings = BaseGrokSettings()
