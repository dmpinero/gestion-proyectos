<template>
  <div id="app" class="min-h-screen flex flex-col">
    <!-- Barra de navegación -->
    <nav class="bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <!-- Logo -->
          <div class="flex-shrink-0 flex items-center">
            <router-link to="/" class="text-xl font-bold text-gray-900">
              Gestión de Proyectos
            </router-link>
          </div>
          
          <!-- Menú de navegación -->
          <div class="hidden sm:ml-6 sm:flex sm:items-center space-x-8">
            <router-link 
              to="/dashboard" 
              class="text-gray-500 hover:text-gray-700 px-3 py-2 text-sm font-medium"
              active-class="text-indigo-600 border-b-2 border-indigo-500"
              v-if="authStore.isAuthenticated"
            >
              Dashboard
            </router-link>
            <router-link 
              to="/dashboard" 
              class="text-gray-500 hover:text-gray-700 px-3 py-2 text-sm font-medium"
              active-class="text-indigo-600 border-b-2 border-indigo-500"
              v-if="authStore.isAuthenticated"
            >
              Proyectos
            </router-link>
            <router-link 
              to="/login" 
              class="text-gray-500 hover:text-gray-700 px-3 py-2 text-sm font-medium"
              active-class="text-indigo-600"
              v-if="!authStore.isAuthenticated"
            >
              Iniciar Sesión
            </router-link>
            <button 
              type="button" 
              class="ml-8 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              @click="openRegisterModal"
              v-if="!authStore.isAuthenticated"
            >
              Crear una cuenta
            </button>
            <button 
              type="button" 
              class="ml-8 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
              @click="authStore.logout()"
              v-if="authStore.isAuthenticated"
            >
              Cerrar Sesión
            </button>
          </div>
          
          <!-- Botón móvil -->
          <div class="-mr-2 flex items-center sm:hidden">
            <button 
              type="button" 
              class="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-500"
              @click="isMenuOpen = !isMenuOpen"
            >
              <span class="sr-only">Abrir menú principal</span>
              <svg 
                class="h-6 w-6" 
                xmlns="http://www.w3.org/2000/svg" 
                fill="none" 
                viewBox="0 0 24 24" 
                stroke="currentColor"
                :class="{'hidden': isMenuOpen, 'block': !isMenuOpen}"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              </svg>
              <svg 
                class="h-6 w-6" 
                xmlns="http://www.w3.org/2000/svg" 
                fill="none" 
                viewBox="0 0 24 24" 
                stroke="currentColor"
                :class="{'block': isMenuOpen, 'hidden': !isMenuOpen}"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      </div>
      
      <!-- Menú móvil -->
      <div 
        class="sm:hidden" 
        :class="{'block': isMenuOpen, 'hidden': !isMenuOpen}"
      >
        <div class="pt-2 pb-3 space-y-1">
          <router-link 
            to="/" 
            class="block px-3 py-2 text-base font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-50"
            @click.native="isMenuOpen = false"
          >
            Inicio
          </router-link>
          <router-link 
            to="/proyectos" 
            class="block px-3 py-2 text-base font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-50"
            @click.native="isMenuOpen = false"
          >
            Proyectos
          </router-link>
          <router-link 
            to="/login" 
            class="block px-3 py-2 text-base font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-50"
            @click.native="isMenuOpen = false"
          >
            Iniciar Sesión
          </router-link>
          <button 
            type="button" 
            class="block w-full text-left px-3 py-2 text-base font-medium text-indigo-600 hover:text-indigo-800 hover:bg-gray-50"
            @click="openRegisterModal"
          >
            Crear una cuenta
          </button>
        </div>
      </div>
    </nav>

    <!-- Contenido principal -->
    <main class="flex-grow">
      <router-view />
    </main>

    <!-- Pie de página -->
    <footer class="bg-white border-t border-gray-200">
      <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <p class="text-center text-sm text-gray-500">
          &copy; {{ currentYear }} Gestión de Proyectos. Todos los derechos reservados.
        </p>
      </div>
    </footer>
  </div>
</template>

<script>
import { useAuthStore } from '@/stores/authStore';

export default {
  name: 'App',
  data() {
    return {
      isMenuOpen: false
    };
  },
  setup() {
    const authStore = useAuthStore();
    return { authStore };
  },
  methods: {
    openRegisterModal() {
      this.authStore.openRegisterModal();
      this.isMenuOpen = false; // Cerrar el menú móvil si está abierto
    }
  },
  computed: {
    currentYear() {
      return new Date().getFullYear();
    }
  },
  watch: {
    $route() {
      // Cerrar el menú móvil al cambiar de ruta
      this.isMenuOpen = false;
    }
  }
}
</script>

<style>
/* Estilos globales */
#app {
  font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #1f2937;
}

/* Transiciones de página */
.page-enter-active,
.page-leave-active {
  transition: opacity 0.2s ease;
}

.page-enter-from,
.page-leave-to {
  opacity: 0;
}

/* Estilos para enlaces del router */
.router-link-active {
  color: #4f46e5;
}

/* Transiciones de página */
.page-enter-active,
.page-leave-active {
  transition: opacity 0.2s ease;
}

.page-enter-from,
.page-leave-to {
  opacity: 0;
}
</style>
