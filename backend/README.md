# Backend - Gestión de Proyectos

Backend desarrollado con FastAPI para la aplicación de gestión de proyectos.

## 🚀 Características

- **Framework**: FastAPI
- **Base de datos**: MySQL
- **ORM**: SQLAlchemy
- **Autenticación**: JWT
- **Migraciones**: Alembic
- **Documentación automática**: Swagger UI y ReDoc

## 🛠️ Configuración

### Requisitos

- Python 3.8+
- MySQL 8.0+
- pip

### Instalación

1. Clonar el repositorio
2. Crear y activar entorno virtual:
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # Unix/macOS
   source venv/bin/activate
   ```

3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Configurar variables de entorno (crear archivo `.env` en la raíz del backend):
   ```env
   DEBUG=True
   DATABASE_URL=mysql+pymysql://usuario:contraseña@localhost:3306/nombre_bd?charset=utf8mb4
   SECRET_KEY=tu_clave_secreta
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   CORS_ORIGINS=http://localhost:3000,http://localhost:8000
   ```

5. Inicializar la base de datos:
   ```bash
   # Crear tablas
   python -m scripts.db_utils.create_tables
   
   # O aplicar migraciones con Alembic
   alembic upgrade head
   ```

## 🚀 Ejecución

```bash
uvicorn main:app --reload
```

La documentación interactiva estará disponible en:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📁 Estructura del proyecto

```
backend/
├── alembic/               # Migraciones de la base de datos
├── app/                   # Código fuente de la aplicación
│   ├── api/               # Endpoints de la API
│   ├── core/              # Configuración y utilidades
│   ├── db/                # Configuración de la base de datos
│   ├── models/            # Modelos de SQLAlchemy
│   └── schemas/           # Esquemas Pydantic
├── scripts/               # Scripts de utilidad
│   ├── checks/           # Scripts de verificación
│   ├── db_utils/         # Utilidades de base de datos
│   └── tests/            # Pruebas manuales
├── tests/                 # Pruebas automatizadas
├── .env.example          # Plantilla de variables de entorno
├── alembic.ini           # Configuración de Alembic
├── main.py               # Punto de entrada de la aplicación
├── requirements.txt      # Dependencias principales
└── requirements-test.txt # Dependencias de prueba
```

## 🧪 Pruebas

### Pruebas unitarias

```bash
pytest
```

### Cobertura de pruebas

```bash
pytest --cov=app tests/
```

## 📝 Licencia

Este proyecto está bajo la licencia MIT. Ver el archivo `LICENSE` para más detalles.
