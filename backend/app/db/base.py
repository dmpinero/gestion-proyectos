from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Importar la clase Base desde base_class.py
from app.db.base_class import Base

# Importar todos los modelos para que SQLAlchemy los reconozca
from app.models.user import User  # Importamos el modelo User explícitamente

from app.core.config import settings

# Crear el motor de SQLAlchemy para MySQL
engine = create_engine(
    settings.DATABASE_URL
)

# Crear una fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Obtiene una sesión de base de datos.
    Se asegura de que la sesión se cierre correctamente después de su uso.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
