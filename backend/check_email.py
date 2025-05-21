"""
Script para verificar si un email específico existe en la base de datos.
"""
import sys
import pymysql

# Configuración de la base de datos
DB_HOST = "172.18.96.1"
DB_PORT = 3306
DB_USER = "gestion_app"
DB_PASSWORD = "DMP73noesilva"
DB_NAME = "gestion_proyectos"

def check_email(email):
    """Verificar si un email existe en la base de datos."""
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
        
        # Buscar usuarios con email similar
        cursor.execute("SELECT * FROM users WHERE email LIKE %s", (f"%{email}%",))
        similar_users = cursor.fetchall()
        
        print(f"\nUsuarios con email similar a '{email}':")
        if similar_users:
            for user in similar_users:
                print(f"- ID: {user[0]}, Email: {user[1]}, Nombre: {user[3]} {user[4]}")
        else:
            print("No se encontraron usuarios con email similar.")
        
        # Buscar usuario con email exacto
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        exact_user = cursor.fetchone()
        
        print(f"\nUsuario con email exacto '{email}':")
        if exact_user:
            print(f"- ID: {exact_user[0]}, Email: {exact_user[1]}, Nombre: {exact_user[3]} {exact_user[4]}")
        else:
            print("No se encontró ningún usuario con ese email exacto.")
        
        # Mostrar todos los usuarios
        cursor.execute("SELECT id, email, first_name, last_name FROM users")
        all_users = cursor.fetchall()
        
        print("\nTodos los usuarios en la base de datos:")
        for user in all_users:
            print(f"- ID: {user[0]}, Email: {user[1]}, Nombre: {user[2]} {user[3]}")
        
        # Cerrar la conexión
        cursor.close()
        conn.close()
        
        return True
    except Exception as e:
        print(f"[ERROR] Error al verificar el email: {e}")
        return False

if __name__ == "__main__":
    email = "dmpinero@gmail.com"
    if len(sys.argv) > 1:
        email = sys.argv[1]
    
    success = check_email(email)
    sys.exit(0 if success else 1)
