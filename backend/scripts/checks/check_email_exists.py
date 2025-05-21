"""
Script para verificar si un email específico ya existe en la base de datos.
"""
import sys
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.models.user import User
from app.db.base import Base
from app.core.config import settings

def check_email_exists(email):
    """Verificar si un email ya existe en la base de datos."""
    # Crear conexión a la base de datos
    SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Crear sesión
    db = SessionLocal()
    
    try:
        print(f"[INFO] Verificando si el email '{email}' existe en la base de datos...")
        
        # Consultar la base de datos
        user = db.query(User).filter(User.email == email).first()
        
        if user:
            print(f"[ENCONTRADO] El email '{email}' está registrado:")
            print(f"  - ID: {user.id}")
            print(f"  - Nombre: {user.first_name} {user.last_name}")
            print(f"  - Activo: {user.is_active}")
            return True
        else:
            print(f"[NO ENCONTRADO] El email '{email}' NO está registrado en la base de datos.")
            return False
            
    except Exception as e:
        print(f"[ERROR] Error al verificar el email: {str(e)}")
        return None
    finally:
        db.close()

def list_all_users():
    """Listar todos los usuarios en la base de datos."""
    # Crear conexión a la base de datos
    SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Crear sesión
    db = SessionLocal()
    
    try:
        print("\n[INFO] Listando todos los usuarios en la base de datos:")
        
        # Consultar la base de datos
        users = db.query(User).all()
        
        if users:
            print(f"[INFO] Se encontraron {len(users)} usuarios:")
            for user in users:
                print(f"  - ID: {user.id}, Email: {user.email}, Nombre: {user.first_name} {user.last_name}")
        else:
            print("[INFO] No hay usuarios registrados en la base de datos.")
            
    except Exception as e:
        print(f"[ERROR] Error al listar usuarios: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        email = sys.argv[1]
        check_email_exists(email)
    else:
        print("[ERROR] Debe proporcionar un email como argumento.")
        print("Uso: python check_email_exists.py <email>")
        sys.exit(1)
    
    # Listar todos los usuarios
    list_all_users()
