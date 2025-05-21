"""
Script para verificar directamente en la base de datos MySQL si un email específico existe.
"""
import pymysql
import sys
from app.core.config import settings

def check_email_in_db(email):
    """Verificar directamente en la base de datos MySQL si un email existe."""
    try:
        # Conectar directamente a MySQL
        conn = pymysql.connect(
            host=settings.DATABASE_HOST,
            port=int(settings.DATABASE_PORT),
            user=settings.DATABASE_USER,
            password=settings.DATABASE_PASSWORD,
            database=settings.DATABASE_NAME
        )
        
        print(f"[INFO] Conexión a MySQL establecida correctamente.")
        print(f"[INFO] Verificando si el email '{email}' existe en la base de datos...")
        
        # Ejecutar consulta para verificar si el email existe
        with conn.cursor() as cursor:
            # Consulta case-insensitive
            cursor.execute("SELECT id, email, first_name, last_name FROM users WHERE LOWER(email) = LOWER(%s)", (email,))
            user = cursor.fetchone()
            
            if user:
                print(f"[ENCONTRADO] El email '{email}' está registrado:")
                print(f"  - ID: {user[0]}")
                print(f"  - Email: {user[1]}")
                print(f"  - Nombre: {user[2]} {user[3]}")
                return True
            else:
                print(f"[NO ENCONTRADO] El email '{email}' NO está registrado en la base de datos.")
                
                # Listar todos los usuarios para verificar
                cursor.execute("SELECT id, email FROM users")
                users = cursor.fetchall()
                
                print(f"\n[INFO] Usuarios existentes en la base de datos ({len(users)}):")
                for u in users:
                    print(f"  - ID: {u[0]}, Email: {u[1]}")
                
                return False
        
    except Exception as e:
        print(f"[ERROR] Error al verificar el email: {str(e)}")
        import traceback
        traceback.print_exc()
        return None
    finally:
        if 'conn' in locals() and conn:
            conn.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        email = sys.argv[1]
        check_email_in_db(email)
    else:
        print("[ERROR] Debe proporcionar un email como argumento.")
        print("Uso: python check_email_in_db.py <email>")
        sys.exit(1)
