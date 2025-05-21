// ***********************************************
// Comandos personalizados mínimos
// ***********************************************

// Comando básico para iniciar sesión
Cypress.Commands.add('login', (email, password) => {
  cy.visit('/login')
  cy.get('input[type="email"]').type(email)
  cy.get('input[type="password"]').type(password)
  cy.get('button[type="submit"]').click()
})
