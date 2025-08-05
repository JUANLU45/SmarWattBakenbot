# 📊 DOCUMENTACIÓN ENDPOINT: `/api/v1/energy/tariffs/recommendations`

## 🏷️ INFORMACIÓN GENERAL

**URL COMPLETA DE PRODUCCIÓN:** `https://energy-ia-api-1010012211318.europe-west1.run.app/api/v1/energy/tariffs/recommendations`

**MICROSERVICIO:** Energy IA API (energy_ia_api_COPY)

**MÉTODO HTTP:** GET

**AUTENTICACIÓN:** ✅ Requerida (Token Firebase JWT)

**PREFIJO:** `/api/v1/energy`

---

## 🔧 IMPLEMENTACIÓN BACKEND

### 📍 Ubicación del Código
```
Archivo: /app/routes.py
Línea: 524-640
Decoradores: @energy_bp.route("/tariffs/recommendations", methods=["GET"]) @token_required
Función: get_tariff_recommendations_route()
```

### 🔐 Autenticación y Autorización
```python
@token_required
def get_tariff_recommendations_route():
    user_id = g.user.get("uid")  # Obtiene UID del token Firebase
```

### 📥 PARÁMETROS DE ENTRADA
**Tipo:** Ninguno (GET sin parámetros)
**Validación:** Token Firebase válido en header Authorization

### 🔄 FLUJO DE PROCESAMIENTO

#### PASO 1: Obtención del Perfil de Usuario
```python
# Llamada HTTP a Expert Bot API
expert_bot_url = current_app.config.get("EXPERT_BOT_API_URL")
response = requests.get(
    f"{expert_bot_url}/api/v1/energy/users/profile",
    headers={"Authorization": f"Bearer {g.token}"},
    timeout=15,
)
```

**URL DEPENDENCIA:** `https://expert-bot-api-1010012211318.europe-west1.run.app/api/v1/energy/users/profile`

#### PASO 2: Validación de Datos
```python
consumption_profile = {
    "user_id": user_id,
    "avg_kwh": consumption_data["last_invoice_data"].get("kwh_consumidos", 0),
    "peak_percent": consumption_data["last_invoice_data"].get("peak_percent_from_invoice", 50),
    "contracted_power_kw": consumption_data["last_invoice_data"].get("potencia_contratada_kw", 0),
    "num_inhabitants": consumption_data.get("num_inhabitants", 2),
    "home_type": consumption_data.get("home_type", "apartment"),
    "current_annual_cost": consumption_data["last_invoice_data"].get("importe_total", 0) * 12,
    "current_supplier": consumption_data["last_invoice_data"].get("supplier_name", "Unknown"),
    "usage_pattern": consumption_data.get("usage_pattern", "normal"),
}
```

#### PASO 3: Generación de Recomendación
```python
service = get_recommender_service()  # EnterpriseTariffRecommenderService
recommendation = service.get_advanced_recommendation(consumption_profile)
```

### 📤 RESPUESTA EXITOSA (HTTP 200)
```json
{
    "status": "success",
    "message": "Recomendación de tarifas generada exitosamente",
    "data": {
        "user_profile": {
            "user_id": "string",
            "avg_kwh": "number",
            "peak_percent": "number",
            "contracted_power_kw": "number",
            "num_inhabitants": "number",
            "home_type": "string",
            "current_annual_cost": "number",
            "current_supplier": "string",
            "usage_pattern": "string"
        },
        "best_recommendation": {
            "tariff": "object",
            "cost_analysis": {
                "annual_cost": "number",
                "monthly_cost": "number",
                "annual_savings": "number",
                "savings_percentage": "number"
            },
            "suitability_score": "number",
            "pros": ["string"],
            "cons": ["string"],
            "recommendation_reason": "string"
        },
        "top_3_alternatives": ["object"],
        "market_analysis": {
            "total_tariffs_analyzed": "number",
            "average_market_price": "number",
            "cheapest_option": "object",
            "most_popular": "object"
        },
        "ml_insights": "object",
        "generated_at": "string",
        "expires_at": "string"
    },
    "meta": {
        "generated_at": "2025-07-31T...",
        "service_version": "2025.1.0",
        "enterprise_mode": true
    }
}
```

### ❌ MANEJO DE ERRORES

#### Error 404 - Sin Perfil de Usuario
```json
{
    "status": "error",
    "message": "No se encontró perfil de consumo detallado para el usuario. Por favor, sube una factura.",
    "error_code": 404
}
```

#### Error 400 - Datos Incompletos
```json
{
    "status": "error",
    "message": "Datos de consumo incompletos para generar recomendación",
    "error_code": 400
}
```

#### Error 500 - Error de Configuración
```json
{
    "status": "error",
    "message": "Configuración de servicio Expert Bot no disponible",
    "error_code": 500
}
```

#### Error 500 - Error Interno
```json
{
    "status": "error",
    "message": "Error interno del servidor",
    "error_code": 500
}
```

---

## 🌐 IMPLEMENTACIÓN FRONTEND

### 📍 Ubicación del Código
```
Archivo: /src/services/dashboardService.js
Línea: 10-80
Función: getEnergyAnalysis()
Cliente API: energyIaApiClient
```

### 🔧 Implementación JavaScript
```javascript
async getEnergyAnalysis(analysisParams = {}) {
  try {
    console.log('🔍 Obteniendo análisis energético REAL desde /tariffs/recommendations');

    // ✅ USAR ENDPOINT REAL: /api/v1/energy/tariffs/recommendations
    const response = await energyIaApiClient.get(
      '/api/v1/energy/tariffs/recommendations',
      {
        timeout: 30000,
        headers: {
          'Content-Type': 'application/json',
        },
      },
    );

    const recommendationData = response.data.data;

    // ✅ MAPEAR DATOS REALES A FORMATO QUE ESPERA EL FRONTEND
    const analysisData = {
      consumptionPattern: this._analyzeConsumptionPattern(recommendationData.user_profile),
      peakHours: this._extractPeakHours(recommendationData.user_profile),
      efficiency: this._calculateEfficiencyScore(recommendationData.best_recommendation),
    };

    return analysisData;
  } catch (error) {
    console.error('❌ Error obteniendo análisis energético:', error);
    throw error;
  }
}
```

### 🔗 Configuración del Cliente API
```javascript
// Archivo: /src/services/apiClient.js
export const energyIaApiClient = createApiClient(
  import.meta.env.VITE_ENERGY_IA_API_URL  // https://energy-ia-api-1010012211318.europe-west1.run.app
);
```

### 🔐 Autenticación Automática
```javascript
// Interceptor de autenticación automático
const authInterceptor = async (config) => {
  const user = getAuth().currentUser;
  if (user) {
    const token = await user.getIdToken(true);
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
};
```

### 📤 Procesamiento de Respuesta
```javascript
// Transformación de datos para el frontend
const analysisData = {
  consumptionPattern: this._analyzeConsumptionPattern(recommendationData.user_profile),
  peakHours: this._extractPeakHours(recommendationData.user_profile),
  efficiency: this._calculateEfficiencyScore(recommendationData.best_recommendation),
};
```

### ❌ Manejo de Errores Frontend
```javascript
catch (error) {
  console.error('❌ Error obteniendo análisis energético:', error);
  
  if (error.isNetworkError) {
    // Error de conexión
  } else if (error.status === 404) {
    // Usuario sin perfil
  } else if (error.status === 400) {
    // Datos incompletos
  } else if (error.status === 500) {
    // Error interno
  }
  
  throw error;
}
```

---

## 🔍 DEPENDENCIAS Y COMUNICACIÓN

### 📡 Comunicación Inter-Servicios
```
Frontend (energyIaApiClient) 
    ↓ GET /api/v1/energy/tariffs/recommendations
Energy IA API (energy_ia_api_COPY)
    ↓ GET /api/v1/energy/users/profile  
Expert Bot API (expert_bot_api_COPY)
    ↓ BigQuery + ML Service
Respuesta Final
```

### 🔧 Servicios Utilizados
1. **EnterpriseTariffRecommenderService** - Motor de recomendaciones
2. **BigQuery Client** - Datos de tarifas del mercado
3. **VertexAI Service** - ML para refinamiento
4. **Expert Bot API** - Perfil de usuario

---

## ⚙️ CONFIGURACIÓN DE PRODUCCIÓN

### 🌍 Variables de Entorno Backend
```bash
EXPERT_BOT_API_URL=https://expert-bot-api-1010012211318.europe-west1.run.app
GCP_PROJECT_ID=smatwatt
BQ_DATASET_ID=smartwatt_data
BQ_MARKET_TARIFFS_TABLE_ID=market_electricity_tariffs
```

### 🌍 Variables de Entorno Frontend
```bash
VITE_ENERGY_IA_API_URL=https://energy-ia-api-1010012211318.europe-west1.run.app
```

---

## 🚀 ESTADO DE PRODUCCIÓN

✅ **BACKEND:** Implementado y funcional en energy-ia-api-1010012211318.europe-west1.run.app
✅ **FRONTEND:** Implementado en dashboardService.js
✅ **AUTENTICACIÓN:** Firebase JWT configurado
✅ **DEPENDENCIAS:** Expert Bot API configurado
✅ **MANEJO DE ERRORES:** Completo y robusto
✅ **LOGGING:** Implementado para debugging

---

## 📋 CHECKLIST DE VERIFICACIÓN

- [x] Endpoint disponible en producción
- [x] Prefijo `/api/v1/energy` correcto
- [x] Autenticación Firebase JWT
- [x] Comunicación con Expert Bot API
- [x] Manejo completo de errores
- [x] Logging detallado
- [x] Frontend correctamente configurado
- [x] Variables de entorno configuradas
- [x] Timeout adecuado (30s frontend, 15s backend)
- [x] Headers correctos
