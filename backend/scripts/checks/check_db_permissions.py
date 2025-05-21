"""
Script para verificar los permisos del usuario de la base de datos.
"""
import pymysql
import sys

# Configuración de la base de datos
DB_HOST = "172.18.96.1"
DB_PORT = 3306
DB_USER = "gestion_app"
DB_PASSWORD = "DMP73noesilva"
DB_NAME = "gestion_proyectos"

def check_db_permissions():
    """Verificar los permisos del usuario en la base de datos."""
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
        
        # Verificar permisos
        cursor.execute("SHOW GRANTS FOR CURRENT_USER()")
        grants = cursor.fetchall()
        
        print("\nPermisos del usuario actual:")
        for grant in grants:
            print(f"- {grant[0]}")
        
        # Probar operaciones de escritura
        print("\nProbando operaciones de escritura:")
        
        # Crear una tabla temporal
        try:
            cursor.execute("CREATE TEMPORARY TABLE test_permissions (id INT, name VARCHAR(50))")
            print("[OK] Creación de tabla temporal exitosa.")
            
            # Insertar datos
            try:
                cursor.execute("INSERT INTO test_permissions VALUES (1, 'Test')")
                conn.commit()
                print("[OK] Inserción de datos exitosa.")
                
                # Verificar datos
                cursor.execute("SELECT * FROM test_permissions")
                data = cursor.fetchall()
                print(f"[OK] Lectura de datos exitosa: {data}")
                
                # Actualizar datos
                try:
                    cursor.execute("UPDATE test_permissions SET name = 'Updated' WHERE id = 1")
                    conn.commit()
                    print("[OK] Actualización de datos exitosa.")
                    
                    # Eliminar datos
                    try:
                        cursor.execute("DELETE FROM test_permissions WHERE id = 1")
                        conn.commit()
                        print("[OK] Eliminación de datos exitosa.")
                    except Exception as e:
                        print(f"[ERROR] No se pueden eliminar datos: {e}")
                except Exception as e:
                    print(f"[ERROR] No se pueden actualizar datos: {e}")
            except Exception as e:
                print(f"[ERROR] No se pueden insertar datos: {e}")
        except Exception as e:
            print(f"[ERROR] No se puede crear tabla temporal: {e}")
        
        # Verificar tablas existentes
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        print("\nTablas en la base de datos:")
        for table in tables:
            print(f"- {table[0]}")
            
            # Verificar permisos en cada tabla
            try:
                cursor.execute(f"SHOW GRANTS FOR CURRENT_USER ON {DB_NAME}.{table[0]}")
                table_grants = cursor.fetchall()
                for grant in table_grants:
                    print(f"  - {grant[0]}")
            except Exception as e:
                print(f"  - No se pueden obtener permisos específicos: {e}")
        
        # Cerrar la conexión
        cursor.close()
        conn.close()
        
        return True
    except Exception as e:
        print(f"[ERROR] Error al verificar permisos: {e}")
        return False

if __name__ == "__main__":
    success = check_db_permissions()
    sys.exit(0 if success else 1)
