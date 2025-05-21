describe('Registro de Usuario', () => {
  // Datos de prueba
  const testUser = {
    firstName: 'Juan',
    lastName: 'Pérez',
    email: 'test@example.com',
    password: 'Password123!',
    role: 'user'
  };

  beforeEach(() => {
    // Visitar la página principal
    cy.visit('/');
    cy.clearLocalStorage();
    
    // Configurar interceptor para las peticiones de registro
    cy.intercept('POST', '/api/auth/register').as('registerRequest');
  });

  it('Debe abrir el modal de registro al hacer clic en el botón "Crear una cuenta"', () => {
    // Hacer clic en el botón de registro
    cy.contains('button', 'Crear una cuenta').click();
    
    // Verificar que el modal esté visible
    cy.get('form').should('be.visible');
    cy.contains('h3', 'Crear una cuenta').should('be.visible');
  });

  it('Debe mostrar errores de validación al intentar enviar el formulario vacío', () => {
    // Abrir el modal de registro
    cy.contains('button', 'Crear una cuenta').click();
    
    // Verificar que el modal esté visible
    cy.get('form').should('be.visible');
    
    // Intentar enviar el formulario vacío
    cy.get('form').within(() => {
      cy.contains('button', 'Crear cuenta').click();
    });
    
    // Verificar que se muestran errores de validación
    // Nota: Esto depende de la validación HTML5 del navegador
    cy.get('form').within(() => {
      cy.get('input:invalid').should('exist');
    });
  });

  it('Debe mostrar error cuando las contraseñas no coinciden', () => {
    // Abrir el modal de registro
    cy.contains('button', 'Crear una cuenta').click();
    
    // Rellenar el formulario con contraseñas diferentes
    cy.get('form').within(() => {
      cy.get('input[id="first-name"]').type(testUser.firstName);
      cy.get('input[id="last-name"]').type(testUser.lastName);
      cy.get('input[id="email"]').type(testUser.email);
      cy.get('input[id="password"]').type(testUser.password);
      cy.get('input[id="password-confirm"]').type('contraseña-diferente');
      cy.get('select[id="role"]').select(testUser.role);
      
      // Enviar el formulario
      cy.contains('button', 'Crear cuenta').click();
    });
    
    // Verificar que se muestra el mensaje de error
    cy.contains('Las contraseñas no coinciden').should('be.visible');
  });

  it('Debe registrar un usuario exitosamente', () => {
    // Configurar mock para simular registro exitoso
    cy.intercept('POST', '/api/auth/register', {
      statusCode: 201,
      body: {
        message: 'Usuario registrado exitosamente',
        user: {
          id: 1,
          email: testUser.email,
          firstName: testUser.firstName,
          lastName: testUser.lastName,
          role: testUser.role
        }
      }
    }).as('registerSuccess');
    
    // Abrir el modal de registro
    cy.contains('button', 'Crear una cuenta').click();
    
    // Rellenar el formulario
    cy.get('form').within(() => {
      cy.get('input[id="first-name"]').type(testUser.firstName);
      cy.get('input[id="last-name"]').type(testUser.lastName);
      cy.get('input[id="email"]').type(testUser.email);
      cy.get('input[id="password"]').type(testUser.password);
      cy.get('input[id="password-confirm"]').type(testUser.password);
      cy.get('select[id="role"]').select(testUser.role);
      
      // Enviar el formulario
      cy.contains('button', 'Crear cuenta').click();
    });
    
    // Esperar a que se complete la petición
    cy.wait('@registerSuccess');
    
    // Verificar que se muestra el mensaje de éxito
    cy.contains('¡Registro exitoso!').should('be.visible');
  });

  it('Debe mostrar error si el correo ya está registrado', () => {
    // Configurar mock para simular error de correo duplicado
    cy.intercept('POST', '/api/auth/register', {
      statusCode: 400,
      body: {
        message: 'El correo electrónico ya está registrado',
        error: 'EMAIL_ALREADY_EXISTS'
      }
    }).as('registerError');
    
    // Abrir el modal de registro
    cy.contains('button', 'Crear una cuenta').click();
    
    // Rellenar el formulario
    cy.get('form').within(() => {
      cy.get('input[id="first-name"]').type(testUser.firstName);
      cy.get('input[id="last-name"]').type(testUser.lastName);
      cy.get('input[id="email"]').type(testUser.email);
      cy.get('input[id="password"]').type(testUser.password);
      cy.get('input[id="password-confirm"]').type(testUser.password);
      cy.get('select[id="role"]').select(testUser.role);
      
      // Enviar el formulario
      cy.contains('button', 'Crear cuenta').click();
    });
    
    // Esperar a que se complete la petición
    cy.wait('@registerError');
    
    // Verificar que se muestra el mensaje de error
    cy.contains('El correo electrónico ya está registrado').should('be.visible');
  });
});
