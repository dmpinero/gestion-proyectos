@echo off
echo Limpiando node_modules y archivos temporales...

if exist node_modules (
  echo Eliminando node_modules...
  rmdir /s /q node_modules
)

if exist package-lock.json (
  echo Eliminando package-lock.json...
  del package-lock.json
)

echo Limpieza completada.
