from logging.config import fileConfig
import os
import sys

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Añadir el directorio del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar la configuración y los modelos
from app.core.config import settings
from app.db.base_class import Base
from app.models.user import User  # Importar explícitamente todos los modelos

# Forzar el uso del dialecto MySQL
from sqlalchemy.dialects import mysql
from sqlalchemy.dialects.mysql.pymysql import MySQLDialect_pymysql

# Importar el dialecto específico para MySQL
from sqlalchemy.engine.url import make_url
from sqlalchemy.dialects.mysql import dialect

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Sobrescribir la URL de la base de datos con la de nuestra aplicación
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    # Forzar el uso del dialecto MySQL
    url_obj = make_url(url)
    if url_obj.get_dialect().name == 'mysql':
        context.configure(
            url=url,
            target_metadata=target_metadata,
            literal_binds=True,
            dialect_opts={"paramstyle": "named"},
            compare_type=True,  # Comparar tipos de columnas
            compare_server_default=True,  # Comparar valores por defecto,
            dialect=dialect()
        )
    else:
        context.configure(
            url=url,
            target_metadata=target_metadata,
            literal_binds=True,
            dialect_opts={"paramstyle": "named"},
            compare_type=True,  # Comparar tipos de columnas
            compare_server_default=True,  # Comparar valores por defecto
        )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # Obtener la URL de la base de datos
    url = config.get_main_option("sqlalchemy.url")
    url_obj = make_url(url)
    
    # Configurar el motor con opciones específicas para MySQL
    if url_obj.get_dialect().name == 'mysql':
        connectable = engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            connect_args={"charset": "utf8mb4"}
        )
    else:
        connectable = engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

    with connectable.connect() as connection:
        # Usar el dialecto MySQL si corresponde
        if url_obj.get_dialect().name == 'mysql':
            context.configure(
                connection=connection, 
                target_metadata=target_metadata,
                compare_type=True,  # Comparar tipos de columnas
                compare_server_default=True,  # Comparar valores por defecto,
                dialect=dialect()
            )
        else:
            context.configure(
                connection=connection, 
                target_metadata=target_metadata,
                compare_type=True,  # Comparar tipos de columnas
                compare_server_default=True,  # Comparar valores por defecto
            )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
