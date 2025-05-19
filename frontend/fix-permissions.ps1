# Script para corregir permisos y limpiar el proyecto
Write-Host "Corrigiendo permisos y limpiando el proyecto..." -ForegroundColor Cyan

# Limpiar caché de npm
if (Test-Path node_modules) {
    Write-Host "Eliminando node_modules..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force node_modules
}

# Eliminar archivos temporales
if (Test-Path package-lock.json) {
    Write-Host "Eliminando package-lock.json..." -ForegroundColor Yellow
    Remove-Item -Force package-lock.json
}

# Instalar dependencias
Write-Host "Instalando dependencias..." -ForegroundColor Cyan
npm install

Write-Host "Proceso completado. Intenta ejecutar 'npm run dev' nuevamente." -ForegroundColor Green
