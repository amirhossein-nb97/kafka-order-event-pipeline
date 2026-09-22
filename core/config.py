from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # PostgreSQL
    database_host: str
    database_port: int
    database_name: str
    database_user: str
    database_password: str

    # Kafka
    kafka_bootstrap_servers: str
    kafka_topic: str
    kafka_group_id: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()