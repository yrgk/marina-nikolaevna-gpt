import os
from dotenv import load_dotenv


load_dotenv()

class Config:
    BASE_URL = os.getenv("BASE_URL")
    OPENAI_KEY = os.getenv("OPENAI_KEY")
    BOT_TOKEN = os.getenv("BOT_TOKEN")

CONFIG = Config()