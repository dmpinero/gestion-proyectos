def clean_env_file():
    # Leer el contenido actual del archivo .env
    with open('.env', 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()
    
    # Eliminar el BOM y espacios en blanco al inicio de cada línea
    cleaned_lines = []
    for line in lines:
        # Eliminar el BOM (si existe) y espacios en blanco al inicio
        line = line.lstrip('\ufeff').lstrip()
        # Eliminar líneas vacías o comentarios sin valor
        if line and not line.startswith('#') and '=' in line:
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip()
            cleaned_lines.append(f"{key}={value}")
    
    # Escribir el contenido limpio de vuelta al archivo
    with open('.env', 'w', encoding='utf-8') as f:
        f.write('\n'.join(cleaned_lines) + '\n')

if __name__ == "__main__":
    clean_env_file()
    print("Archivo .env limpiado exitosamente.")
