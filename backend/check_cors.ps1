# Verificar si el archivo .env existe, si no, copiar de .env.example
if (-not (Test-Path .env)) {
    Copy-Item .env.example .env
    Write-Host "Archivo .env creado a partir de .env.example"
}

# Leer el archivo .env
$envContent = Get-Content .env -Raw

# Verificar la configuración de CORS_ORIGINS
$corsLine = ($envContent -split [System.Environment]::NewLine) | Where-Object { $_ -match "^CORS_ORIGINS=" }

if ($corsLine) {
    $corsOrigins = $corsLine -replace '^CORS_ORIGINS=[\"'']?(.*?)[\"'']?$', '$1'
    Write-Host "CORS_ORIGINS actual: $corsOrigins"
    
    # Verificar si incluye localhost:3000
    if ($corsOrigins -notmatch "localhost:3000") {
        Write-Host "Añadiendo localhost:3000 a CORS_ORIGINS..."
        $newCorsLine = "CORS_ORIGINS=$corsOrigins,http://localhost:3000"
        $envContent = $envContent -replace [regex]::Escape($corsLine), $newCorsLine
        $envContent | Set-Content .env -NoNewline
        Write-Host "CORS_ORIGINS actualizado correctamente"
    } else {
        Write-Host "CORS_ORIGINS ya incluye localhost:3000"
    }
} else {
    Write-Host "No se encontró la variable CORS_ORIGINS en .env"
    Add-Content -Path .env -Value "`n# Configuración de CORS (orígenes permitidos separados por comas)`nCORS_ORIGINS=http://localhost:3000"
    Write-Host "Variable CORS_ORIGINS añadida a .env"
}

# Mostrar la configuración actual
Write-Host "`nConfiguración actual de CORS:"
Get-Content .env | Select-String "CORS_"
