from pydantic_settings import SettingsConfigDict,BaseSettings
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent

class Settings(BaseSettings):
    DATABASE_URL:str
    SERIALIZER_SECRET:str
    model_config = SettingsConfigDict(
        env_file=BASE_PATH/".env",
        extra = "ignore"
    )

Config = Settings()