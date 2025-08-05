# 🔧 DOCUMENTACIÓN ENDPOINT: `/api/v1/energy/admin/tariffs/add`

## 🏷️ INFORMACIÓN GENERAL

**URL COMPLETA DE PRODUCCIÓN:** `https://energy-ia-api-1010012211318.europe-west1.run.app/api/v1/energy/admin/tariffs/add`

**MICROSERVICIO:** Energy IA API (energy_ia_api_COPY)

**MÉTODO HTTP:** POST

**AUTENTICACIÓN:** ✅ Requerida (Token Firebase JWT + Admin)

**PREFIJO:** `/api/v1/energy`

**PERMISOS:** ADMIN SOLAMENTE

---

## 🔧 IMPLEMENTACIÓN BACKEND

### 📍 Ubicación del Código
```
Archivo: /app/routes.py
Línea: 711-812
Decoradores: @energy_bp.route("/admin/tariffs/add", methods=["POST", "OPTIONS"]) @admin_required
Función: add_tariff_data()
```

### 🔐 Autenticación y Autorización
```python
@admin_required
def add_tariff_data():
    # Solo usuarios admin pueden acceder
    # Decorador verifica token Firebase + rol admin
```

### 📥 PARÁMETROS DE ENTRADA (JSON BODY)
```json
{
    "supplier_name": "string (OBLIGATORIO)",
    "tariff_name": "string (OBLIGATORIO)",
    "tariff_type": "string (OBLIGATORIO)",
    "fixed_term_price": "number (OBLIGATORIO)",
    "variable_term_price": "number (OBLIGATORIO)",
    "provider_name": "string (OPCIONAL - usa supplier_name si no se provee)",
    "tariff_id": "string (OPCIONAL - se genera automáticamente)",
    "peak_price": "number (OPCIONAL)",
    "valley_price": "number (OPCIONAL)",
    "power_price_per_kw_per_month": "number (OPCIONAL)"
}
```

### 🔄 FLUJO DE PROCESAMIENTO

#### PASO 1: Validación CORS
```python
if request.method == "OPTIONS":
    response = Response()
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response, 200
```

#### PASO 2: Validación de Campos Obligatorios
```python
required_fields = [
    "supplier_name",
    "tariff_name", 
    "tariff_type",
    "fixed_term_price",
    "variable_term_price",
]
for field in required_fields:
    if field not in data:
        raise AppError(f"Campo requerido faltante: {field}", 400)
```

#### PASO 3: Preparación de Datos para BigQuery
```python
tariff_data = {
    "provider_name": data.get("provider_name", data.get("supplier_name", "")),
    "tariff_name": data["tariff_name"],
    "tariff_type": data["tariff_type"],
    "tariff_id": data.get(
        "tariff_id",
        f"{data.get('provider_name', data.get('supplier_name', ''))}-{data['tariff_name']}-{int(now_spanish().timestamp())}",
    ),
    "fixed_monthly_fee": float(data.get("fixed_monthly_fee", data.get("fixed_term_price", 0))),
    "kwh_price_flat": float(data.get("kwh_price_flat", data.get("variable_term_price", 0))),
    "kwh_price_peak": float(data.get("kwh_price_peak", data.get("peak_price", 0))),
    "kwh_price_valley": float(data.get("kwh_price_valley", data.get("valley_price", 0))),
    "power_price_per_kw_per_month": float(data.get("power_price_per_kw_per_month", 0)),
    "is_pvpc": data.get("is_pvpc", data.get("tariff_type", "").lower() == "pvpc"),
    "is_active": data.get("is_active", True),
    "update_timestamp": now_spanish(),
    "created_by_admin": g.user.get("uid"),
    "data_source": "admin_panel",
}
```

#### PASO 4: Validación Antiduplicados Robusta
```python
is_duplicate = check_duplicate_tariff_robust(
    bq_client,
    table_id,
    data.get("provider_name", data.get("supplier_name")),
    data.get("tariff_name"),
    data.get("tariff_type"),
)

if is_duplicate:
    return jsonify({
        "status": "duplicate_prevented",
        "message": f"Tarifa ya existe: {provider_name} - {tariff_name}",
        "duplicate_data": {...}
    }), 409
```

#### PASO 5: Inserción en BigQuery
```python
table = bq_client.get_table(table_id)
errors = bq_client.insert_rows_json(table, [tariff_data])

if errors:
    raise AppError(f"Error insertando datos: {errors}", 500)
```

### 📤 RESPUESTA EXITOSA (HTTP 201)
```json
{
    "status": "success",
    "message": "Tarifa añadida exitosamente",
    "data": {
        "provider_name": "string",
        "tariff_name": "string",
        "inserted_at": "2025-07-31T..."
    }
}
```

### ❌ MANEJO DE ERRORES

#### Error 400 - Datos Requeridos Faltantes
```json
{
    "status": "error",
    "message": "Campo requerido faltante: supplier_name"
}
```

#### Error 409 - Duplicado Detectado
```json
{
    "status": "duplicate_prevented",
    "message": "Tarifa ya existe: Iberdrola - Tarifa 2.0TD",
    "duplicate_data": {
        "provider_name": "Iberdrola",
        "tariff_name": "Tarifa 2.0TD",
        "tariff_type": "residential"
    }
}
```

#### Error 500 - Error BigQuery
```json
{
    "status": "error",
    "message": "Error insertando datos: [BigQuery error details]"
}
```

---

## 🌐 IMPLEMENTACIÓN FRONTEND

### 📍 Ubicación del Código
```
Archivo: /src/services/adminTariffAddService.js
Línea: 1-314
Clase: AdminTariffAddService
Cliente API: energyIaApiClient
```

### ❌ PROBLEMA DETECTADO: URL INCORRECTA EN FRONTEND
```javascript
// ❌ FRONTEND INCORRECTO (Línea 13):
this.endpoint = '/api/v1/admin/tariffs/add';

// ✅ DEBERÍA SER:
this.endpoint = '/api/v1/energy/admin/tariffs/add';
```

### 🔧 Implementación JavaScript (CORREGIDA)
```javascript
class AdminTariffAddService {
  constructor() {
    // ✅ ENDPOINT CORRECTO CON PREFIJO /api/v1/energy
    this.endpoint = '/api/v1/energy/admin/tariffs/add';
    
    this.config = {
      timeout: 30000,
      retries: 3,
      retryDelay: 1000,
    };
  }

  async addTariff(tariffData) {
    try {
      // ✅ VALIDACIÓN EXHAUSTIVA
      const validation = this.validateTariffData(tariffData);
      if (!validation.isValid) {
        return {
          success: false,
          error: 'Datos de tarifa inválidos',
          details: validation.errors,
          warnings: validation.warnings,
        };
      }

      // ✅ ENVÍO CON REINTENTOS
      const response = await energyIaApiClient.post(
        this.endpoint, // ✅ AHORA CORRECTO: /api/v1/energy/admin/tariffs/add
        validation.cleanData,
        {
          timeout: this.config.timeout,
          headers: {
            'Content-Type': 'application/json',
            'X-Admin-Action': 'add-tariff',
            'X-Request-ID': `tariff_add_${Date.now()}`,
          },
        },
      );

      return {
        success: true,
        message: 'Tarifa añadida exitosamente',
        data: response.data,
        tariff_id: response.data.tariff_id || response.data.id,
        timestamp: new Date().toISOString(),
      };

    } catch (error) {
      return {
        success: false,
        error: 'Error añadiendo tarifa',
        message: this.getErrorMessage(error),
        details: error.response?.data || error.message,
      };
    }
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

### 📋 Validación de Campos Frontend
```javascript
validateTariffData(tariffData) {
  const requiredFields = {
    provider: 'string',        // → supplier_name en backend
    tariff_name: 'string',     // → tariff_name
    price_kwh: 'number',       // → variable_term_price
    fixed_cost: 'number',      // → fixed_term_price
    tariff_type: 'string',     // → tariff_type
  };

  // ✅ MAPEO CORRECTO FRONTEND → BACKEND
  const sanitized = {
    supplier_name: tariffData.provider?.toString().trim(),
    tariff_name: tariffData.tariff_name?.toString().trim(),
    variable_term_price: parseFloat(tariffData.price_kwh),
    fixed_term_price: parseFloat(tariffData.fixed_cost),
    tariff_type: tariffData.tariff_type?.toString().trim(),
  };
}
```

### ❌ Manejo de Errores Frontend
```javascript
getErrorMessage(error) {
  if (error.response?.status === 401) {
    return 'No tienes permisos de administrador';
  }
  if (error.response?.status === 400) {
    return error.response.data?.message || 'Datos de tarifa inválidos';
  }
  if (error.response?.status === 409) {
    return 'Ya existe una tarifa con ese nombre o datos similares';
  }
  if (error.response?.status === 500) {
    return 'Error interno del servidor. Contacta con soporte técnico';
  }
  return 'Error desconocido. Inténtalo de nuevo más tarde';
}
```

---

## 🔍 DEPENDENCIAS Y COMUNICACIÓN

### 📡 Flujo de Comunicación
```
Frontend (energyIaApiClient) 
    ↓ POST /api/v1/energy/admin/tariffs/add
Energy IA API (energy_ia_api_COPY)
    ↓ check_duplicate_tariff_robust()
    ↓ BigQuery Insert
BigQuery Table: market_electricity_tariffs
```

### 🔧 Servicios Utilizados
1. **BigQuery Client** - Inserción de datos
2. **check_duplicate_tariff_robust()** - Validación antiduplicados
3. **admin_required decorator** - Autorización
4. **Firebase JWT** - Autenticación

---

## ⚙️ CONFIGURACIÓN DE PRODUCCIÓN

### 🌍 Variables de Entorno Backend
```bash
GCP_PROJECT_ID=smatwatt
BQ_DATASET_ID=smartwatt_data
BQ_MARKET_TARIFFS_TABLE_ID=market_electricity_tariffs
```

### 🌍 Variables de Entorno Frontend
```bash
VITE_ENERGY_IA_API_URL=https://energy-ia-api-1010012211318.europe-west1.run.app
```

---

## 🚨 PROBLEMAS DETECTADOS Y SOLUCIONES

### ❌ PROBLEMA 1: URL INCORRECTA EN FRONTEND
**Ubicación:** `/src/services/adminTariffAddService.js` línea 13
**Error:** `this.endpoint = '/api/v1/admin/tariffs/add';`
**Corrección:** `this.endpoint = '/api/v1/energy/admin/tariffs/add';`

### ❌ PROBLEMA 2: MAPEO DE CAMPOS INCONSISTENTE
**Frontend envía:** `provider, price_kwh, fixed_cost`
**Backend espera:** `supplier_name, variable_term_price, fixed_term_price`
**Solución:** Mapear correctamente en sanitizeTariffData()

---

## 🚀 ESTADO DE PRODUCCIÓN

✅ **BACKEND:** Implementado y funcional en energy-ia-api-1010012211318.europe-west1.run.app
❌ **FRONTEND:** URL incorrecta - REQUIERE CORRECCIÓN
✅ **AUTENTICACIÓN:** Firebase JWT + Admin required
✅ **ANTIDUPLICADOS:** Sistema robusto implementado
✅ **MANEJO DE ERRORES:** Completo y robusto
✅ **VALIDACIÓN:** Exhaustiva en ambos lados

---

## 📋 CHECKLIST DE VERIFICACIÓN

- [x] Endpoint disponible en producción
- [x] Prefijo `/api/v1/energy` correcto en backend  
- [ ] **PENDIENTE:** Corregir URL en frontend
- [x] Autenticación Firebase JWT + Admin
- [x] Validación antiduplicados
- [x] Manejo completo de errores
- [x] Logging detallado
- [ ] **PENDIENTE:** Mapeo de campos consistente
- [x] Variables de entorno configuradas
- [x] Timeout adecuado (30s frontend)
- [x] Headers CORS configurados
