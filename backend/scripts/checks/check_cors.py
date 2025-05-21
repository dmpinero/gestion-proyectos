import os
import re

def main():
    # Verificar si el archivo .env existe, si no, copiar de .env.example
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            with open('.env.example', 'r') as src, open('.env', 'w') as dst:
                dst.write(src.read())
            print("Archivo .env creado a partir de .env.example")
        else:
            print("Error: No se encontró el archivo .env.example")
            return

    # Leer el archivo .env
    with open('.env', 'r') as f:
        env_content = f.read()

    # Buscar la línea CORS_ORIGINS
    cors_match = re.search(r'^CORS_ORIGINS=([^\n]*)', env_content, re.MULTILINE)
    
    if cors_match:
        cors_origins = cors_match.group(1).strip('\"\'')
        print(f"CORS_ORIGINS actual: {cors_origins}")
        
        # Verificar si incluye localhost:3000
        if 'localhost:3000' not in cors_origins:
            print("Añadiendo localhost:3000 a CORS_ORIGINS...")
            new_cors_line = f"CORS_ORIGINS={cors_origins},http://localhost:3000"
            new_env_content = re.sub(
                r'^CORS_ORIGINS=.*$',
                new_cors_line,
                env_content,
                flags=re.MULTILINE
            )
            with open('.env', 'w') as f:
                f.write(new_env_content)
            print("CORS_ORIGINS actualizado correctamente")
        else:
            print("CORS_ORIGINS ya incluye localhost:3000")
    else:
        print("No se encontró la variable CORS_ORIGINS en .env")
        with open('.env', 'a') as f:
            f.write("\n# Configuración de CORS (orígenes permitidos separados por comas)\n")
            f.write("CORS_ORIGINS=http://localhost:3000\n")
        print("Variable CORS_ORIGINS añadida a .env")

    # Mostrar la configuración actual
    print("\nConfiguración actual de CORS:")
    with open('.env', 'r') as f:
        for line in f:
            if 'CORS_' in line:
                print(line.strip())

if __name__ == "__main__":
    main()
