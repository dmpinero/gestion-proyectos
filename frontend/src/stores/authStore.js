import { defineStore } from 'pinia';
import { authService } from '@/services/authService';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    showRegisterModal: false,
    user: null,
    token: localStorage.getItem('token') || null,
    loading: false,
    error: null
  }),
  
  getters: {
    isAuthenticated: (state) => !!state.token,
  },
  
  actions: {
    openRegisterModal() {
      this.showRegisterModal = true;
    },
    
    closeRegisterModal() {
      this.showRegisterModal = false;
    },
    
    toggleRegisterModal() {
      this.showRegisterModal = !this.showRegisterModal;
    },
    
    async register(userData) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await authService.register(userData);
        
        // Guardar token en localStorage y store
        if (response && response.token) {
          console.log('Token recibido:', response.token);
          // Guardar token en localStorage
          localStorage.setItem('token', response.token);
          // Guardar token en el store
          this.token = response.token;
          
          // Guardar datos del usuario
          if (response.user) {
            this.user = response.user;
            console.log('Usuario guardado en el store:', this.user);
            
            // Guardar datos del usuario en localStorage para persistencia
            localStorage.setItem('user', JSON.stringify(response.user));
          }
          
          // Verificar que el token se guardó correctamente
          const storedToken = localStorage.getItem('token');
          console.log('Token guardado en localStorage:', storedToken);
          
          // Definir un flag para indicar que el usuario acaba de registrarse
          localStorage.setItem('justRegistered', 'true');
        } else {
          console.warn('No se recibió token en la respuesta del registro:', response);
        }
        
        // Cerrar el modal de registro
        this.closeRegisterModal();
        
        return response;
      } catch (error) {
        console.error('Error en el registro:', error);
        this.error = error.message || 'Error al registrar el usuario';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    async login(credentials) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await authService.login(credentials);
        
        // Guardar token en localStorage y store
        if (response.access_token || response.token) {
          const token = response.access_token || response.token;
          localStorage.setItem('token', token);
          this.token = token;
          this.user = response.user || {};
        }
        
        return response;
      } catch (error) {
        console.error('Error en login:', error);
        this.error = error.message || 'Error al iniciar sesión';
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    logout() {
      // Eliminar token del localStorage y store
      localStorage.removeItem('token');
      this.token = null;
      this.user = null;
      
      // Redireccionar a la página de login
      if (window.router) {
        window.router.push('/login');
      }
    },
    
    // Verificar si el token es válido
    checkAuth() {
      const token = localStorage.getItem('token');
      if (token) {
        this.token = token;
        return true;
      }
      return false;
    }
  }
});
