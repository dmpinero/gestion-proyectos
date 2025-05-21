"""
Script para inicializar la base de datos MySQL y configurar Alembic.
Este script:
1. Crea las tablas necesarias en MySQL
2. Configura Alembic para usar MySQL
3. Crea una migración inicial que refleja el estado actual de la base de datos
"""
import os
import sys
import subprocess
import pymysql
from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuración de la base de datos
DB_HOST = "172.18.96.1"
DB_PORT = 3306
DB_USER = "gestion_app"
DB_PASSWORD = "DMP73noesilva"
DB_NAME = "gestion_proyectos"
DB_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

# Crear el motor de SQLAlchemy
engine = create_engine(DB_URL)

# Crear una fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base para los modelos
Base = declarative_base()

def run_command(command):
    """Ejecutar un comando y mostrar su salida."""
    print(f"Ejecutando: {command}")
    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )
    stdout, stderr = process.communicate()
    
    if stdout:
        print(stdout)
    if stderr:
        print(stderr)
    
    return process.returncode

def create_tables_direct():
    """Crear tablas directamente con SQL."""
    try:
        # Conectar a la base de datos
        conn = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        
        print("[OK] Conexión a la base de datos establecida correctamente.")
        
        # Crear un cursor
        cursor = conn.cursor()
        
        # Verificar tablas existentes
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"Tablas existentes antes de la creación: {[t[0] for t in tables]}")
        
        # Crear la tabla de usuarios si no existe
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            hashed_password VARCHAR(255) NOT NULL,
            first_name VARCHAR(255),
            last_name VARCHAR(255),
            is_active BOOLEAN DEFAULT TRUE,
            is_superuser BOOLEAN DEFAULT FALSE,
            INDEX idx_email (email),
            INDEX idx_first_name (first_name),
            INDEX idx_last_name (last_name)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        
        cursor.execute(create_table_sql)
        conn.commit()
        
        print("[OK] Tabla 'users' creada correctamente.")
        
        # Verificar tablas después de la creación
        cursor.execute("SHOW TABLES")
        tables_after = cursor.fetchall()
        print(f"Tablas existentes después de la creación: {[t[0] for t in tables_after]}")
        
        # Mostrar la estructura de la tabla de usuarios
        cursor.execute("DESCRIBE users")
        columns = cursor.fetchall()
        print("\nEstructura de la tabla 'users':")
        for column in columns:
            print(f"  - {column[0]}: {column[1]}")
        
        # Cerrar la conexión
        cursor.close()
        conn.close()
        
        return True
    except Exception as e:
        print(f"[ERROR] Error al crear la tabla de usuarios: {e}")
        return False

def update_alembic_ini():
    """Actualizar el archivo alembic.ini para usar MySQL."""
    try:
        alembic_ini_path = os.path.join(os.path.dirname(__file__), "alembic.ini")
        
        with open(alembic_ini_path, "r") as f:
            content = f.read()
        
        # Reemplazar la URL de SQLite con la URL de MySQL
        content = content.replace(
            "sqlalchemy.url = driver://user:pass@localhost/dbname",
            f"sqlalchemy.url = {DB_URL}"
        )
        
        with open(alembic_ini_path, "w") as f:
            f.write(content)
        
        print("[OK] Archivo alembic.ini actualizado correctamente.")
        return True
    except Exception as e:
        print(f"[ERROR] Error al actualizar alembic.ini: {e}")
        return False

def initialize_alembic():
    """Inicializar Alembic con la base de datos actual."""
    try:
        # Marcar la revisión actual como la cabeza
        run_command("python -m alembic stamp head")
        
        # Crear una nueva migración que refleje el estado actual
        run_command("python -m alembic revision --autogenerate -m \"estado_inicial_mysql\"")
        
        print("[OK] Alembic inicializado correctamente.")
        return True
    except Exception as e:
        print(f"[ERROR] Error al inicializar Alembic: {e}")
        return False

def main():
    """Función principal."""
    print("=== Inicializando la base de datos MySQL ===")
    
    # Paso 1: Crear las tablas directamente con SQL
    if not create_tables_direct():
        print("[ERROR] No se pudieron crear las tablas. Abortando.")
        return 1
    
    # Paso 2: Actualizar el archivo alembic.ini
    if not update_alembic_ini():
        print("[ERROR] No se pudo actualizar alembic.ini. Abortando.")
        return 1
    
    # Paso 3: Inicializar Alembic
    if not initialize_alembic():
        print("[ERROR] No se pudo inicializar Alembic. Abortando.")
        return 1
    
    print("\n=== Inicialización completada con éxito ===")
    print("\nAhora puedes usar los siguientes comandos para gestionar la base de datos:")
    print("  - python manage_db.py migrate: Aplicar migraciones pendientes")
    print("  - python manage_db.py create \"descripción\": Crear una nueva migración")
    print("  - python manage_db.py history: Ver el historial de migraciones")
    print("  - python manage_db.py current: Ver la revisión actual")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
