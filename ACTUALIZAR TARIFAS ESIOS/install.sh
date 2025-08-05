#!/bin/bash
# 🚀 SCRIPT DE INSTALACIÓN Y CONFIGURACIÓN ESIOS
# ===============================================

echo "🏢 INSTALANDO ACTUALIZADOR ESIOS SMARWATT"
echo "=========================================="

# Crear directorio logs
mkdir -p logs
echo "📁 Directorio logs creado"

# Instalar dependencias Python
echo "📦 Instalando dependencias..."
pip install -r requirements.txt

# Verificar instalación
if [ $? -eq 0 ]; then
    echo "✅ Dependencias instaladas correctamente"
else
    echo "❌ Error instalando dependencias"
    exit 1
fi

# Configurar variables de entorno
if [ ! -f .env ]; then
    echo "⚙️ Creando archivo de configuración..."
    cp .env.example .env
    echo "📝 Archivo .env creado desde plantilla"
    echo ""
    echo "🔧 CONFIGURACIÓN REQUERIDA:"
    echo "  1. Editar archivo .env"
    echo "  2. Configurar ESIOS_API_KEY"
    echo "  3. Configurar SMARWATT_ADMIN_TOKEN"
    echo ""
    echo "📧 Solicitar API Key ESIOS: consultasios@ree.es"
    echo "🔑 Asunto: 'Personal token request'"
else
    echo "✅ Archivo .env ya existe"
fi

echo ""
echo "🎉 INSTALACIÓN COMPLETADA"
echo ""
echo "📋 PRÓXIMOS PASOS:"
echo "  1. Configurar .env con tus credenciales"
echo "  2. Ejecutar test: python esios_tariff_updater.py --sync-now"
echo "  3. Para modo automático: python esios_tariff_updater.py"
echo ""
