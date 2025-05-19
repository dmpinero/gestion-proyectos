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
    full_name: Optional[str] = None
    is_active: Optional[bool] = True

class UserCreate(UserBase):
    """Esquema para la creación de usuarios."""
    password: str

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

class UserLogin(BaseModel):
    """Esquema para el inicio de sesión de usuarios."""
    email: EmailStr
    password: str
