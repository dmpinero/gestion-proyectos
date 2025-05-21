# language: es
Característica: Registro de usuarios
  Como usuario no registrado
  Quiero poder crear una cuenta en la aplicación
  Para poder acceder a las funcionalidades exclusivas para usuarios registrados

  Escenario: Mostrar formulario de registro
    Dado que estoy en la página de login
    Cuando hago clic en el enlace "Regístrate"
    Entonces debería ver el formulario de registro
    Y debería ver campos para nombre, apellidos, email, contraseña y confirmación de contraseña
    Y debería ver un selector de rol
    Y debería ver una casilla para aceptar los términos y condiciones

  Escenario: Validación de campos obligatorios
    Dado que estoy en el formulario de registro
    Cuando intento enviar el formulario sin rellenar ningún campo
    Entonces debería ver errores de validación para los campos obligatorios

  Escenario: Validación de contraseñas coincidentes
    Dado que estoy en el formulario de registro
    Cuando relleno el formulario con contraseñas diferentes
      | campo          | valor                 |
      | nombre         | Juan                  |
      | apellidos      | Pérez                 |
      | email          | juan.perez@example.com|
      | contraseña     | Password123!          |
      | confirmación   | OtraContraseña123!    |
    Y hago clic en el botón "Crear cuenta"
    Entonces debería ver un mensaje de error indicando que las contraseñas no coinciden

  Escenario: Registro exitoso
    Dado que estoy en el formulario de registro
    Cuando relleno el formulario con datos válidos
      | campo          | valor                 |
      | nombre         | Juan                  |
      | apellidos      | Pérez                 |
      | email          | juan.perez@example.com|
      | contraseña     | Password123!          |
      | confirmación   | Password123!          |
      | rol            | user                  |
    Y acepto los términos y condiciones
    Y hago clic en el botón "Crear cuenta"
    Entonces debería ver un mensaje de éxito
    Y debería ser redirigido a la página de login

  Escenario: Error de correo electrónico ya registrado
    Dado que estoy en el formulario de registro
    Cuando relleno el formulario con un correo electrónico ya registrado
    Y hago clic en el botón "Crear cuenta"
    Entonces debería ver un mensaje de error indicando que el correo ya está registrado
