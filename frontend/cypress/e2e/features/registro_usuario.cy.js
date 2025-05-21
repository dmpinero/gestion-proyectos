/// <reference types="cypress" />

// Implementación de los pasos de BDD para el registro de usuario
describe('Registro de usuario en la interfaz', () => {
  // Datos del usuario de prueba
  const testUser = {
    firstName: 'Usuario',
    lastName: 'Prueba',
    email: 'usuario@example.com',
    password: 'Contraseña123!',
    passwordConfirm: 'Contraseña123!'
  };

  beforeEach(() => {
    // Background: el usuario está en la página de login
    cy.visit('/login');
    cy.clearLocalStorage();
    
    // Configurar interceptores para las peticiones de API
    cy.intercept('POST', '/api/auth/register', (req) => {
      req.reply({
        statusCode: 201,
        body: {
          token: 'fake-jwt-token',
          user: {
            id: 1,
            email: req.body.email,
            firstName: req.body.firstName,
            lastName: req.body.lastName,
            role: 'user'
          }
        }
      });
    }).as('registerRequest');
    
    cy.intercept('POST', '/api/auth/login', (req) => {
      req.reply({
        statusCode: 200,
        body: {
          token: 'fake-jwt-token',
          user: {
            id: 1,
            email: req.body.email,
            firstName: 'Usuario',
            lastName: 'Prueba',
            role: 'user'
          }
        }
      });
    }).as('loginRequest');
  });

  it('Registro exitoso y redirección', () => {
    // When el usuario hace clic en el botón "Crear una cuenta"
    cy.contains('Crear una cuenta').click();
    
    // Then debe abrirse el modal de registro
    cy.get('[role="dialog"]').should('be.visible');
    
    // When el usuario completa el formulario
    cy.get('#first-name').type(testUser.firstName);
    cy.get('#last-name').type(testUser.lastName);
    cy.get('#email').type(testUser.email);
    cy.get('#password').type(testUser.password);
    cy.get('#password-confirm').type(testUser.passwordConfirm);
    
    // And hace clic en el botón "Crear cuenta"
    cy.contains('button', 'Crear cuenta').click();
    
    // Then el sistema debe registrar al usuario
    cy.wait('@registerRequest').its('request.body').should('deep.include', {
      firstName: testUser.firstName,
      lastName: testUser.lastName,
      email: testUser.email
    });
    
    // And debe cerrarse el modal de registro
    cy.get('[role="dialog"]').should('not.exist');
    
    // And el usuario debe ser redirigido a la página de dashboard
    cy.url().should('include', '/dashboard');
    
    // And debe mostrarse el nombre del usuario en la página
    cy.contains(testUser.firstName).should('be.visible');
  });

  it('Validación de campos obligatorios', () => {
    // When el usuario hace clic en el botón "Crear una cuenta"
    cy.contains('Crear una cuenta').click();
    
    // Then debe abrirse el modal de registro
    cy.get('[role="dialog"]').should('be.visible');
    
    // When el usuario hace clic en el botón "Crear cuenta" sin completar los campos
    cy.contains('button', 'Crear cuenta').click();
    
    // Then debe mostrarse un mensaje de error para cada campo obligatorio
    cy.get('[role="dialog"]').within(() => {
      // Verificar mensajes de error para cada campo
      cy.contains('El nombre es requerido').should('be.visible');
      cy.contains('El apellido es requerido').should('be.visible');
      cy.contains('El email es requerido').should('be.visible');
      cy.contains('La contraseña es requerida').should('be.visible');
    });
  });

  it('Validación de contraseñas coincidentes', () => {
    // When el usuario hace clic en el botón "Crear una cuenta"
    cy.contains('Crear una cuenta').click();
    
    // Then debe abrirse el modal de registro
    cy.get('[role="dialog"]').should('be.visible');
    
    // When el usuario completa el formulario con contraseñas diferentes
    cy.get('#first-name').type(testUser.firstName);
    cy.get('#last-name').type(testUser.lastName);
    cy.get('#email').type(testUser.email);
    cy.get('#password').type(testUser.password);
    cy.get('#password-confirm').type('OtraContraseña!');
    
    // And hace clic en el botón "Crear cuenta"
    cy.contains('button', 'Crear cuenta').click();
    
    // Then debe mostrarse un mensaje de error indicando que las contraseñas no coinciden
    cy.contains('Las contraseñas no coinciden').should('be.visible');
  });
});
