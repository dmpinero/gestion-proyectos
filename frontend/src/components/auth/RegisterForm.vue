<template>
  <div class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
    <div class="flex items-end justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
      <!-- Fondo oscuro -->
      <div class="fixed inset-0 transition-opacity bg-gray-500 bg-opacity-75" aria-hidden="true" @click="$emit('close')"></div>

      <!-- Contenido del modal -->
      <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>

      <div class="inline-block w-full max-w-md p-6 my-8 overflow-hidden text-left align-middle transition-all transform bg-white rounded-lg shadow-xl sm:my-8 sm:max-w-lg sm:w-full">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-medium leading-6 text-gray-900" id="modal-title">
            Crear una cuenta
          </h3>
          <button @click="$emit('close')" class="text-gray-400 hover:text-gray-500">
            <span class="sr-only">Cerrar</span>
            <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <form @submit.prevent="handleSubmit" class="mt-4 space-y-6">
          <div class="grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-6">
            <!-- Nombre -->
            <div class="sm:col-span-3">
              <label for="first-name" class="block text-sm font-medium text-gray-700">Nombre</label>
              <input
                v-model="formData.firstName"
                type="text"
                id="first-name"
                autocomplete="given-name"
                required
                class="block w-full px-3 py-2 mt-1 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              />
            </div>

            <!-- Apellidos -->
            <div class="sm:col-span-3">
              <label for="last-name" class="block text-sm font-medium text-gray-700">Apellidos</label>
              <input
                v-model="formData.lastName"
                type="text"
                id="last-name"
                autocomplete="family-name"
                required
                class="block w-full px-3 py-2 mt-1 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              />
            </div>

            <!-- Email -->
            <div class="sm:col-span-6">
              <label for="email" class="block text-sm font-medium text-gray-700">Correo electrónico</label>
              <input
                v-model="formData.email"
                type="email"
                id="email"
                autocomplete="email"
                required
                class="block w-full px-3 py-2 mt-1 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              />
            </div>

            <!-- Contraseña -->
            <div class="sm:col-span-3">
              <label for="password" class="block text-sm font-medium text-gray-700">Contraseña</label>
              <input
                v-model="formData.password"
                type="password"
                id="password"
                autocomplete="new-password"
                required
                minlength="8"
                class="block w-full px-3 py-2 mt-1 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              />
              <p class="mt-1 text-xs text-gray-500">Mínimo 8 caracteres</p>
            </div>

            <!-- Confirmar Contraseña -->
            <div class="sm:col-span-3">
              <label for="password-confirm" class="block text-sm font-medium text-gray-700">Confirmar contraseña</label>
              <input
                v-model="formData.passwordConfirm"
                type="password"
                id="password-confirm"
                autocomplete="new-password"
                required
                class="block w-full px-3 py-2 mt-1 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              />
            </div>

            <!-- Rol -->
            <div class="sm:col-span-6">
              <label for="role" class="block text-sm font-medium text-gray-700">Rol</label>
              <select
                v-model="formData.role"
                id="role"
                required
                class="block w-full px-3 py-2 mt-1 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              >
                <option value="">Selecciona un rol</option>
                <option value="admin">Administrador</option>
                <option value="manager">Gestor</option>
                <option value="user" selected>Usuario</option>
              </select>
            </div>
          </div>

          <!-- Espacio para mensajes adicionales si se necesitan -->
          <div class="mt-2"></div>

          <!-- Mensajes de error -->
          <div v-if="error && !emailAlreadyRegistered" class="p-4 text-sm text-red-700 bg-red-100 rounded-md">
            {{ error }}
          </div>
          
          <!-- Mensaje especial para email ya registrado -->
          <div v-if="emailAlreadyRegistered" class="p-4 text-sm bg-yellow-50 rounded-md border border-yellow-200">
            <p class="text-yellow-700 font-medium">{{ error }}</p>
            <p class="mt-2 text-yellow-600">¿Ya tienes una cuenta? Puedes iniciar sesión directamente:</p>
            <div class="mt-3">
              <button 
                type="button"
                @click="goToLogin"
                class="inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-indigo-600 border border-transparent rounded-md shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                Iniciar sesión
              </button>
            </div>
          </div>

          <!-- Botones -->
          <div class="flex justify-end mt-6 space-x-3">
            <button
              type="button"
              @click="$emit('close')"
              class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Cancelar
            </button>
            <button
              type="submit"
              :disabled="loading"
              class="inline-flex justify-center px-4 py-2 text-sm font-medium text-white bg-indigo-600 border border-transparent rounded-md shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span v-if="loading">
                <svg class="w-5 h-5 mr-2 -ml-1 text-white animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              </span>
              <span>Crear cuenta</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import authService from '../../services/authService';

export default {
  name: 'RegisterForm',
  data() {
    return {
      formData: {
        firstName: '',
        lastName: '',
        email: '',
        password: '',
        passwordConfirm: '',
        role: 'user'
      },
      loading: false,
      error: '',
      emailAlreadyRegistered: false
    }
  },
  methods: {
    goToLogin() {
      // Cerrar el modal de registro
      this.$emit('close')
      
      // Emitir evento para ir a la página de login
      this.$emit('go-to-login', this.formData.email)
    },
    async handleSubmit() {
      // Validar contraseñas coincidentes
      if (this.formData.password !== this.formData.passwordConfirm) {
        this.error = 'Las contraseñas no coinciden'
        return
      }

      this.loading = true
      this.error = ''

      try {
        // Preparar los datos para la API
        const userData = {
          email: this.formData.email,
          firstName: this.formData.firstName,
          lastName: this.formData.lastName,
          password: this.formData.password
        }

        console.log('Enviando datos de registro:', userData)

        // Llamar al servicio de autenticación para registrar al usuario
        const response = await authService.register(userData)
        console.log('Respuesta del registro:', response)
        
        if (response && response.user) {
          // Emitir evento de registro exitoso con los datos del usuario y mensaje
          this.$emit('registered', {
            email: response.user.email,
            name: `${response.user.firstName} ${response.user.lastName}`.trim(),
            message: '¡Registro exitoso! Por favor inicia sesión.'
          })
          
          // Cerrar el modal después de un breve retraso
          setTimeout(() => {
            this.$emit('close')
          }, 300)
          
          // Resetear formulario
          this.resetForm()
        } else {
          console.warn('Respuesta sin datos de usuario:', response)
          throw new Error('La respuesta del servidor no contiene datos de usuario')
        }
      } catch (error) {
        console.error('Error al registrar:', error)
        
        // Manejo detallado de errores
        if (error.response) {
          console.error('Error del servidor:', error.response)
          // Error del servidor con respuesta
          if (error.response.data && error.response.data.detail) {
            // Traducir mensajes de error comunes del backend
            if (error.response.data.detail === 'Email already registered') {
              this.error = 'El correo electrónico ya está registrado.'
              this.emailAlreadyRegistered = true
              // Resaltar el campo de email como error
              this.$refs.emailInput?.focus()
            } else {
              this.error = error.response.data.detail
            }
          } else if (error.response.status === 400) {
            this.error = 'Los datos proporcionados son inválidos. Por favor, revisa la información.'
          } else if (error.response.status === 500) {
            this.error = 'Error interno del servidor. Por favor, inténtalo más tarde.'
          } else {
            this.error = `Error del servidor: ${error.response.status}`
          }
        } else if (error.request) {
          // La petición fue hecha pero no se recibió respuesta
          console.error('No se recibió respuesta:', error.request)
          this.error = 'No se pudo conectar con el servidor. Por favor, verifica tu conexión.'
        } else {
          // Error en la configuración de la petición
          this.error = error.message || 'Error al crear la cuenta. Por favor, inténtalo de nuevo.'
        }
      } finally {
        this.loading = false
      }
    },
    resetForm() {
      this.formData = {
        firstName: '',
        lastName: '',
        email: '',
        password: '',
        passwordConfirm: '',
        role: 'user'
      }
      this.error = ''
      this.emailAlreadyRegistered = false
    }
  },
  watch: {
    show(newVal) {
      if (newVal) {
        // Resetear el formulario cuando se muestra el modal
        this.resetForm()
        document.body.style.overflow = 'hidden'
      } else {
        document.body.style.overflow = 'auto'
      }
    }
  },
  beforeUnmount() {
    document.body.style.overflow = 'auto'
  }
}
</script>
