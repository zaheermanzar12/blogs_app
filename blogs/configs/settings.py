from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SKIP_AUTH: bool = False
    APP_PORT: int = 8000
    API_PREFIX: str = "/blogs"
    LOG_LEVEL: str = "info"
    AUTH0_JWKS_URL: str =""

    DB_PORT: str = "5432"
    DB_NAME: str = "blogs_db"
    DB_USER: str = "postgres"
    DB_HOST: str = "localhost"
    DB_PASSWORD: str = "enetapps"

    DB_MIN_CONNECTIONS: int = 2
    DB_MAX_CONNECTIONS: int = 10


settings = Settings()