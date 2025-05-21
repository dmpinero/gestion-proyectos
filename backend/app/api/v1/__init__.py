"""
Módulo para la versión 1 de la API.
"""

from fastapi import APIRouter

# Crear el router principal para la API v1
router = APIRouter(prefix="/v1", tags=["v1"])

# Importar los endpoints
from .endpoints import auth  # noqa

# Incluir los routers de los endpoints
router.include_router(auth.router)
