# Gestión de Proyectos - Frontend

Aplicación web para la gestión de proyectos desarrollada con Vue 3, Vite, Tailwind CSS y Pinia.

## Características

- Autenticación de usuarios (login/registro)
- Dashboard interactivo
- Diseño responsivo con Tailwind CSS
- Gestión de estado con Pinia
- Enrutamiento con Vue Router
- Validación de formularios
- Pruebas E2E con Cypress

## Requisitos previos

- Node.js (versión 16 o superior)
- npm (versión 9 o superior) o yarn

## Instalación

1. Clona el repositorio:
   ```bash
   git clone <url-del-repositorio>
   cd gestion-proyectos/frontend
   ```

2. Instala las dependencias:
   ```bash
   npm install
   # o si usas yarn
   yarn install
   ```

3. Dependencias adicionales para la conexión con el backend:
   ```bash
   npm install axios pinia@^2.1.7 vue-toastification@next
   # o si usas yarn
   yarn add axios pinia@^2.1.7 vue-toastification@next
   ```

## Ejecución

### Desarrollo

```bash
cd frontend
npm run dev
# o si usas yarn
yarn dev
```

La aplicación estará disponible en: http://localhost:3000

### Producción

```bash
npm run build
npm run preview
# o si usas yarn
yarn build
yarn preview
```

## Pruebas

### Ejecutar pruebas E2E con Cypress

```bash
npm run cypress:open
# o si usas yarn
yarn cypress:open
```

## Estructura del proyecto

```
src/
├── assets/          # Archivos estáticos (CSS, imágenes)
├── components/      # Componentes reutilizables
│   └── auth/        # Componentes de autenticación
├── router/          # Configuración de rutas
├── services/        # Servicios para comunicación con API
├── stores/          # Stores de Pinia para gestión de estado
├── views/           # Vistas/páginas de la aplicación
│   └── auth/        # Vistas de autenticación
├── App.vue          # Componente raíz
└── main.js          # Punto de entrada de la aplicación
```

## Notas sobre Cypress

Si experimentas problemas con Cypress, asegúrate de:

1. Usar Node.js versión 16 o superior
2. Verificar que los archivos de configuración de Cypress usen sintaxis CommonJS (require) en lugar de ES modules (import)
3. Simplificar la configuración de Cypress eliminando opciones complejas

Para más información, consulta la documentación oficial de Cypress: https://docs.cypress.io/
