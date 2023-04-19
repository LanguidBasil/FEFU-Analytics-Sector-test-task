from pydantic import BaseSettings


class AppSettings(BaseSettings):        
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    POSTGRES_DB_ADDRESS: str
    POSTGRES_DB_PORT: str
    