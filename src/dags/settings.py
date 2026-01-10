from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    clickhouse_host: str
    clickhouse_port: int
    clickhouse_user: str
    clickhouse_password: str = ""
    clickhouse_db: str

settings = Settings()
