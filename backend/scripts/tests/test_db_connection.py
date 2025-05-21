import pymysql
import logging
from app.core.config import settings

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_mysql_connection():
    """
    Prueba la conexión a la base de datos MySQL
    """
    try:
        logger.info("Intentando conectar a MySQL...")
        logger.info(f"Host: {settings.DATABASE_HOST}")
        logger.info(f"Puerto: {settings.DATABASE_PORT}")
        logger.info(f"Usuario: {settings.DATABASE_USER}")
        logger.info(f"Base de datos: {settings.DATABASE_NAME}")
        
        # Intentar conectar a MySQL
        conn = pymysql.connect(
            host=settings.DATABASE_HOST,
            port=int(settings.DATABASE_PORT),
            user=settings.DATABASE_USER,
            password=settings.DATABASE_PASSWORD,
            database=settings.DATABASE_NAME
        )
        
        logger.info("¡Conexión exitosa a MySQL!")
        
        # Verificar si la tabla 'users' existe
        with conn.cursor() as cursor:
            cursor.execute("SHOW TABLES LIKE 'users'")
            table_exists = cursor.fetchone()
            
            if table_exists:
                logger.info("La tabla 'users' existe en la base de datos")
                
                # Contar usuarios en la tabla
                cursor.execute("SELECT COUNT(*) FROM users")
                user_count = cursor.fetchone()[0]
                logger.info(f"Número de usuarios en la tabla: {user_count}")
                
                # Listar todos los usuarios
                cursor.execute("SELECT id, email FROM users")
                users = cursor.fetchall()
                
                if users:
                    logger.info("Usuarios encontrados:")
                    for user in users:
                        logger.info(f"ID: {user[0]}, Email: {user[1]}")
                else:
                    logger.info("No hay usuarios en la tabla")
            else:
                logger.warning("La tabla 'users' no existe en la base de datos")
        
        conn.close()
        logger.info("Conexión cerrada")
        return True
    except Exception as e:
        logger.error(f"Error al conectar a MySQL: {str(e)}")
        return False

if __name__ == "__main__":
    test_mysql_connection()
