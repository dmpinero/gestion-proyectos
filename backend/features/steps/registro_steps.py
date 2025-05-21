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

# Cliente de prueba
client = TestClient(app)

def get_test_db():
    """Crea una nueva sesión de base de datos para pruebas."""
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

# Antecedentes
@given('que tengo un usuario registrado con email "([^"]*)"')
def step_impl(context, email):
    # Crear un usuario de prueba en la base de datos
    db = next(get_test_db())
    
    # Verificar si el usuario ya existe
    user = db.query(User).filter(User.email == email).first()
    if not user:
        # Crear el usuario si no existe
        user = User(
            email=email,
            first_name="Usuario",
            last_name="Ejemplo",
            hashed_password=get_password_hash("Password123!"),
            role="user",
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    context.user = user

# Pasos para "Cuando"
@when('envío una petición POST a "([^"]*)" con:')
def step_impl(context, url):
    # Obtener los datos de la tabla
    table = context.table
    headers = table.headings
    row = table[0]
    
    # Construir el cuerpo de la petición
    body = {}
    for header in headers:
        body[header] = row[header]
    
    # Realizar la petición
    response = client.post(f"{BASE_URL}{url}", json=body)
    
    # Guardar la respuesta en el contexto
    context.response = response
    context.response_json = response.json() if response.headers.get("content-type") == "application/json" else {}

# Pasos para "Entonces"
@then('la respuesta debe tener un código de estado (\d+)')
def step_impl(context, status_code):
    assert context.response.status_code == int(status_code), \
        f"Se esperaba un código de estado {status_code}, pero se recibió {context.response.status_code}"

@then('la respuesta debe contener un mensaje de éxito "([^"]*)"')
def step_impl(context, message):
    assert "message" in context.response_json, \
        f"La respuesta no contiene el campo 'message': {context.response_json}"
    assert context.response_json["message"] == message, \
        f"Se esperaba el mensaje '{message}', pero se recibió '{context.response_json.get('message')}'"

@then('la respuesta debe contener los datos del usuario registrado')
def step_impl(context):
    assert "user" in context.response_json, \
        f"La respuesta no contiene el campo 'user': {context.response_json}"
    
    user = context.response_json["user"]
    assert "id" in user, "El usuario no tiene ID"
    assert "email" in user, "El usuario no tiene email"
    assert "firstName" in user, "El usuario no tiene nombre"
    assert "lastName" in user, "El usuario no tiene apellido"
    assert "role" in user, "El usuario no tiene rol"
    
    # Verificar que no se devuelve la contraseña
    assert "password" not in user, "La respuesta contiene la contraseña del usuario"
    assert "hashed_password" not in user, "La respuesta contiene el hash de la contraseña"

@then('la respuesta debe contener el mensaje de error "([^"]*)"')
def step_impl(context, message):
    assert "error" in context.response_json, \
        f"La respuesta no contiene el campo 'error': {context.response_json}"
    assert "message" in context.response_json, \
        f"La respuesta no contiene el campo 'message': {context.response_json}"
    assert context.response_json["message"] == message, \
        f"Se esperaba el mensaje '{message}', pero se recibió '{context.response_json.get('message')}'"

@then('la respuesta debe indicar que faltan campos obligatorios')
def step_impl(context):
    assert context.response.status_code == 422, \
        f"Se esperaba un código de estado 422, pero se recibió {context.response.status_code}"
    
    assert "detail" in context.response_json, \
        f"La respuesta no contiene el campo 'detail': {context.response_json}"
    
    # Verificar que hay al menos un error de validación
    detail = context.response_json["detail"]
    assert isinstance(detail, list), "El campo 'detail' no es una lista"
    assert len(detail) > 0, "No hay errores de validación en la respuesta"
    
    # Verificar que los errores son de campos requeridos
    for error in detail:
        assert "msg" in error, f"El error no contiene el campo 'msg': {error}"
        assert "field required" in error["msg"], \
            f"Se esperaba un mensaje de campo requerido, pero se recibió '{error['msg']}'"
