import api from './api';

export const authService = {
  async register(userData) {
    try {
      console.log('Enviando datos al backend:', userData);
      // La ruta debe coincidir con la configuración del backend
      const response = await api.post('/v1/auth/register', userData);
      console.log('Respuesta del backend:', response.data);
      
      // Guardar el token en localStorage si el registro es exitoso
      if (response.data && response.data.token) {
        localStorage.setItem('token', response.data.token);
      }
      return response.data;
    } catch (error) {
      console.error('Error en el registro:', error);
      // Mostrar más detalles del error para depuración
      if (error.response) {
        console.error('Respuesta del servidor:', error.response.data);
        console.error('Estado HTTP:', error.response.status);
      }
      throw error;
    }
  },
  
  async login(credentials) {
    try {
      console.log('Intentando iniciar sesión con:', credentials);
      // La ruta debe coincidir con la configuración del backend
      const response = await api.post('/v1/auth/login', credentials);
      console.log('Respuesta del login:', response.data);
      
      // Guardar el token en localStorage
      if (response.data && (response.data.access_token || response.data.token)) {
        const token = response.data.access_token || response.data.token;
        localStorage.setItem('token', token);
      }
      return response.data;
    } catch (error) {
      console.error('Error en el login:', error);
      // Mostrar más detalles del error para depuración
      if (error.response) {
        console.error('Respuesta del servidor:', error.response.data);
        console.error('Estado HTTP:', error.response.status);
      }
      throw error;
    }
  },
  
  logout() {
    // Eliminar el token del localStorage
    localStorage.removeItem('token');
  },
  
  getToken() {
    return localStorage.getItem('token');
  },
  
  isAuthenticated() {
    return !!this.getToken();
  }
};

export default authService;
