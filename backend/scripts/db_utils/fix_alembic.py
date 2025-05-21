"""
Script para corregir la configuración de Alembic y forzar el uso del dialecto MySQL.
"""
import os
import sys
import subprocess
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

# Configuración de la base de datos
DB_HOST = "172.18.96.1"
DB_PORT = 3306
DB_USER = "gestion_app"
DB_PASSWORD = "DMP73noesilva"
DB_NAME = "gestion_proyectos"
DB_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

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

def fix_alembic_env():
    """Corregir el archivo env.py para forzar el uso del dialecto MySQL."""
    try:
        env_py_path = os.path.join(os.path.dirname(__file__), "migrations", "env.py")
        
        # Leer el contenido actual
        with open(env_py_path, "r") as f:
            content = f.read()
        
        # Modificar la configuración para forzar el uso del dialecto MySQL
        if "config.get_section(config.config_ini_section)" not in content:
            # Reemplazar la línea que obtiene la sección de configuración
            content = content.replace(
                "config.get_section(config.config_ini_section, {})",
                "config.get_section(config.config_ini_section)"
            )
        
        # Agregar una línea para forzar el dialecto MySQL
        if "from sqlalchemy.dialects.mysql.pymysql import MySQLDialect_pymysql" not in content:
            # Agregar la importación del dialecto MySQL
            content = content.replace(
                "from sqlalchemy.dialects import mysql",
                "from sqlalchemy.dialects import mysql\nfrom sqlalchemy.dialects.mysql.pymysql import MySQLDialect_pymysql"
            )
        
        # Guardar los cambios
        with open(env_py_path, "w") as f:
            f.write(content)
        
        print("[OK] Archivo env.py actualizado correctamente.")
        return True
    except Exception as e:
        print(f"[ERROR] Error al actualizar env.py: {e}")
        return False

def main():
    """Función principal."""
    print("=== Corrigiendo la configuración de Alembic ===")
    
    # Paso 1: Corregir el archivo env.py
    if not fix_alembic_env():
        print("[ERROR] No se pudo corregir el archivo env.py. Abortando.")
        return 1
    
    # Paso 2: Verificar la conexión a la base de datos
    try:
        engine = create_engine(DB_URL)
        connection = engine.connect()
        connection.close()
        print("[OK] Conexión a la base de datos establecida correctamente.")
    except Exception as e:
        print(f"[ERROR] Error al conectar a la base de datos: {e}")
        return 1
    
    # Paso 3: Verificar las tablas existentes
    try:
        engine = create_engine(DB_URL)
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"Tablas existentes en la base de datos: {tables}")
        
        if "users" in tables:
            print("[OK] La tabla 'users' existe en la base de datos.")
        else:
            print("[ADVERTENCIA] La tabla 'users' no existe en la base de datos.")
    except Exception as e:
        print(f"[ERROR] Error al verificar las tablas: {e}")
        return 1
    
    # Paso 4: Crear una nueva migración para verificar que Alembic funciona correctamente
    run_command("python -m alembic revision -m \"verificar_configuracion_mysql\"")
    
    print("\n=== Corrección completada ===")
    print("\nAhora puedes usar los siguientes comandos para gestionar la base de datos:")
    print("  - python manage_db.py migrate: Aplicar migraciones pendientes")
    print("  - python manage_db.py create \"descripción\": Crear una nueva migración")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
