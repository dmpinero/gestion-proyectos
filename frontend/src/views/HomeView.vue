<template>
  <div class="home">
    <header class="header">
      <h1>Bienvenido a Gestión de Proyectos</h1>
      <p class="lead">Una aplicación para gestionar tus proyectos y tareas de manera eficiente</p>
    </header>

    <main class="main-content">
      <section class="features">
        <h2>Características principales</h2>
        <div class="feature-list">
          <div class="feature-card">
            <h3>Gestión de Proyectos</h3>
            <p>Crea y organiza tus proyectos de manera sencilla.</p>
          </div>
          <div class="feature-card">
            <h3>Tareas</h3>
            <p>Administra las tareas de cada proyecto.</p>
          </div>
          <div class="feature-card">
            <h3>Colaboración</h3>
            <p>Trabaja en equipo de manera efectiva.</p>
          </div>
        </div>
      </section>

      <section class="cta">
        <h2>¿Listo para comenzar?</h2>
        <p>Inicia sesión o crea una cuenta para acceder a todas las funciones.</p>
        <div class="cta-buttons">
          <router-link to="/login" class="btn btn-primary">Iniciar Sesión</router-link>
          <button @click="openRegisterModal" class="btn btn-outline">Crear una cuenta</button>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
import { useAuthStore } from '@/stores/authStore';

export default {
  name: 'HomeView',
  setup() {
    const authStore = useAuthStore();
    return { authStore };
  },
  methods: {
    openRegisterModal() {
      this.authStore.openRegisterModal();
    }
  }
}
</script>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.header {
  text-align: center;
  margin-bottom: 3rem;
  padding: 2rem 0;
  border-bottom: 1px solid #eee;
}

.header h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  color: var(--primary-color);
}

.lead {
  font-size: 1.25rem;
  color: var(--secondary-color);
  max-width: 700px;
  margin: 0 auto;
}

.features {
  margin-bottom: 4rem;
}

.features h2 {
  text-align: center;
  margin-bottom: 2rem;
}

.feature-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.feature-card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.feature-card h3 {
  color: var(--primary-color);
  margin-bottom: 0.5rem;
}

.cta {
  text-align: center;
  background: white;
  padding: 3rem 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.cta h2 {
  margin-bottom: 1rem;
}

.cta p {
  margin-bottom: 2rem;
  color: var(--secondary-color);
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.cta-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.btn-outline {
  background: transparent;
  border: 1px solid var(--primary-color);
  color: var(--primary-color);
}

.btn-outline:hover {
  background-color: rgba(74, 111, 165, 0.1);
  text-decoration: none;
}
</style>
