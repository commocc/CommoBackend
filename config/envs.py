from typing import Optional, List
from pydantic import BaseSettings, AnyUrl


class EnvSettings(BaseSettings):
    SECRET_KEY: str
    DEBUG: bool = False

    DOMAIN_API: str = "app.bashkort.org"
    SENTRY: str = None

    TIMEZONE: str = "Europe/Moscow"

    POSTGRES_PORT: int = 5432
    POSTGRES_HOST: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 600
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 10080

    # telegram and openai
    TELEGRAM_BOT_TOKEN: str
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-ada-002"

    ALLOWED_TELEGRAM_USER_IDS: Optional[List[str]] = ["*"]
    SHOW_USAGE: bool = True
    PROXY_URL: Optional[str] = None

    REDIS_HOST: str = 'localhost'
    REDIS_PASS: str = ''
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_MAX_CONNECTIONS: int = 30

    def get_allowed_telegram_user_ids(self) -> str:
        if self.ALLOWED_TELEGRAM_USER_IDS == ["*"]:
            return "*"
        return ",".join(self.ALLOWED_TELEGRAM_USER_IDS)

    class Config:
        case_sensitive = True
        env_file = ".env"


envs = EnvSettings()

