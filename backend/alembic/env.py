from logging.config import fileConfig

from alembic import context

from backend.config.settings import settings
from backend.database.database import Base, engine


# ============================================================
# IMPORTAR TODOS LOS MODELOS
# ============================================================

from backend.models.user import User  # noqa: F401
from backend.models.project import Project  # noqa: F401
from backend.models.assistant import Assistant  # noqa: F401
from backend.models.conversation import Conversation, Message  # noqa: F401
from backend.models.document import Document  # noqa: F401
from backend.models.chunk import Chunk  # noqa: F401
from backend.models.assistant_tool import AssistantTool  # noqa: F401


# ============================================================
# CONFIGURACIÓN DE ALEMBIC
# ============================================================

config = context.config


# ============================================================
# CONFIGURACIÓN DE LOGGING
# ============================================================

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# ============================================================
# METADATA DE SQLALCHEMY
# ============================================================

target_metadata = Base.metadata


# ============================================================
# MIGRACIONES OFFLINE
# ============================================================

def run_migrations_offline() -> None:
    """
    Ejecuta las migraciones en modo offline.
    """

    url = settings.DATABASE_URL

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={
            "paramstyle": "named",
        },
    )

    with context.begin_transaction():
        context.run_migrations()


# ============================================================
# MIGRACIONES ONLINE
# ============================================================

def run_migrations_online() -> None:
    """
    Ejecuta las migraciones conectándose directamente
    a la base de datos.
    """

    connectable = engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


# ============================================================
# EJECUTAR MIGRACIONES
# ============================================================

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

    