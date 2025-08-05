@echo off
REM =================================================================
REM 🏢 VERIFICADOR DE ENDPOINTS SMARWATT - SCRIPT DE EJECUCIÓN
REM =================================================================
REM
REM PROPÓSITO:
REM Este script ejecuta la verificación completa de endpoints de los
REM microservicios Expert Bot API y Energy IA API de SmarWatt.
REM
REM FUNCIONES:
REM ✅ Ejecuta verificación completa
REM ✅ Genera reportes automáticamente  
REM ✅ Muestra resultados en consola
REM ✅ Guarda logs detallados
REM
REM AUTOR: Sistema de Verificación Empresarial SmarWatt
REM FECHA: 2025-07-21
REM =================================================================

echo.
echo 🏢 VERIFICADOR DE ENDPOINTS SMARWATT - MICROSERVICIOS
echo ===========================================================
echo.
echo Iniciando verificación de endpoints...
echo.

REM Cambiar al directorio del script
cd /d "%~dp0"

REM Verificar si Python está disponible
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python no está instalado o no está en el PATH
    echo.
    echo Por favor instale Python 3.7+ desde: https://python.org
    pause
    exit /b 1
)

echo ✅ Python detectado
echo.

REM Verificar si requests está instalado
python -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Instalando dependencias necesarias...
    pip install requests urllib3
    if errorlevel 1 (
        echo ❌ Error instalando dependencias
        pause
        exit /b 1
    )
    echo ✅ Dependencias instaladas
    echo.
)

REM Ejecutar verificación simple
echo 🚀 Ejecutando verificación simple de endpoints...
echo.
python verificar_endpoints_simple.py

if errorlevel 1 (
    echo.
    echo ❌ Error durante la verificación simple
    echo.
    echo ⚡ Intentando verificación completa...
    echo.
    
    REM Si falla la simple, intentar la completa
    python verificar_endpoints_completo.py
    
    if errorlevel 1 (
        echo ❌ Error en ambas verificaciones
        echo.
        echo 🔍 Posibles causas:
        echo   - Los servicios no están ejecutándose
        echo   - Problemas de conectividad de red
        echo   - Configuración de firewall
        echo.
        pause
        exit /b 1
    )
)

echo.
echo ✅ Verificación completada exitosamente
echo.
echo 📁 Los reportes han sido generados en esta carpeta:
dir /b *.md *.json *.txt 2>nul
echo.

REM Preguntar si abrir los reportes
set /p abrir="¿Desea abrir el reporte más reciente? (s/n): "
if /i "%abrir%"=="s" (
    for /f "delims=" %%f in ('dir /b /od REPORTE_*.md 2^>nul ^| findstr /r ".*"') do set ultimo_reporte=%%f
    if defined ultimo_reporte (
        echo Abriendo %ultimo_reporte%...
        start "" "%ultimo_reporte%"
    ) else (
        echo No se encontraron reportes.
    )
)

echo.
echo 🎯 Para ejecutar nuevamente: ejecutar_verificacion.bat
echo 📞 Soporte técnico: desarrollo@smarwatt.com
echo.

pause
