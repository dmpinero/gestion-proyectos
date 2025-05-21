from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.config import settings
from app.db.base import Base, engine

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    description="API para la gestión de proyectos y tareas",
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuración de CORS - Simplificada para desarrollo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir cualquier origen en desarrollo
    allow_credentials=False,  # Deshabilitar credenciales para evitar conflictos
    allow_methods=["*"],  # Permitir todos los métodos
    allow_headers=["*"],  # Permitir todos los encabezados
)

# Middleware para manejar las solicitudes OPTIONS (preflight)
@app.middleware("http")
async def options_middleware(request: Request, call_next):
    if request.method == "OPTIONS":
        # Responder directamente a las solicitudes OPTIONS
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Requested-With, Accept",
            "Access-Control-Max-Age": "86400",  # 24 horas
        }
        return JSONResponse(content={}, status_code=200, headers=headers)
    
    # Para otras solicitudes, continuar con el flujo normal
    response = await call_next(request)
    
    # Asegurarse de que siempre se envíen los encabezados CORS
    response.headers["Access-Control-Allow-Origin"] = "*"
    
    return response

# En desarrollo, no utilizamos verificación de host
# Esto permite que cualquier host pueda acceder a la API
# Montar archivos estáticos (para documentación, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    """
    Ruta raíz de la API.
    Devuelve un mensaje de bienvenida e información básica de la API.
    """
    return {
        "message": f"¡Bienvenido a {settings.APP_NAME}!",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "redoc": "/redoc"
    }

# Importar el router principal de la API
from app.api import api_router
from app.core.config import settings

# Incluir el router principal de la API
app.include_router(api_router)

# Importar otros routers (descomentar cuando estén listos)
# from app.api.routers import proyectos, tareas, usuarios
# app.include_router(proyectos.router, prefix=f"{settings.API_V1_STR}/proyectos", tags=["proyectos"])
# app.include_router(tareas.router, prefix=f"{settings.API_V1_STR}/tareas", tags=["tareas"])
# app.include_router(usuarios.router, prefix=f"{settings.API_V1_STR}/usuarios", tags=["usuarios"])

# Manejador de errores global

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail if hasattr(exc, 'detail') else str(exc)}
    )

@app.exception_handler(404)
async def not_found_exception_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": "Recurso no encontrado"}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body}
    )

# Ejecutar la aplicación con uvicorn directamente
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
