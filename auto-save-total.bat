@echo off
setlocal enabledelayedexpansion

echo.
echo 🔄 ============================================
echo    GUARDADO AUTOMÁTICO TOTAL ACTIVADO
echo 🔄 ============================================
echo.

:: Obtener timestamp
for /f "tokens=2 delims==" %%I in ("wmic os get localdatetime /value") do set datetime=%%I
set timestamp=!datetime:~0,4!-!datetime:~4,2!-!datetime:~6,2!_!datetime:~8,2!-!datetime:~10,2!-!datetime:~12,2!

:: Verificar si hay cambios
git diff --quiet
if !errorlevel! neq 0 goto save_changes

git diff --staged --quiet  
if !errorlevel! neq 0 goto save_changes

echo ✅ No hay cambios nuevos para guardar
goto end

:save_changes
echo 💾 Detectados cambios - Guardando automáticamente...
git add .

:: Verificar qué archivos se modificaron
echo.
echo 📁 Archivos modificados:
git diff --cached --name-only
echo.

:: Crear mensaje de commit descriptivo
set "commit_msg=💾 AUTO-SAVE [!timestamp!]: Cambios guardados automáticamente"

:: Verificar archivos específicos importantes
git diff --cached --name-only | findstr "ai_learning_service.py" >nul
if !errorlevel! equ 0 set "commit_msg=🧠 AUTO-SAVE [!timestamp!]: Cambios en AI Learning Service"

git diff --cached --name-only | findstr "energy_service.py" >nul  
if !errorlevel! equ 0 set "commit_msg=⚡ AUTO-SAVE [!timestamp!]: Cambios en Energy Service"

git diff --cached --name-only | findstr "ANALISIS_ERRORES" >nul
if !errorlevel! equ 0 set "commit_msg=📊 AUTO-SAVE [!timestamp!]: Actualización análisis de errores"

:: Hacer commit
git commit -m "!commit_msg!"

if !errorlevel! equ 0 (
    echo ✅ CAMBIOS GUARDADOS EXITOSAMENTE EN GIT
    echo 📝 Commit: !commit_msg!
    echo 🕒 Timestamp: !timestamp!
) else (
    echo ❌ ERROR al guardar cambios
)

:end
echo.
echo 🔒 Guardado automático completado
echo 🔄 ============================================
echo.
