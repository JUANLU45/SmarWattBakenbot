# 🤖 DOCUMENTACIÓN COMPLETA - EXPERT BOT API

## 📋 **INFORMACIÓN GENERAL**

**Nombre del Microservicio:** Expert Bot API  
**Versión:** 2.0.0 - EMPRESARIAL COPY  
**Puerto:** 8080  
**Tecnología:** Flask + Python 3.10+  
**Base de Datos:** Firebase Firestore + BigQuery  
**Autenticación:** Firebase Admin SDK + JWT

---

## 📁 **ESTRUCTURA COMPLETA DE ARCHIVOS**

```
expert_bot_api_COPY/
│
├── 📄 ARCHIVOS DE CONFIGURACIÓN
│   ├── .env                     # Variables de entorno (SENSIBLE)
│   ├── .env.example            # Plantilla de variables de entorno
│   ├── .dockerignore           # Archivos ignorados por Docker
│   ├── Dockerfile              # Configuración de contenedor Docker
│   ├── pyproject.toml          # Configuración del proyecto Python
│   ├── requirements-base.txt   # Dependencias base del proyecto
│   ├── requirements-dev.txt    # Dependencias de desarrollo
│   ├── requirements-ml.txt     # Dependencias de Machine Learning
│   ├── requirements.txt        # TODAS las dependencias
│   └── run.py                  # 🚀 ARCHIVO PRINCIPAL DE EJECUCIÓN
│
├── 📦 app/ - NÚCLEO DE LA APLICACIÓN
│   ├── __init__.py             # ⚙️ Inicializador de la aplicación Flask
│   ├── config.py               # 🔧 Configuraciones por entorno
│   │
│   ├── 🛣️ RUTAS PRINCIPALES
│   ├── routes.py               # Endpoints básicos y salud del sistema
│   ├── async_routes.py         # 🔄 Endpoints de tareas asíncronas + ADMIN
│   ├── energy_routes.py        # ⚡ Endpoints de energía y perfiles
│   ├── cross_service_routes.py # 🔗 Comunicación entre microservicios
│   └── links_routes.py         # 🔗 Gestión de enlaces y redirecciones
│   │
│   ├── 🔧 SERVICIOS CORE
│   ├── energy_service.py       # 📊 Lógica de negocio energética
│   └── services/               # 📁 Servicios especializados
│       ├── ai_service.py       # 🤖 Servicio de IA y Machine Learning
│       ├── async_service.py    # ⏰ Gestión de tareas asíncronas
│       ├── bigquery_service.py # 📈 Integración con BigQuery
│       ├── energy_service.py   # ⚡ Servicios energéticos avanzados
│       ├── firebase_service.py # 🔥 Integración con Firebase
│       └── ml_service.py       # 🧠 Servicios de Machine Learning
│
├── 🔐 smarwatt_auth/ - SISTEMA DE AUTENTICACIÓN
│   ├── __init__.py            # Inicializador del módulo de auth
│   └── auth.py                # 🛡️ Decoradores y lógica de autenticación
│
├── 🛠️ utils/ - UTILIDADES EMPRESARIALES
│   ├── __init__.py            # Inicializador de utilidades
│   ├── error_handlers.py      # 🚨 Manejo de errores empresarial
│   ├── logging_config.py      # 📝 Configuración de logs
│   └── validators.py          # ✅ Validadores de datos
│
├── 📊 logs/ - ARCHIVOS DE LOG
│   └── expert_bot_api_*.log   # Logs rotativos por fecha
│
├── 🧪 ARCHIVOS DE TESTING
│   └── test_integration.py    # Tests de integración
│
└── 🐳 ARCHIVOS DOCKER Y CACHE
    └── __pycache__/           # Cache de Python (auto-generado)
```

---

## ⚙️ **COMPONENTES PRINCIPALES**

### 1️⃣ **run.py - EJECUTOR PRINCIPAL**

**Ubicación:** `expert_bot_api_COPY/run.py`

**Función:** Punto de entrada principal de la aplicación

**Características:**

- ✅ Configuración de logging empresarial
- ✅ Inicialización de la aplicación Flask
- ✅ Configuración de entorno automática
- ✅ Manejo de errores de inicio
- ✅ Logging rotativo por fechas

**Configuración de Inicio:**

```python
# Variables de entorno importantes
PORT = int(os.getenv("PORT", 8080))
HOST = os.getenv("HOST", "0.0.0.0")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
FLASK_CONFIG =**s.ge**nv("FLASK_CONFIG", "production")

```

### 2️⃣ **app/**init**.py - INICIALIZADOR DE APLICACIÓN**

**Ubicación:** `expert_bot_api_COPY/app/__init__.py`

**Función:** Configuración y creación de la aplicación Flask

**Componentes Críticos:**

- 🔥 **Inicialización Firebase Admin SDK**
- 🌐 **Configuración CORS empresarial**

- 🛣️ **Registro de blueprints**
- 🚨 **Manejo de errores global**
- 📝 **Middleware de logging**

**Blueprints Registrados:**

```python
# Registro de rutas principales
app.register_blueprint(routes_bp, url_prefix="/api/v1")
app.register_blueprint(async_bp, url_prefix="/api/v1/async")

app.register_blueprint(energy_bp, url_prefix="/api/v1/energy")
app.register_blueprint(cross_service_bp, url_prefix="/api/v1/chat")
app.register_blueprint(links_bp, url_prefix="/api/v1/links")
```

### 3️⃣ **config.py - CONFIGURACIONES POR ENTORNO**

**Ubicación:** `expert_bot_api_COPY/app/config.py`

**Función:** Gestión de configuraciones por entorno (development, production, testing)

**Configuraciones Críticas:**

- 🔑 **Credenciales Google Cloud**
- 📊 **Configuración BigQuery**
- 🔥 **Configuración Firebase**

- 🌐 **CORS Origins**
- 📝 **Niveles de logging**

---

## 🛣️ **DOCUMENTACIÓN DE RUTAS**

### 1️⃣ **routes.py - ENDPOINTS BÁSICOS**

**Prefijo:** `/api/v1`

| Endpoint   | Método | Función             | Descripción                    |
| ---------- | ------ | ------------------- | ------------------------------ |
| `/health`  | GET    | `health_check()`    | ✅ Estado de salud del sistema |
| `/ready`   | GET    | `readiness_check()` | ✅ Estado de preparación       |
| `/version` | GET    | `get_version()`     | 📊 Información de versión      |

### 2️⃣ **async_routes.py - TAREAS ASÍNCRONAS + ADMIN**

**Prefijo:** `/api/v1/async`

| Endpoint                  | Método | Auth     | Función                                             |
| ------------------------- | ------ | -------- | --------------------------------------------------- |
| `/submit`                 | POST   | 🔒 Token | `submit_task()` - Enviar tarea asíncrona            |
| `/status/<task_id>`       | GET    | 🔒 Token | `get_task_status()` - Estado de tarea               |
| `/admin/system/metrics`   | GET    | 🏢 Admin | `get_admin_system_metrics()` - Métricas del sistema |
| `/admin/tasks/management` | GET    | 🏢 Admin | `get_admin_task_management()` - Gestión de tareas   |

### 3️⃣ **energy_routes.py - SERVICIOS ENERGÉTICOS**

**Prefijo:** `/api/v1/energy`

| Endpoint   | Método | Auth     | Función                                                     |
| ---------- | ------ | -------- | ----------------------------------------------------------- |
| `/profile` | GET    | 🔒 Token | `get_user_energy_profile()` - Perfil energético del usuario |

| `/consumption/analysis` | POST | 🔒 Token | `analyze_consumption()` - Análisis de consumo |
| `/recommendations` | GET | 🔒 Token | `get_energy_recommendations()` - Recomendaciones |

### 4️⃣ **cross_service_routes.py - COMUNICACIÓN INTER-MICROSERVICIOS**

**Prefijo:** `/api/v1/chat`

| Endpoint         | Método | Auth     | Función                                                         |
| ---------------- | ------ | -------- | --------------------------------------------------------------- |
| `/cross-service` | POST   | 🔒 Token | `handle_cross_service_request()` - Comunicación entre servicios |

### 5️⃣ **links_routes.py - GESTIÓN DE ENLACES**

**Prefijo:** `/api/v1/links`

| Endpoint             | Método | Auth     | Función                            |
| -------------------- | ------ | -------- | ---------------------------------- |
| `/create`            | POST   | 🔒 Token | `create_link()` - Crear enlace     |
| `/resolve/<link_id>` | GET    | Público  | `resolve_link()` - Resolver enlace |

---

## 🔧 **SERVICIOS ESPECIALIZADOS**

### 1️⃣ **energy_service.py - SERVICIOS ENERGÉTICOS CORE**

**Ubicación:** `app/energy_service.py`

**Funciones Principales:**

- 🔄 `_get_user_energy_profile_enterprise()` - Obtención de perfiles energéticos
- ✨ `_create_minimal_user_profile()` - **CREACIÓN AUTOMÁTICA DE PERFILES**
- 📊 `get_enhanced_user_context()` - Contexto completo del usuario

**Funcionalidad Crítica:**

```python
# Auto-creación de perfiles cuando no existen
if not profile_data:
    logger.info(f"Perfil no encontrado para {user_id}, creando perfil mínimo")
    minimal_profile = await _create_minimal_user_profile(user_id, firebase_user)

```

### 2️⃣ **services/async_service.py - GESTIÓN ASÍNCRONA**

**Funciones Principales:**

- ⏰ `submit_task()` - Envío de tareas asíncronas
- 📊 `get_task_status()` - Estado de tareas
- 📈 `get_system_status()` - Métricas del sistema
- 👥 `get_worker_metrics()` - Métricas de workers

### 3️⃣ **services/bigquery_service.py - INTEGRACIÓN BIGQUERY**

**Funciones Principales:**

- 📊 `execute_query()` - Ejecución de queries
- 💾 `insert_data()` - Inserción de datos

- 📈 `get_analytics_data()` - Datos analíticos

### 4️⃣ **services/firebase_service.py - INTEGRACIÓN FIREBASE**

**Funciones Principales:**

- 👤 `get_user_profile()` - Perfiles de usuario
- 💾 `update_user_data()` - Actualización de datos
- 🔐 `verify_token()` - Verificación de tokens

---

## 🔐 **SISTEMA DE AUTENTICACIÓN**

### **smarwatt_auth/auth.py**

**Decoradores Disponibles:**

- 🔒 `@token_required` - Autenticación básica
- 🏢 `@admin_required` - Acceso administrativo
- 📊 `@enterprise_auth` - Autenticación empresarial

**Usuario Admin Autorizado:**

- **Nombre:** "Tomates Juanlu"
- **UID:** `56bE1dNrjef8kO0Erg1qKQytKAq2`
- **Rol:** `admin`

**Flujo de Autenticación:**

```python
1. Extracción del token del header Authorization
2. Verificación con Firebase Admin SDK
3. Obtención del contexto del usuario

4. Validación de roles y permisos
5. Establecimiento del contexto global (g.user)
```

---

## 💾 **INTEGRACIÓN CON BASES DE DATOS**

### **Firebase Firestore - Colecciones:**

- 👥 `users` - Datos básicos de usuarios
- 📊 `user_profiles_enriched` - Perfiles energéticos completos
- 📄 `documents` - Documentos subidos
- 🔗 `links` - Enlaces gestionados

### **BigQuery - Tablas:**

- ⏰ `async_tasks` - Tareas asíncronas
- 👥 `worker_metrics` - Métricas de workers
- 📊 `user_analytics` - Analítica de usuarios

- 📄 `uploaded_documents_log` - Log de documentos

---

## 🚀 **INSTRUCCIONES DE DESPLIEGUE**

### **1. Preparación del Entorno:**

```bash

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con las credenciales correctas
```

### **2. Ejecución Local:**

```bash
# Modo desarrollo
python run.py


# Modo producción
export FLASK_CONFIG=production
python run.py
```

### **3. Docker:**

```bash
# Construir imagen
docker build -t expert-bot-api .


# Ejecutar contenedor
docker run -p 8080:8080 expert-bot-api
```

### **4. Google Cloud Run:**

```bash
# Deploy automático
gcloud run deploy expert-bot-api \
  --source . \
  --platform managed \
  --region europe-west1 \
  --allow-unauthenticated
```

---

## 🛠️ **MANTENIMIENTO Y MONITORIZACIÓN**

### **Logs Importantes:**

- 📝 `expert_bot_api_YYYYMMDD.log` - Logs principales
- 🚨 `error.log` - Solo errores críticos
- 📊 `access.log` - Logs de acceso HTTP

### **Métricas a Monitorizar:**

- 🏃 **Rendimiento:** Tiempo de respuesta de endpoints
- 👥 **Usuarios:** Nuevos registros y actividad
- ⚡ **Tareas:** Cola de tareas asíncronas
- 💾 **Memoria:** Uso de recursos del sistema

### **Endpoints de Salud:**

- `/api/v1/health` - Estado general
- `/api/v1/ready` - Preparación para tráfico
- `/api/v1/version` - Información de versión

### **Alertas Críticas:**

- 🚨 Error rate > 5%
- ⏰ Response time > 2s
- 💾 Memory usage > 80%
- 📊 BigQuery quota exceeded

---

## 🔧 **CONFIGURACIÓN DE VARIABLES DE ENTORNO**

### **Variables Críticas (.env):**

```env

# Configuración de la aplicación
FLASK_CONFIG=production
PORT=8080
DEBUG=False

# Google Cloud Platform

GCP_PROJECT_ID=smarwatt-c85f4
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json

# BigQuery
BQ_DATASET_ID=smarwatt_data
BQ_ASYNC_TASKS_TABLE_ID=async_tasks

BQ_WORKER_METRICS_TABLE_ID=worker_metrics

# Firebase
FIREBASE_PROJECT_ID=smarwatt-c85f4

# Seguridad
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=https://smarwatt.com,https://admin.smarwatt.com

# Logging

LOG_LEVEL=INFO
```

---

## 🐛 **SOLUCIÓN DE PROBLEMAS COMUNES**

### **1. Error de Autenticación Firebase:**

```

Error: Firebase Admin SDK no inicializado
Solución: Verificar GOOGLE_APPLICATION_CREDENTIALS
```

### **2. Error de Conexión BigQuery:**

```
Error: 403 Forbidden
Solución: Verificar permisos del service account
```

### **3. Error en Creación de Perfiles:**

```
Error: user_profiles_enriched no encontrado
Solución: Verificar que la colección existe en Firestore
```

### **4. Error de CORS:**

```
Error: CORS policy blocked
Solución: Añadir dominio a CORS_ORIGINS en .env
```

---

## 📈 **ROADMAP Y MEJORAS FUTURAS**

### **Versión 2.1.0:**

- 🤖 Integración con más modelos de IA

- 📊 Dashboard de analítica avanzada
- 🔄 Mejoras en el sistema de tareas asíncronas

### **Versión 2.2.0:**

- 🌍 Soporte multi-idioma
- 📱 API móvil optimizada
- 🔐 Autenticación SSO

### **Versión 3.0.0:**

- 🚀 Migración a arquitectura de microservicios
- ☁️ Soporte multi-cloud

- 🧠 IA predictiva avanzada

---

## 🔗 **COMUNICACIÓN ENTRE MICROSERVICIOS**

### **ARQUITECTURA DE COMUNICACIÓN**

El Expert Bot API actúa como el **servicio central de gestión de usuarios y datos**, mientras que Energy IA API se especializa en **conversaciones y análisis energético**. La comunicación entre ambos es bidireccional y robusta.

```
┌─────────────────────┐         ┌─────────────────────┐
│                     │  HTTP   │                     │
│   ENERGY IA API     │ ──────► │   EXPERT BOT API    │
│   (Puerto 8081)     │ Requests│   (Puerto 8080)     │
│                     │ ◄────── │                     │
└─────────────────────┘         └─────────────────────┘
     Especialista                  Gestor Central
     Conversacional                de Datos
```

### **1️⃣ ENDPOINT DE COMUNICACIÓN PRINCIPAL**

#### **Expert Bot API - Receptor Cross-Service**

**Endpoint:** `POST /api/v1/chat/cross-service`  
**Ubicación:** `expert_bot_api_COPY/app/cross_service_routes.py`

**Función:** Recibe peticiones del Energy IA API para procesamiento con contexto completo del usuario.

**Request Format:**

```json
{
    "message": "¿Cuánto puedo ahorrar cambiando de tarifa?",
    "user_id": "user_abc123",
    "source": "energy_ia_api",
    "conversation_context": {
        "previous_messages": [...],
        "current_topic": "tariff_comparison"
    }
}
```

**Response Format:**

```json
{
  "status": "success",
  "response": "Basándome en tu perfil energético, Juan...",
  "conversation_id": "conv_xyz789",
  "user_context": {
    "user_name": "Juan",
    "has_complete_data": true,
    "home_type": "apartment",

    "consumption_profile": "medium"
  },
  "timestamp": "2025-01-20T10:30:00Z"
}
```

### **2️⃣ FLUJO DE COMUNICACIÓN DETALLADO**

#### **Escenario: Usuario chatea en Energy IA API**

1. **📱 Usuario envía mensaje** al chatbot en Energy IA API
2. **🔍 Energy IA API valida** el token del usuario
3. **📞 Solicitud Cross-Service** a Expert Bot API:

   ```python
   # Energy IA API hace petición
   response = requests.post(

       f"{expert_bot_url}/api/v1/chat/cross-service",
       headers={"Authorization": f"Bearer {user_token}"},
       json={
           "message": user_message,
           "user_id": user_id,
           "source": "energy_ia_api"
       }
   )
   ```

4. **🏢 Expert Bot API procesa** la petición:

   - Verifica autenticación del usuario
   - Obtiene/crea perfil energético del usuario
   - Enriquece contexto con datos de BigQuery/Firebase
   - Procesa mensaje con ChatService especializado

5. **📊 Respuesta enriquecida** de Expert Bot API:

   - Contexto completo del usuario
   - Respuesta procesada con IA
   - Metadatos de conversación

6. **🤖 Energy IA API genera** respuesta final:

   - Combina contexto recibido
   - Aplica especialización energética

   - Personaliza respuesta con nombre del usuario
   - Retorna respuesta al usuario

### **3️⃣ GESTIÓN DE PERFILES DE USUARIO**

#### **Auto-Creación de Perfiles (Expert Bot API)**

**Función:** `_create_minimal_user_profile()`  
**Ubicación:** `expert_bot_api_COPY/app/energy_service.py`

Cuando Energy IA API solicita contexto de un usuario nuevo:

```python
# Si no existe perfil, se crea automáticamente
if not profile_data:
    logger.info(f"Perfil no encontrado para {user_id}, creando perfil mínimo")
    minimal_profile = await _create_minimal_user_profile(user_id, firebase_user)

# Extracción del nombre real del displayName
user_name = firebase_user.display_name or "Usuario"

# Se almacena en el campo user_id (que contiene el nombre real)
```

#### **Sincronización de Datos:**

- ✅ **Firebase Firestore**: Datos de perfil y preferencias
- ✅ **BigQuery**: Analítica y métricas de uso
- ✅ **Tiempo Real**: Sincronización inmediata entre servicios

### **4️⃣ MANEJO ROBUSTO DE ERRORES**

#### **Fallbacks Implementados:**

1. **🔄 Timeout de Comunicación:**

   ```python
   try:
       response = requests.get(url, timeout=5)
   except requests.exceptions.Timeout:
       return self._get_cached_context(user_token)
   ```

2. **🌐 Error de Conexión:**

   ```python
   except requests.exceptions.ConnectionError:
       logger.warning("Error de conexión - modo offline")
       return self._get_empty_context()
   ```

3. **👤 Usuario Sin Perfil:**

   ```python
   # Expert Bot API crea automáticamente perfil mínimo
   if not user_profile:
       minimal_profile = create_minimal_user_profile(user_id)
   ```

### **5️⃣ AUTENTICACIÓN ENTRE SERVICIOS**

#### **Token Forwarding:**

```python
# Energy IA API reenvía token del usuario
headers = {"Authorization": f"Bearer {user_token}"}

# Expert Bot API valida el mismo token

@token_required
def handle_cross_service_communication():
    # El decorador valida automáticamente el token
```

#### **Validación de Origen:**

```python
# Verificar que la petición viene de Energy IA API
if source != "energy_ia_api":
    raise AppError("Fuente no autorizada para este endpoint", 403)
```

### **6️⃣ LOGGING Y MONITORIZACIÓN**

#### **Logging Cross-Service:**

```python
# En Expert Bot API
logger.info(
    "Comunicación entre servicios recibida - Usuario: %s, Fuente: %s",
    user_id, source
)

# En Energy IA API
logger.info(
    "Obteniendo contexto de usuario desde expert-bot-api: %s",
    user_id
)
```

#### **Métricas a Monitorizar:**

- ⏱️ **Latencia Cross-Service**: Tiempo de respuesta entre servicios
- 📊 **Tasa de Éxito**: % de comunicaciones exitosas
- 🔄 **Uso de Fallbacks**: Frecuencia de uso de contextos cache/vacío
- 👥 **Creación de Perfiles**: Nuevos usuarios procesados automáticamente

### **7️⃣ CONFIGURACIÓN DE ENDPOINTS**

#### **Variables de Entorno Críticas:**

```env
# En Energy IA API
EXPERT_BOT_API_URL=http://localhost:8080

# En Expert Bot API
ENERGY_IA_API_URL=http://localhost:8081

# URLs de producción en Cloud Run
EXPERT_BOT_API_URL=https://expert-bot-api-service-url
ENERGY_IA_API_URL=https://energy-ia-api-service-url
```

### **8️⃣ TESTING DE COMUNICACIÓN**

#### **Verificación de Conectividad:**

```python
# Test de comunicación básica
response = requests.get(f"{expert_bot_url}/api/v1/health")
assert response.status_code == 200

# Test de cross-service con usuario real
response = requests.post(
    f"{expert_bot_url}/api/v1/chat/cross-service",
    headers={"Authorization": f"Bearer {valid_token}"},
    json={"message": "test", "user_id": "test_user", "source": "energy_ia_api"}
)
assert response.status_code == 200
```

### **9️⃣ VENTAJAS DE LA ARQUITECTURA**

- 🎯 **Separación de Responsabilidades**: Cada servicio tiene su especialización
- 🔄 **Escalabilidad Independiente**: Los servicios pueden escalar por separado
- 🛡️ **Robustez**: Fallbacks automáticos ante fallos de comunicación
- 📊 **Trazabilidad**: Logging completo de comunicaciones inter-servicio
- ⚡ **Performance**: Auto-creación de perfiles reduce llamadas repetitivas
