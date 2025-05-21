# Gestión de Proyectos

Aplicación para la gestión de proyectos y tareas desarrollada con Vue.js 3 (frontend) y FastAPI (backend).

## 🚀 Características

- **Frontend**: Vue.js 3 con Composition API, Vue Router y Pinia
- **Backend**: FastAPI con SQLAlchemy
- **Base de datos**: SQLite (desarrollo) / MySQL (producción)
- **Migraciones**: Alembic para gestionar cambios en el esquema de la base de datos
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
   cd backend
   pip install -r requirements.txt
   ```

   ### Dependencias adicionales para MySQL:
   ```bash
   pip install pymysql
   ```

3. (Opcional) Si agregas nuevas dependencias, actualiza el archivo requirements.txt:
   ```bash
   pip freeze > requirements.txt
   ```
   
   **Nota:** Asegúrate de revisar el archivo generado para incluir solo las dependencias necesarias del proyecto.

4. Configurar variables de entorno (crear archivo `.env` en la raíz del proyecto):

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
   ```bash
   cd backend
   uvicorn main:app --reload
   ```
   
   La aplicación estará disponible en: http://localhost:8000
   
   - Documentación de la API (Swagger UI): http://localhost:8000/docs
   - Documentación alternativa (ReDoc): http://localhost:8000/redoc

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
