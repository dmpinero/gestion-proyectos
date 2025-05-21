from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Any, Dict
import logging
import traceback

from app.core.security import get_password_hash, create_access_token, verify_password
from app.db.base import get_db
from app.models.user import User
from app.schemas.token import Token, UserLogin, UserCreate, UserResponse
from datetime import timedelta
from app.core.config import settings

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/register", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
) -> Any:
    """
    Registra un nuevo usuario en el sistema.
    """
    logger.info(f"Intento de registro para el email: {user_data.email}")
    
    try:
        # Verificar si el email ya está registrado (primero con SQLAlchemy por simplicidad)
        logger.info(f"Verificando si el email ya existe: {user_data.email}")
        
        # Imprimir información sobre la sesión de base de datos
        logger.info(f"Información de la sesión de BD: {db.bind.url}")
        
        # Verificar primero con SQLAlchemy (más simple y menos propenso a errores)
        try:
            # Verificar si el email existe (case insensitive para mayor seguridad)
            existing_user = db.query(User).filter(User.email.ilike(user_data.email)).first()
            
            if existing_user:
                logger.warning(f"Intento de registro con email ya existente: {user_data.email} (ID: {existing_user.id})")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El email ya está registrado"
                )
            else:
                logger.info(f"Email {user_data.email} disponible para registro")
                
                # Listar algunos usuarios para verificación (limitado a 5 para no sobrecargar los logs)
                all_users = db.query(User.id, User.email).limit(5).all()
                logger.info(f"Muestra de usuarios existentes: {all_users}")
                
                # Contar usuarios totales
                user_count = db.query(User).count()
                logger.info(f"Total de usuarios en la base de datos: {user_count}")
        except HTTPException:
            # Re-lanzar excepciones HTTP para mantener el código de estado y el mensaje
            raise
        except Exception as e:
            logger.error(f"Error al verificar si el email existe con SQLAlchemy: {str(e)}")
            logger.error(traceback.format_exc())
            
            # Intentar con conexión directa a MySQL como respaldo
            try:
                import pymysql
                from app.core.config import settings
                
                logger.info("Intentando verificación directa con MySQL como respaldo")
                
                # Conectar directamente a MySQL
                conn = pymysql.connect(
                    host=settings.DATABASE_HOST,
                    port=int(settings.DATABASE_PORT),
                    user=settings.DATABASE_USER,
                    password=settings.DATABASE_PASSWORD,
                    database=settings.DATABASE_NAME,
                    connect_timeout=5  # Timeout de conexión de 5 segundos
                )
                
                # Verificar si el email existe (case insensitive)
                with conn.cursor() as cursor:
                    cursor.execute("SELECT id, email FROM users WHERE LOWER(email) = LOWER(%s)", (user_data.email,))
                    existing_user_data = cursor.fetchone()
                    
                    if existing_user_data:
                        logger.warning(f"Intento de registro con email ya existente (MySQL): {user_data.email} (ID: {existing_user_data[0]})")
                        conn.close()
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="El email ya está registrado"
                        )
                    else:
                        logger.info(f"Email {user_data.email} disponible para registro (MySQL)")
                
                conn.close()
            except HTTPException:
                # Re-lanzar excepciones HTTP
                raise
            except Exception as inner_e:
                logger.error(f"Error en la verificación directa con MySQL: {str(inner_e)}")
                logger.error(traceback.format_exc())
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error al verificar si el email ya está registrado"
                )
        
        # Generar hash de la contraseña
        hashed_password = get_password_hash(user_data.password)
        logger.debug(f"Hash de contraseña generado para el usuario: {user_data.email}")
        
        # Crear el usuario
        new_user = User(
            email=user_data.email,
            first_name=user_data.firstName if user_data.firstName else "",
            last_name=user_data.lastName if user_data.lastName else "",
            hashed_password=hashed_password,
            is_active=True,
        )
        
        # Guardar en la base de datos
        logger.info(f"Guardando nuevo usuario en la base de datos: {user_data.email}")
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        # Verificar que el usuario se haya guardado correctamente
        saved_user = db.query(User).filter(User.email == user_data.email).first()
        if not saved_user:
            logger.error(f"Error: El usuario {user_data.email} no se guardó correctamente en la base de datos")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al guardar el usuario en la base de datos"
            )
        
        logger.info(f"Usuario registrado exitosamente: {user_data.email} (ID: {new_user.id})")
        
        # Crear token de acceso
        from app.core.config import settings  # Importar settings aquí para asegurar que esté disponible
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            subject=new_user.email,
            expires_delta=access_token_expires
        )
    except HTTPException as e:
        # Re-lanzar excepciones HTTP para que FastAPI las maneje correctamente
        raise e
    except Exception as e:
        # Capturar y registrar cualquier otra excepción
        error_msg = f"Error inesperado al registrar usuario: {str(e)}"
        logger.error(error_msg)
        logger.error(traceback.format_exc())
        db.rollback()  # Revertir la transacción en caso de error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al registrar el usuario"
        )
    
    # Devolver datos del usuario y token
    return {
        "user": {
            "id": new_user.id,
            "email": new_user.email,
            "firstName": new_user.first_name,
            "lastName": new_user.last_name,
            "isActive": new_user.is_active,
        },
        "token": access_token,
        "token_type": "bearer"
    }

@router.post("/login", response_model=Token)
def login_for_access_token(
    form_data: UserLogin,
    db: Session = Depends(get_db)
) -> Any:
    """
    Inicia sesión y devuelve un token de acceso.
    """
    logger.info(f"Intento de inicio de sesión para el email: {form_data.email}")
    
    try:
        # Buscar el usuario por email
        user = db.query(User).filter(User.email == form_data.email).first()
        
        if not user:
            logger.warning(f"Intento de inicio de sesión con email no registrado: {form_data.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Verificar si la contraseña es correcta
        if not verify_password(form_data.password, user.hashed_password):
            logger.warning(f"Contraseña incorrecta para el usuario: {form_data.email}")
            logger.debug(f"Contraseña proporcionada: {form_data.password} (longitud: {len(form_data.password)})")
            logger.debug(f"Hash almacenado: {user.hashed_password[:10]}... (truncado)")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Verificar si el usuario está activo
        if not user.is_active:
            logger.warning(f"Intento de inicio de sesión con usuario inactivo: {form_data.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuario inactivo"
            )
        
        logger.info(f"Inicio de sesión exitoso para el usuario: {form_data.email} (ID: {user.id})")
        
        # Crear y devolver el token de acceso
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            subject=user.email, 
            expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "firstName": user.first_name,
                "lastName": user.last_name,
                "isActive": user.is_active
            }
        }
    except HTTPException as e:
        # Re-lanzar excepciones HTTP para que FastAPI las maneje correctamente
        raise e
    except Exception as e:
        # Capturar y registrar cualquier otra excepción
        error_msg = f"Error inesperado al iniciar sesión: {str(e)}"
        logger.error(error_msg)
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al iniciar sesión"
        )

# Versión compatible con OAuth2 para Swagger UI
@router.post("/login/access-token", response_model=Token)
def login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> Any:
    """
    Inicio de sesión OAuth2 compatible (para la documentación de Swagger UI).
    """
    # Buscar el usuario por email
    user = db.query(User).filter(User.email == form_data.username).first()
    
    # Verificar si el usuario existe y la contraseña es correcta
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verificar si el usuario está activo
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo"
        )
    
    # Crear y devolver el token de acceso
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.email, 
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
