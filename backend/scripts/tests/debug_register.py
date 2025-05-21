"""
Script para depurar el proceso de registro de usuarios.
"""
import pymysql
import json
import sys

# Configuración de la base de datos
DB_HOST = "172.18.96.1"
DB_PORT = 3306
DB_USER = "gestion_app"
DB_PASSWORD = "DMP73noesilva"
DB_NAME = "gestion_proyectos"

def debug_register(email):
    """Depurar el proceso de registro para un email específico."""
    try:
        # Conectar a la base de datos
        conn = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        
        print(f"[OK] Conexión a la base de datos establecida correctamente.")
        
        # Crear un cursor
        cursor = conn.cursor()
        
        # Verificar si el email existe (case insensitive)
        cursor.execute("SELECT * FROM users WHERE LOWER(email) = LOWER(%s)", (email,))
        user_case_insensitive = cursor.fetchone()
        
        if user_case_insensitive:
            print(f"\n[ENCONTRADO] Usuario con email (case insensitive) '{email}':")
            print(f"- ID: {user_case_insensitive[0]}, Email: {user_case_insensitive[1]}")
            print(f"- Nombre: {user_case_insensitive[3]} {user_case_insensitive[4]}")
            print(f"- Activo: {user_case_insensitive[5]}, Superusuario: {user_case_insensitive[6]}")
        else:
            print(f"\n[NO ENCONTRADO] No se encontró ningún usuario con email '{email}' (case insensitive).")
        
        # Verificar si hay emails similares
        cursor.execute("SELECT * FROM users WHERE email LIKE %s", (f"%{email.split('@')[0]}%",))
        similar_users = cursor.fetchall()
        
        if similar_users:
            print(f"\n[SIMILARES] Usuarios con email similar:")
            for user in similar_users:
                print(f"- ID: {user[0]}, Email: {user[1]}")
        else:
            print(f"\n[SIMILARES] No se encontraron usuarios con email similar.")
        
        # Intentar eliminar cualquier usuario con este email (para limpiar)
        cursor.execute("DELETE FROM users WHERE LOWER(email) = LOWER(%s)", (email,))
        deleted_count = cursor.rowcount
        conn.commit()
        
        if deleted_count > 0:
            print(f"\n[LIMPIEZA] Se eliminaron {deleted_count} usuarios con email '{email}'.")
        else:
            print(f"\n[LIMPIEZA] No se encontraron usuarios para eliminar.")
        
        # Mostrar todos los usuarios
        cursor.execute("SELECT id, email FROM users")
        all_users = cursor.fetchall()
        
        print("\n[TODOS] Usuarios en la base de datos:")
        for user in all_users:
            print(f"- ID: {user[0]}, Email: {user[1]}")
        
        # Cerrar la conexión
        cursor.close()
        conn.close()
        
        return True
    except Exception as e:
        print(f"[ERROR] Error al depurar el registro: {e}")
        return False

if __name__ == "__main__":
    email = "dmpinero@gmail.com"
    if len(sys.argv) > 1:
        email = sys.argv[1]
    
    success = debug_register(email)
    sys.exit(0 if success else 1)
