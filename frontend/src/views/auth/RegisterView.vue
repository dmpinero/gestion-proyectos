<template>
  <AuthLayout
    title="Crear una cuenta"
    subtitle="Completa el formulario para registrarte"
    link-text="¿Ya tienes una cuenta?"
    link-label="Inicia sesión"
    :link-to="{ name: 'Login' }"
  >
    <form @submit.prevent="handleRegister" class="space-y-6">
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

      <!-- Nombre -->
      <div>
        <label for="name" class="block text-sm font-medium text-gray-700">
          Nombre completo
        </label>
        <div class="mt-1 relative rounded-md shadow-sm">
          <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <svg class="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
            </svg>
          </div>
          <input
            id="name"
            v-model="name"
            type="text"
            autocomplete="name"
            required
            class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            :class="{ 'border-red-300 text-red-900 placeholder-red-300 focus:ring-red-500 focus:border-red-500': errors.name }"
            placeholder="Juan Pérez"
          />
        </div>
        <p v-if="errors.name" class="mt-2 text-sm text-red-600">{{ errors.name }}</p>
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
        <label for="password" class="block text-sm font-medium text-gray-700">
          Contraseña
        </label>
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
            autocomplete="new-password"
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
              aria-label="Toggle password visibility"
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

      <!-- Confirmar Contraseña -->
      <div>
        <label for="password_confirmation" class="block text-sm font-medium text-gray-700">
          Confirmar Contraseña
        </label>
        <div class="mt-1 relative rounded-md shadow-sm">
          <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <svg class="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clip-rule="evenodd" />
            </svg>
          </div>
          <input
            id="password_confirmation"
            v-model="passwordConfirmation"
            :type="showPasswordConfirmation ? 'text' : 'password'"
            autocomplete="new-password"
            required
            class="block w-full pl-10 pr-10 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            :class="{ 'border-red-300 text-red-900 placeholder-red-300 focus:ring-red-500 focus:border-red-500': errors.passwordConfirmation }"
            placeholder="••••••••"
          />
          <div class="absolute inset-y-0 right-0 pr-3 flex items-center">
            <button
              type="button"
              class="text-gray-500 hover:text-gray-700 focus:outline-none"
              @click="showPasswordConfirmation = !showPasswordConfirmation"
              aria-label="Toggle password confirmation visibility"
            >
              <svg v-if="!showPasswordConfirmation" class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
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
        <p v-if="errors.passwordConfirmation" class="mt-2 text-sm text-red-600">{{ errors.passwordConfirmation }}</p>
      </div>

      <!-- Términos y condiciones -->
      <div class="flex items-start">
        <div class="flex items-center h-5">
          <input
            id="terms"
            v-model="termsAccepted"
            type="checkbox"
            required
            class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
          />
        </div>
        <div class="ml-3 text-sm">
          <label for="terms" class="font-medium text-gray-700">Acepto los </label>
          <a href="#" class="text-indigo-600 hover:text-indigo-500">términos y condiciones</a>
          <p v-if="errors.termsAccepted" class="mt-1 text-sm text-red-600">{{ errors.termsAccepted }}</p>
        </div>
      </div>

      <!-- Botón de envío -->
      <div>
        <button
          type="submit"
          class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          :class="{ 'opacity-75 cursor-not-allowed': loading }"
          :disabled="loading"
        >
          <svg v-if="loading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span v-else>Crear cuenta</span>
        </button>
      </div>
    </form>
  </AuthLayout>
</template>

<script>
import AuthLayout from '@/components/auth/AuthLayout.vue';

export default {
  name: 'RegisterView',
  components: {
    AuthLayout
  },
  data() {
    return {
      name: '',
      email: '',
      password: '',
      passwordConfirmation: '',
      termsAccepted: false,
      showPassword: false,
      showPasswordConfirmation: false,
      loading: false,
      errors: {
        form: '',
        name: '',
        email: '',
        password: '',
        passwordConfirmation: '',
        termsAccepted: ''
      }
    };
  },
  methods: {
    validateForm() {
      let isValid = true;
      this.errors = { 
        form: '',
        name: '',
        email: '',
        password: '',
        passwordConfirmation: '',
        termsAccepted: ''
      };

      // Validar nombre
      if (!this.name) {
        this.errors.name = 'El nombre es obligatorio';
        isValid = false;
      } else if (this.name.length < 3) {
        this.errors.name = 'El nombre debe tener al menos 3 caracteres';
        isValid = false;
      }

      // Validar email
      if (!this.email) {
        this.errors.email = 'El correo electrónico es obligatorio';
        isValid = false;
      } else if (!/\S+@\S+\.\S+/.test(this.email)) {
        this.errors.email = 'Por favor ingresa un correo electrónico válido';
        isValid = false;
      }

      // Validar contraseña
      if (!this.password) {
        this.errors.password = 'La contraseña es obligatoria';
        isValid = false;
      } else if (this.password.length < 8) {
        this.errors.password = 'La contraseña debe tener al menos 8 caracteres';
        isValid = false;
      } else if (!/(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+/.test(this.password)) {
        this.errors.password = 'La contraseña debe contener al menos una mayúscula, una minúscula y un número';
        isValid = false;
      }

      // Validar confirmación de contraseña
      if (this.password !== this.passwordConfirmation) {
        this.errors.passwordConfirmation = 'Las contraseñas no coinciden';
        isValid = false;
      }

      // Validar términos y condiciones
      if (!this.termsAccepted) {
        this.errors.termsAccepted = 'Debes aceptar los términos y condiciones';
        isValid = false;
      }

      return isValid;
    },
    async handleRegister() {
      if (!this.validateForm()) {
        return;
      }

      this.loading = true;
      this.errors.form = '';

      try {
        // Simulamos una petición de registro
        await new Promise((resolve, reject) => {
          setTimeout(() => {
            // Simulamos un registro exitoso
            if (this.email && this.password) {
              resolve();
            } else {
              reject(new Error('Error al crear la cuenta. Por favor, inténtalo de nuevo.'));
            }
          }, 1500);
        });

        // Mostrar mensaje de éxito y redirigir al login
        this.$router.push({ 
          name: 'Login', 
          query: { registered: 'true' } 
        });
      } catch (error) {
        console.error('Error al registrar:', error);
        this.errors.form = error.message || 'Error al crear la cuenta. Por favor, inténtalo de nuevo.';
      } finally {
        this.loading = false;
      }
    }
  },
  mounted() {
    // Si hay un parámetro de registro exitoso, mostramos un mensaje
    if (this.$route.query.registered === 'true') {
      this.$toast.success('¡Registro exitoso! Por favor inicia sesión.');
    }
  }
};
</script>

<style scoped>
/* Estilos específicos del componente */
</style>
