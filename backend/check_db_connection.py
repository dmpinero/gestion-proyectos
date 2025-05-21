"""
Script para verificar la configuración de conexión a la base de datos MySQL.
"""
import os
import pymysql
from sqlalchemy import create_engine, text
from app.core.config import settings

def check_db_connection():
    """Verificar la configuración de conexión a la base de datos MySQL."""
    try:
        # Mostrar la URL de conexión (ocultando la contraseña por seguridad)
        db_url = settings.DATABASE_URL
        safe_url = db_url.replace(settings.DATABASE_PASSWORD, '********')
        print(f"[INFO] URL de conexión a la base de datos: {safe_url}")
        
        print("\n[INFO] Detalles de conexión MySQL:")
        print(f"  - Driver: mysql+pymysql")
        print(f"  - Usuario: {settings.DATABASE_USER}")
        print(f"  - Host: {settings.DATABASE_HOST}")
        print(f"  - Puerto: {settings.DATABASE_PORT}")
        print(f"  - Base de datos: {settings.DATABASE_NAME}")
        
        # Crear conexión a la base de datos
        engine = create_engine(db_url)
        
        # Probar conexión
        with engine.connect() as connection:
            print("\n[OK] Conexión a la base de datos MySQL establecida correctamente.")
            
            # Obtener información del servidor
            result = connection.execute(text("SELECT VERSION()"))
            version = result.scalar()
            print(f"[INFO] Versión del servidor MySQL: {version}")
            
            # Listar tablas
            result = connection.execute(text("SHOW TABLES"))
            tables = [row[0] for row in result]
            
            print("\n[INFO] Tablas en la base de datos MySQL:")
            for table in tables:
                print(f"  - {table}")
                
                # Contar registros en cada tabla
                count_result = connection.execute(text(f"SELECT COUNT(*) FROM {table}"))
                count = count_result.scalar()
                print(f"    * Registros: {count}")
                
                # Si es la tabla de usuarios, mostrar los primeros 10
                if table.lower() == 'users':
                    print(f"\n[INFO] Primeros 10 usuarios en la tabla '{table}':")
                    users_result = connection.execute(text(f"SELECT id, email, first_name, last_name, is_active FROM {table} LIMIT 10"))
                    users = [row for row in users_result]
                    
                    if users:
                        for user in users:
                            print(f"  - ID: {user[0]}, Email: {user[1]}, Nombre: {user[2]} {user[3]}, Activo: {user[4]}")
                    else:
                        print("  * No hay usuarios en la tabla.")
            
    except Exception as e:
        print(f"[ERROR] Error al verificar la conexión MySQL: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_db_connection()
