# Gestión de Proyectos

Aplicación para la gestión de proyectos y tareas desarrollada con Vue.js 3 (frontend) y FastAPI (backend).

## 🚀 Características

- **Frontend**: Vue.js 3 con Composition API, Vue Router y Pinia
- **Backend**: FastAPI con SQLAlchemy
- **Base de datos**: SQLite (desarrollo) / PostgreSQL (producción)
- **Autenticación**: JWT
- **Pruebas**: Unitarias, de integración y E2E

## 🛠️ Requisitos

- Python 3.8+
- Node.js 16+
- npm o yarn

## 🚀 Instalación

### Backend

1. Crear y activar entorno virtual:
   ```bash
   python -m venv venv
   # En Windows:
   .\venv\Scripts\activate
   # En Unix/macOS:
   source venv/bin/activate
   ```

2. Instalar dependencias:
   ```bash
   pip install -r backend/requirements.txt
   ```

3. Configurar variables de entorno (crear archivo `.env` en la raíz del proyecto):
   ```
   DATABASE_URL=sqlite:///./gestion_proyectos.db
   SECRET_KEY=tu_clave_secreta_aqui
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

4. Iniciar el servidor de desarrollo:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

### Frontend

1. Instalar dependencias:
   ```bash
   cd frontend
   npm install
   ```

2. Iniciar el servidor de desarrollo:
   ```bash
   npm run dev
   ```

## 🧪 Ejecutar pruebas

### Backend
```bash
# Todas las pruebas
pytest

# Con cobertura
pytest --cov=app

# Pruebas BDD
behave
```

### Frontend
```bash
# Pruebas unitarias
npm run test:unit

# Pruebas E2E (interfaz gráfica)
npm run test:e2e

# Pruebas E2E (consola)
npm run test:e2e:ci
```

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor, lee nuestras [pautas de contribución](CONTRIBUTING.md) antes de enviar un pull request.
