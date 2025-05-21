// Prueba básica de autenticación
describe('Autenticación - Prueba Simple', () => {
  beforeEach(() => {
    // Visitar la página principal antes de cada prueba
    cy.visit('/');
  });

  it('Debe cargar la página principal correctamente', () => {
    // Verificar que la página se ha cargado
    cy.get('body').should('be.visible');
  });

  it('Debe navegar a la página de login', () => {
    // Navegar a la página de login
    cy.visit('/login');
    
    // Verificar que la página se ha cargado
    cy.get('body').should('be.visible');
  });
});
