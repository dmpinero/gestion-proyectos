import os
import sys
from pathlib import Path

def before_scenario(context, scenario):
    """Se ejecuta antes de cada escenario."""
    # Asegurarse de que el directorio raíz del proyecto esté en el PYTHONPATH
    backend_dir = str(Path(__file__).parent.parent.resolve())
    if backend_dir not in sys.path:
        sys.path.insert(0, backend_dir)
    
    # Configurar la base de datos de prueba
    os.environ['TESTING'] = 'True'
    os.environ['DATABASE_URL'] = 'sqlite:///./test.db'
    
    # Importar después de configurar las variables de entorno
    from app.db.base import Base, engine, SessionLocal
    from fastapi.testclient import TestClient
    from main import app
    
    # Crear tablas en la base de datos
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    # Configurar el cliente de prueba
    context.client = TestClient(app, base_url="http://testserver")
    context.db = SessionLocal()

def after_scenario(context, scenario):
    """Se ejecuta después de cada escenario."""
    # Cerrar la sesión de la base de datos
    if hasattr(context, 'db'):
        context.db.close()
    
    # Limpiar la base de datos
    from app.db.base import Base, engine
    from sqlalchemy.orm import sessionmaker
    
    # Eliminar todas las tablas
    Base.metadata.drop_all(bind=engine)
    
    # Cerrar la conexión
    engine.dispose()
    
    # Limpiar las variables de entorno de prueba
    if 'TESTING' in os.environ:
        del os.environ['TESTING']
    if 'DATABASE_URL' in os.environ:
        del os.environ['DATABASE_URL']
