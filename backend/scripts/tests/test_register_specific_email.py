"""
Script para probar el registro de un email específico y verificar si ya existe en la base de datos.
"""
import requests
import json
import sys

def test_register_email(email, first_name, last_name, password):
    """Probar el registro de un email específico."""
    url = "http://localhost:8000/api/v1/auth/register"
    
    # Datos para el registro
    data = {
        "email": email,
        "firstName": first_name,
        "lastName": last_name,
        "password": password
    }
    
    print(f"Intentando registrar el email: {email}")
    print(f"Datos: {json.dumps(data)}")
    
    # Enviar solicitud
    try:
        # Añadir encabezados para evitar el error de host inválido
        headers = {
            'Host': 'localhost:8000',
            'Origin': 'http://localhost:8000',
            'Referer': 'http://localhost:8000/'
        }
        response = requests.post(url, json=data, headers=headers)
        
        # Mostrar información de la respuesta
        print(f"Código de estado: {response.status_code}")
        print(f"Respuesta: {response.text}")
        
        if response.status_code == 201:
            print("Registro exitoso!")
            return True
        else:
            print(f"Error en el registro: {response.text}")
            return False
    except Exception as e:
        print(f"Error al enviar solicitud: {e}")
        return False

if __name__ == "__main__":
    email = "dmpinero@gmail.com"
    first_name = "Daniel"
    last_name = "Martinez"
    password = "password123"
    
    if len(sys.argv) > 1:
        email = sys.argv[1]
    if len(sys.argv) > 2:
        first_name = sys.argv[2]
    if len(sys.argv) > 3:
        last_name = sys.argv[3]
    if len(sys.argv) > 4:
        password = sys.argv[4]
    
    success = test_register_email(email, first_name, last_name, password)
    sys.exit(0 if success else 1)
