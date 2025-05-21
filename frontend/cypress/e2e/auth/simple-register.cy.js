// Prueba simplificada de registro
describe('Registro de Usuario', () => {
  beforeEach(() => {
    // Visitar la página principal
    cy.visit('/');
    cy.clearLocalStorage();
  });

  it('Debe mostrar el botón de registro', () => {
    // Verificar que el botón de registro está visible
    cy.contains('Crear una cuenta').should('be.visible');
  });

  it('Debe abrir el modal de registro al hacer clic en el botón', () => {
    // Hacer clic en el botón de registro
    cy.contains('Crear una cuenta').click();
    
    // Verificar que el modal está visible (usando un timeout más largo)
    cy.get('[role="dialog"]', { timeout: 10000 }).should('be.visible');
  });

  it('Debe contener los campos necesarios en el formulario de registro', () => {
    // Hacer clic en el botón de registro
    cy.contains('Crear una cuenta').click();
    
    // Verificar que el modal está visible
    cy.get('[role="dialog"]', { timeout: 10000 }).should('be.visible');
    
    // Verificar que los campos del formulario están presentes
    cy.get('[role="dialog"]').within(() => {
      cy.get('input[id="first-name"]').should('exist');
      cy.get('input[id="last-name"]').should('exist');
      cy.get('input[id="email"]').should('exist');
      cy.get('input[id="password"]').should('exist');
      cy.get('input[id="password-confirm"]').should('exist');
    });
  });
});
