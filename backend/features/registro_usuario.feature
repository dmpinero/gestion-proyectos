Feature: Registro de usuario
  Como usuario no registrado
  Quiero poder crear una cuenta en el sistema
  Para poder acceder a las funcionalidades de la aplicación

  Background:
    Given el sistema está preparado para registrar usuarios

  Scenario: Registro exitoso de un nuevo usuario
    When el usuario envía sus datos de registro con:
      | firstName | lastName | email               | password      |
      | Usuario   | Prueba   | usuario@example.com | Contraseña123!|
    Then el sistema debe crear el usuario en la base de datos
    And la respuesta debe incluir un token de autenticación
    And la respuesta debe incluir los datos del usuario creado
    And el código de respuesta debe ser 201

  Scenario: Intento de registro con email ya existente
    Given ya existe un usuario con email "usuario@example.com"
    When el usuario envía sus datos de registro con:
      | firstName | lastName | email               | password      |
      | Usuario   | Prueba   | usuario@example.com | Contraseña123!|
    Then la respuesta debe indicar que el email ya está en uso
    And el código de respuesta debe ser 400

  Scenario: Intento de registro con datos incompletos
    When el usuario envía sus datos de registro sin el campo "email":
      | firstName | lastName | password      |
      | Usuario   | Prueba   | Contraseña123!|
    Then la respuesta debe indicar que faltan campos obligatorios
    And el código de respuesta debe ser 422

  Scenario: Intento de registro con contraseña débil
    When el usuario envía sus datos de registro con:
      | firstName | lastName | email               | password |
      | Usuario   | Prueba   | usuario@example.com | 123456   |
    Then la respuesta debe indicar que la contraseña es débil
    And el código de respuesta debe ser 400
