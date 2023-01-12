from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    CLIENT_ORIGIN = os.getenv("CLIENT_ORIGIN")
    DATABASE_URL = os.getenv("DATABASE_URL")


settings = Settings()