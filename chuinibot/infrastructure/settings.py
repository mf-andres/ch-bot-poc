from pydantic import BaseSettings


class Settings(BaseSettings):
    telegram_token: str
    rocketchat_token: str
