import requests
import json
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_register_user():
    """
    Prueba directa del endpoint de registro de usuarios
    """
    url = "http://localhost:8000/api/v1/auth/register"
    
    # Datos de prueba
    data = {
        "email": "dmpinero@gmail.com",
        "firstName": "Daniel",
        "lastName": "Martinez Piñero",
        "password": "12345678"
    }
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Host": "localhost:8000",
        "Origin": "http://localhost:8000"
    }
    
    try:
        logger.info(f"Enviando solicitud POST a {url}")
        logger.info(f"Datos: {json.dumps(data)}")
        logger.info(f"Headers: {headers}")
        
        response = requests.post(url, json=data, headers=headers)
        
        logger.info(f"Código de estado: {response.status_code}")
        logger.info(f"Respuesta: {response.text}")
        
        if response.status_code == 201:
            logger.info("¡Registro exitoso!")
            return True
        else:
            logger.error(f"Error en el registro: {response.text}")
            return False
    except Exception as e:
        logger.error(f"Excepción: {str(e)}")
        return False

if __name__ == "__main__":
    test_register_user()
