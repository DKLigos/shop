import os
from typing import Any, Dict, Optional

from pydantic import BaseSettings, PostgresDsn, validator


class AsyncPostgresDsn(PostgresDsn):
    allowed_schemes = {"postgres+asyncpg", "postgresql+asyncpg"}


class Settings(BaseSettings):
    PROJECT_NAME: str = "shop"
    LOG_LEVEL: str = "info"
    PROJECT_ROOT: str = ""
    REPORT_DIR: str = 'reports'
    LOAD_FILE_PATH: str = 'load_file'
    HTML_TEMPLATE_CLAIM_PATH: str = 'templates_claim'
    VOLUME_DIR_PATH: str = '/opt/app'

    @validator('LOAD_FILE_PATH', allow_reuse=True)
    def assemble_path(cls, v: str, values: Dict[str, Any]) -> str:  # noqa B902
        return os.path.join(values['PROJECT_ROOT'], v)

    PATH_UPLOAD_FILE: str = 'uploads'

    @validator('PATH_UPLOAD_FILE', allow_reuse=True)
    def path_upload_file_valid(cls, v: str, values: Dict[str, Any]) -> str:  # noqa B902
        return os.path.join(values['PROJECT_ROOT'], v)

    SIGNER_DIR_PATH: str = 'signers'

    @validator('SIGNER_DIR_PATH', allow_reuse=True)
    def dirs_path_valid(cls, v: str, values: Dict[str, Any]) -> str:  # noqa B902
        return os.path.join(values['PATH_UPLOAD_FILE'], v)


    SESSION_PREFIX: str = "async_session:{id_session}"
    LOCK_PREFIX: str = "lock:sts:{name}:{args}"
    MIGRATION_PREFIX: str = 'migration:shop'
    THREAD_POOL_SIZE: int = 50  # Max worker count for ThreadPoolExecutor

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_POOL_SIZE: int = 5
    POSTGRES_MAX_OVERFLOW: int = 50
    POSTGRES_POOL_TIMEOUT: int = 300
    SQLALCHEMY_DATABASE_URI: Optional[AsyncPostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", allow_reuse=True)
    def assemble_db_connection(
            cls, v: Optional[str], values: Dict[str, Any]  # noqa B902
    ) -> Any:
        if isinstance(v, str):
            return v
        return AsyncPostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    # migration on_start
    MIGRATION: bool = False

    URL: str = "http://localhost:8000"


settings = Settings(_env_file='.env.config', _env_file_encoding='utf-8')

