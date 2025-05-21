import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css'
import App from './App.vue'

// Importar estilos globales
import './assets/tailwind.css'
import './assets/main.css'

// Importar vistas
import LoginView from '@/views/auth/LoginView.vue'
import RegisterView from '@/views/auth/RegisterView.vue'
import RegisterSuccessView from '@/views/auth/RegisterSuccessView.vue'
import DashboardView from '@/views/DashboardView.vue'

// Configuración de toast
const toastOptions = {
  position: 'top-right',
  timeout: 5000,
  closeOnClick: true,
  pauseOnFocusLoss: true,
  pauseOnHover: true,
  draggable: true,
  draggablePercent: 0.6,
  showCloseButtonOnHover: false,
  hideProgressBar: false,
  closeButton: 'button',
  icon: true,
  rtl: false
}

// Configuración de la aplicación
const app = createApp(App)

// Usar Pinia para el manejo de estado
const pinia = createPinia()
app.use(pinia)

// Usar Toast para notificaciones
app.use(Toast, toastOptions)

// Configuración del router
const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/login'
    },
    {
      path: '/login',
      name: 'Login',
      component: LoginView,
      meta: { requiresAuth: false }
    },
    {
      path: '/register',
      name: 'Register',
      component: RegisterView,
      meta: { requiresAuth: false }
    },
    {
      path: '/register-success',
      name: 'RegisterSuccess',
      component: RegisterSuccessView,
      meta: { requiresAuth: false }
    },
    {
      path: '/dashboard',
      name: 'Dashboard',
      component: DashboardView,
      meta: { requiresAuth: true }
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/login'
    }
  ]
})

// Función para verificar si el token es válido
const isAuthenticated = () => {
  const token = localStorage.getItem('token');
  console.log('Verificando autenticación, token:', token);
  
  // Aquí podrías agregar lógica para verificar si el token ha expirado
  // Por ahora, simplemente verificamos que exista
  return !!token;
};

// Guardia de navegación
router.beforeEach((to, from, next) => {
  // Verificar si hay un flag de registro exitoso
  const justRegistered = localStorage.getItem('justRegistered') === 'true';
  
  // Si el usuario acaba de registrarse y va al dashboard, permitir el acceso
  if (justRegistered && to.name === 'Dashboard') {
    console.log('Usuario recién registrado, permitiendo acceso al dashboard');
    // Limpiar el flag después de usarlo
    localStorage.removeItem('justRegistered');
    return next();
  }
  
  // Verificar si la ruta requiere autenticación
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const isUserAuthenticated = isAuthenticated();
  
  console.log('Guardia de navegación:', {
    ruta: to.path,
    requiresAuth,
    isUserAuthenticated,
    justRegistered
  });
  
  if (requiresAuth && !isUserAuthenticated) {
    // Redirigir al login si la ruta requiere autenticación y el usuario no está autenticado
    next({ 
      name: 'Login', 
      query: { 
        redirect: to.fullPath,
        message: 'Por favor inicia sesión para acceder a esta página'
      } 
    });
  } else if ((to.name === 'Login' || to.name === 'Register') && isUserAuthenticated) {
    // Redirigir al dashboard si el usuario ya está autenticado y trata de acceder al login o registro
    next({ name: 'Dashboard' });
  } else {
    // Continuar con la navegación normal
    next();
  }
});

// Hacer que el router esté disponible globalmente
window.router = router

// Usar el router
app.use(router)

// Montar la aplicación
app.mount('#app');

// Exportar la aplicación para pruebas
export { app, router }
