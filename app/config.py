import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Config class
    """

    SEARCH_API_URL = os.getenv("SEARCH_API_URL")
    LOCATION_API_URL = os.getenv("LOCATION_API_URL")
    API_KEY = os.getenv("API_KEY")
    USER_AGENT = os.getenv("USER_AGENT")
    REDIS_URL = os.getenv("REDIS_URL")
