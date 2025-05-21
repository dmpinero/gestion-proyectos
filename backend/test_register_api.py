"""
Script para probar directamente el endpoint de registro y diagnosticar problemas.
"""
import requests
import json
import sys
import pymysql
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuración de la base de datos
DB_HOST = "172.18.96.1"
DB_PORT = 3306
DB_USER = "gestion_app"
DB_PASSWORD = "DMP73noesilva"
DB_NAME = "gestion_proyectos"

def check_db_connection():
    """Verificar la conexión a la base de datos."""
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        logger.info("Conexión a la base de datos establecida correctamente.")
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Error al conectar a la base de datos: {e}")
        return False

def check_user_exists(email):
    """Verificar si un usuario existe en la base de datos."""
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()
        
        # Verificar si el email existe
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        
        if user:
            logger.info(f"Usuario encontrado: ID={user[0]}, Email={user[1]}")
        else:
            logger.info(f"No se encontró ningún usuario con email '{email}'")
        
        cursor.close()
        conn.close()
        
        return user is not None
    except Exception as e:
        logger.error(f"Error al verificar usuario: {e}")
        return False

def test_register_api(email, first_name, last_name, password):
    """Probar el endpoint de registro directamente."""
    url = "http://localhost:8000/api/v1/auth/register"
    
    # Datos para el registro
    data = {
        "email": email,
        "firstName": first_name,
        "lastName": last_name,
        "password": password
    }
    
    logger.info(f"Enviando solicitud de registro para: {email}")
    logger.info(f"Datos: {json.dumps(data)}")
    
    # Verificar si el usuario ya existe antes de intentar registrarlo
    if check_user_exists(email):
        logger.warning(f"El usuario con email '{email}' ya existe en la base de datos.")
    
    # Enviar solicitud
    try:
        response = requests.post(url, json=data)
        
        # Mostrar información de la respuesta
        logger.info(f"Código de estado: {response.status_code}")
        logger.info(f"Respuesta: {response.text}")
        
        if response.status_code == 201:
            logger.info("Registro exitoso!")
            
            # Verificar si el usuario se creó en la base de datos
            if check_user_exists(email):
                logger.info(f"Usuario con email '{email}' confirmado en la base de datos.")
            else:
                logger.warning(f"Usuario con email '{email}' no encontrado en la base de datos a pesar de respuesta exitosa.")
        else:
            logger.error(f"Error en el registro: {response.text}")
        
        return response
    except Exception as e:
        logger.error(f"Error al enviar solicitud: {e}")
        return None

if __name__ == "__main__":
    # Verificar conexión a la base de datos
    if not check_db_connection():
        sys.exit(1)
    
    # Email para prueba
    test_email = "test_user_123@example.com"
    if len(sys.argv) > 1:
        test_email = sys.argv[1]
    
    # Probar el endpoint de registro
    test_register_api(
        email=test_email,
        first_name="Test",
        last_name="User",
        password="password123"
    )
