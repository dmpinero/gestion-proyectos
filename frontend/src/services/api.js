import axios from 'axios';

// Configuración de axios para la API
const api = axios.create({
  // Usar la URL relativa para aprovechar el proxy de Vite
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  timeout: 10000 // 10 segundos de timeout
});

// Interceptor para manejar errores globalmente
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.log('Error en interceptor:', error);
    if (error.response) {
      // El servidor respondió con un estado de error
      // Devolver el objeto error completo para que se pueda acceder a error.response en los catch
      return Promise.reject(error);
    } else if (error.request) {
      // La petición fue hecha pero no se recibió respuesta
      console.error('No se recibió respuesta del servidor:', error.request);
      return Promise.reject({
        message: 'No se pudo conectar con el servidor. Por favor, verifica tu conexión.',
        originalError: error
      });
    } else {
      // Algo más causó el error
      console.error('Error en la configuración de la solicitud:', error.message);
      return Promise.reject({
        message: 'Error al procesar la solicitud.',
        originalError: error
      });
    }
  }
);

export default api;
