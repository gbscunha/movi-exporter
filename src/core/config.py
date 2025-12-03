from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    SYSTEM_A_BASE_URL = os.getenv("SYSTEM_A_BASE_URL")
    SYSTEM_A_TOKEN = os.getenv("SYSTEM_A_TOKEN")


settings = Settings()
