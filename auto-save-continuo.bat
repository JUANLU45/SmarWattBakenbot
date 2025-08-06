@echo off
setlocal EnableDelayedExpansion

:: 🔒 SISTEMA DE GUARDADO AUTOMÁTICO TOTAL
:: Este script guarda TODOS los cambios automáticamente

echo 🚀 INICIANDO GUARDADO AUTOMÁTICO CONTINUO...
echo 📅 Fecha: %date% %time%
echo 📁 Directorio: %cd%
echo.

:loop
    :: Verificar si hay cambios
    git status --porcelain > status.tmp
    
    :: Si hay cambios, guardarlos automáticamente
    for /f %%i in ("status.tmp") do if %%~zi gtr 0 (
        echo 💾 CAMBIOS DETECTADOS - Guardando automáticamente...
        
        :: Timestamp único
        set "timestamp=%date:~6,4%-%date:~3,2%-%date:~0,2%_%time:~0,2%-%time:~3,2%-%time:~6,2%"
        set "timestamp=!timestamp: =0!"
        
        :: Agregar todos los cambios
        git add .
        
        :: Crear commit automático
        git commit -m "💾 AUTO-SAVE [!timestamp!]: Guardado automático continuo"
        
        if !errorlevel! equ 0 (
            echo ✅ CAMBIOS GUARDADOS: !timestamp!
        ) else (
            echo ❌ Error en guardado: !timestamp!
        )
        echo.
    )
    
    :: Limpiar archivo temporal
    del status.tmp >nul 2>&1
    
    :: Esperar 30 segundos antes de la siguiente verificación
    timeout /t 30 /nobreak >nul
    
    :: Mostrar que sigue funcionando
    echo 🔄 Verificando cambios... %time%

goto loop

