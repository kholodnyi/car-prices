from pydantic import BaseSettings

__all__ = ['settings', ]


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str

    # optional settings for scraping
    PROVINCE: str = None

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
