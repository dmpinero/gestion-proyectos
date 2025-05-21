"""
Script para corregir la configuración de la base de datos y asegurarse de que se use MySQL.
"""
import os
import sys
import dotenv

def fix_db_config():
    """Corregir la configuración de la base de datos para usar MySQL."""
    try:
        # Cargar el archivo .env si existe
        env_file = os.path.join(os.getcwd(), '.env')
        if os.path.exists(env_file):
            print(f"[INFO] Archivo .env encontrado en: {env_file}")
            dotenv.load_dotenv(env_file)
            
            # Leer contenido actual
            with open(env_file, 'r') as f:
                env_content = f.read()
                
            print("[INFO] Contenido actual del archivo .env:")
            print("-" * 50)
            print(env_content)
            print("-" * 50)
            
            # Verificar si DATABASE_URL está definido
            if 'DATABASE_URL' in os.environ:
                current_db_url = os.environ['DATABASE_URL']
                print(f"[INFO] DATABASE_URL actual: {current_db_url}")
                
                if 'sqlite' in current_db_url.lower():
                    # Construir la URL de MySQL
                    mysql_url = f"mysql+pymysql://gestion_app:DMP73noesilva@172.18.96.1:3306/gestion_proyectos?charset=utf8mb4"
                    
                    # Actualizar el archivo .env
                    if 'DATABASE_URL=' in env_content:
                        # Reemplazar la línea existente
                        new_content = env_content.replace(f"DATABASE_URL={current_db_url}", f"DATABASE_URL={mysql_url}")
                    else:
                        # Añadir la nueva línea
                        new_content = env_content + f"\nDATABASE_URL={mysql_url}\n"
                    
                    # Guardar los cambios
                    with open(env_file, 'w') as f:
                        f.write(new_content)
                    
                    print(f"[OK] Archivo .env actualizado para usar MySQL.")
                    print(f"[INFO] Nueva URL de base de datos: {mysql_url}")
                else:
                    print("[INFO] La configuración ya está usando MySQL, no es necesario hacer cambios.")
            else:
                # DATABASE_URL no está en las variables de entorno, añadirlo al .env
                mysql_url = f"mysql+pymysql://gestion_app:DMP73noesilva@172.18.96.1:3306/gestion_proyectos?charset=utf8mb4"
                
                # Añadir al archivo .env
                with open(env_file, 'a') as f:
                    f.write(f"\nDATABASE_URL={mysql_url}\n")
                
                print(f"[OK] Variable DATABASE_URL añadida al archivo .env.")
                print(f"[INFO] URL de base de datos configurada: {mysql_url}")
        else:
            # Crear un nuevo archivo .env
            mysql_url = f"mysql+pymysql://gestion_app:DMP73noesilva@172.18.96.1:3306/gestion_proyectos?charset=utf8mb4"
            
            with open(env_file, 'w') as f:
                f.write(f"DATABASE_URL={mysql_url}\n")
            
            print(f"[OK] Archivo .env creado con la configuración de MySQL.")
            print(f"[INFO] URL de base de datos configurada: {mysql_url}")
        
        print("\n[INFO] Para aplicar los cambios, reinicia la aplicación.")
        
    except Exception as e:
        print(f"[ERROR] Error al corregir la configuración: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix_db_config()
