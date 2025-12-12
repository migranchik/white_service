from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bot_token: Optional[str] = None
    BOT_USERNAME: Optional[str] = None

    API_LINK : str | None = "https://api.whiteservice.xyz/"

    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "whitevpn"
    DB_PASSWORD: str = "whitevpn_password"
    DB_NAME: str = "whitevpn"

    REMNAWAVE_BASE_URL: str | None = None
    REMNAWAVE_TOKEN: str | None = None
    REMNAWAVE_BASE_SUB_LINK: str | None = None

    YOOKASSA_SHOP_ID: str | None = None
    YOOKASSA_SECRET_KEY: str | None = None
    YOOKASSA_RETURN_URL: str | None = None
    YOOKASSA_WEBHOOK_URL: str | None = None

    REFERRAL_PERCENT: float | None = None

    @property
    def database_url(self) -> str:
        # async URL для SQLAlchemy + asyncpg
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"


settings = Settings()
