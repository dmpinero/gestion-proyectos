# Scripts de Utilidad

Este directorio contiene scripts de utilidad para el proyecto, organizados en las siguientes categorías:

## Estructura de Directorios

- `checks/`: Scripts para verificar el estado del sistema, conexiones a la base de datos, etc.
- `db_utils/`: Utilidades para la gestión de la base de datos (creación, migración, etc.)
- `tests/`: Scripts de prueba de integración/manuales (las pruebas unitarias están en el directorio `../tests`)
- `backup/`: Scripts para realizar copias de seguridad (si es necesario)

## Diferencia entre tests/ y ../tests/

- `../tests/`: Contiene pruebas unitarias automatizadas que se ejecutan con pytest
- `scripts/tests/`: Contiene scripts de prueba manuales o de integración que pueden requerir configuración específica

## Uso

Cada script debe documentar su propio uso. Ejecuta cualquier script con el flag `-h` o `--help` para ver sus opciones.

## Convenciones

- Los scripts deben ser independientes y documentados
- Deben manejar errores de manera adecuada
- Deben ser compatibles con el entorno de desarrollo local
