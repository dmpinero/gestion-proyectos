"""
Script para verificar la configuración real de la base de datos que está usando la aplicación.
"""
import os
from app.core.config import settings
import inspect

def check_actual_db():
    """Verificar la configuración real de la base de datos."""
    try:
        # Mostrar la URL de conexión actual
        db_url = settings.DATABASE_URL
        print(f"[INFO] URL de conexión a la base de datos actual: {db_url}")
        
        # Verificar si es MySQL o SQLite
        if 'sqlite' in db_url.lower():
            print("[ALERTA] La aplicación está configurada para usar SQLite, no MySQL.")
        elif 'mysql' in db_url.lower():
            print("[INFO] La aplicación está configurada para usar MySQL correctamente.")
        else:
            print(f"[INFO] La aplicación está usando otro tipo de base de datos: {db_url.split('://')[0]}")
        
        # Verificar variables de entorno
        print("\n[INFO] Variables de entorno relacionadas con la base de datos:")
        for env_var in os.environ:
            if 'DB' in env_var.upper() or 'DATABASE' in env_var.upper() or 'SQL' in env_var.upper():
                print(f"  - {env_var}: {os.environ[env_var]}")
        
        # Verificar la configuración real de settings
        print("\n[INFO] Valores actuales en el objeto settings:")
        for attr_name in dir(settings):
            if not attr_name.startswith('__') and not callable(getattr(settings, attr_name)):
                attr_value = getattr(settings, attr_name)
                if isinstance(attr_value, str) and ('password' in attr_name.lower() or 'secret' in attr_name.lower()):
                    print(f"  - {attr_name}: ********")
                else:
                    print(f"  - {attr_name}: {attr_value}")
        
    except Exception as e:
        print(f"[ERROR] Error al verificar la configuración: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_actual_db()
