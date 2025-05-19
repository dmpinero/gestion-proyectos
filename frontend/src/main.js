import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'

// Importar estilos globales
import './assets/main.css'

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
      name: 'Home',
      component: () => import('./views/HomeView.vue')
    },
    // Otras rutas se agregarán aquí
  ]
})

app.use(router)

// Montar la aplicación
app.mount('#app')

// Exportar la aplicación para pruebas
export { app, router }
