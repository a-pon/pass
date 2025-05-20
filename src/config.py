from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_host: str = Field(alias="FSTR_DB_HOST")
    db_port: int = Field(alias="FSTR_DB_PORT")
    db_login: str = Field(alias="FSTR_DB_LOGIN")
    db_pass: str = Field(alias="FSTR_DB_PASS")
    db_name: str = Field(alias="FSTR_DB_NAME")

    @property
    def _dsn_auth_part(self) -> str:
        return f'{self.db_login}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}'

    @property
    def db_url(self) -> str:
        return f'postgresql+asyncpg://{self._dsn_auth_part}'

    # Синхронное соединение для alembic
    @property
    def db_sync_url(self) -> str:
        return f'postgresql://{self._dsn_auth_part}'

    class Config:
        env_file = '.env'
        # env_file_encoding = 'utf-8'
        populate_by_name = True


settings = Settings()
