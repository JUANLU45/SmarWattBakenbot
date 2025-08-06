@echo off
echo 🔄 GUARDANDO CAMBIOS AUTOMÁTICAMENTE...
git add .
set timestamp=%date:~6,4%-%date:~3,2%-%date:~0,2%_%time:~0,2%-%time:~3,2%-%time:~6,2%
git commit -m "💾 AUTO-SAVE: %timestamp% - Cambios guardados automáticamente"
echo ✅ CAMBIOS GUARDADOS EN GIT: %timestamp%

