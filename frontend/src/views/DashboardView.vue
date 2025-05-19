<template>
  <div class="min-h-screen bg-gray-100">
    <!-- Barra de navegación -->
    <nav class="bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex">
            <div class="flex-shrink-0 flex items-center">
              <span class="text-xl font-bold text-indigo-600">Gestión de Proyectos</span>
            </div>
            <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
              <router-link 
                to="/dashboard" 
                class="border-indigo-500 text-gray-900 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                active-class="border-indigo-500 text-gray-900"
                exact
              >
                Inicio
              </router-link>
              <router-link 
                to="/projects" 
                class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                active-class="border-indigo-500 text-gray-900"
              >
                Proyectos
              </router-link>
              <router-link 
                to="/tasks" 
                class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                active-class="border-indigo-500 text-gray-900"
              >
                Tareas
              </router-link>
            </div>
          </div>
          <div class="hidden sm:ml-6 sm:flex sm:items-center">
            <div class="ml-3 relative">
              <div>
                <button 
                  @click="isProfileMenuOpen = !isProfileMenuOpen" 
                  class="bg-white rounded-full flex text-sm focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500" 
                  id="user-menu" 
                  aria-expanded="false" 
                  aria-haspopup="true"
                >
                  <span class="sr-only">Abrir menú de usuario</span>
                  <div class="h-8 w-8 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-600 font-medium">
                    {{ userInitials }}
                  </div>
                </button>
              </div>
              <!-- Menú desplegable del perfil -->
              <div 
                v-show="isProfileMenuOpen" 
                ref="profileMenu"
                class="origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg py-1 bg-white ring-1 ring-black ring-opacity-5 focus:outline-none z-50" 
                role="menu" 
                aria-orientation="vertical" 
                aria-labelledby="user-menu"
                tabindex="-1"
              >
                <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100" role="menuitem" tabindex="-1" id="user-menu-item-0">Tu perfil</a>
                <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100" role="menuitem" tabindex="-1" id="user-menu-item-1">Configuración</a>
                <button 
                  @click="handleLogout" 
                  class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100" 
                  role="menuitem" 
                  tabindex="-1" 
                  id="user-menu-item-2"
                >
                  Cerrar sesión
                </button>
              </div>
            </div>
          </div>
          <div class="-mr-2 flex items-center sm:hidden">
            <!-- Mobile menu button -->
            <button 
              @click="isMobileMenuOpen = !isMobileMenuOpen" 
              class="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-500" 
              aria-expanded="false"
            >
              <span class="sr-only">Abrir menú principal</span>
              <!-- Icono de menú -->
              <svg 
                :class="{'hidden': isMobileMenuOpen, 'block': !isMobileMenuOpen}" 
                class="h-6 w-6" 
                xmlns="http://www.w3.org/2000/svg" 
                fill="none" 
                viewBox="0 0 24 24" 
                stroke="currentColor" 
                aria-hidden="true"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              </svg>
              <!-- Icono de cerrar -->
              <svg 
                :class="{'hidden': !isMobileMenuOpen, 'block': isMobileMenuOpen}" 
                class="h-6 w-6" 
                xmlns="http://www.w3.org/2000/svg" 
                fill="none" 
                viewBox="0 0 24 24" 
                stroke="currentColor" 
                aria-hidden="true"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Menú móvil -->
      <div :class="{'block': isMobileMenuOpen, 'hidden': !isMobileMenuOpen}" class="sm:hidden">
        <div class="pt-2 pb-3 space-y-1">
          <router-link 
            to="/dashboard" 
            class="bg-indigo-50 border-indigo-500 text-indigo-700 block pl-3 pr-4 py-2 border-l-4 text-base font-medium"
            active-class="bg-indigo-50 border-indigo-500 text-indigo-700"
            exact
          >
            Inicio
          </router-link>
          <router-link 
            to="/projects" 
            class="border-transparent text-gray-600 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-800 block pl-3 pr-4 py-2 border-l-4 text-base font-medium"
            active-class="bg-indigo-50 border-indigo-500 text-indigo-700"
          >
            Proyectos
          </router-link>
          <router-link 
            to="/tasks" 
            class="border-transparent text-gray-600 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-800 block pl-3 pr-4 py-2 border-l-4 text-base font-medium"
            active-class="bg-indigo-50 border-indigo-500 text-indigo-700"
          >
            Tareas
          </router-link>
        </div>
        <div class="pt-4 pb-3 border-t border-gray-200">
          <div class="flex items-center px-4">
            <div class="flex-shrink-0">
              <div class="h-10 w-10 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-600 font-medium">
                {{ userInitials }}
              </div>
            </div>
            <div class="ml-3">
              <div class="text-base font-medium text-gray-800">{{ userName }}</div>
              <div class="text-sm font-medium text-gray-500">{{ userEmail }}</div>
            </div>
          </div>
          <div class="mt-3 space-y-1">
            <a href="#" class="block px-4 py-2 text-base font-medium text-gray-500 hover:text-gray-800 hover:bg-gray-100">Tu perfil</a>
            <a href="#" class="block px-4 py-2 text-base font-medium text-gray-500 hover:text-gray-800 hover:bg-gray-100">Configuración</a>
            <button 
              @click="handleLogout" 
              class="w-full text-left px-4 py-2 text-base font-medium text-gray-500 hover:text-gray-800 hover:bg-gray-100"
            >
              Cerrar sesión
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- Contenido principal -->
    <div class="py-10">
      <header>
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h1 class="text-3xl font-bold text-gray-900">Panel de control</h1>
        </div>
      </header>
      <main>
        <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
          <!-- Contenido del dashboard -->
          <div class="px-4 py-8 sm:px-0">
            <div class="border-4 border-dashed border-gray-200 rounded-lg h-96 flex items-center justify-center">
              <p class="text-gray-500">Contenido del dashboard</p>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script>
  import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';

export default {
  name: 'DashboardView',
  setup() {
    const router = useRouter();
    const isProfileMenuOpen = ref(false);
    const isMobileMenuOpen = ref(false);
    const profileMenu = ref(null);
    
    // Datos del usuario (simulados)
    const user = {
      name: 'Juan Pérez',
      email: 'juan.perez@example.com'
    };

    // Iniciales del usuario
    const userInitials = computed(() => {
      return user.name
        .split(' ')
        .map(name => name[0])
        .join('')
        .toUpperCase()
        .substring(0, 2);
    });

    // Cerrar menú de perfil al hacer clic fuera
    const closeProfileMenu = (event) => {
      if (profileMenu.value && !profileMenu.value.contains(event.target)) {
        isProfileMenuOpen.value = false;
      }
    };

    // Agregar evento de clic global cuando el menú está abierto
    onMounted(() => {
      document.addEventListener('click', closeProfileMenu);
    });

    // Limpiar el evento al desmontar el componente
    onUnmounted(() => {
      document.removeEventListener('click', closeProfileMenu);
    });

    // Cerrar sesión
    const handleLogout = () => {
      // Eliminar datos de autenticación
      localStorage.removeItem('isAuthenticated');
      localStorage.removeItem('user');
      
      // Redirigir al login
      router.push({ name: 'Login' });
    };

    return {
      isProfileMenuOpen,
      isMobileMenuOpen,
      profileMenu,
      userName: user.name,
      userEmail: user.email,
      userInitials,
      closeProfileMenu,
      handleLogout
    };
  }
};
</script>

<style scoped>
/* Estilos específicos del dashboard */
</style>
