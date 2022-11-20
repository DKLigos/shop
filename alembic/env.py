import os

from sqlalchemy import engine_from_config, pool

from alembic import context
from env import loadenv

loadenv()

from logging.config import fileConfig

config = context.config

# fileConfig(config.config_file_name, disable_existing_loggers=False)

from app.db.base import Base  # noqa

target_metadata = Base.metadata


def include_name(name, type_, parent_names):
    if type_ == "schema":
        return name in [None, "shop"]
    elif type_ == "table":
        return parent_names["schema_qualified_table_name"] in target_metadata.tables
    else:
        return True


def get_url():
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "")
    server = os.getenv("POSTGRES_SERVER", "db")
    db = os.getenv("POSTGRES_DB", "shop")
    return f"postgresql://{user}:{password}@{server}/{db}"


cfg = dict(
    target_metadata=target_metadata,
    dialect_opts={"paramstyle": "named"},
    version_table='shop',
    version_table_schema='alembic',
    compare_type=True,
    include_name=include_name,
    include_schemas=True,
)


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    cfg['url'] = get_url()
    cfg['literal_binds'] = True,
    context.configure(**cfg)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    current_tenant = context.get_x_argument(as_dictionary=True).get("tenant")
    with connectable.connect() as connection:
        if current_tenant:
            connection.dialect.default_schema_name = current_tenant
        cfg['connection'] = connection
        context.configure(**cfg)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
