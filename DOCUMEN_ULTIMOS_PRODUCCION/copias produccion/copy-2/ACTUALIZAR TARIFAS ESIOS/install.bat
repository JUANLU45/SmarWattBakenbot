@echo off
REM 🚀 SCRIPT DE INSTALACIÓN WINDOWS - ACTUALIZADOR ESIOS
REM ======================================================

echo 🏢 INSTALANDO ACTUALIZADOR ESIOS SMARWATT
echo ==========================================

REM Crear directorio logs
if not exist logs mkdir logs
echo 📁 Directorio logs creado

REM Instalar dependencias Python
echo 📦 Instalando dependencias...
pip install -r requirements.txt

if %errorlevel% equ 0 (
    echo ✅ Dependencias instaladas correctamente
) else (
    echo ❌ Error instalando dependencias
    pause
    exit /b 1
)

REM Configurar variables de entorno
if not exist .env (
    echo ⚙️ Creando archivo de configuración...
    copy .env.example .env
    echo 📝 Archivo .env creado desde plantilla
    echo.
    echo 🔧 CONFIGURACIÓN REQUERIDA:
    echo   1. Editar archivo .env
    echo   2. Configurar ESIOS_API_KEY
    echo   3. Configurar SMARWATT_ADMIN_TOKEN
    echo.
    echo 📧 Solicitar API Key ESIOS: consultasios@ree.es
    echo 🔑 Asunto: 'Personal token request'
) else (
    echo ✅ Archivo .env ya existe
)

echo.
echo 🎉 INSTALACIÓN COMPLETADA
echo.
echo 📋 PRÓXIMOS PASOS:
echo   1. Configurar .env con tus credenciales
echo   2. Ejecutar test: python esios_tariff_updater.py --sync-now
echo   3. Para modo automático: python esios_tariff_updater.py
echo.

pause
