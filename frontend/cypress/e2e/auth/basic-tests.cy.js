// Pruebas básicas de autenticación
describe('Autenticación', () => {
  beforeEach(() => {
    // Visitar la página principal antes de cada prueba
    cy.visit('/');
    cy.clearLocalStorage();
  });

  it('Debe mostrar el botón de registro en la página principal', () => {
    // Verificar que el botón de registro está visible
    cy.contains('button', 'Crear una cuenta').should('be.visible');
  });

  it('Debe mostrar el formulario de login correctamente', () => {
    // Navegar a la página de login
    cy.visit('/login');
    
    // Verificar que el formulario está visible
    cy.get('form').should('be.visible');
    
    // Verificar que los campos del formulario están presentes
    cy.get('input[type="email"]').should('exist');
    cy.get('input[type="password"]').should('exist');
    cy.get('button[type="submit"]').should('exist');
  });

  it('Debe abrir el modal de registro al hacer clic en el botón', () => {
    // Hacer clic en el botón de registro
    cy.contains('button', 'Crear una cuenta').click();
    
    // Verificar que el modal está visible
    cy.get('[role="dialog"]').should('be.visible');
    
    // Verificar que el formulario de registro está presente
    cy.get('[role="dialog"] form').should('exist');
  });
});
