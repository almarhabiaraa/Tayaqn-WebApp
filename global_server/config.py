from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    HOST: str
    PORT: int
    MODEL_PATH: str
    SCALER_PATH: str
    FEATURES_PATH: str
    API_KEY: str
    DEVICE: str 
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()