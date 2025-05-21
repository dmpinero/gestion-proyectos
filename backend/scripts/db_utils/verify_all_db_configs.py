"""
Script para verificar todas las posibles fuentes de configuración de la base de datos
y asegurarse de que estamos usando MySQL en todos los puntos.
"""
import os
import sys
import importlib.util
import inspect
from sqlalchemy import create_engine, text
import traceback

def verify_all_db_configs():
    """Verificar todas las posibles fuentes de configuración de la base de datos."""
    print("=" * 80)
    print("VERIFICACIÓN COMPLETA DE CONFIGURACIÓN DE BASE DE DATOS")
    print("=" * 80)
    
    # 1. Verificar variables de entorno
    print("\n1. VARIABLES DE ENTORNO:")
    print("-" * 50)
    db_env_vars = {}
    for env_var in os.environ:
        if 'DB' in env_var.upper() or 'DATABASE' in env_var.upper() or 'SQL' in env_var.upper():
            db_env_vars[env_var] = os.environ[env_var]
            print(f"  - {env_var}: {os.environ[env_var]}")
    
    if not db_env_vars:
        print("  * No se encontraron variables de entorno relacionadas con la base de datos.")
    
    # 2. Verificar archivo .env
    print("\n2. ARCHIVO .ENV:")
    print("-" * 50)
    env_file = os.path.join(os.getcwd(), '.env')
    if os.path.exists(env_file):
        print(f"  * Archivo .env encontrado en: {env_file}")
        with open(env_file, 'r') as f:
            env_content = f.read()
            print("  * Contenido del archivo .env:")
            for line in env_content.splitlines():
                if line.strip() and not line.strip().startswith('#'):
                    print(f"    - {line}")
    else:
        print("  * No se encontró archivo .env en el directorio actual.")
    
    # 3. Verificar configuración en app/core/config.py
    print("\n3. CONFIGURACIÓN EN app/core/config.py:")
    print("-" * 50)
    try:
        from app.core.config import settings
        print(f"  * DATABASE_URL en settings: {settings.DATABASE_URL}")
        print(f"  * DATABASE_HOST en settings: {settings.DATABASE_HOST}")
        print(f"  * DATABASE_PORT en settings: {settings.DATABASE_PORT}")
        print(f"  * DATABASE_USER en settings: {settings.DATABASE_USER}")
        print(f"  * DATABASE_NAME en settings: {settings.DATABASE_NAME}")
    except Exception as e:
        print(f"  * Error al importar configuración: {str(e)}")
    
    # 4. Verificar configuración en app/db/base.py
    print("\n4. CONFIGURACIÓN EN app/db/base.py:")
    print("-" * 50)
    try:
        from app.db.base import engine
        print(f"  * URL del motor de base de datos: {engine.url}")
        
        # Intentar una consulta simple para verificar la conexión
        try:
            with engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                print(f"  * Conexión exitosa a la base de datos: {result.scalar()}")
        except Exception as e:
            print(f"  * Error al conectar a la base de datos: {str(e)}")
    except Exception as e:
        print(f"  * Error al importar motor de base de datos: {str(e)}")
    
    # 5. Verificar configuración en alembic.ini y migrations/env.py
    print("\n5. CONFIGURACIÓN DE ALEMBIC:")
    print("-" * 50)
    alembic_ini = os.path.join(os.getcwd(), 'alembic.ini')
    if os.path.exists(alembic_ini):
        print(f"  * Archivo alembic.ini encontrado en: {alembic_ini}")
        # Buscar la línea sqlalchemy.url
        with open(alembic_ini, 'r') as f:
            for line in f:
                if 'sqlalchemy.url' in line and not line.strip().startswith('#'):
                    print(f"    - {line.strip()}")
    else:
        print("  * No se encontró archivo alembic.ini en el directorio actual.")
    
    migrations_env = os.path.join(os.getcwd(), 'migrations', 'env.py')
    if os.path.exists(migrations_env):
        print(f"  * Archivo migrations/env.py encontrado en: {migrations_env}")
        # Cargar el módulo env.py para inspeccionar su configuración
        try:
            spec = importlib.util.spec_from_file_location("env", migrations_env)
            env_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(env_module)
            
            # Buscar configuración de base de datos en el módulo
            for name, obj in inspect.getmembers(env_module):
                if name == 'config' and hasattr(obj, 'get_main_option'):
                    db_url = obj.get_main_option("sqlalchemy.url")
                    print(f"    - sqlalchemy.url en config: {db_url}")
        except Exception as e:
            print(f"  * Error al inspeccionar migrations/env.py: {str(e)}")
    else:
        print("  * No se encontró archivo migrations/env.py.")
    
    # 6. Verificar si hay alguna otra configuración de base de datos en el proyecto
    print("\n6. BÚSQUEDA DE OTRAS CONFIGURACIONES DE BASE DE DATOS:")
    print("-" * 50)
    # Esta parte es más compleja y podría requerir una búsqueda recursiva en todos los archivos
    # Por ahora, simplemente buscaremos en algunos archivos clave
    
    # 7. Probar la conexión a la base de datos MySQL directamente
    print("\n7. PRUEBA DE CONEXIÓN DIRECTA A MYSQL:")
    print("-" * 50)
    try:
        import pymysql
        
        # Extraer los datos de conexión de la URL
        from app.core.config import settings
        
        # Intentar conectar directamente con pymysql
        try:
            conn = pymysql.connect(
                host=settings.DATABASE_HOST,
                port=int(settings.DATABASE_PORT),
                user=settings.DATABASE_USER,
                password=settings.DATABASE_PASSWORD,
                database=settings.DATABASE_NAME
            )
            print(f"  * Conexión directa a MySQL exitosa.")
            
            # Ejecutar una consulta simple
            with conn.cursor() as cursor:
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                print(f"  * Tablas en la base de datos:")
                for table in tables:
                    print(f"    - {table[0]}")
                    
                    # Si es la tabla de usuarios, mostrar los primeros 5
                    if table[0].lower() == 'users':
                        cursor.execute(f"SELECT id, email, first_name, last_name, is_active FROM {table[0]} LIMIT 5")
                        users = cursor.fetchall()
                        print(f"      * Primeros 5 usuarios:")
                        for user in users:
                            print(f"        - ID: {user[0]}, Email: {user[1]}, Nombre: {user[2]} {user[3]}, Activo: {user[4]}")
            
            conn.close()
        except Exception as e:
            print(f"  * Error al conectar directamente a MySQL: {str(e)}")
            traceback.print_exc()
    except ImportError:
        print("  * No se pudo importar pymysql. Asegúrate de que está instalado.")
    
    print("\n" + "=" * 80)
    print("FIN DE LA VERIFICACIÓN")
    print("=" * 80)

if __name__ == "__main__":
    verify_all_db_configs()
