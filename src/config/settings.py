from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    groq_api_key: str
    db_path: str = "data/db/inventory.db"
    approval_threshold: float = 10000.0
    log_level: str = "INFO"

    class Config:
        env_file = ".env"


settings = Settings()