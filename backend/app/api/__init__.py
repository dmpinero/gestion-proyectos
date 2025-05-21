"""
Paquete principal de la API.
"""

from fastapi import APIRouter

# Crear el router principal de la API
api_router = APIRouter()

# Importar la versión 1 de la API
from .v1 import router as v1_router

# Incluir el router de la versión 1
api_router.include_router(v1_router, prefix="/api")
