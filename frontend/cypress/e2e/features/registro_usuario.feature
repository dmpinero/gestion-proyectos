Feature: Registro de usuario en la interfaz
  Como usuario no registrado
  Quiero poder crear una cuenta a través de la interfaz
  Para poder acceder a las funcionalidades de la aplicación

  Background:
    Given el usuario está en la página de login

  Scenario: Registro exitoso y redirección
    When el usuario hace clic en el botón "Crear una cuenta"
    Then debe abrirse el modal de registro
    When el usuario completa el formulario con:
      | firstName | lastName | email               | password      | passwordConfirm |
      | Usuario   | Prueba   | usuario@example.com | Contraseña123!| Contraseña123!  |
    And hace clic en el botón "Crear cuenta"
    Then el sistema debe registrar al usuario
    And debe cerrarse el modal de registro
    And el usuario debe ser redirigido a la página de dashboard
    And debe mostrarse el nombre del usuario en la página

  Scenario: Validación de campos obligatorios
    When el usuario hace clic en el botón "Crear una cuenta"
    Then debe abrirse el modal de registro
    When el usuario hace clic en el botón "Crear cuenta" sin completar los campos
    Then debe mostrarse un mensaje de error para cada campo obligatorio

  Scenario: Validación de contraseñas coincidentes
    When el usuario hace clic en el botón "Crear una cuenta"
    Then debe abrirse el modal de registro
    When el usuario completa el formulario con:
      | firstName | lastName | email               | password      | passwordConfirm |
      | Usuario   | Prueba   | usuario@example.com | Contraseña123!| OtraContraseña! |
    And hace clic en el botón "Crear cuenta"
    Then debe mostrarse un mensaje de error indicando que las contraseñas no coinciden
