from pydantic import BaseSettings


class Settings(BaseSettings):
    server_host: str = "127.0.0.1"
    server_port: int = 8000
    database_url: str = 'sqlite:///./database.sqlite3'

    jwt_secret_key = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    jwt_algoritm = "HS256"
    access_token_expire_minutes = 30


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8'
)
