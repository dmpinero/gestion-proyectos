"""
Script para probar el inicio de sesión con un usuario existente.
"""
import requests
import json
import sys

def test_login_api(email, password):
    """Probar el endpoint de login directamente."""
    url = "http://localhost:8000/api/v1/auth/login"
    
    # Datos para el login
    data = {
        "email": email,
        "password": password
    }
    
    print(f"Intentando iniciar sesión con: {email}")
    print(f"Datos: {json.dumps(data)}")
    
    # Enviar solicitud
    try:
        response = requests.post(url, json=data)
        
        # Mostrar información de la respuesta
        print(f"Código de estado: {response.status_code}")
        print(f"Respuesta: {response.text}")
        
        if response.status_code == 200:
            print("Inicio de sesión exitoso!")
            return True
        else:
            print(f"Error en el inicio de sesión: {response.text}")
            return False
    except Exception as e:
        print(f"Error al enviar solicitud: {e}")
        return False

if __name__ == "__main__":
    email = "nuevo_usuario_test@example.com"
    password = "password123"
    
    if len(sys.argv) > 1:
        email = sys.argv[1]
    if len(sys.argv) > 2:
        password = sys.argv[2]
    
    success = test_login_api(email, password)
    sys.exit(0 if success else 1)
