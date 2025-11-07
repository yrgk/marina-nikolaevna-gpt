import os
from dotenv import load_dotenv


load_dotenv()

class Config:
    BASE_URL = os.getenv("BASE_URL")
    OPENAI_KEY = os.getenv("OPENAI_KEY")

CONFIG = Config()