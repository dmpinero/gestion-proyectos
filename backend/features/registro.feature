# language: es
# encoding: utf-8

Característica: Registro de usuarios
  Como visitante del sistema
  Quiero poder registrarme como usuario
  Para acceder a las funcionalidades restringidas

  Escenario: Registro exitoso de usuario
    Cuando envío una petición POST a "/register" con:
      | firstName | lastName | email                | password     | passwordConfirm | role |
      | Juan      | Pérez    | juan.perez@ejemplo.com | Password123! | Password123!    | user |
    Entonces la respuesta debe tener un código de estado 201
    Y la respuesta debe contener un mensaje de éxito "Usuario registrado exitosamente"
    Y la respuesta debe contener los datos del usuario registrado

  Escenario: Intento de registro con correo electrónico ya existente
    Dado que tengo un usuario registrado con email "usuario@ejemplo.com"
    Cuando envío una petición POST a "/register" con:
      | firstName | lastName | email             | password     | passwordConfirm | role |
      | Usuario   | Ejemplo  | usuario@ejemplo.com | Password123! | Password123!    | user |
    Entonces la respuesta debe tener un código de estado 400
    Y la respuesta debe contener el mensaje de error "El correo electrónico ya está registrado"

  Escenario: Intento de registro con contraseñas que no coinciden
    Cuando envío una petición POST a "/register" con:
      | firstName | lastName | email                | password     | passwordConfirm   | role |
      | Juan      | Pérez    | juan.perez@ejemplo.com | Password123! | OtraContraseña123 | user |
    Entonces la respuesta debe tener un código de estado 422
    Y la respuesta debe contener el mensaje de error "Las contraseñas no coinciden"

  Escenario: Intento de registro con datos incompletos
    Cuando envío una petición POST a "/register" con:
      | firstName | email                |
      | Juan      | juan.perez@ejemplo.com |
    Entonces la respuesta debe tener un código de estado 422
    Y la respuesta debe indicar que faltan campos obligatorios

  Escenario: Intento de registro con formato de correo inválido
    Cuando envío una petición POST a "/register" con:
      | firstName | lastName | email         | password     | passwordConfirm | role |
      | Juan      | Pérez    | correo-invalido | Password123! | Password123!    | user |
    Entonces la respuesta debe tener un código de estado 422
    Y la respuesta debe contener el mensaje de error "Formato de correo electrónico inválido"
