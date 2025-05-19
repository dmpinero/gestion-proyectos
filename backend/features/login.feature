# language: es
# encoding: utf-8

Característica: Autenticación de usuarios
  Como usuario del sistema
  Quiero poder iniciar sesión
  Para acceder a las funcionalidades restringidas

  Antecedentes:
    Dado que tengo un usuario registrado con email "usuario@ejemplo.com" y contraseña "micontrasena"

  Escenario: Inicio de sesión exitoso
    Cuando envío una petición POST a "/login" con:
      | email             | password     |
      | usuario@ejemplo.com | micontrasena |
    Entonces la respuesta debe tener un código de estado 200
    Y la respuesta debe contener un token de acceso

  Escenario: Inicio de sesión con credenciales incorrectas
    Cuando envío una petición POST a "/login" con:
      | email             | password       |
      | usuario@ejemplo.com | contrasenaincorrecta |
    Entonces la respuesta debe tener un código de estado 401
    Y la respuesta debe contener el mensaje de error "Credenciales incorrectas"

  Escenario: Intento de inicio de sesión sin contraseña
    Cuando envío una petición POST a "/login" con:
      | email             |
      | usuario@ejemplo.com |
    Entonces la respuesta debe tener un código de estado 422
    Y la respuesta debe indicar que el campo contraseña es requerido
