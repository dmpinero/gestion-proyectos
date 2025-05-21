"""
Script para crear directamente la tabla de usuarios en MySQL.
"""
import pymysql
import sys

# Configuración de la base de datos
DB_HOST = "172.18.96.1"
DB_PORT = 3306
DB_USER = "gestion_app"
DB_PASSWORD = "DMP73noesilva"
DB_NAME = "gestion_proyectos"

def create_users_table():
    """Crear la tabla de usuarios directamente con SQL."""
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
        
        # Verificar permisos del usuario
        cursor.execute("SHOW GRANTS FOR CURRENT_USER")
        grants = cursor.fetchall()
        print("\nPermisos del usuario actual:")
        for grant in grants:
            print(f"  - {grant[0]}")
        
        # Cerrar la conexión
        cursor.close()
        conn.close()
        
        return True
    except Exception as e:
        print(f"[ERROR] Error al crear la tabla de usuarios: {e}")
        return False

if __name__ == "__main__":
    success = create_users_table()
    sys.exit(0 if success else 1)
