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
        full_name="Test User",
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
        json={"email": "nonexistent@example.com", "password": "testpassword"},
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Credenciales incorrectas"
