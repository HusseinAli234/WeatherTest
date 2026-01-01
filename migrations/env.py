import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context

# 1. Импортируйте ваш конфиг и модели
from app.core.config import settings
from app.core.database import Base
# Обязательно импортируйте модель User, чтобы Alembic её "увидел"
from app.models.user import User 

config = context.config

# Настройка логирования
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 2. Укажите метаданные ваших моделей
target_metadata = Base.metadata

def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    """Запуск миграций в асинхронном режиме"""
    
    # Берем настройки из alembic.ini, но заменяем URL на тот, что в нашем конфиге
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = settings.DATABASE_URL

    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        # Так как Alembic внутри синхронный, мы используем run_sync
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

if context.is_offline_mode():
    # Оффлайн режим (генерирует SQL-скрипт) остается без изменений
    context.configure(
        url=settings.DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()
else:
    # 3. Запускаем асинхронную функцию
    asyncio.run(run_migrations_online())