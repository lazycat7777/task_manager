from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str = "db"
    DB_PORT: int = 5432
    DB_NAME: str = "task_db"
    DB_USER: str = "postgres"
    DB_PASS: str = "postgres"

    class Config:
        env_file = ".env"

settings = Settings()
