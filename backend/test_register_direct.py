import requests
import json

# URL del endpoint de registro
url = "http://localhost:8000/api/v1/auth/register"

# Datos para el registro
data = {
    "email": "dmpinero@gmail.com",
    "firstName": "Daniel",
    "lastName": "Martinez Piñero",
    "password": "12345678"
}

# Encabezados de la solicitud
headers = {
    "Content-Type": "application/json"
}

# Realizar la solicitud POST
try:
    print(f"Enviando solicitud a {url}")
    print(f"Datos: {json.dumps(data)}")
    
    response = requests.post(url, json=data, headers=headers)
    
    print(f"Código de estado: {response.status_code}")
    print(f"Respuesta: {response.text}")
    
    # Si la respuesta es exitosa, mostrar el token
    if response.status_code == 201:
        response_data = response.json()
        print("Registro exitoso!")
        print(f"Token: {response_data.get('token')}")
    else:
        print(f"Error en el registro: {response.text}")
        
except Exception as e:
    print(f"Error al realizar la solicitud: {str(e)}")
