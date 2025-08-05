# 🚀 Simulador de Entrenamiento IA - SmarWatt

## 📋 Descripción

Sistema autónomo de generación de datos sintéticos para entrenar los modelos de IA de SmarWatt en producción. Diseñado para ser completamente realista, coste-eficiente y alineado con los microservicios desplegados en Google Cloud Run.

## 🏗️ Arquitectura

```
simulador_entrenamiento_ia/
├── 📄 .env.example         # Variables de entorno de producción
├── 📄 README.md           # Esta documentación
├── 📄 requirements.txt    # Dependencias Python
├── ⚙️ config/            # Configuración del simulador
│   ├── 📄 __init__.py
│   ├── 📄 simulation_config.py  # Control de costes y autonomía
│   └── 📄 profiles.json         # Perfiles ficticios españoles
├── 📊 data/              # Generadores de datos
│   ├── 📄 es_data_generators.py # Datos realistas españoles
│   └── 📄 chat_messages.json   # Mensajes predefinidos
└── 🚀 src/               # Código fuente
    ├── 📄 __init__.py
    ├── 📄 api_client.py           # Cliente HTTP para microservicios
    ├── 📄 profile_generator.py    # Generador de perfiles
    ├── 📄 interaction_simulator.py # Motor de simulación
    └── 📄 autonomous_runner.py    # Orquestador principal
```

## 🎯 Características

### ✅ Integración Real con Producción

- **URLs Reales**: Conecta directamente con los microservicios desplegados en Google Cloud Run
- **Tablas BigQuery**: Utiliza las mismas tablas que el sistema en producción
- **Autenticación Firebase**: Sistema de autenticación real con tokens válidos
- **Datos Españoles**: Generación de datos realistas del mercado español

### 💰 Control de Costes

- **Parametrización Granular**: Control preciso del número de usuarios y llamadas
- **Límites de Gasto**: Configuración de límites máximos de coste diario
- **Ejecución Programada**: Intervalos configurables para evitar picos de carga
- **Monitoreo en Tiempo Real**: Seguimiento del gasto y las métricas

### 🔄 Autonomía Total

- **Modo Autónomo**: Ejecución continua sin intervención manual
- **Reintentos Inteligentes**: Manejo robusto de errores y reintentos
- **Logging Detallado**: Registro completo de todas las operaciones
- **Health Checks**: Verificación automática del estado de los servicios

## 🚀 Instalación y Configuración

### 1. Preparar el Entorno

```bash
# Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configurar Variables de Entorno

```bash
# Copiar el archivo de configuración
copy .env.example .env

# Editar .env con tu token Firebase real
# AUTH_TOKEN=tu_token_firebase_aqui
```

### 3. Ejecutar el Simulador

```bash
# Modo manual (una ejecución)
python src/autonomous_runner.py

# Modo autónomo (ejecución continua)
# Editar config/simulation_config.py: AUTONOMOUS_MODE = True
python src/autonomous_runner.py
```

## ⚙️ Configuración de Parámetros

### Control de Costes (`config/simulation_config.py`)

```python
# Número de usuarios por ejecución (impacto directo en coste)
NUM_USERS_PER_RUN = 50

# Interacciones por usuario
API_CALLS_PER_USER = 10

# Intervalos de ejecución (en horas)
EXECUTION_INTERVAL_HOURS = 24

# Porcentajes de simulación
INVOICE_UPLOAD_RATE = 0.20      # 20% suben facturas
RECOMMENDATION_REQUEST_RATE = 0.50  # 50% piden recomendaciones
```

### Estimación de Costes

- **50 usuarios × 10 interacciones = 500 llamadas API**
- **Coste estimado por día: ~$2-5 USD**
- **BigQuery queries: ~1000 consultas/día**
- **Firebase Auth: Incluido en plan gratuito**

## 📊 Endpoints Utilizados

### Energy IA API

- `POST /api/v1/chatbot/message/v2` - Chat optimizado
- `GET /api/v1/energy/tariffs/recommendations` - Recomendaciones

### Expert Bot API

- `POST /api/v1/energy/manual-data` - Datos manuales
- `POST /api/v1/energy/consumption` - Subida de facturas
- `GET /api/v1/energy/users/profile` - Perfil de usuario

## 🎲 Datos Generados

### Perfiles de Usuario Realistas

- **Consumo kWh**: 150-450 kWh/mes (rangos españoles reales)
- **Potencia**: 3.45-11.5 kW (valores estándar)
- **Comercializadoras**: Iberdrola, Endesa, Naturgy, EDP
- **Códigos Postales**: Madrid, Barcelona, Valencia, Sevilla
- **Tipos de Vivienda**: apartment, house, chalet

### Mensajes de Chat Variados

- Preguntas sobre facturas eléctricas
- Consultas de ahorro energético
- Comparativas de tarifas
- Dudas sobre PVPC y mercado regulado

## 📈 Monitoreo y Métricas

El simulador registra automáticamente:

- ✅ Usuarios creados correctamente
- 💬 Mensajes de chat enviados
- 💰 Recomendaciones solicitadas
- ❌ Errores y fallos de API
- ⏱️ Tiempos de respuesta
- 💲 Estimación de costes

## 🔒 Seguridad

- **Tokens Reales**: Utiliza autenticación Firebase válida
- **HTTPS**: Todas las comunicaciones son seguras
- **Límites de Rate**: Protección contra uso excesivo
- **Logging Seguro**: No expone información sensible

## 🚨 Advertencias Importantes

⚠️ **PRODUCCIÓN REAL**: Este simulador interactúa con servicios en producción reales
⚠️ **COSTES**: Monitorea los gastos de Google Cloud regularmente  
⚠️ **LÍMITES**: Respeta los límites de API y BigQuery
⚠️ **TOKENS**: Mantén seguros tus tokens de autenticación

## 🔧 Troubleshooting

### Error de Autenticación

```bash
# Verificar token Firebase
curl -H "Authorization: Bearer TU_TOKEN" \
  https://energy-ia-api-1010012211318.europe-west1.run.app/health
```

### Error de Conexión

```bash
# Verificar conectividad
ping energy-ia-api-1010012211318.europe-west1.run.app
```

### Costes Excesivos

1. Reducir `NUM_USERS_PER_RUN`
2. Aumentar `EXECUTION_INTERVAL_HOURS`
3. Verificar `MAX_DAILY_COST_USD`

## 📞 Soporte

Para problemas técnicos, revisar:

1. Logs del simulador (`simulador_entrenamiento.log`)
2. Logs de Google Cloud Run
3. Métricas de BigQuery
4. Estado de los servicios en Google Cloud Console
