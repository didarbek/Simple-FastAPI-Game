from pydantic import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = True
    MODE: str = 'development'
    NAME: str = 'Simple Game'
    HOST: str = '127.0.0.1'
    PORT: int = 8000
    LOG_LEVEL: str = 'info'

    PG_DSN: str = 'postgresql://postgres:postgres@localhost:5432/simple_game'
    PG_DSN_ROOT: str = 'postgresql://postgres:postgres@localhost:5432/postgres'
    PG_TEST_DB_NAME: str = 'simple_game'
    DEFAULT_USER_AVATAR: str = ''

    class Config:
        env_file = '.env'


config = Settings()
