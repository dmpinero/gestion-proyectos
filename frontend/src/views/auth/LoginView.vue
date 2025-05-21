<template>
  <div>
    <AuthLayout
      title="Iniciar Sesión"
      subtitle="Ingresa tus credenciales para acceder a tu cuenta"
      link-text="¿No tienes una cuenta?"
      @link-click="openRegisterModal"
    >
    <form @submit.prevent="handleLogin" class="space-y-6">
      <!-- Mensaje de error general -->
      <div v-if="errors.form" class="bg-red-50 border-l-4 border-red-400 p-4">
        <div class="flex">
          <div class="flex-shrink-0">
            <svg class="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
            </svg>
          </div>
          <div class="ml-3">
            <p class="text-sm text-red-700">
              {{ errors.form }}
            </p>
          </div>
        </div>
      </div>

      <!-- Email -->
      <div>
        <label for="email" class="block text-sm font-medium text-gray-700">
          Correo Electrónico
        </label>
        <div class="mt-1 relative rounded-md shadow-sm">
          <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <svg class="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z" />
              <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z" />
            </svg>
          </div>
          <input
            id="email"
            v-model="email"
            type="email"
            autocomplete="email"
            required
            class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            :class="{ 'border-red-300 text-red-900 placeholder-red-300 focus:ring-red-500 focus:border-red-500': errors.email }"
            placeholder="tu@email.com"
          />
        </div>
        <p v-if="errors.email" class="mt-2 text-sm text-red-600">{{ errors.email }}</p>
      </div>

      <!-- Contraseña -->
      <div>
        <div class="flex justify-between">
          <label for="password" class="block text-sm font-medium text-gray-700">
            Contraseña
          </label>
          <div class="text-sm">
            <router-link to="/forgot-password" class="font-medium text-indigo-600 hover:text-indigo-500">
              ¿Olvidaste tu contraseña?
            </router-link>
          </div>
        </div>
        <div class="mt-1 relative rounded-md shadow-sm">
          <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <svg class="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clip-rule="evenodd" />
            </svg>
          </div>
          <input
            id="password"
            v-model="password"
            :type="showPassword ? 'text' : 'password'"
            autocomplete="current-password"
            required
            class="block w-full pl-10 pr-10 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            :class="{ 'border-red-300 text-red-900 placeholder-red-300 focus:ring-red-500 focus:border-red-500': errors.password }"
            placeholder="••••••••"
          />
          <div class="absolute inset-y-0 right-0 pr-3 flex items-center">
            <button
              type="button"
              class="text-gray-500 hover:text-gray-700 focus:outline-none"
              @click="showPassword = !showPassword"
            >
              <svg v-if="!showPassword" class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
                <path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd" />
              </svg>
              <svg v-else class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M3.707 2.293a1 1 0 00-1.414 1.414l14 14a1 1 0 001.414-1.414l-1.473-1.473A10.014 10.014 0 0019.542 10C18.268 5.943 14.478 3 10 3a9.958 9.958 0 00-4.512 1.074l-1.78-1.781zm4.261 4.26l1.514 1.515a2.003 2.003 0 012.45 2.45l1.514 1.514a4 4 0 00-5.478-5.478z" clip-rule="evenodd" />
                <path d="M12.454 16.697L9.75 13.992a4 4 0 01-3.742-3.741L2.335 6.578A9.98 9.98 0 00.458 10c1.274 4.057 5.065 7 9.542 7 .847 0 1.669-.105 2.454-.303z" />
              </svg>
            </button>
          </div>
        </div>
        <p v-if="errors.password" class="mt-2 text-sm text-red-600">{{ errors.password }}</p>
      </div>

      <!-- Recordar sesión -->
      <div class="flex items-center justify-between">
        <div class="flex items-center">
          <input
            id="remember-me"
            v-model="rememberMe"
            type="checkbox"
            class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
          />
          <label for="remember-me" class="ml-2 block text-sm text-gray-900">
            Recordar mi sesión
          </label>
        </div>
      </div>

      <!-- Botón de envío -->
      <div>
        <button
          type="submit"
          class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          :class="{ 'opacity-75 cursor-not-allowed': isLoading }"
          :disabled="isLoading"
        >
          <svg v-if="isLoading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span v-else>Iniciar Sesión</span>
        </button>
      </div>
      <!-- Botón directo para registro (alternativa) -->
      <div class="mt-6 text-center">
        <button 
          type="button" 
          @click="openRegisterModal" 
          class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          Crear una cuenta
        </button>
      </div>
    </form>
    </AuthLayout>

    <!-- Componente RegisterForm (ya incluye su propia implementación de modal) -->
    <RegisterForm
      v-if="authStore.showRegisterModal"
      @close="authStore.closeRegisterModal()"
      @success="handleRegistrationSuccess"
    />
  </div>
</template>

<script>
import { ref } from 'vue';
import { useAuthStore } from '@/stores/authStore';
import AuthLayout from '@/components/auth/AuthLayout.vue';
import RegisterForm from '@/components/auth/RegisterForm.vue';

export default {
  name: 'LoginView',
  components: {
    AuthLayout,
    RegisterForm
  },
  setup() {
    const authStore = useAuthStore();
    const email = ref('')
    const password = ref('')
    const rememberMe = ref(false)
    const showPassword = ref(false)
    const errors = ref({
      form: null,
      email: null,
      password: null
    })
    const isLoading = ref(false)

    return {
      authStore,
      email,
      password,
      rememberMe,
      showPassword,
      errors,
      isLoading
    }
  },
  methods: {
    openRegisterModal() {
      // Usar el store para mostrar el modal
      this.authStore.openRegisterModal();
    },
    validateForm() {
      this.errors = {
        form: null,
        email: null,
        password: null
      };

      if (!this.email) {
        this.errors.email = 'El correo electrónico es obligatorio';
        return false;
      }

      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(this.email)) {
        this.errors.email = 'Por favor ingresa un correo electrónico válido';
        return false;
      }

      if (!this.password) {
        this.errors.password = 'La contraseña es obligatoria';
        return false;
      }

      return true;
    },
    async handleLogin() {
      if (!this.validateForm()) return;

      this.isLoading = true;
      this.errors.form = null;

      try {
        // Usar el store de autenticación para iniciar sesión
        const credentials = {
          email: this.email,
          password: this.password
        };
        
        console.log('Intentando iniciar sesión con:', this.email);
        
        // Llamar al método login del store
        await this.authStore.login(credentials);
        
        // Si llegamos aquí, el login fue exitoso
        console.log('Login exitoso, redirigiendo al dashboard');
        
        // Guardar email si se seleccionó recordar
        if (this.rememberMe) {
          localStorage.setItem('savedEmail', this.email);
        } else {
          localStorage.removeItem('savedEmail');
        }
        
        // Redirigir al dashboard
        this.$router.push('/dashboard');
      } catch (error) {
        console.error('Error en el inicio de sesión:', error);
        
        // Manejo detallado de errores
        if (error.response) {
          if (error.response.status === 401) {
            this.errors.form = 'Credenciales inválidas. Por favor, verifica tu correo y contraseña.';
          } else if (error.response.data && error.response.data.detail) {
            this.errors.form = error.response.data.detail;
          } else {
            this.errors.form = `Error del servidor: ${error.response.status}`;
          }
        } else if (error.message) {
          this.errors.form = error.message;
        } else {
          this.errors.form = 'Ocurrió un error al iniciar sesión. Por favor, inténtalo de nuevo.';
        }
      } finally {
        this.isLoading = false;
      }
    },
    handleRegistrationSuccess(userData) {
      // Mostrar mensaje de éxito
      this.errors.form = null;
      this.authStore.closeRegisterModal();
      
      // Usar el mensaje del objeto userData si existe, o un mensaje predeterminado
      const message = userData && userData.message ? userData.message : '¡Registro exitoso! Por favor inicia sesión.';
      
      // Verificar que $toast esté disponible antes de usarlo
      if (this.$toast) {
        this.$toast.success(message);
      } else {
        console.log('Mensaje de éxito:', message);
        // Alternativa si $toast no está disponible
        alert(message);
      }
    }
  },
  mounted() {
    // Verificar si hay un mensaje en la URL
    const urlParams = new URLSearchParams(window.location.search);
    const message = urlParams.get('message');
    const registered = urlParams.get('registered');
    const email = urlParams.get('email');
    
    if (message) {
      this.$toast.info(message);
    }
    
    // Si el usuario viene de un registro exitoso, mostrar un mensaje de bienvenida
    if (registered === 'true') {
      this.$toast.success('¡Registro exitoso! Ahora puedes iniciar sesión con tus credenciales.');
      
      // Si tenemos el email, prellenarlo en el formulario
      if (email) {
        this.formData.email = email;
      }
    } else {
      // Si no hay email en la URL, usar el guardado en localStorage
      const savedEmail = localStorage.getItem('savedEmail');
      if (savedEmail) {
        this.email = savedEmail;
        this.rememberMe = true;
      }
    }
  },
  beforeUnmount() {
    // Limpiar el body style cuando el componente se desmonte
    document.body.style.overflow = 'auto';
  }
}
</script>

<style scoped>
/* Estilos específicos del componente */
.modal-wrapper {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 50;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
