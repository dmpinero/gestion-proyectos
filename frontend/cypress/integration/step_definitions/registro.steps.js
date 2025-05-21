/// <reference types="cypress" />

// Paso 1: Configuración inicial
beforeEach(() => {
  // Interceptar peticiones de registro
  cy.intercept('POST', '/api/auth/register').as('registerRequest');
});

// Pasos comunes
const visitarPaginaLogin = () => {
  cy.visit('/login');
  cy.get('form').should('be.visible');
};

const abrirFormularioRegistro = () => {
  visitarPaginaLogin();
  cy.contains('Regístrate').click();
  cy.get('h3').contains('Crear una cuenta').should('be.visible');
};

const rellenarCampo = (campo, valor) => {
  switch (campo.toLowerCase()) {
    case 'nombre':
      cy.get('#first-name').clear().type(valor);
      break;
    case 'apellidos':
      cy.get('#last-name').clear().type(valor);
      break;
    case 'email':
      cy.get('#email').clear().type(valor);
      break;
    case 'contraseña':
      cy.get('#password').clear().type(valor);
      break;
    case 'confirmación':
      cy.get('#password-confirm').clear().type(valor);
      break;
    case 'rol':
      cy.get('#role').select(valor);
      break;
    default:
      throw new Error(`Campo no reconocido: ${campo}`);
  }
};

const rellenarFormulario = (datosTabla) => {
  datosTabla.forEach(fila => {
    rellenarCampo(fila.campo, fila.valor);
  });
};

// Definiciones de pasos (Given, When, Then)

// Given
Cypress.Commands.add('given_estoy_en_pagina_login', () => {
  visitarPaginaLogin();
});

Cypress.Commands.add('given_estoy_en_formulario_registro', () => {
  abrirFormularioRegistro();
});

// When
Cypress.Commands.add('when_hago_clic_en_enlace', (enlace) => {
  cy.contains(enlace).click();
});

Cypress.Commands.add('when_intento_enviar_formulario_vacio', () => {
  cy.contains('button', 'Crear cuenta').click();
});

Cypress.Commands.add('when_relleno_formulario_con_contraseñas_diferentes', (datosTabla) => {
  rellenarFormulario(datosTabla);
});

Cypress.Commands.add('when_relleno_formulario_con_datos_validos', (datosTabla) => {
  rellenarFormulario(datosTabla);
});

Cypress.Commands.add('when_acepto_terminos', () => {
  cy.get('#terms').check({ force: true });
});

Cypress.Commands.add('when_hago_clic_en_boton', (boton) => {
  cy.contains('button', boton).click();
});

Cypress.Commands.add('when_relleno_formulario_con_correo_existente', () => {
  // Configurar mock para simular correo ya registrado
  cy.intercept('POST', '/api/auth/register', {
    statusCode: 400,
    body: {
      message: 'El correo electrónico ya está registrado',
      error: 'EMAIL_ALREADY_EXISTS'
    },
    delay: 300
  }).as('registerError');
  
  // Rellenar formulario con datos de prueba
  cy.get('#first-name').type('Usuario');
  cy.get('#last-name').type('Existente');
  cy.get('#email').type('usuario.existente@example.com');
  cy.get('#password').type('Password123!');
  cy.get('#password-confirm').type('Password123!');
  cy.get('#role').select('user');
  cy.get('#terms').check({ force: true });
});

// Then
Cypress.Commands.add('then_deberia_ver_formulario_registro', () => {
  cy.get('h3').should('contain', 'Crear una cuenta');
});

Cypress.Commands.add('then_deberia_ver_campos', () => {
  cy.get('#first-name').should('be.visible');
  cy.get('#last-name').should('be.visible');
  cy.get('#email').should('be.visible');
  cy.get('#password').should('be.visible');
  cy.get('#password-confirm').should('be.visible');
});

Cypress.Commands.add('then_deberia_ver_selector_rol', () => {
  cy.get('#role').should('be.visible');
});

Cypress.Commands.add('then_deberia_ver_casilla_terminos', () => {
  cy.get('#terms').should('be.visible');
});

Cypress.Commands.add('then_deberia_ver_errores_validacion', () => {
  cy.get('#first-name:invalid').should('exist');
  cy.get('#last-name:invalid').should('exist');
  cy.get('#email:invalid').should('exist');
  cy.get('#password:invalid').should('exist');
});

Cypress.Commands.add('then_deberia_ver_mensaje_error_contraseñas', () => {
  cy.contains('Las contraseñas no coinciden').should('be.visible');
});

Cypress.Commands.add('then_deberia_ver_mensaje_exito', () => {
  // Configurar mock para simular registro exitoso
  cy.intercept('POST', '/api/auth/register', {
    statusCode: 201,
    body: {
      message: 'Usuario registrado exitosamente',
      user: {
        id: 1,
        email: 'juan.perez@example.com',
        firstName: 'Juan',
        lastName: 'Pérez',
        role: 'user'
      }
    },
    delay: 300
  }).as('registerSuccess');
  
  // Esperar a que se complete la petición
  cy.wait('@registerSuccess');
  
  // Verificar mensaje de éxito
  cy.contains('¡Registro exitoso!').should('be.visible');
});

Cypress.Commands.add('then_deberia_ser_redirigido_login', () => {
  // Verificar que el modal se cerró (después de un breve retraso)
  cy.wait(400);
  cy.get('h3').should('not.exist');
});

Cypress.Commands.add('then_deberia_ver_mensaje_error_correo_registrado', () => {
  // Esperar a que se complete la petición
  cy.wait('@registerError');
  
  // Verificar mensaje de error
  cy.contains('El correo electrónico ya está registrado').should('be.visible');
});

// Implementación de los escenarios

describe('Registro de usuarios', () => {
  it('Mostrar formulario de registro', () => {
    cy.given_estoy_en_pagina_login();
    cy.when_hago_clic_en_enlace('Regístrate');
    cy.then_deberia_ver_formulario_registro();
    cy.then_deberia_ver_campos();
    cy.then_deberia_ver_selector_rol();
    cy.then_deberia_ver_casilla_terminos();
    
    // Tomar captura de pantalla
    cy.screenshot('bdd-registro-formulario');
  });
  
  it('Validación de campos obligatorios', () => {
    cy.given_estoy_en_formulario_registro();
    cy.when_intento_enviar_formulario_vacio();
    cy.then_deberia_ver_errores_validacion();
    
    // Tomar captura de pantalla
    cy.screenshot('bdd-registro-validacion');
  });
  
  it('Validación de contraseñas coincidentes', () => {
    cy.given_estoy_en_formulario_registro();
    cy.when_relleno_formulario_con_contraseñas_diferentes([
      { campo: 'nombre', valor: 'Juan' },
      { campo: 'apellidos', valor: 'Pérez' },
      { campo: 'email', valor: 'juan.perez@example.com' },
      { campo: 'contraseña', valor: 'Password123!' },
      { campo: 'confirmación', valor: 'OtraContraseña123!' }
    ]);
    cy.when_acepto_terminos();
    cy.when_hago_clic_en_boton('Crear cuenta');
    cy.then_deberia_ver_mensaje_error_contraseñas();
    
    // Tomar captura de pantalla
    cy.screenshot('bdd-registro-contraseñas');
  });
  
  it('Registro exitoso', () => {
    cy.given_estoy_en_formulario_registro();
    cy.when_relleno_formulario_con_datos_validos([
      { campo: 'nombre', valor: 'Juan' },
      { campo: 'apellidos', valor: 'Pérez' },
      { campo: 'email', valor: 'juan.perez@example.com' },
      { campo: 'contraseña', valor: 'Password123!' },
      { campo: 'confirmación', valor: 'Password123!' },
      { campo: 'rol', valor: 'user' }
    ]);
    cy.when_acepto_terminos();
    cy.when_hago_clic_en_boton('Crear cuenta');
    cy.then_deberia_ver_mensaje_exito();
    cy.then_deberia_ser_redirigido_login();
    
    // Tomar captura de pantalla
    cy.screenshot('bdd-registro-exitoso');
  });
  
  it('Error de correo electrónico ya registrado', () => {
    cy.given_estoy_en_formulario_registro();
    cy.when_relleno_formulario_con_correo_existente();
    cy.when_hago_clic_en_boton('Crear cuenta');
    cy.then_deberia_ver_mensaje_error_correo_registrado();
    
    // Tomar captura de pantalla
    cy.screenshot('bdd-registro-correo-existente');
  });
});
