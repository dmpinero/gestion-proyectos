/// <reference types="cypress" />

// Prueba completa del flujo de registro y redirección
describe('Registro de usuario y redirección', () => {
  // Datos del usuario de prueba
  const testUser = {
    firstName: 'Usuario',
    lastName: 'Prueba',
    email: 'usuario.prueba@example.com',
    password: 'Contraseña123!'
  };

  beforeEach(() => {
    // Visitar la página de login antes de cada prueba
    cy.visit('/login');
    cy.clearLocalStorage();
    
    // Configurar interceptores para las peticiones de API
    cy.intercept('POST', '/api/auth/register', (req) => {
      // Simular una respuesta exitosa del servidor
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
    
    // Interceptar las peticiones de redirección después del registro
    cy.intercept('GET', '/dashboard*', {
      statusCode: 200,
      body: '<html><body><h1>Dashboard</h1><p>Bienvenido, Usuario Prueba</p></body></html>'
    }).as('dashboardRequest');
  });

  it('Debe registrar un usuario y redirigir a la página de dashboard', () => {
    // Verificar que estamos en la página de login
    cy.url().should('include', '/login');
    
    // Hacer clic en el botón para abrir el modal de registro
    cy.contains('Crear una cuenta').click();
    
    // Verificar que el modal está visible
    cy.get('[role="dialog"]').should('be.visible');
    
    // Rellenar el formulario de registro
    cy.get('#first-name').type(testUser.firstName);
    cy.get('#last-name').type(testUser.lastName);
    cy.get('#email').type(testUser.email);
    cy.get('#password').type(testUser.password);
    cy.get('#password-confirm').type(testUser.password);
    
    // Enviar el formulario de registro
    cy.contains('button', 'Crear cuenta').click();
    
    // Esperar a que se complete la petición de registro
    cy.wait('@registerRequest').then((interception) => {
      // Verificar que los datos enviados son correctos
      expect(interception.request.body).to.include({
        firstName: testUser.firstName,
        lastName: testUser.lastName,
        email: testUser.email
      });
      
      // Verificar que la respuesta contiene un token
      expect(interception.response.body).to.have.property('token');
      
      // Verificar que la respuesta contiene los datos del usuario
      expect(interception.response.body).to.have.property('user');
      expect(interception.response.body.user).to.include({
        email: testUser.email,
        firstName: testUser.firstName,
        lastName: testUser.lastName
      });
    });
    
    // Verificar que el modal se ha cerrado
    cy.get('[role="dialog"]').should('not.exist');
    
    // Verificar que hemos sido redirigidos a la página de dashboard
    cy.url().should('include', '/dashboard');
    
    // Verificar que se muestra el nombre del usuario en la página
    cy.contains(testUser.firstName).should('be.visible');
  });
});
