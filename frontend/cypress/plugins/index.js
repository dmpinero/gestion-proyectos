/// <reference types="cypress" />

/**
 * @type {Cypress.PluginConfig}
 */
export default (on, config) => {
  // Configuración para integrar BDD con Cypress
  on('file:preprocessor', (file) => {
    // Verificar si el archivo es un archivo de características (.feature)
    if (file.filePath.endsWith('.feature')) {
      // Cargar el archivo de características y ejecutar los pasos correspondientes
      const featurePath = file.filePath;
      const stepDefinitionsPath = featurePath.replace('.feature', '.steps.js');
      
      // Registrar la ruta del archivo de características y sus definiciones de pasos
      console.log(`Procesando archivo de características: ${featurePath}`);
      console.log(`Usando definiciones de pasos: ${stepDefinitionsPath}`);
      
      // Devolver el archivo sin modificar para que Cypress lo procese
      return file;
    }
    
    // Para otros tipos de archivos, devolver el archivo sin modificar
    return file;
  });
  
  return config;
};
