import subprocess
import json
import sys

def test_register_with_curl():
    """
    Prueba el endpoint de registro usando curl directamente para evitar problemas de host
    """
    # Datos para el registro
    data = {
        "email": "dmpinero@gmail.com",
        "firstName": "Daniel",
        "lastName": "Martinez Piñero",
        "password": "12345678"
    }
    
    # Convertir a JSON
    json_data = json.dumps(data)
    
    # Comando curl
    curl_command = [
        'curl',
        '-X', 'POST',
        'http://localhost:8000/api/v1/auth/register',
        '-H', 'Content-Type: application/json',
        '-H', 'Accept: application/json',
        '-d', json_data,
        '-v'  # Modo verbose para ver los encabezados
    ]
    
    print(f"Ejecutando comando: {' '.join(curl_command)}")
    
    try:
        # Ejecutar curl y capturar la salida
        result = subprocess.run(
            curl_command, 
            capture_output=True, 
            text=True
        )
        
        print("\n--- SALIDA ESTÁNDAR ---")
        print(result.stdout)
        
        print("\n--- SALIDA DE ERROR ---")
        print(result.stderr)
        
        print(f"\nCódigo de salida: {result.returncode}")
        
        return result.returncode == 0
    except Exception as e:
        print(f"Error al ejecutar curl: {str(e)}")
        return False

if __name__ == "__main__":
    # Verificar si curl está disponible
    try:
        subprocess.run(['curl', '--version'], capture_output=True, check=True)
    except (subprocess.SubprocessError, FileNotFoundError):
        print("Error: curl no está instalado o no está disponible en el PATH")
        sys.exit(1)
    
    # Ejecutar la prueba
    success = test_register_with_curl()
    
    if success:
        print("\n¡Prueba completada con éxito!")
    else:
        print("\nLa prueba falló. Revisa los mensajes de error para más detalles.")
