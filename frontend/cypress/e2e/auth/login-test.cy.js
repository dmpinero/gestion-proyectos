// Prueba de inicio de sesión
describe('Inicio de sesión', () => {
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
    // Limpiar el almacenamiento local para asegurar un estado limpio
    cy.clearLocalStorage();
  });

  it('Debe mostrar el formulario de login correctamente', () => {
    // Verificar que el formulario de login está visible
    cy.get('form').should('be.visible');
    
    // Verificar que los campos del formulario están presentes
    cy.get('input[type="email"]').should('exist');
    cy.get('input[type="password"]').should('exist');
    cy.get('button[type="submit"]').should('exist');
  });

  it('Debe registrar un nuevo usuario y luego iniciar sesión', () => {
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
    
    // Esperar a que se complete el registro (mock)
    cy.intercept('POST', '/api/auth/register', {
      statusCode: 201,
      body: {
        message: 'Usuario registrado exitosamente',
        user: {
          id: 1,
          email: testUser.email,
          firstName: testUser.firstName,
          lastName: testUser.lastName,
          role: 'user'
        }
      }
    }).as('registerRequest');
    
    // Verificar que el modal se ha cerrado
    cy.get('[role="dialog"]').should('not.exist');
    
    // Iniciar sesión con el usuario recién creado
    cy.get('input[type="email"]').type(testUser.email);
    cy.get('input[type="password"]').type(testUser.password);
    
    // Interceptar la petición de login
    cy.intercept('POST', '/api/auth/login', {
      statusCode: 200,
      body: {
        token: 'fake-jwt-token',
        user: {
          id: 1,
          email: testUser.email,
          firstName: testUser.firstName,
          lastName: testUser.lastName,
          role: 'user'
        }
      }
    }).as('loginRequest');
    
    // Hacer clic en el botón de iniciar sesión
    cy.get('button[type="submit"]').click();
    
    // Esperar a que se complete la petición de login
    cy.wait('@loginRequest');
    
    // Verificar que hemos sido redirigidos a la página de dashboard o home
    cy.url().should('include', '/dashboard');
    
    // Verificar que se muestra el nombre del usuario en la página
    cy.contains(testUser.firstName).should('be.visible');
  });
});
