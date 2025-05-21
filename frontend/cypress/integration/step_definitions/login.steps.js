/// <reference types="cypress" />

// Paso 1: Configuración inicial
beforeEach(() => {
  // Interceptar peticiones de login
  cy.intercept('POST', '/api/auth/login').as('loginRequest');
});

// Pasos comunes
const visitarPaginaLogin = () => {
  cy.visit('/login');
  cy.get('form').should('be.visible');
};

const rellenarCampo = (campo, valor) => {
  switch (campo.toLowerCase()) {
    case 'email':
      cy.get('input[type="email"]').clear().type(valor);
      break;
    case 'contraseña':
      cy.get('input[type="password"]').clear().type(valor);
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

Cypress.Commands.add('given_intento_acceder_ruta_protegida', () => {
  cy.visit('/dashboard/profile');
  // Verificar redirección al login
  cy.url().should('include', '/login');
});

// When
Cypress.Commands.add('when_intento_enviar_formulario_vacio', () => {
  cy.get('button[type="submit"]').click();
});

Cypress.Commands.add('when_relleno_campo_correo_invalido', (datosTabla) => {
  rellenarFormulario(datosTabla);
});

Cypress.Commands.add('when_relleno_formulario_credenciales_invalidas', (datosTabla) => {
  // Configurar mock para simular credenciales inválidas
  cy.intercept('POST', '/api/auth/login', {
    statusCode: 401,
    body: {
      message: 'Credenciales inválidas',
      error: 'INVALID_CREDENTIALS'
    },
    delay: 300
  }).as('loginError');
  
  rellenarFormulario(datosTabla);
});

Cypress.Commands.add('when_relleno_formulario_credenciales_validas', (datosTabla) => {
  // Configurar mock para simular login exitoso
  cy.intercept('POST', '/api/auth/login', {
    statusCode: 200,
    body: {
      token: 'fake-jwt-token',
      user: {
        id: 1,
        email: 'usuario@ejemplo.com',
        firstName: 'Usuario',
        lastName: 'Ejemplo',
        role: 'user'
      }
    },
    delay: 300
  }).as('loginSuccess');
  
  rellenarFormulario(datosTabla);
});

Cypress.Commands.add('when_hago_clic_en_boton', (boton) => {
  cy.contains('button', boton).click();
});

Cypress.Commands.add('when_inicio_sesion_credenciales_validas', () => {
  // Configurar mock para simular login exitoso con redirección
  cy.intercept('POST', '/api/auth/login', {
    statusCode: 200,
    body: {
      token: 'fake-jwt-token',
      user: {
        id: 1,
        email: 'usuario@ejemplo.com',
        firstName: 'Usuario',
        lastName: 'Ejemplo',
        role: 'user'
      },
      redirectUrl: '/dashboard/profile'
    },
    delay: 300
  }).as('loginRedirect');
  
  // Rellenar formulario
  cy.get('input[type="email"]').type('usuario@ejemplo.com');
  cy.get('input[type="password"]').type('Password123!');
  cy.get('button[type="submit"]').click();
  
  // Esperar a que se complete la petición
  cy.wait('@loginRedirect');
});

// Then
Cypress.Commands.add('then_deberia_ver_formulario_login', () => {
  cy.get('h2').should('contain', 'Iniciar Sesión');
});

Cypress.Commands.add('then_deberia_ver_campos_login', () => {
  cy.get('input[type="email"]').should('be.visible');
  cy.get('input[type="password"]').should('be.visible');
});

Cypress.Commands.add('then_deberia_ver_boton_login', () => {
  cy.get('button[type="submit"]').should('be.visible').and('contain', 'Iniciar Sesión');
});

Cypress.Commands.add('then_deberia_ver_enlace_registro', () => {
  cy.contains('a', 'Regístrate').should('be.visible');
});

Cypress.Commands.add('then_deberia_ver_errores_validacion_login', () => {
  cy.get('input[type="email"]:invalid').should('exist');
  cy.get('input[type="password"]:invalid').should('exist');
});

Cypress.Commands.add('then_deberia_ver_error_formato_correo', () => {
  cy.get('input[type="email"]:invalid').should('exist');
});

Cypress.Commands.add('then_deberia_ver_mensaje_error_credenciales', () => {
  // Esperar a que se complete la petición
  cy.wait('@loginError');
  
  // Verificar mensaje de error
  cy.contains('Credenciales inválidas').should('be.visible');
});

Cypress.Commands.add('then_deberia_ser_redirigido_dashboard', () => {
  // Esperar a que se complete la petición
  cy.wait('@loginSuccess');
  
  // Verificar redirección
  cy.url().should('include', '/dashboard');
});

Cypress.Commands.add('then_deberia_ser_redirigido_ruta_original', () => {
  // Verificar redirección a la ruta original
  cy.url().should('include', '/dashboard/profile');
});

// Implementación de los escenarios

describe('Inicio de sesión de usuarios', () => {
  it('Mostrar formulario de login', () => {
    cy.given_estoy_en_pagina_login();
    cy.then_deberia_ver_formulario_login();
    cy.then_deberia_ver_campos_login();
    cy.then_deberia_ver_boton_login();
    cy.then_deberia_ver_enlace_registro();
    
    // Tomar captura de pantalla
    cy.screenshot('bdd-login-formulario');
  });
  
  it('Validación de campos obligatorios', () => {
    cy.given_estoy_en_pagina_login();
    cy.when_intento_enviar_formulario_vacio();
    cy.then_deberia_ver_errores_validacion_login();
    
    // Tomar captura de pantalla
    cy.screenshot('bdd-login-validacion');
  });
  
  it('Validación de formato de correo electrónico', () => {
    cy.given_estoy_en_pagina_login();
    cy.when_relleno_campo_correo_invalido([
      { campo: 'email', valor: 'correo-invalido' }
    ]);
    cy.when_hago_clic_en_boton('Iniciar Sesión');
    cy.then_deberia_ver_error_formato_correo();
    
    // Tomar captura de pantalla
    cy.screenshot('bdd-login-formato-correo');
  });
  
  it('Error con credenciales inválidas', () => {
    cy.given_estoy_en_pagina_login();
    cy.when_relleno_formulario_credenciales_invalidas([
      { campo: 'email', valor: 'usuario@invalido.com' },
      { campo: 'contraseña', valor: 'contraseñaincorrecta' }
    ]);
    cy.when_hago_clic_en_boton('Iniciar Sesión');
    cy.then_deberia_ver_mensaje_error_credenciales();
    
    // Tomar captura de pantalla
    cy.screenshot('bdd-login-credenciales-invalidas');
  });
  
  it('Inicio de sesión exitoso', () => {
    cy.given_estoy_en_pagina_login();
    cy.when_relleno_formulario_credenciales_validas([
      { campo: 'email', valor: 'usuario@ejemplo.com' },
      { campo: 'contraseña', valor: 'Password123!' }
    ]);
    cy.when_hago_clic_en_boton('Iniciar Sesión');
    cy.then_deberia_ser_redirigido_dashboard();
    
    // Tomar captura de pantalla
    cy.screenshot('bdd-login-exitoso');
  });
  
  it('Redirección después del login', () => {
    cy.given_intento_acceder_ruta_protegida();
    cy.when_inicio_sesion_credenciales_validas();
    cy.then_deberia_ser_redirigido_ruta_original();
    
    // Tomar captura de pantalla
    cy.screenshot('bdd-login-redireccion');
  });
});
