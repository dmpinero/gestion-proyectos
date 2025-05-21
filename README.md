# 🚀 Gestión de Proyectos

Aplicación web para la gestión de proyectos y tareas desarrollada con Vue.js 3 (frontend) y FastAPI (backend).

## 🌟 Características Principales

### Frontend
- **Framework**: Vue.js 3 con Composition API
- **Estado**: Pinia
- **Enrutamiento**: Vue Router
- **Estilos**: Tailwind CSS
- **Componentes UI**: Headless UI
- **Iconos**: Heroicons
- **Bundler**: Vite 4.x

### Backend
- **Framework**: FastAPI
- **Base de datos**: SQLite (desarrollo) / MySQL (producción)
- **ORM**: SQLAlchemy 2.0
- **Autenticación**: JWT (JSON Web Tokens)
- **Migraciones**: Alembic
- **Documentación**: Swagger UI y ReDoc integrados
- **Validación de datos**: Pydantic v2

## 📋 Requisitos

- **Backend**:
  - Python 3.10+
  - SQLite3 (incluido en Python)
  - MySQL 8.0+ (opcional para producción)
  - pip (gestor de paquetes de Python)
  - Poetry (recomendado) o pip para gestión de dependencias

- **Frontend**:
  - Node.js 18+ (LTS)
  - npm 9+ o yarn 1.22+
  - Vite 4.x

## 🏗️ Estructura del Proyecto

```
gestion-proyectos/
├── backend/                  # Código del backend (FastAPI)
│   ├── alembic/             # Migraciones de base de datos
│   ├── app/                  # Código de la aplicación
│   │   ├── api/              # Endpoints de la API
│   │   ├── core/             # Configuración y utilidades centrales
│   │   ├── db/               # Configuración de base de datos
│   │   └── models/           # Modelos de SQLAlchemy
│   ├── scripts/              # Scripts de utilidad
│   │   ├── checks/           # Scripts de verificación
│   │   ├── db_utils/         # Utilidades de base de datos
│   │   └── tests/            # Pruebas y depuración
│   ├── .env.example          # Plantilla de variables de entorno
│   ├── alembic.ini           # Configuración de Alembic
│   ├── main.py               # Punto de entrada de la aplicación
│   └── requirements.txt      # Dependencias de Python
├── frontend/                 # Código del frontend (Vue 3)
│   ├── public/               # Archivos estáticos
│   ├── src/                  # Código fuente
│   │   ├── assets/           # Recursos estáticos
│   │   ├── components/       # Componentes Vue
│   │   ├── router/          # Configuración de rutas
│   │   ├── stores/          # Tiendas Pinia
│   │   └── views/           # Vistas/páginas
│   ├── .env.development     # Variables de entorno de desarrollo
│   ├── index.html           # Página principal
│   ├── package.json         # Dependencias y scripts
│   └── vite.config.js       # Configuración de Vite
├── .gitignore               # Archivos ignorados por Git
└── README.md                # Este archivo
```

## 🚀 Instalación Rápida

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/gestion-proyectos.git
cd gestion-proyectos
```

### 2. Configuración del Backend

```bash
# Navegar al directorio del backend
cd backend

# Crear y activar entorno virtual (recomendado)
python -m venv venv
# Windows
.\venv\Scripts\activate
# Unix/macOS
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar el archivo .env con tu configuración

# Inicializar la base de datos (SQLite por defecto)
python -m scripts.db_utils.create_tables

# O si prefieres usar migraciones con Alembic
alembic upgrade head
```

### 3. Configuración del Frontend

```bash
# Volver al directorio raíz
cd ..

# Navegar al directorio del frontend
cd frontend

# Instalar dependencias
npm install
```

## 🏃 Ejecución

### Backend

```bash
# En el directorio backend
uvicorn main:app --reload
```

### Frontend

```bash
# En el directorio frontend
npm run dev
```

La aplicación estará disponible en:
- Frontend: http://localhost:3000
- Backend (API): http://localhost:8000
- Documentación de la API: http://localhost:8000/docs
- Documentación alternativa: http://localhost:8000/redoc

## 🏗️ Estructura del Proyecto

```
gestion-proyectos/
├── backend/              # Backend en FastAPI
│   ├── alembic/         # Migraciones de la base de datos
│   ├── app/              # Código fuente del backend
│   ├── scripts/          # Scripts de utilidad
│   ├── tests/            # Pruebas automatizadas
│   ├── .env.example      # Plantilla de variables de entorno
│   ├── alembic.ini       # Configuración de Alembic
│   ├── main.py           # Punto de entrada del backend
│   ├── requirements.txt  # Dependencias principales
│   └── README.md        # Documentación del backend
│
└── frontend/            # Frontend en Vue.js 3
    ├── public/           # Archivos estáticos
    ├── src/              # Código fuente del frontend
    ├── .env.example      # Variables de entorno de ejemplo
    ├── package.json      # Dependencias y scripts
    └── README.md        # Documentación del frontend
```

## 🧪 Pruebas

### Backend
```bash
cd backend
pytest
```

### Frontend
```bash
cd frontend
npm run test:unit
```

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🤝 Contribución

Las contribuciones son bienvenidas. Por favor, lee las [guías de contribución](CONTRIBUTING.md) para más detalles.

## 📧 Contacto

Tu Nombre - [@tu_usuario](https://twitter.com/tu_usuario) - email@ejemplo.com

Enlace del proyecto: [https://github.com/tu-usuario/gestion-proyectos](https://github.com/tu-usuario/gestion-proyectos)

   ### Para SQLite (desarrollo local):
   ```
   DATABASE_URL=sqlite:///./gestion_proyectos.db
   SECRET_KEY=tu_clave_secreta_aqui
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

   ### Para MySQL:
   ```
   DATABASE_HOST=172.18.96.1  # IP del host Windows desde WSL (ajustar según tu configuración)
   DATABASE_PORT=3306
   DATABASE_USER=gestion_app
   DATABASE_PASSWORD=tu_contraseña_aqui
   DATABASE_NAME=gestion_proyectos
   DATABASE_URL=mysql+pymysql://gestion_app:tu_contraseña_aqui@172.18.96.1:3306/gestion_proyectos?charset=utf8mb4
   SECRET_KEY=tu_clave_secreta_aqui
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

   **Nota:** Si estás usando MySQL desde WSL, asegúrate de que el servidor MySQL en Windows esté configurado para aceptar conexiones remotas y que el usuario tenga los permisos adecuados.

### Configuración de MySQL en Windows para aceptar conexiones desde WSL

1. **Editar la configuración de MySQL**:
   - Localiza el archivo `my.ini` (generalmente en `C:\ProgramData\MySQL\MySQL Server X.X\`)
   - Busca la línea `bind-address` y cámbiala a `0.0.0.0` o coméntala
   - Reinicia el servicio de MySQL

2. **Crear usuario y base de datos**:
   - Conectándote a MySQL desde Windows, ejecuta:
   ```sql
   -- Crear la base de datos
   CREATE DATABASE IF NOT EXISTS gestion_proyectos;
   
   -- Crear usuario con acceso desde cualquier host
   CREATE USER 'gestion_app'@'%' IDENTIFIED BY 'tu_contraseña_aqui';
   
   -- Otorgar permisos
   GRANT ALL PRIVILEGES ON gestion_proyectos.* TO 'gestion_app'@'%';
   
   -- Aplicar cambios
   FLUSH PRIVILEGES;
   ```

3. **Configurar el Firewall de Windows**:
   - Abre el Panel de control > Sistema y seguridad > Firewall de Windows
   - Añade una regla para permitir conexiones entrantes al puerto 3306

4. **Verificar la conexión desde WSL**:
   ```bash
   # Reemplaza la IP con la del host Windows desde WSL
   mysql -h 172.18.96.1 -u gestion_app -p
   ```

5. **Crear y gestionar las tablas de la base de datos**:

   ### Inicializar la base de datos por primera vez
   ```bash
   cd backend
   # Inicializar la base de datos MySQL y configurar Alembic
   python init_mysql_db.py
   
   # O si prefieres crear solo las tablas sin configurar Alembic
   python create_tables_direct.py
   ```

   ### Usando el script de gestión de base de datos para operaciones diarias
   ```bash
   cd backend
   # Ver el estado actual de las migraciones
   python manage_db.py current

   # Crear una nueva migración cuando cambies los modelos
   python manage_db.py create "descripción del cambio"

   # Aplicar todas las migraciones pendientes
   python manage_db.py migrate

   # Ver historial de migraciones
   python manage_db.py history

   # Revertir la última migración
   python manage_db.py rollback
   ```
   
   ### Solucionar problemas con Alembic
   ```bash
   # Si tienes problemas con Alembic y MySQL
   python fix_alembic.py
   ```

6. Iniciar el servidor de desarrollo:
 ## 🚀 Despliegue

### Backend en Producción

1. **Requisitos**:
   - Servidor Linux (Ubuntu 22.04 recomendado)
   - Python 3.10+
   - MySQL 8.0+ o PostgreSQL 13+
   - Nginx (como proxy inverso)
   - Supervisor o systemd (para gestión de procesos)

2. **Configuración**:
   ```bash
   # Instalar dependencias del sistema
   sudo apt update
   sudo apt install -y python3-pip python3-venv nginx
   
   # Clonar el repositorio
   git clone https://github.com/tu-usuario/gestion-proyectos.git
   cd gestion-proyectos/backend
   
   # Configurar entorno virtual
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt gunicorn
   
   # Configurar variables de entorno
   cp .env.example .env
   nano .env  # Configurar según producción
   
   # Aplicar migraciones
   alembic upgrade head
   
   # Probar que funciona
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
   ```

3. **Configurar Nginx**:
   ```nginx
   server {
       listen 80;
       server_name tuejemplo.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       }
   }
   ```

4. **Configurar systemd** (en `/etc/systemd/system/gestion-proyectos.service`):
   ```ini
   [Unit]
   Description=Gestión de Proyectos Backend
   After=network.target

   [Service]
   User=usuario
   Group=www-data
   WorkingDirectory=/ruta/a/gestion-proyectos/backend
   Environment="PATH=/ruta/a/gestion-proyectos/backend/venv/bin"
   ExecStart=/ruta/a/gestion-proyectos/backend/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

### Frontend en Producción

1. **Construir para producción**:
   ```bash
   cd frontend
   npm install
   npm run build
   ```

2. **Configurar Nginx** para servir los archivos estáticos:
   ```nginx
   server {
       listen 80;
       server_name app.tuejemplo.com;
       root /ruta/a/gestion-proyectos/frontend/dist;
       index index.html;

       location / {
           try_files $uri $uri/ /index.html;
       }

       location /api {
           proxy_pass http://localhost:8000;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection 'upgrade';
           proxy_set_header Host $host;
           proxy_cache_bypass $http_upgrade;
       }
   }
   ```

3. **Opciones alternativas de despliegue**:
   - **Vercel**: Despliegue directo desde GitHub
   - **Netlify**: Despliegue continuo con integración Git
   - **GitHub Pages**: Para el frontend (requiere configuración especial para SPA)

## 🔧 Desarrollo

### Estructura de ramas
- `main`: Rama principal, solo código estable
- `develop`: Rama de integración para características en desarrollo
- `feature/*`: Ramas para nuevas características
- `hotfix/*`: Ramas para correcciones críticas

### Convenciones de commits
Usamos [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:` Nueva característica
- `fix:` Corrección de errores
- `docs:` Cambios en la documentación
- `style:` Cambios de formato (puntos y coma, indentación, etc.)
- `refactor:` Cambios que no corrigen errores ni agregan funcionalidades
- `perf:` Cambios que mejoran el rendimiento
- `test:` Agregar o corregir pruebas
- `chore:` Cambios en el proceso de construcción o herramientas auxiliares

Ejemplo:
```bash
git commit -m "feat(usuarios): agregar autenticación con JWT"
```

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor, lee nuestras [pautas de contribución](CONTRIBUTING.md) antes de enviar un pull request.

## 📞 Soporte

Si tienes preguntas o necesitas ayuda, por favor [abre un issue](https://github.com/tu-usuario/gestion-proyectos/issues).

### Backend
```bash
# Todas las pruebas
pytest
# Con cobertura
pytest --cov=app

# Pruebas BDD
behave
```

## 💾 Gestión de la base de datos

### Estructura de la base de datos

La aplicación utiliza SQLAlchemy como ORM y Alembic para gestionar las migraciones. La estructura principal incluye:

- **users**: Tabla de usuarios para autenticación y permisos
- (Otras tablas se irán agregando según se desarrolle la aplicación)

### Flujo de trabajo para cambios en la base de datos

1. **Modificar los modelos** en `app/models/`
2. **Crear una migración** con `python manage_db.py create "descripción del cambio"`
3. **Revisar el archivo de migración** generado en `migrations/versions/`
4. **Aplicar la migración** con `python manage_db.py migrate`

### Scripts disponibles para gestionar la base de datos

- **init_mysql_db.py**: Inicializa la base de datos MySQL y configura Alembic correctamente
- **create_tables_direct.py**: Crea las tablas directamente con SQL, sin usar Alembic
- **fix_alembic.py**: Corrige problemas de configuración entre Alembic y MySQL
- **manage_db.py**: Script principal para gestionar migraciones y operaciones de base de datos

### Problemas conocidos con Alembic y MySQL

Existen varios problemas técnicos al usar Alembic con MySQL en este proyecto:

1. **Problema de dialecto**: Alembic está configurado para usar el dialecto SQLite por defecto, aunque la URL de conexión sea para MySQL. Esto se ve en los mensajes de log que muestran `Context impl SQLiteImpl` cuando ejecutamos comandos de Alembic.

2. **Migraciones vacías**: Las migraciones generadas automáticamente están vacías (contienen solo `pass` en los métodos `upgrade()` y `downgrade()`). Esto ocurre porque Alembic no puede detectar correctamente las diferencias entre el estado actual de la base de datos y los modelos definidos.

3. **Problemas de importación**: Puede haber problemas de importación circular entre los módulos que definen los modelos y la configuración de la base de datos, lo que dificulta que Alembic detecte correctamente los modelos.

4. **Estado de migraciones**: Las migraciones existentes ya están marcadas como aplicadas en Alembic, pero no contienen el código para crear las tablas.

### Por qué `create_tables_direct.py` es la solución recomendada

1. **Conexión directa**: Este script se conecta directamente a MySQL usando PyMySQL, sin pasar por la capa de abstracción de SQLAlchemy y Alembic.

2. **SQL explícito**: Utiliza SQL explícito para crear la tabla `users` con la estructura exacta requerida, sin depender de la detección automática de modelos.

3. **Simplicidad**: Al ser un enfoque más directo, evita los problemas de configuración y detección que pueden ocurrir con Alembic.

### Recomendaciones para gestionar la base de datos

- **Configuración inicial**: Usar `create_tables_direct.py` para crear las tablas iniciales.
- **Cambios futuros simples**: Modificar y volver a ejecutar `create_tables_direct.py`.
- **Sistema de migraciones**: Si necesitas un sistema de migraciones más robusto, ejecuta primero `fix_alembic.py` para corregir la configuración de Alembic, y luego crea nuevas migraciones.

### Solucionar problemas comunes

- **Error de conexión a MySQL desde WSL**: Verificar la IP del host Windows y los permisos de firewall
- **Alembic usa SQLite en lugar de MySQL**: Ejecutar `python fix_alembic.py` para corregir la configuración
- **Tablas no creadas**: Ejecutar `python create_tables_direct.py` para crear las tablas directamente
- **Conflictos de migración**: Usar `python manage_db.py current` y `python manage_db.py history` para diagnosticar

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
