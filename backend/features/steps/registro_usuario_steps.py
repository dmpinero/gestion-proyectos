from behave import given, when, then
import json
import requests
from hamcrest import assert_that, equal_to, has_key, contains_string

# URL base para las pruebas
BASE_URL = "http://localhost:8000"

@given('el sistema está preparado para registrar usuarios')
def step_impl(context):
    # Configuración inicial para las pruebas
    context.headers = {
        "Content-Type": "application/json"
    }
    context.api_url = f"{BASE_URL}/api/auth/register"

@given('ya existe un usuario con email "{email}"')
def step_impl(context, email):
    # Simular que ya existe un usuario con ese email
    context.existing_email = email
    
    # Configurar el interceptor para simular que el email ya está en uso
    context.email_already_exists = True

@when('el usuario envía sus datos de registro con')
def step_impl(context):
    # Extraer datos de la tabla
    row = context.table[0]
    context.request_data = {
        "firstName": row["firstName"],
        "lastName": row["lastName"],
        "email": row["email"],
        "password": row["password"]
    }
    
    # Enviar solicitud POST al endpoint de registro
    context.response = requests.post(
        context.api_url,
        headers=context.headers,
        data=json.dumps(context.request_data)
    )
    
    # Guardar la respuesta JSON para verificaciones posteriores
    try:
        context.response_json = context.response.json()
    except json.JSONDecodeError:
        context.response_json = {}

@when('el usuario envía sus datos de registro sin el campo "{field}"')
def step_impl(context, field):
    # Extraer datos de la tabla
    row = context.table[0]
    context.request_data = {}
    
    # Añadir todos los campos excepto el especificado
    for key in row.headings:
        if key != field:
            context.request_data[key] = row[key]
    
    # Enviar solicitud POST al endpoint de registro
    context.response = requests.post(
        context.api_url,
        headers=context.headers,
        data=json.dumps(context.request_data)
    )
    
    # Guardar la respuesta JSON para verificaciones posteriores
    try:
        context.response_json = context.response.json()
    except json.JSONDecodeError:
        context.response_json = {}

@then('el sistema debe crear el usuario en la base de datos')
def step_impl(context):
    # Verificar que la respuesta indica que el usuario se ha creado correctamente
    assert context.response.status_code == 201, \
        f"Se esperaba un código de estado 201, pero se recibió {context.response.status_code}"
    
    # Verificar que la respuesta contiene los datos del usuario
    assert "user" in context.response_json, "La respuesta no contiene los datos del usuario"
    user_data = context.response_json["user"]
    
    # Verificar que los datos del usuario coinciden con los enviados
    assert user_data["email"] == context.request_data["email"], "El email del usuario no coincide"
    assert user_data["firstName"] == context.request_data["firstName"], "El nombre del usuario no coincide"
    assert user_data["lastName"] == context.request_data["lastName"], "El apellido del usuario no coincide"

@then('la respuesta debe incluir un token de autenticación')
def step_impl(context):
    assert_that(context.response_json, has_key("token"))
    assert context.response_json["token"] is not None, "El token de autenticación es nulo"
    assert len(context.response_json["token"]) > 0, "El token de autenticación está vacío"

@then('la respuesta debe incluir los datos del usuario creado')
def step_impl(context):
    assert_that(context.response_json, has_key("user"))
    user_data = context.response_json["user"]
    
    assert_that(user_data, has_key("id"))
    assert_that(user_data, has_key("email"))
    assert_that(user_data, has_key("firstName"))
    assert_that(user_data, has_key("lastName"))
    assert_that(user_data, has_key("role"))
    
    assert user_data["email"] == context.request_data["email"], f"El email del usuario no coincide"
    assert user_data["firstName"] == context.request_data["firstName"], f"El nombre del usuario no coincide"
    assert user_data["lastName"] == context.request_data["lastName"], f"El apellido del usuario no coincide"

@then('el código de respuesta debe ser {status_code:d}')
def step_impl(context, status_code):
    assert_that(context.response.status_code, equal_to(status_code))

@then('la respuesta debe indicar que el email ya está en uso')
def step_impl(context):
    assert_that(context.response.status_code, equal_to(400))
    assert_that(context.response_json, has_key("detail"))
    assert_that(context.response_json["detail"], contains_string("Email already registered"))

@then('la respuesta debe indicar que la contraseña es débil')
def step_impl(context):
    assert_that(context.response.status_code, equal_to(400))
    assert_that(context.response_json, has_key("detail"))
    assert_that(context.response_json["detail"], contains_string("Password too weak"))
