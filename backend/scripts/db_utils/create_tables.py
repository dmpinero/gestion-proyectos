"""
Script para crear las tablas en la base de datos.
Ejecutar con: python create_tables.py
"""
import sys
from sqlalchemy import inspect

# Importar la clase Base y el motor
from app.db.base_class import Base
from app.db.base import engine

# Importar todos los modelos para que SQLAlchemy los reconozca
from app.models.user import User

def create_tables():
    """Crear todas las tablas definidas en los modelos."""
    try:
        # Verificar si hay conexión a la base de datos
        conn = engine.connect()
        conn.close()
        print("[OK] Conexión a la base de datos establecida correctamente.")
        
        # Obtener las tablas existentes
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()
        print(f"Tablas existentes antes de la creación: {existing_tables}")
        
        # Crear las tablas
        Base.metadata.create_all(bind=engine)
        print("[OK] Tablas creadas correctamente.")
        
        # Verificar las tablas creadas
        inspector = inspect(engine)
        tables_after = inspector.get_table_names()
        print(f"Tablas existentes después de la creación: {tables_after}")
        
        # Mostrar la estructura de la tabla de usuarios
        if "users" in tables_after:
            columns = inspector.get_columns("users")
            print("\nEstructura de la tabla 'users':")
            for column in columns:
                print(f"  - {column['name']}: {column['type']}")
        
        return True
    except Exception as e:
        print(f"[ERROR] Error al crear las tablas: {e}")
        return False

if __name__ == "__main__":
    success = create_tables()
    sys.exit(0 if success else 1)
