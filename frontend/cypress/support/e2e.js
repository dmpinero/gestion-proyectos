// ***********************************************************
// Configuración mínima para pruebas e2e
// ***********************************************************

// Importar comandos personalizados
require('./commands');

// Manejar excepciones no capturadas
Cypress.on('uncaught:exception', () => {
  return false;
});
