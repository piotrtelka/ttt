from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    trello_api_key: str = Field(..., env="TRELLO_API_KEY")
    trello_api_secret: str = Field(..., env="TRELLO_API_SECRET")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def load_credentials():
    return Settings()
