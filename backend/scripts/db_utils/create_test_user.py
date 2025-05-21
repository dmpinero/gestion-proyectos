"""
Script para crear un usuario de prueba en la base de datos.
"""
import sys
import pymysql
from app.core.security import get_password_hash

# Configuración de la base de datos
DB_HOST = "172.18.96.1"
DB_PORT = 3306
DB_USER = "gestion_app"
DB_PASSWORD = "DMP73noesilva"
DB_NAME = "gestion_proyectos"

def create_test_user():
    """Crear un usuario de prueba en la base de datos."""
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
        
        # Datos del usuario de prueba
        email = "admin@example.com"
        password = "admin123"
        first_name = "Admin"
        last_name = "User"
        
        # Generar hash de la contraseña
        hashed_password = get_password_hash(password)
        
        # Verificar si el usuario ya existe
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            print(f"[INFO] El usuario {email} ya existe en la base de datos.")
            print(f"- ID: {existing_user[0]}")
            print(f"- Email: {existing_user[1]}")
            print(f"- Nombre: {existing_user[3]} {existing_user[4]}")
            return True
        
        # Insertar el usuario en la base de datos
        insert_sql = """
        INSERT INTO users (email, hashed_password, first_name, last_name, is_active, is_superuser)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(insert_sql, (
            email,
            hashed_password,
            first_name,
            last_name,
            True,  # is_active
            True   # is_superuser
        ))
        
        conn.commit()
        
        # Verificar que el usuario se haya creado correctamente
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        
        if user:
            print(f"[OK] Usuario creado correctamente:")
            print(f"- ID: {user[0]}")
            print(f"- Email: {user[1]}")
            print(f"- Nombre: {user[3]} {user[4]}")
            print(f"- Contraseña: {password} (sin hash)")
        else:
            print("[ERROR] No se pudo crear el usuario.")
            return False
        
        # Mostrar todos los usuarios en la base de datos
        cursor.execute("SELECT * FROM users")
        all_users = cursor.fetchall()
        
        print("\nUsuarios en la base de datos:")
        for u in all_users:
            print(f"- ID: {u[0]}, Email: {u[1]}, Nombre: {u[3]} {u[4]}")
        
        # Cerrar la conexión
        cursor.close()
        conn.close()
        
        return True
    except Exception as e:
        print(f"[ERROR] Error al crear el usuario de prueba: {e}")
        return False

if __name__ == "__main__":
    success = create_test_user()
    sys.exit(0 if success else 1)
