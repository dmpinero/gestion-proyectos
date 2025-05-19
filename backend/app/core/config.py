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
    
    # Configuración de la base de datos
    DATABASE_URL: str = "sqlite:///./gestion_proyectos.db"
    
    # Configuración de autenticación
    SECRET_KEY: str
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
