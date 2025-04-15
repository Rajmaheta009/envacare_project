from logging.config import fileConfig
import os
from sqlalchemy import engine_from_config, pool
from alembic import context

# ✅ Load .env from the backend directory
from dotenv import load_dotenv
from pathlib import Path

# Construct the absolute path to .env in the backend folder
env_path = Path(__file__).resolve().parent.parent / "backend" / ".env"
load_dotenv(dotenv_path=env_path)

# Get the DATABASE_URL from the .env file
DATABASE_URL = os.getenv("DATABASE_URL")

# 🔐 Check and ensure it's valid
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found. Check backend/.env file.")

# Alembic Config object
config = context.config

# Override the URL in alembic.ini
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Model metadata (optional)
target_metadata = None

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
