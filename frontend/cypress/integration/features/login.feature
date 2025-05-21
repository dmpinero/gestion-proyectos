# language: es
Característica: Inicio de sesión de usuarios
  Como usuario registrado
  Quiero poder iniciar sesión en la aplicación
  Para acceder a las funcionalidades exclusivas para usuarios autenticados

  Escenario: Mostrar formulario de login
    Dado que estoy en la página de login
    Entonces debería ver el formulario de inicio de sesión
    Y debería ver campos para email y contraseña
    Y debería ver un botón para iniciar sesión
    Y debería ver un enlace para registrarme

  Escenario: Validación de campos obligatorios
    Dado que estoy en la página de login
    Cuando intento enviar el formulario sin rellenar ningún campo
    Entonces debería ver errores de validación para los campos obligatorios

  Escenario: Validación de formato de correo electrónico
    Dado que estoy en la página de login
    Cuando relleno el campo de correo con un formato inválido
      | campo          | valor           |
      | email          | correo-invalido |
    Y hago clic en el botón "Iniciar Sesión"
    Entonces debería ver un error de validación para el formato de correo

  Escenario: Error con credenciales inválidas
    Dado que estoy en la página de login
    Cuando relleno el formulario con credenciales inválidas
      | campo          | valor                 |
      | email          | usuario@invalido.com  |
      | contraseña     | contraseñaincorrecta  |
    Y hago clic en el botón "Iniciar Sesión"
    Entonces debería ver un mensaje de error indicando credenciales inválidas

  Escenario: Inicio de sesión exitoso
    Dado que estoy en la página de login
    Cuando relleno el formulario con credenciales válidas
      | campo          | valor                 |
      | email          | usuario@ejemplo.com   |
      | contraseña     | Password123!          |
    Y hago clic en el botón "Iniciar Sesión"
    Entonces debería ser redirigido al dashboard

  Escenario: Redirección después del login
    Dado que intento acceder a una ruta protegida sin autenticación
    Y soy redirigido a la página de login
    Cuando inicio sesión con credenciales válidas
    Entonces debería ser redirigido a la ruta protegida original
