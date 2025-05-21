from pydantic import BaseModel, EmailStr
from typing import Optional

class Token(BaseModel):
    """Esquema para el token de acceso."""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Esquema para los datos del token."""
    email: Optional[str] = None

class UserBase(BaseModel):
    """Esquema base para usuarios."""
    email: EmailStr
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    is_active: Optional[bool] = True

class UserCreate(UserBase):
    """Esquema para la creación de usuarios."""
    password: str
    
    class Config:
        schema_extra = {
            "example": {
                "email": "usuario@example.com",
                "firstName": "Usuario",
                "lastName": "Prueba",
                "password": "Contraseña123!"
            }
        }

class UserInDBBase(UserBase):
    """Esquema base para usuarios en la base de datos."""
    id: Optional[int] = None
    is_superuser: bool = False

    class Config:
        from_attributes = True

class User(UserInDBBase):
    """Esquema para la respuesta de usuarios."""
    pass

class UserInDB(UserInDBBase):
    """Esquema para usuarios en la base de datos con contraseña."""
    hashed_password: str

class UserResponse(BaseModel):
    """Esquema para la respuesta de usuarios."""
    id: int
    email: EmailStr
    firstName: str
    lastName: str
    isActive: bool
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    """Esquema para el inicio de sesión de usuarios."""
    email: EmailStr
    password: str
