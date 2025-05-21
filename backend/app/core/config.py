from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

class Settings(BaseSettings):
    # Configuración de la aplicación
    APP_NAME: str = "Gestión de Proyectos"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    
    # Configuración de la API
    API_V1_STR: str = "/api/v1"
    
    # Configuración de la base de datos
    # Usamos la IP del gateway de WSL para conectar a MySQL en Windows
    DATABASE_HOST: str = "172.18.96.1"
    DATABASE_PORT: str = "3306"
    DATABASE_USER: str = "gestion_app"  # Usuario específico para la aplicación
    DATABASE_PASSWORD: str = "DMP73noesilva"
    DATABASE_NAME: str = "gestion_proyectos"
    DATABASE_URL: str = f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}?charset=utf8mb4"
    
    # Configuración de autenticación
    SECRET_KEY: str = "clave_secreta_por_defecto_cambiar_en_produccion"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Configuración de CORS
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8000"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
