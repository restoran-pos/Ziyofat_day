from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    
    PROJECT_NAME: str
    DEBUG: bool
    MEDIA_PATH: str = "media_uploads/"
    BASE_URL: str = "https://ziyofat.uz"

    SESSION_ID_EXPIRE_DAYS: int = 1
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    class Config:
        env_file=".env"

settings = Settings()
