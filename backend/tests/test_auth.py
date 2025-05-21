import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.db.base import Base, engine, SessionLocal
from app.models.user import User
from app.core.security import get_password_hash
from main import app

# Configurar la base de datos de prueba
@pytest.fixture(scope="module")
def test_db():
    # Crear todas las tablas
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # Crear un usuario de prueba
    hashed_password = get_password_hash("testpassword")
    user = User(
        email="test@example.com",
        hashed_password=hashed_password,
        first_name="Test",
        last_name="User",
        is_active=True
    )
    db.add(user)
    db.commit()
    
    yield db
    
    # Limpiar después de las pruebas
    db.query(User).delete()
    db.commit()
    db.close()
    
    # Eliminar tablas
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        yield test_client

def test_login_success(client, test_db):
    """Prueba el inicio de sesión exitoso."""
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "testpassword"},
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password(client, test_db):
    """Prueba el inicio de sesión con contraseña incorrecta."""
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "wrongpassword"},
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Credenciales incorrectas"

def test_login_nonexistent_user(client, test_db):
    """Prueba el inicio de sesión con un usuario que no existe."""
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "nonexistent@example.com", "password": "wrongpassword"},
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Incorrect email or password"

def test_register_user(client, test_db):
    """Prueba el registro de un nuevo usuario."""
    # Datos para el nuevo usuario
    new_user_data = {
        "email": "newuser@example.com",
        "firstName": "New",
        "lastName": "User",
        "password": "securepassword123"
    }
    
    # Enviar solicitud de registro
    response = client.post(
        "/api/v1/auth/register",
        json=new_user_data,
        headers={"Content-Type": "application/json"}
    )
    
    # Verificar respuesta
    assert response.status_code == 201, f"Error en el registro: {response.text}"
    data = response.json()
    assert "token" in data
    assert data["token_type"] == "bearer"
    
    # Verificar que el usuario se haya creado en la base de datos
    user = test_db.query(User).filter(User.email == new_user_data["email"]).first()
    assert user is not None
    assert user.email == new_user_data["email"]
    assert user.first_name == new_user_data["firstName"]
    assert user.last_name == new_user_data["lastName"]
    
    # Limpiar: eliminar el usuario creado para esta prueba
    test_db.delete(user)
    test_db.commit()
