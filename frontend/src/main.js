import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'

// Importar estilos globales
import './assets/tailwind.css'

// Importar vistas
import LoginView from '@/views/auth/LoginView.vue'
import RegisterView from '@/views/auth/RegisterView.vue'
import DashboardView from '@/views/DashboardView.vue'

// Configuración de la aplicación
const app = createApp(App)

// Usar Pinia para el manejo de estado
const pinia = createPinia()
app.use(pinia)

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

// Guardia de navegación
router.beforeEach((to, from, next) => {
  // Verificar si la ruta requiere autenticación
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const isAuthenticated = localStorage.getItem('isAuthenticated');
  
  if (requiresAuth && !isAuthenticated) {
    // Redirigir al login si la ruta requiere autenticación y el usuario no está autenticado
    next({ name: 'Login', query: { redirect: to.fullPath } });
  } else if ((to.name === 'Login' || to.name === 'Register') && isAuthenticated) {
    // Redirigir al dashboard si el usuario ya está autenticado y trata de acceder al login o registro
    next({ name: 'Dashboard' });
  } else {
    // Continuar con la navegación normal
    next();
  }
});

// Usar el router
app.use(router);

// Montar la aplicación
app.mount('#app');

// Exportar la aplicación para pruebas
export { app, router }
