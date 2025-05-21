describe('Inicio de Sesión', () => {
  // Datos de prueba
  const testUser = {
    email: 'usuario@ejemplo.com',
    password: 'Password123!'
  };

  beforeEach(() => {
    // Visitar la página de login
    cy.visit('/login');
    cy.clearLocalStorage();
    
    // Configurar interceptor para las peticiones de login
    cy.intercept('POST', '/api/auth/login').as('loginRequest');
  });

  it('Debe mostrar el formulario de login correctamente', () => {
    // Verificar que el formulario esté visible
    cy.get('form').should('be.visible');
    
    // Verificar que los campos del formulario estén presentes
    cy.get('input[type="email"]').should('be.visible');
    cy.get('input[type="password"]').should('be.visible');
    cy.get('button[type="submit"]').should('be.visible');
    
    // Verificar que el botón de registro esté presente
    cy.contains('Crear una cuenta').should('exist');
  });

  it('Debe validar campos obligatorios', () => {
    // Intentar enviar el formulario vacío
    cy.get('form').within(() => {
      cy.get('button[type="submit"]').click();
    });
    
    // Verificar que se muestran errores de validación
    cy.get('form').within(() => {
      cy.get('input:invalid').should('exist');
    });
  });

  it('Debe validar formato de correo electrónico', () => {
    // Rellenar con correo inválido
    cy.get('form').within(() => {
      cy.get('input[type="email"]').type('correo-invalido');
      cy.get('input[type="password"]').type('password123');
      cy.get('button[type="submit"]').click();
    });
    
    // Verificar validación del navegador para formato de email
    cy.get('input[type="email"]:invalid').should('exist');
  });

  it('Debe mostrar error con credenciales inválidas', () => {
    // Configurar mock para simular credenciales inválidas
    cy.intercept('POST', '/api/auth/login', {
      statusCode: 401,
      body: {
        message: 'Credenciales inválidas',
        error: 'INVALID_CREDENTIALS'
      }
    }).as('loginError');
    
    // Rellenar el formulario con credenciales incorrectas
    cy.get('form').within(() => {
      cy.get('input[type="email"]').type('usuario@invalido.com');
      cy.get('input[type="password"]').type('contraseñaincorrecta');
      cy.get('button[type="submit"]').click();
    });
    
    // Esperar a que se complete la petición
    cy.wait('@loginError');
    
    // Verificar que se muestre el mensaje de error
    cy.contains('Credenciales inválidas').should('be.visible');
  });

  it('Debe iniciar sesión correctamente y redirigir al dashboard', () => {
    // Configurar mock para simular inicio de sesión exitoso
    cy.intercept('POST', '/api/auth/login', {
      statusCode: 200,
      body: {
        token: 'fake-jwt-token',
        user: {
          id: 1,
          email: testUser.email,
          firstName: 'Usuario',
          lastName: 'Prueba',
          role: 'user'
        }
      }
    }).as('loginSuccess');
    
    // Rellenar el formulario con credenciales válidas
    cy.get('form').within(() => {
      cy.get('input[type="email"]').type(testUser.email);
      cy.get('input[type="password"]').type(testUser.password);
      cy.get('button[type="submit"]').click();
    });
    
    // Esperar a que se complete la petición
    cy.wait('@loginSuccess');
    
    // Verificar que se haya redirigido al dashboard
    cy.url().should('include', '/dashboard');
    
    // Verificar que el token se haya guardado en localStorage
    cy.window().its('localStorage.token').should('exist');
  });

  it('Debe redirigir a la página solicitada después del login', () => {
    // Visitar una ruta protegida
    cy.visit('/dashboard/profile');
    
    // Debería redirigir al login
    cy.url().should('include', '/login');
    
    // Configurar mock para simular inicio de sesión exitoso
    cy.intercept('POST', '/api/auth/login', {
      statusCode: 200,
      body: {
        token: 'fake-jwt-token',
        user: {
          id: 1,
          email: testUser.email,
          firstName: 'Usuario',
          lastName: 'Prueba',
          role: 'user'
        }
      }
    }).as('loginRedirect');
    
    // Iniciar sesión
    cy.get('form').within(() => {
      cy.get('input[type="email"]').type(testUser.email);
      cy.get('input[type="password"]').type(testUser.password);
      cy.get('button[type="submit"]').click();
    });
    
    // Esperar a que se complete la petición
    cy.wait('@loginRedirect');
    
    // Debería redirigir a la ruta solicitada originalmente
    cy.url().should('include', '/dashboard/profile');
  });
});
