// ***********************************************************
// Configuración para pruebas de componentes
// ***********************************************************

// Importar Vue
import { mount } from 'cypress/vue'

// Importar estilos globales
import '@/assets/main.css'

// Configuración de comandos para pruebas de componentes
Cypress.Commands.add('mount', mount)

// Manejar excepciones no capturadas
Cypress.on('uncaught:exception', (err, runnable) => {
  // No fallar la prueba por errores no atrapados
  return false
})
