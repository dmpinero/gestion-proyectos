# Archivo de inicialización del paquete routers
from .auth import router as auth_router

# Asegúrate de importar aquí todos los routers que crees
__all__ = ["auth_router"]
