# ⚡ DOCUMENTACIÓN COMPLETA - ENERGY IA API

## 📋 **INFORMACIÓN GENERAL**

**Nombre del Microservicio:** Energy IA API  
**Versión:** 2025.1.0 - EMPRESARIAL COPY  
**Puerto:** 8081  
**Tecnología:** Flask + Python 3.10+  
**Base de Datos:** Firebase Firestore + BigQuery  
**Autenticación:** Firebase Admin SDK + JWT  
**Especialización:** Análisis energético, gestión de tarifas, chatbot IA

---

## 📁 **ESTRUCTURA COMPLETA DE ARCHIVOS**

```
energy_ia_api_COPY/
│
├── 📄 ARCHIVOS DE CONFIGURACIÓN
│   ├── .env                     # Variables de entorno (SENSIBLE)
│   ├── .firebaserc             # Configuración específica de Firebase
│   ├── .dockerignore           # Archivos ignorados por Docker
│   ├── Dockerfile              # Configuración de contenedor Docker
│   ├── pyproject.toml          # Configuración del proyecto Python
│   ├── requirements-base.txt   # Dependencias base del proyecto
│   ├── requirements-dev.txt    # Dependencias de desarrollo
│   ├── requirements-ml.txt     # Dependencias de Machine Learning IA
│   ├── requirements.txt        # TODAS las dependencias
│   └── run.py                  # 🚀 ARCHIVO PRINCIPAL DE EJECUCIÓN
│
├── 📦 app/ - NÚCLEO DE LA APLICACIÓN
│   ├── __init__.py             # ⚙️ Inicializador de la aplicación Flask
│   ├── config.py               # 🔧 Configuraciones por entorno
│   │
│   ├── 🛣️ RUTAS PRINCIPALES
│   ├── routes.py               # ⚡ Endpoints energéticos + ADMIN tarifas
│   ├── chatbot_routes.py       # 🤖 Endpoints del chatbot IA
│   └── links_routes.py         # 🔗 Gestión de enlaces específicos
│   │
│   ├── 🔧 SERVICIOS ESPECIALIZADOS
│   └── services/               # 📁 Servicios de análisis energético
│       ├── analysis_service.py # 📊 Análisis de consumo energético
│       ├── chatbot_service.py  # 🤖 Lógica del chatbot IA
│       ├── billing_service.py  # 💰 Servicios de facturación
│       ├── tariff_service.py   # ⚡ Gestión de tarifas energéticas
│       └── recommendation_service.py # 💡 Sistema de recomendaciones
│
├── 🔐 smarwatt_auth/ - SISTEMA DE AUTENTICACIÓN
│   ├── __init__.py            # Inicializador del módulo de auth
│   ├── auth.py                # 🛡️ Decoradores y lógica de autenticación
│   └── smarwatt_auth/         # 📁 Submódulo de autenticación legacy
│       └── auth.py            # 🔄 Implementación alternativa de auth
│
├── 🛠️ utils/ - UTILIDADES ESPECIALIZADAS
│   ├── __init__.py            # Inicializador de utilidades
│   ├── data_processors.py     # 📊 Procesadores de datos energéticos
│   ├── ml_models.py           # 🧠 Modelos de Machine Learning
│   └── esios_client.py        # 🌐 Cliente para API de ESIOS (precios energía)
│
├── 📊 logs/ - ARCHIVOS DE LOG
│   └── energy_ia_api.log      # Logs específicos del servicio energético
│
└── 🐳 ARCHIVOS DOCKER Y CACHE
    └── __pycache__/           # Cache de Python (auto-generado)
```

---

## ⚙️ **COMPONENTES PRINCIPALES**

### 1️⃣ **run.py - EJECUTOR PRINCIPAL**

**Ubicación:** `energy_ia_api_COPY/run.py`

**Función:** Punto de entrada principal especializado en servicios energéticos

**Características Empresariales:**

- ✅ Configuración logging empresarial específico para energía
- ✅ Inicialización con modo empresarial
- ✅ Configuración de variables específicas de energía
- ✅ Integración con APIs externas (ESIOS)
- ✅ Monitorización de servicios energéticos

**Configuración Especializada:**

```python
# Variables específicas de energía
app.config["ENTERPRISE_MODE"] = True
app.config["API_VERSION"] = "2025.1.0"
app.config["ENERGY_SPECIALIZATION"] = True
app.config["ESIOS_INTEGRATION"] = True
```

### 2️⃣ **app/**init**.py - INICIALIZADOR ENERGÉTICO**

**Ubicación:** `energy_ia_api_COPY/app/__init__.py`

**Función:** Configuración especializada para servicios energéticos

**Componentes Específicos:**

- ⚡ **Integración con APIs energéticas externas**
- 🤖 **Configuración específica para chatbot IA**
- 📊 **Conexión con datos de mercado energético**
- 💰 **Integración con sistemas de facturación**

**Blueprints Especializados:**

```python
# Registro de rutas energéticas
app.register_blueprint(energy_routes_bp, url_prefix="/api/v1/energy")
app.register_blueprint(chatbot_bp, url_prefix="/api/v1/chatbot")
app.register_blueprint(links_bp, url_prefix="/api/v1/links")
```

### 3️⃣ **config.py - CONFIGURACIONES ENERGÉTICAS**

**Ubicación:** `energy_ia_api_COPY/app/config.py`

**Configuraciones Específicas:**

- ⚡ **APIs de mercado energético (ESIOS)**
- 📊 **Tablas BigQuery específicas de energía**
- 💰 **Configuración de sistemas de facturación**
- 🤖 **Parámetros del chatbot IA**

---

## 🛣️ **DOCUMENTACIÓN DE RUTAS ESPECIALIZADAS**

### 1️⃣ **routes.py - SERVICIOS ENERGÉTICOS + ADMIN**

**Prefijo:** `/api/v1/energy`

#### **ENDPOINTS PÚBLICOS DE ENERGÍA:**

| Endpoint                | Método | Auth    | Función                                           |
| ----------------------- | ------ | ------- | ------------------------------------------------- |
| `/tariffs/search`       | GET    | Público | `search_tariffs()` - Buscar tarifas disponibles   |
| `/tariffs/compare`      | POST   | Público | `compare_tariffs()` - Comparar tarifas            |
| `/consumption/estimate` | POST   | Público | `estimate_consumption()` - Estimar consumo        |
| `/market/prices`        | GET    | Público | `get_market_prices()` - Precios de mercado actual |

#### **ENDPOINTS ADMINISTRATIVOS DE TARIFAS:**

| Endpoint                   | Método | Auth     | Función                                            |
| -------------------------- | ------ | -------- | -------------------------------------------------- |
| `/admin/tariffs/add`       | POST   | 🏢 Admin | `add_tariff_data()` - **Añadir tarifa individual** |
| `/admin/tariffs/batch-add` | POST   | 🏢 Admin | `batch_add_tariffs()` - **Añadir tarifas en lote** |

#### **ENDPOINTS DE USUARIO AUTENTICADO:**

| Endpoint                | Método | Auth     | Función                                                       |
| ----------------------- | ------ | -------- | ------------------------------------------------------------- |
| `/user/profile`         | GET    | 🔒 Token | `get_user_energy_profile()` - Perfil energético               |
| `/user/consumption`     | GET    | 🔒 Token | `get_user_consumption()` - Historial de consumo               |
| `/user/bills`           | GET    | 🔒 Token | `get_user_bills()` - Facturas del usuario                     |
| `/user/recommendations` | GET    | 🔒 Token | `get_user_recommendations()` - Recomendaciones personalizadas |

### 2️⃣ **chatbot_routes.py - CHATBOT IA ESPECIALIZADO**

**Prefijo:** `/api/v1/chatbot`

| Endpoint   | Método | Auth     | Función                                                    |
| ---------- | ------ | -------- | ---------------------------------------------------------- |
| `/chat`    | POST   | 🔒 Token | `chat_endpoint()` - **Conversación principal del chatbot** |
| `/context` | GET    | 🔒 Token | `get_chat_context()` - Contexto de conversación            |
| `/history` | GET    | 🔒 Token | `get_chat_history()` - Historial de conversaciones         |

#### **FLUJO DEL CHATBOT IA:**

```python
1. Recepción del mensaje del usuario
2. Obtención del contexto del usuario desde expert-bot-api
3. Análisis del mensaje con IA especializada en energía
4. Generación de respuesta personalizada
5. Actualización del contexto de conversación
6. Retorno de respuesta con datos energéticos relevantes
```

### 3️⃣ **links_routes.py - ENLACES ENERGÉTICOS**

**Prefijo:** `/api/v1/links`

| Endpoint                       | Método | Auth    | Función                                              |
| ------------------------------ | ------ | ------- | ---------------------------------------------------- |
| `/energy-report/<link_id>`     | GET    | Público | `get_energy_report()` - Reportes energéticos         |
| `/tariff-comparison/<link_id>` | GET    | Público | `get_tariff_comparison()` - Comparaciones de tarifas |

---

## 🔧 **SERVICIOS ESPECIALIZADOS EN ENERGÍA**

### 1️⃣ **services/analysis_service.py - ANÁLISIS ENERGÉTICO**

**Funciones Principales:**

- 📊 `analyze_consumption_patterns()` - Análisis de patrones de consumo
- 📈 `calculate_efficiency_metrics()` - Métricas de eficiencia
- 💰 `estimate_savings()` - Estimación de ahorros
- 📉 `detect_anomalies()` - Detección de anomalías en consumo

**Algoritmos Implementados:**

- 🧮 Análisis de series temporales para consumo
- 📊 Clustering de patrones de uso
- 🔍 Detección de outliers
- 📈 Predicción de consumo futuro

### 2️⃣ **services/chatbot_service.py - IA CONVERSACIONAL**

**Funciones Principales:**

- 🤖 `process_user_message()` - Procesamiento de mensajes
- 🧠 `generate_ai_response()` - Generación de respuestas IA
- 💬 `maintain_conversation_context()` - Contexto conversacional
- 📊 `extract_energy_intent()` - Extracción de intenciones energéticas

**Capacidades del Chatbot:**

- 💡 Recomendaciones de ahorro energético
- 📊 Explicación de facturas y consumos
- ⚡ Información sobre tarifas
- 🏠 Consejos de eficiencia doméstica

### 3️⃣ **services/billing_service.py - FACTURACIÓN**

**Funciones Principales:**

- 💰 `calculate_bill_estimate()` - Estimación de facturas
- 📄 `parse_bill_data()` - Análisis de facturas subidas
- 📊 `generate_consumption_report()` - Reportes de consumo
- 💸 `calculate_potential_savings()` - Cálculo de ahorros potenciales

### 4️⃣ **services/tariff_service.py - GESTIÓN DE TARIFAS**

**Funciones Principales:**

- ⚡ `get_available_tariffs()` - Tarifas disponibles
- 🔍 `find_best_tariff()` - Búsqueda de mejor tarifa
- 📊 `compare_tariff_costs()` - Comparación de costos
- 🏷️ `validate_tariff_data()` - Validación de datos de tarifas

**Integración con Fuentes Externas:**

- 🌐 **ESIOS API** - Precios oficiales del mercado
- 📊 **BigQuery** - Historial de tarifas
- 🔄 **Actualizaciones automáticas** de precios

### 5️⃣ **services/recommendation_service.py - RECOMENDACIONES IA**

**Funciones Principales:**

- 💡 `generate_personalized_recommendations()` - Recomendaciones personalizadas
- 🏠 `analyze_home_efficiency()` - Análisis de eficiencia del hogar
- 📱 `suggest_usage_optimizations()` - Optimizaciones de uso
- 💰 `calculate_roi_improvements()` - ROI de mejoras

---

## 🔐 **SISTEMA DE AUTENTICACIÓN ENERGÉTICO**

### **Decoradores Especializados:**

- 🔒 `@token_required` - Autenticación básica
- 🏢 `@admin_required` - **Acceso administrativo para gestión de tarifas**
- ⚡ `@energy_user_required` - Usuario con perfil energético

### **Flujo de Autenticación para Tarifas Admin:**

```python
1. Verificación del token de administrador
2. Validación del rol 'admin'
3. Verificación de permisos de gestión de tarifas
4. Establecimiento de contexto administrativo
5. Logging de actividad administrativa
```

---

## 💾 **INTEGRACIÓN CON BASES DE DATOS ENERGÉTICAS**

### **Firebase Firestore - Colecciones Energéticas:**

- ⚡ `energy_profiles` - Perfiles energéticos de usuarios
- 💰 `user_bills` - Facturas procesadas
- 🏠 `consumption_data` - Datos de consumo
- 💬 `chat_conversations` - Conversaciones del chatbot

### **BigQuery - Tablas Energéticas:**

- ⚡ `market_tariffs` - **Tarifas del mercado energético**
- 📊 `consumption_analytics` - Analítica de consumo
- 💰 `billing_data` - Datos de facturación
- 🤖 `chatbot_interactions` - Interacciones del chatbot
- 📄 `uploaded_documents_log` - **Log de documentos subidos**

---

## 🤖 **FUNCIONALIDAD DEL CHATBOT IA**

### **Capacidades Principales:**

1. **🏠 Análisis de Facturas:**

   - Procesamiento automático de PDFs
   - Extracción de datos de consumo
   - Identificación de patrones de gasto

2. **💡 Recomendaciones Personalizadas:**

   - Análisis del perfil del usuario
   - Sugerencias de ahorro específicas
   - Comparación con usuarios similares

3. **⚡ Información de Tarifas:**

   - Explicación de diferentes tipos de tarifa
   - Cálculo de ahorros por cambio de tarifa
   - Alertas de mejores ofertas

4. **📊 Monitorización de Consumo:**
   - Seguimiento de tendencias
   - Alertas de consumo anómalo
   - Predicciones de facturas futuras

### **Flujo de Conversación:**

```python
Usuario: "¿Por qué mi factura de luz es tan alta este mes?"

Chatbot IA:
1. Analiza el perfil energético del usuario
2. Revisa facturas anteriores
3. Identifica incrementos de consumo
4. Compara con patrones estacionales
5. Genera respuesta personalizada con:
   - Causas probables del incremento
   - Recomendaciones específicas de ahorro
   - Comparación con tarifa actual vs. alternativas
   - Consejos de eficiencia energética
```

---

## 🏢 **FUNCIONALIDAD ADMINISTRATIVA DE TARIFAS**

### **1. Añadir Tarifa Individual (`/admin/tariffs/add`):**

**Características:**

- ✅ Validación robusta de datos
- ✅ Prevención de duplicados
- ✅ Mapeo automático de campos
- ✅ Logging de actividad administrativa
- ✅ Respuesta detallada con estadísticas

**Campos Procesados:**

```python
{
    "provider_name": "Nombre del proveedor",
    "tariff_name": "Nombre de la tarifa",
    "tariff_type": "regulated|free_market|pvpc",
    "fixed_monthly_fee": 25.50,
    "kwh_price_flat": 0.085,
    "kwh_price_peak": 0.095,
    "kwh_price_valley": 0.075,
    "power_price_per_kw_per_month": 3.45,
    "is_pvpc": false,
    "is_active": true
}
```

### **2. Añadir Tarifas en Lote (`/admin/tariffs/batch-add`):**

**Características:**

- 📦 Procesamiento masivo de tarifas
- 🔍 Validación individual por tarifa
- 📊 Estadísticas detalladas de procesamiento
- 🛡️ Manejo robusto de errores
- 📝 Logging completo de operaciones

**Estadísticas de Respuesta:**

```json
{
  "statistics": {
    "total_processed": 20,
    "successfully_inserted": 15,
    "duplicates_prevented": 3,
    "validation_errors_handled": 2
  }
}
```

---

## 🌐 **INTEGRACIÓN CON APIS EXTERNAS**

### **1. ESIOS API (Operador del Sistema Eléctrico Español):**

- 📊 Precios horarios del mercado
- ⚡ Precios PVPC oficiales
- 📈 Datos de demanda eléctrica
- 🌍 Información de renovables

### **2. Comunicación con Expert Bot API:**

- 🔄 Cross-service requests para contexto de usuario
- 📊 Sincronización de perfiles energéticos
- 💬 Intercambio de datos de conversación

---

## 🚀 **INSTRUCCIONES DE DESPLIEGUE ENERGÉTICO**

### **1. Configuración Específica de Energía:**

```env
# APIs externas de energía
ESIOS_API_TOKEN=your-esios-token
ENERGY_MARKET_API_URL=https://api.esios.ree.es

# Configuración BigQuery energética
BQ_MARKET_TARIFFS_TABLE_ID=market_tariffs
BQ_CONSUMPTION_TABLE_ID=consumption_analytics
BQ_BILLING_TABLE_ID=billing_data

# Configuración del chatbot IA
CHATBOT_MODEL=gpt-4-energy-specialist
CHATBOT_CONTEXT_WINDOW=8192
AI_RESPONSE_MAX_LENGTH=1000
```

### **2. Ejecución con Servicios Energéticos:**

```bash
# Verificar conexión con APIs energéticas
python utils/test_esios_connection.py

# Ejecutar con modo energético
export ENERGY_MODE=true
python run.py
```

---

## 🛠️ **MANTENIMIENTO ESPECÍFICO DE ENERGÍA**

### **Tareas de Mantenimiento Regulares:**

1. **🔄 Actualización de Tarifas:**

   - Ejecutar script de actualización diaria
   - Verificar nuevas tarifas de proveedores
   - Validar precios PVPC

2. **📊 Análisis de Calidad de Datos:**

   - Verificar consistencia de datos de consumo
   - Validar cálculos de facturación
   - Revisar anomalías en patrones

3. **🤖 Optimización del Chatbot:**
   - Revisar precisión de respuestas
   - Actualizar base de conocimiento energético
   - Ajustar algoritmos de recomendación

### **Métricas Específicas a Monitorizar:**

- ⚡ **Precisión de Cálculos:** Exactitud en estimaciones de ahorro
- 🤖 **Satisfacción del Chatbot:** Rating de utilidad de respuestas
- 📊 **Calidad de Datos:** Completitud de perfiles energéticos
- 🔄 **Sincronización:** Tiempo de respuesta cross-service

---

## 🐛 **SOLUCIÓN DE PROBLEMAS ENERGÉTICOS**

### **1. Error en Cálculos de Tarifas:**

```
Error: Precios PVPC no disponibles
Solución: Verificar conexión con ESIOS API
```

### **2. Chatbot No Responde Adecuadamente:**

```
Error: Contexto de usuario incompleto
Solución: Verificar comunicación con expert-bot-api
```

### **3. Datos de Consumo Inconsistentes:**

```
Error: Anomalías en patrones de consumo
Solución: Ejecutar script de validación de datos
```

---

## 📈 **ROADMAP ENERGÉTICO**

### **Versión 2025.2.0:**

- 🌞 Integración con datos de energía solar
- 🔋 Soporte para almacenamiento energético
- 📱 Optimización para dispositivos IoT

### **Versión 2025.3.0:**

- 🌍 Expansión a mercados energéticos europeos
- 🧠 IA predictiva para precios de energía
- 🏭 Soporte para consumidores industriales

### **Versión 2026.1.0:**

- ⚡ Gestión de vehículos eléctricos
- 🏠 Smart home automation
- 🌐 Blockchain para trading energético

---

## 🔗 **COMUNICACIÓN CON EXPERT BOT API**

### **ARQUITECTURA DE COMUNICACIÓN ENERGÉTICA**

El Energy IA API se especializa en **conversaciones inteligentes sobre energía** y colabora estrechamente con Expert Bot API para obtener **contexto completo del usuario** y gestionar **perfiles energéticos**.

```
┌─────────────────────┐         ┌─────────────────────┐
│                     │  Cross  │                     │
│   ENERGY IA API     │ Service │   EXPERT BOT API    │
│   (Chatbot IA)      │ ──────► │   (User Context)    │
│   Puerto 8081       │ Request │   Puerto 8080       │
│                     │         │                     │
└─────────────────────┘         └─────────────────────┘
  🤖 Especialista IA              📊 Gestor de Perfiles
  🗣️ Conversaciones               👤 Datos de Usuario
  ⚡ Análisis Energético           💾 Firebase/BigQuery
```

### **1️⃣ FLUJO DE COMUNICACIÓN CHATBOT**

#### **Endpoint Principal del Chatbot**

**Endpoint:** `POST /api/v1/chatbot/chat`  
**Ubicación:** `energy_ia_api_COPY/app/chatbot_routes.py`

#### **Proceso de Conversación Completo:**

1. **👤 Usuario envía mensaje** al chatbot de Energy IA API
2. **🔐 Validación de autenticación** con token del usuario
3. **📞 Solicitud de contexto** a Expert Bot API:

   ```python
   # Energy IA API solicita contexto del usuario
   def get_user_context_robust(self, user_token: str) -> Dict[str, Any]:
       headers = {"Authorization": f"Bearer {user_token}"}
       response = requests.get(
           f"{self.expert_bot_url}/api/v1/energy/users/profile",
           headers=headers,
           timeout=5
       )
   ```

4. **🏢 Expert Bot API responde** con contexto enriquecido:

   ```json
   {
     "user_name": "Juan",
     "home_type": "apartment",
     "num_inhabitants": 3,
     "consumption_kwh": 350,
     "has_solar_panels": false,
     "heating_type": "gas",
     "post_code_prefix": "28"
   }
   ```

5. **🤖 Generación de respuesta IA** personalizada:

   ```python
   # Procesamiento con contexto energético
   ai_response = self.chat_service.generate_contextual_response(
       message=user_message,
       user_context=user_context,
       conversation_history=conversation_history
   )
   ```

6. **📤 Respuesta final** al usuario con personalización completa

### **2️⃣ GESTIÓN ROBUSTA DE CONTEXTO**

#### **Clase EnterpriseChatbotService**

**Ubicación:** `energy_ia_api_COPY/app/chatbot_routes.py`

**Características Principales:**

- 🔄 **Fallbacks automáticos** ante errores de comunicación
- ⏱️ **Timeouts configurables** para evitar bloqueos
- 💾 **Cache de contexto** para usuarios frecuentes
- 🛡️ **Modo offline** cuando Expert Bot API no está disponible

#### **Fallback Strategy:**

```python
def get_user_context_robust(self, user_token: str, timeout: int = 5):
    try:
        # 1. Intentar obtener contexto completo
        response = requests.get(expert_bot_url, headers=headers, timeout=timeout)
        if response.status_code == 200:
            return self._process_user_context(response.json())

        # 2. Si falla, usar contexto vacío (auto-creación activada)
        else:
            return self._get_empty_context()

    except requests.exceptions.Timeout:
        # 3. Timeout: usar contexto cacheado
        return self._get_cached_context(user_token)

    except requests.exceptions.ConnectionError:
        # 4. Sin conexión: modo offline
        return self._get_empty_context()
```

### **3️⃣ PROCESAMIENTO DE CONTEXTO ENERGÉTICO**

#### **Extracción de Nombre del Usuario:**

```python
def _process_user_context(self, profile_data: Dict) -> Dict[str, Any]:
    # USAR user_id como nombre real del usuario
    user_name = profile_data.get("user_id", "").strip()

    # Contexto energético completo
    context = {
        "user_name": user_name,  # 👤 Nombre para personalización
        "has_complete_data": bool(profile_data.get("consumption_kwh")),
        "home_type": profile_data.get("home_type", ""),
        "num_inhabitants": profile_data.get("num_inhabitants", 0),
        "heating_type": profile_data.get("heating_type", ""),
        "has_ac": profile_data.get("has_ac", False),
        "has_solar_panels": profile_data.get("has_solar_panels", False),
        "monthly_consumption": profile_data.get("monthly_consumption_kwh", 0)
    }
    return context
```

### **4️⃣ INTEGRACIÓN CON IA CONVERSACIONAL**

#### **Servicio de Chat Generativo**

**Ubicación:** `energy_ia_api_COPY/app/services/generative_chat_service.py`

**Personalización de Respuestas:**

```python
# El chatbot usa el contexto para personalizar respuestas
user_context = get_user_context_robust(user_token)

ai_prompt = f"""
Usuario: {user_context['user_name']}
Tipo de vivienda: {user_context['home_type']}
Consumo mensual: {user_context['monthly_consumption']} kWh
Pregunta: {user_message}

Responde de forma personalizada y específica para su situación energética.
"""

response = generative_ai.generate_response(ai_prompt)
```

#### **Capacidades de Personalización:**

- 🏠 **Análisis específico** por tipo de vivienda
- 📊 **Recomendaciones basadas** en consumo real
- 💰 **Cálculos de ahorro** personalizados
- ⚡ **Comparaciones de tarifas** según perfil

### **5️⃣ COMUNICACIÓN CROSS-SERVICE AVANZADA**

#### **Expert Bot API - Endpoint Receptor**

**Endpoint:** `POST /api/v1/chat/cross-service`

Cuando Energy IA API necesita procesamiento avanzado:

```python
# Energy IA API envía mensaje para procesamiento
cross_service_request = {
    "message": "Analiza mi consumo y recomienda la mejor tarifa",
    "user_id": user_id,
    "source": "energy_ia_api",
    "conversation_context": {
        "topic": "tariff_optimization",
        "user_preferences": user_preferences
    }
}

response = requests.post(
    f"{expert_bot_url}/api/v1/chat/cross-service",
    headers={"Authorization": f"Bearer {user_token}"},
    json=cross_service_request
)
```

#### **Procesamiento en Expert Bot API:**

- 📊 **Análisis de datos** en BigQuery
- 🔍 **Consultas complejas** de tarifas
- 💡 **Algoritmos de optimización** energética
- 📈 **Generación de reportes** detallados

### **6️⃣ CONFIGURACIÓN DE COMUNICACIÓN**

#### **Variables de Entorno Críticas:**

```env
# URL del Expert Bot API
EXPERT_BOT_API_URL=http://localhost:8080
# En producción: https://expert-bot-api-service-url

# Timeouts de comunicación
CROSS_SERVICE_TIMEOUT=5
CONNECTION_RETRY_ATTEMPTS=3

# Cache de contexto
CONTEXT_CACHE_TTL=300  # 5 minutos
ENABLE_CONTEXT_CACHE=true
```

#### **Configuración en chatbot_routes.py:**

```python
self.expert_bot_url = current_app.config.get(
    "EXPERT_BOT_API_URL",
    "http://localhost:8081"  # Fallback local
)
```

### **7️⃣ LOGGING Y MONITORIZACIÓN DE COMUNICACIÓN**

#### **Logging Detallado:**

```python
# Logging de peticiones cross-service
logger.info(f"🔄 Obteniendo contexto de usuario desde expert-bot-api: {user_id}")
logger.info(f"⏱️ Tiempo de respuesta cross-service: {response_time}ms")
logger.warning(f"⚠️ Fallback activado para usuario: {user_id}")
```

#### **Métricas de Comunicación:**

- ⏱️ **Latencia media** de solicitudes cross-service
- 📊 **Tasa de éxito** de comunicación entre servicios
- 🔄 **Frecuencia de fallbacks** utilizados
- 👥 **Usuarios con contexto completo** vs. contexto vacío

### **8️⃣ VENTAJAS DE LA INTEGRACIÓN**

#### **Para el Usuario:**

- 🤖 **Respuestas personalizadas** con su nombre real
- 📊 **Análisis específicos** basados en su perfil
- 💰 **Recomendaciones precisas** según su consumo
- 🏠 **Consejos adaptados** a su tipo de vivienda

#### **Para el Sistema:**

- 🔄 **Auto-creación** de perfiles faltantes
- 🛡️ **Robustez** ante fallos de comunicación
- 📈 **Escalabilidad** independiente de servicios
- 🎯 **Especialización** de cada microservicio

### **9️⃣ CASOS DE USO TÍPICOS**

#### **1. Usuario Nuevo (Sin Perfil):**

```
Usuario: "Hola, ¿cómo puedo ahorrar en mi factura?"
┌─ Energy IA API solicita contexto
├─ Expert Bot API detecta: usuario sin perfil
├─ Crea automáticamente perfil mínimo
├─ Extrae nombre de Firebase: "María"
└─ Retorna contexto básico

Respuesta: "Hola María, para ayudarte a ahorrar..."
```

#### **2. Usuario con Perfil Completo:**

```
Usuario: "¿Cuánto ahorraría con tarifa nocturna?"
┌─ Energy IA API obtiene contexto completo
├─ Expert Bot API retorna: consumo, horarios, tipo vivienda
├─ Energy IA API calcula específicamente
└─ Respuesta personalizada con cálculos reales

Respuesta: "Juan, con tu consumo de 400kWh/mes y tu patrón nocturno, ahorrarías 45€/mes..."
```

#### **3. Análisis Avanzado:**

```
Usuario: "Hazme un análisis completo de eficiencia"
┌─ Energy IA API detecta: consulta compleja
├─ Envía cross-service request a Expert Bot API
├─ Expert Bot API ejecuta análisis en BigQuery
├─ Genera reporte completo con recomendaciones
└─ Energy IA API presenta resultados conversacionalmente

Respuesta: "He analizado tu perfil completo, Ana. Tu eficiencia actual es..."
```

### **🔟 TESTING DE INTEGRACIÓN**

#### **Tests Automatizados:**

```python
def test_cross_service_communication():
    # Test comunicación básica
    response = chatbot_service.get_user_context_robust(valid_token)
    assert response['user_name'] is not None

def test_fallback_behavior():
    # Test con Expert Bot API caído
    with mock_service_down():
        response = chatbot_service.get_user_context_robust(valid_token)
        assert response == chatbot_service._get_empty_context()
```

#### **Monitorización en Producción:**

- 🏥 **Health checks** entre servicios cada 30 segundos
- 📊 **Dashboards** de latencia cross-service
- 🚨 **Alertas** cuando tasa de fallbacks > 10%
- 📈 **Métricas** de satisfacción del usuario por calidad de respuesta
