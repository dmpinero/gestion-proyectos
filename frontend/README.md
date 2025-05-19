# Gestión de Proyectos - Frontend

Aplicación web para la gestión de proyectos desarrollada con Vue 3, Vite, Tailwind CSS y Pinia.

## Características

- Autenticación de usuarios (login/registro)
- Dashboard interactivo
- Diseño responsivo con Tailwind CSS
- Gestión de estado con Pinia
- Enrutamiento con Vue Router
- Validación de formularios

## Requisitos previos

- Node.js (versión 16 o superior)
- npm (versión 9 o superior) o yarn

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/gestion-proyectos.git
   cd gestion-proyectos/frontend
   ```

2. Instala las dependencias:
   ```bash
   npm install
   # o
   yarn
   ```

## Configuración

1. Copia el archivo de variables de entorno de ejemplo:
   ```bash
   cp .env.example .env
   ```

2. Configura las variables de entorno en el archivo `.env`.

## Desarrollo

Para iniciar el servidor de desarrollo:

```bash
npm run dev
# o
yarn dev
```

La aplicación estará disponible en [http://localhost:3000](http://localhost:3000).

## Construcción para producción

Para crear una versión optimizada para producción:

```bash
npm run build
# o
yarn build
```

Los archivos generados se guardarán en el directorio `dist/`.

## Estructura del proyecto

```
src/
├── assets/          # Archivos estáticos (imágenes, fuentes, etc.)
├── components/      # Componentes reutilizables
├── composables/     # Composable functions
├── router/          # Configuración del enrutador
├── stores/          # Stores de Pinia
├── styles/          # Estilos globales
├── utils/           # Utilidades y helpers
└── views/           # Vistas/páginas
```

## Tecnologías utilizadas

- [Vue 3](https://v3.vuejs.org/)
- [Vite](https://vitejs.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Pinia](https://pinia.vuejs.org/)
- [Vue Router](https://router.vuejs.org/)
- [Headless UI](https://headlessui.dev/) (opcional)

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más información.
