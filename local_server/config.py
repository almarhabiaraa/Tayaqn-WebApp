from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    HOST: str
    PORT: int
    DATABASE_URL: str
    API_KEY: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    MODEL_PATH: str
    SCALER_PATH: str
    GLOBAL_SERVER_URL: str
    DEVICE: str 
    SMTP_SERVER: str
    SMTP_USER: str
    SMTP_PASSWORD: str
    class Config:
        env_file = Path(__file__).parent / ".env"
        env_file_encoding = "utf-8"

settings = Settings()


