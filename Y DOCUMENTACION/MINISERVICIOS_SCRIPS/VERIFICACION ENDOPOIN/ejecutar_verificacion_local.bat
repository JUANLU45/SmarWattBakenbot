@echo off
chcp 65001 >nul
title 🏢 VERIFICADOR LOCAL DE ENDPOINTS - SMARWATT MICROSERVICIOS

echo.
echo ================================================================
echo 🏢 VERIFICADOR LOCAL DE ENDPOINTS - SMARWATT MICROSERVICIOS
echo ================================================================
echo.
echo Este script verifica los endpoints ejecutándose LOCALMENTE
echo en tu ordenador antes del despliegue.
echo.
echo ⚠️  IMPORTANTE: Necesitas tener ambos servicios ejecutándose:
echo    - Expert Bot API en puerto 8080
echo    - Energy IA API en puerto 8081
echo.

pause

echo.
echo 📊 VERIFICANDO DEPENDENCIAS...

REM Verificar si Python está disponible
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no encontrado. Por favor instala Python 3.8+
    pause
    exit /b 1
)

echo ✅ Python detectado

REM Instalar dependencias si es necesario
echo.
echo 📦 INSTALANDO DEPENDENCIAS LOCALES...
python -m pip install requests urllib3 --quiet
if errorlevel 1 (
    echo ⚠️  Problemas instalando dependencias, pero continuando...
) else (
    echo ✅ Dependencias instaladas correctamente
)

echo.
echo 🔍 INSTRUCCIONES ANTES DE CONTINUAR:
echo.
echo 1. ABRIR TERMINAL 1 - Expert Bot API:
echo    cd c:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\expert_bot_api_COPY
echo    python run.py
echo    Debe mostrar: * Running on http://localhost:8080
echo.
echo 2. ABRIR TERMINAL 2 - Energy IA API:
echo    cd c:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\energy_ia_api_COPY
echo    python run.py  
echo    Debe mostrar: * Running on http://localhost:8081
echo.
echo 3. Si los servicios están ejecutándose, presiona cualquier tecla
echo.

pause

echo.
echo 🚀 INICIANDO VERIFICACIÓN LOCAL...
echo ================================================================

python verificar_endpoints_local.py

set SCRIPT_EXIT_CODE=%errorlevel%

echo.
echo ================================================================
echo 📋 VERIFICACIÓN LOCAL COMPLETADA

if %SCRIPT_EXIT_CODE%==0 (
    echo ✅ RESULTADO: TODOS LOS ENDPOINTS CRÍTICOS FUNCIONAN CORRECTAMENTE
    echo ✅ ESTADO: LISTO PARA DESPLEGAR A PRODUCCIÓN
) else (
    echo ❌ RESULTADO: ALGUNOS ENDPOINTS CRÍTICOS FALLAN
    echo ⚠️  ESTADO: CORREGIR PROBLEMAS ANTES DE DESPLEGAR
)

echo.
echo 📁 Consulta el reporte detallado para más información:
dir /B REPORTE_LOCAL_*.md 2>nul | findstr /R "REPORTE_LOCAL_.*\.md" >nul
if errorlevel 1 (
    echo    📄 No se encontró reporte generado
) else (
    for /f %%f in ('dir /B REPORTE_LOCAL_*.md 2^>nul ^| findstr /R "REPORTE_LOCAL_.*\.md"') do (
        echo    📄 %%f
        REM Intentar abrir el reporte
        if exist "%%f" (
            choice /C YN /M "¿Abrir el reporte ahora? [Y/N]" /T 10 /D N >nul
            if errorlevel 2 (
                echo    💡 Puedes abrirlo manualmente después
            ) else (
                start "" "%%f"
            )
        )
    )
)

echo.
echo 💡 PRÓXIMOS PASOS:
if %SCRIPT_EXIT_CODE%==0 (
    echo    ✅ Los microservicios están listos para desplegar
    echo    ✅ Puedes proceder con el despliegue a Cloud Run
    echo    📋 Verificar variables de entorno de producción
) else (
    echo    🔧 Corregir endpoints que fallan
    echo    🔍 Revisar logs de los servicios
    echo    🔄 Ejecutar este script nuevamente después de correcciones
)

echo.
echo ================================================================
echo 🏢 Verificación Local SmarWatt - Completada
echo ================================================================

pause
