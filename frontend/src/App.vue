<template>
  <div id="app">
    <!-- Barra de navegación -->
    <nav class="navbar">
      <div class="container">
        <router-link to="/" class="logo">Gestión de Proyectos</router-link>
        <div class="nav-links">
          <router-link to="/">Inicio</router-link>
          <router-link to="/proyectos">Proyectos</router-link>
          <router-link to="/login" class="btn btn-outline">Iniciar Sesión</router-link>
          <router-link to="/registro" class="btn btn-primary">Registrarse</router-link>
        </div>
      </div>
    </nav>

    <!-- Contenido principal -->
    <main class="main-content">
      <router-view />
    </main>

    <!-- Pie de página -->
    <footer class="footer">
      <div class="container">
        <p>&copy; {{ currentYear }} Gestión de Proyectos. Todos los derechos reservados.</p>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App',
  computed: {
    currentYear() {
      return new Date().getFullYear();
    }
  }
}
</script>

<style>
/* Estilos globales */
#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* Barra de navegación */
.navbar {
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  padding: 1rem 0;
  position: sticky;
  top: 0;
  z-index: 1000;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
  color: var(--primary-color);
  text-decoration: none;
}

.nav-links {
  display: flex;
  gap: 1.5rem;
  align-items: center;
}

.nav-links a {
  color: var(--dark-color);
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s ease;
}

.nav-links a:hover {
  color: var(--primary-color);
  text-decoration: none;
}

/* Contenido principal */
.main-content {
  flex: 1;
  padding: 2rem 0;
}

/* Pie de página */
.footer {
  background-color: var(--dark-color);
  color: white;
  padding: 1.5rem 0;
  text-align: center;
  margin-top: auto;
}

.footer p {
  margin: 0;
  color: rgba(255, 255, 255, 0.8);
}

/* Estilos responsivos */
@media (max-width: 768px) {
  .container {
    flex-direction: column;
    gap: 1rem;
  }
  
  .nav-links {
    flex-direction: column;
    width: 100%;
    gap: 0.5rem;
  }
  
  .nav-links a {
    width: 100%;
    text-align: center;
    padding: 0.5rem 0;
  }
}
</style>
