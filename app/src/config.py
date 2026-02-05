import datetime


from pathlib import Path


from pydantic import BaseModel, Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent  # src
ROOT_DIR = BASE_DIR.parent  # app
ENV_FILE_DEV = ROOT_DIR.parent / "envs/local/app.env"


class Database(BaseModel):
    """
    Database configuration model.

    This model is used to store the necessary database configuration
    for connecting to the database.

    Attributes:
        url (PostgresDsn): The URL of the postgres database.
        echo (bool): Whether to log SQL statements to the console or not.
        echo_pool (bool): Whether to log pool activity to the console or not.
        pool_pre_ping (bool): Whether to check the connection before using it.
        pool_size (int): The size of the connection pool.
        max_overflow (int): The maximum number of connections to add to the pool.
    """

    """"""
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_pre_ping: bool = True
    pool_size: int = 100
    max_overflow: int = 10
    engine_kwargs: dict = {
        "echo_pool": echo_pool,
        "pool_size": pool_size,
        "max_overflow": max_overflow,
        "pool_pre_ping": pool_pre_ping,
    }

    @property
    def naming_convention(self) -> dict[str, str]:
        """Naming convention for the database."""
        return {
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_N_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }


class Settings(BaseSettings):
    db: Database = Field(default_factory=Database)
    time_zone: datetime.tzinfo = datetime.timezone.utc
    api_key: str = Field(default_factory=str, examples=["xxx"])

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_DEV,
        extra="allow",
        case_sensitive=False,
        env_prefix="APP_CONFIG__",
        env_nested_delimiter="__",
    )


settings = Settings()
