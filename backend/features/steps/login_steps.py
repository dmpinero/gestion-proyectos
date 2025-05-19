# -*- coding: utf-8 -*-
from behave import given, when, then, use_step_matcher
from sqlalchemy.orm import Session
import sys
from pathlib import Path
import json
from fastapi.testclient import TestClient

# Añadir el directorio raíz al path para poder importar los módulos
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from app.db.base import Base, engine, get_db
from app.models.user import User
from app.core.security import get_password_hash
from main import app

# Configuración de la base de datos de prueba
Base.metadata.create_all(bind=engine)

def get_db_override():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

# Configuración del cliente de prueba
app.dependency_overrides[get_db] = get_db_override

# Configuración de la URL base
BASE_URL = "/api/v1/auth"

# Usar el matcher de pasos de expresiones regulares
use_step_matcher("re")

# Datos de prueba
TEST_USER_EMAIL = "usuario@ejemplo.com"
TEST_USER_PASSWORD = "micontrasena"

def get_test_db():
    """Crea una nueva sesión de base de datos para pruebas."""
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

# Antecedentes
@given('que tengo un usuario registrado con email "{email}" y contraseña "{password}"')
def step_impl(context, email, password):
    # Crear un usuario de prueba en la base de datos
    db = Session(engine)
    try:
        # Verificar si el usuario ya existe
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            # Actualizar el usuario existente
            existing_user.hashed_password = get_password_hash(password)
            existing_user.is_active = True
        else:
            # Crear un nuevo usuario
            user = User(
                email=email,
                hashed_password=get_password_hash(password),
                full_name="Usuario de Prueba",
                is_active=True
            )
            db.add(user)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

# Pasos para "Cuando"
@when('envío una petición POST a "{url}" con')
def step_impl(context, url):
    # Obtener los datos de la tabla
    data = {}
    for row in context.table.rows:
        # Usar las cabeceras de la tabla como claves
        for heading in row.headings:
            if row[heading]:  # Solo agregar si el valor no está vacío
                data[heading] = row[heading]
    
    # Asegurarse de que la URL comience con la ruta base
    if not url.startswith(BASE_URL):
        url = f"{BASE_URL}{url}"
    
    # Realizar la petición
    context.response = context.client.post(
        url,
        json=data,
        headers={"Content-Type": "application/json"}
    )

# Pasos para "Entonces"
@then('la respuesta debe tener un código de estado {status_code}')
def step_impl(context, status_code):
    expected_status = int(status_code)
    assert context.response.status_code == expected_status, \
        f"Se esperaba el código de estado {status_code} pero se obtuvo {context.response.status_code}. " \
        f"Respuesta: {context.response.text}"

@then('la respuesta debe contener un token de acceso')
def step_impl(context):
    data = context.response.json()
    assert "access_token" in data, f"No se encontró access_token en la respuesta: {data}"
    assert data.get("token_type") == "bearer", f"Tipo de token incorrecto: {data.get('token_type')}"

@then('la respuesta debe contener el mensaje de error "{message}"')
def step_impl(context, message):
    data = context.response.json()
    assert "detail" in data, f"No se encontró 'detail' en la respuesta: {data}"
    
    # Manejar tanto cadenas como listas de errores
    if isinstance(data["detail"], list):
        error_messages = [str(error.get('msg', '')) for error in data["detail"]]
        assert any(message in msg for msg in error_messages), \
            f"No se encontró el mensaje '{message}' en los errores: {error_messages}"
    else:
        assert message in str(data["detail"]), \
            f"No se encontró el mensaje '{message}' en: {data['detail']}"

@then('la respuesta debe indicar que el campo contraseña es requerido')
def step_impl(context):
    data = context.response.json()
    assert "detail" in data, f"No se encontró 'detail' en la respuesta: {data}"
    
    if isinstance(data["detail"], list):
        errors = [str(error.get('msg', '')) for error in data["detail"]]
        assert any("field required" in error.lower() for error in errors), \
            f"No se encontró el error de campo requerido en: {errors}"
    else:
        assert "field required" in str(data["detail"]).lower(), \
            f"No se encontró el error de campo requerido en: {data['detail']}"
