# INSTRUCCIONES DE EJECUCIÓN - TESTING DE PRODUCCIÓN SMARWATT
================================================================

## 🎯 RESUMEN EJECUTIVO

Se han creado **4 scripts profesionales** para testing COMPLETO de producción de los microservicios SmarWatt:

### 📋 SCRIPTS CREADOS

1. **`testing_maestro_produccion.py`** - **SCRIPT PRINCIPAL**
   - Ejecuta TODO el flujo de testing automáticamente
   - Instala dependencias, verifica endpoints, ejecuta testing completo
   - Genera reporte consolidado final

2. **`instalar_dependencias_testing.py`** - Instalador de dependencias
   - Instala: requests, google-cloud-bigquery, firebase-admin, etc.
   - Verificación REAL de instalaciones

3. **`verificacion_endpoints_problematicos.py`** - Verificador especializado
   - Verifica específicamente el endpoint problemático `/api/v1/analysis/sentiment`
   - Testa credenciales Google Cloud y conectividad BigQuery

4. **`script_testing_produccion_completo.py`** - Testing completo
   - Testa TODOS los 34+ endpoints identificados en el código REAL
   - Incluye endpoints de energy-ia-api y expert-bot-api

## 🚀 EJECUCIÓN RECOMENDADA

### Opción 1: AUTOMÁTICA (Recomendada)
```powershell
cd "c:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\DOCUMENTACION Y SCRPT"
python testing_maestro_produccion.py
```

### Opción 2: MANUAL (Por pasos)
```powershell
# 1. Instalar dependencias
python instalar_dependencias_testing.py

# 2. Verificar endpoints problemáticos
python verificacion_endpoints_problematicos.py

# 3. Testing completo
python script_testing_produccion_completo.py
```

## 🔧 COMPONENTES VERIFICADOS

### ✅ URLs DE PRODUCCIÓN REALES
- Energy IA API: `https://energy-ia-api-1010012211318.europe-west1.run.app`
- Expert Bot API: `https://expert-bot-api-1010012211318.europe-west1.run.app`

### ✅ CREDENCIALES REALES CONFIGURADAS
- Firebase Admin SDK: `firebase-adminsdk-fbsvc-key.json`
- Expert Bot Service Account: `expert-bot-api-sa-key.json`

### ✅ ENDPOINTS IDENTIFICADOS EN CÓDIGO REAL
**Energy IA API (13 endpoints):**
- `/health` - Health check
- `/api/v1/chatbot/message` - Chatbot principal
- `/api/v1/chatbot/message/v2` - Chatbot v2
- `/api/v1/chatbot/cross-service` - Cross-service
- `/api/v1/chatbot/conversations` - Listar conversaciones
- `/api/v1/chatbot/conversations/{id}` - Eliminar conversación
- `/api/v1/chatbot/health` - Health chatbot
- `/api/v1/energy/tariffs/recommendations` - Recomendaciones
- `/api/v1/energy/tariffs/market-data` - Datos mercado
- `/api/v1/energy/admin/tariffs/add` - Añadir tarifa
- `/api/v1/energy/admin/tariffs/batch-add` - Lote tarifas
- `/api/v1/energy/tariffs/compare` - Comparar tarifas
- `/api/v1/links/*` - Enlaces (3 endpoints)

**Expert Bot API (8+ endpoints):**
- `/health` - Health check principal
- `/health/detailed` - Health detallado
- `/api/v1/analysis/sentiment` - **PROBLEMÁTICO** (Error 500)
- `/api/v1/analysis/sentiment/internal` - Análisis interno
- `/api/v1/chatbot/session/start` - Iniciar sesión
- `/api/v1/chatbot/message` - Mensaje chat
- `/api/v1/chatbot/new-conversation` - Nueva conversación
- `/api/v1/energy/consumption` - Upload factura

## 🎯 CARACTERÍSTICAS EMPRESARIALES

### 🔒 VERIFICACIONES REALES
- **NO** hay código placebo o simulaciones
- **TODAS** las peticiones son HTTP reales a producción
- **TODAS** las credenciales son service accounts reales
- **TODA** la verificación es contra infraestructura real

### 📊 REPORTES PROFESIONALES
- Logs detallados con timestamps
- Archivos JSON con resultados completos
- Reportes en consola con estadísticas
- Códigos de salida estándar (0=éxito, 1=advertencias, 2=errores)

### 🛡️ MANEJO ROBUSTO DE ERRORES
- Timeouts configurados (30 segundos)
- Reintentos en errores de conexión
- Validación de respuestas HTTP
- Logging de errores completos

## 📋 RESULTADOS ESPERADOS

### ✅ ENDPOINTS QUE DEBERÍAN FUNCIONAR
- Health checks de ambos servicios
- Endpoints básicos de chatbot
- Endpoints de energía y tarifas

### ⚠️ ENDPOINT PROBLEMÁTICO CONOCIDO
- `POST /api/v1/analysis/sentiment` - Error 500
- **Causa**: Constructor de `AILearningService` falla en BigQuery init
- **Solución identificada**: Inicialización lazy de BigQuery

### 📈 MÉTRICAS DE ÉXITO
- **80%+ endpoints funcionando**: Sistema estable
- **50-80% endpoints funcionando**: Necesita atención
- **<50% endpoints funcionando**: Problemas críticos

## 🔍 INFORMACIÓN TÉCNICA

### Dependencias Instaladas Automáticamente
- `requests` - HTTP requests
- `google-cloud-bigquery` - BigQuery API
- `google-auth` - Google authentication
- `firebase-admin` - Firebase Admin SDK

### Archivos de Salida Generados
- `testing_maestro_YYYYMMDD_HHMMSS.log` - Log maestro
- `reporte_testing_maestro_YYYYMMDD_HHMMSS.json` - Reporte consolidado
- `testing_produccion_YYYYMMDD_HHMMSS.log` - Log testing completo
- `verificacion_endpoints_YYYYMMDD_HHMMSS.log` - Log verificación

### Códigos de Salida
- `0` - Éxito completo
- `1` - Completado con advertencias
- `2` - Errores significativos
- `3` - Error crítico/fatal

## 🎉 EJECUCIÓN

Para ejecutar el testing completo:

```powershell
cd "c:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\DOCUMENTACION Y SCRPT"
python testing_maestro_produccion.py
```

El script ejecutará automáticamente:
1. ✅ Instalación de dependencias
2. ✅ Verificación de endpoints problemáticos  
3. ✅ Testing completo de 34+ endpoints
4. ✅ Generación de reporte consolidado

**Total estimado de ejecución: 2-5 minutos**

## 🏆 RESULTADO FINAL

Al completar, tendrás:
- **Estado REAL** de todos los microservicios en producción
- **Identificación precisa** de endpoints con problemas
- **Verificación completa** de infraestructura Google Cloud
- **Reporte profesional** con recomendaciones específicas

¡El sistema está listo para testing de producción sin tolerancia a falsos positivos!
