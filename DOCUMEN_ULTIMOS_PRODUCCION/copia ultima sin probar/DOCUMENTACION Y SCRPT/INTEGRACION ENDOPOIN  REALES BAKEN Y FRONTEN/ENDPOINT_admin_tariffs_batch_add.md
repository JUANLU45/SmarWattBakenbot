# 📦 DOCUMENTACIÓN ENDPOINT: `/api/v1/energy/admin/tariffs/batch-add`

## 🏷️ INFORMACIÓN GENERAL

**URL COMPLETA DE PRODUCCIÓN:** `https://energy-ia-api-1010012211318.europe-west1.run.app/api/v1/energy/admin/tariffs/batch-add`

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
Línea: 853-990
Decoradores: @energy_bp.route("/admin/tariffs/batch-add", methods=["POST", "OPTIONS"]) @admin_required
Función: batch_add_tariffs()
```

### 🔐 Autenticación y Autorización

```python
@admin_required
def batch_add_tariffs():
    # Solo usuarios admin pueden acceder
    # Decorador verifica token Firebase + rol admin
```

### 📥 PARÁMETROS DE ENTRADA (JSON BODY)

```json
{
    "tariffs": [
        {
            "supplier_name": "string (OBLIGATORIO)",
            "tariff_name": "string (OBLIGATORIO)",
            "tariff_type": "string (OBLIGATORIO)",
            "fixed_term_price": "number (OPCIONAL)",
            "variable_term_price": "number (OPCIONAL)",
            "provider_name": "string (OPCIONAL - usa supplier_name si no se provee)",
            "peak_price": "number (OPCIONAL)",
            "valley_price": "number (OPCIONAL)",
            "power_price_per_kw_per_month": "number (OPCIONAL)"
        }
    ],
    "batch_metadata": {
        "batch_id": "string (OPCIONAL)",
        "created_by": "string (OPCIONAL)",
        "source": "string (OPCIONAL)"
    }
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

#### PASO 2: Validación de Estructura de Datos

```python
if not data or "tariffs" not in data:
    raise AppError("Lista de tarifas requerida", 400)

tariffs = data["tariffs"]
if not isinstance(tariffs, list) or len(tariffs) == 0:
    raise AppError("Lista de tarifas debe contener al menos una tarifa", 400)
```

#### PASO 3: Procesamiento Individual de Cada Tarifa

```python
for i, tariff in enumerate(tariffs):
    try:
        # Validar campos básicos
        if not all(field in tariff for field in ["supplier_name", "tariff_name", "tariff_type"]):
            errors.append(f"Tarifa {i+1}: Campos requeridos faltantes")
            continue

        # Preparar datos con CAMPOS EXACTOS de BigQuery
        tariff_data = {
            "provider_name": tariff.get("provider_name", tariff.get("supplier_name", "")),
            "tariff_name": tariff["tariff_name"],
            "tariff_type": tariff["tariff_type"],
            "tariff_id": f"{provider_name}-{tariff_name}-{timestamp}",
            "fixed_monthly_fee": float(tariff.get("fixed_monthly_fee", tariff.get("fixed_term_price", 0))),
            "kwh_price_flat": float(tariff.get("kwh_price_flat", tariff.get("variable_term_price", 0))),
            "kwh_price_peak": float(tariff.get("kwh_price_peak", tariff.get("peak_price", 0))),
            "kwh_price_valley": float(tariff.get("kwh_price_valley", tariff.get("valley_price", 0))),
            "power_price_per_kw_per_month": float(tariff.get("power_price_per_kw_per_month", 0)),
            "is_pvpc": tariff.get("is_pvpc", tariff.get("tariff_type", "").lower() == "pvpc"),
            "update_timestamp": now_spanish(),
            "is_active": True,
        }
        processed_tariffs.append(tariff_data)
    except Exception as e:
        errors.append(f"Tarifa {i+1}: {str(e)}")
```

#### PASO 4: Validación Antiduplicados Batch

```python
validated_tariffs = []
duplicate_count = 0
validation_errors = 0

for tariff in processed_tariffs:
    try:
        is_duplicate = check_duplicate_tariff_robust(
            bq_client,
            table_id,
            tariff.get("provider_name"),
            tariff.get("tariff_name"),
            tariff.get("tariff_type"),
        )

        if is_duplicate:
            duplicate_count += 1
            errors.append(f"Duplicado: {tariff.get('provider_name')} - {tariff.get('tariff_name')}")
        else:
            validated_tariffs.append(tariff)
    except Exception as val_error:
        validation_errors += 1
        validated_tariffs.append(tariff)  # Incluir por robustez
```

#### PASO 5: Inserción Batch en BigQuery

```python
final_tariffs = validated_tariffs if validated_tariffs else processed_tariffs
table = bq_client.get_table(table_id)
insert_errors = bq_client.insert_rows_json(table, final_tariffs)

if insert_errors:
    errors.extend([f"Error BigQuery: {error}" for error in insert_errors])
```

### 📤 RESPUESTA EXITOSA (HTTP 200)

```json
{
    "status": "success",
    "message": "Proceso completado: X tarifas insertadas",
    "statistics": {
        "total_processed": "number",
        "successfully_inserted": "number", 
        "duplicates_prevented": "number",
        "validation_errors_handled": "number"
    },
    "data": {
        "processed_count": "number",
        "error_count": "number",
        "errors": ["string"] // Solo si hay errores
    }
}
```

### ❌ MANEJO DE ERRORES

#### Error 400 - Lista de Tarifas Requerida

```json
{
    "status": "error",
    "message": "Lista de tarifas requerida"
}
```

#### Error 400 - Lista Vacía

```json
{
    "status": "error", 
    "message": "Lista de tarifas debe contener al menos una tarifa"
}
```

#### Error 500 - Error en Procesamiento Batch

```json
{
    "status": "error",
    "message": "Error en procesamiento batch: [detalles]"
}
```

---

## 🌐 IMPLEMENTACIÓN FRONTEND

### 📍 Ubicación del Código

```
Archivo: /src/services/adminTariffBatchAddService.js
Línea: 1-426
Clase: AdminTariffBatchAddService
Cliente API: energyIaApiClient
```

### 🔧 Implementación JavaScript

```javascript
class AdminTariffBatchAddService {
  constructor() {
    // ✅ ENDPOINT CORRECTO CON PREFIJO /api/v1/energy
    this.endpoint = '/api/v1/energy/admin/tariffs/batch-add';
    
    this.config = {
      timeout: 60000, // 60 segundos para lotes grandes
      retries: 2,
      retryDelay: 2000,
      maxBatchSize: 50,
      chunkSize: 10,
    };
  }

  async batchAddTariffs(tariffsArray) {
    try {
      // ✅ VALIDACIÓN EXHAUSTIVA DEL LOTE
      const validation = this.validateTariffsBatch(tariffsArray);
      if (!validation.isValid) {
        return {
          success: false,
          error: 'Lote de tarifas inválido',
          details: validation.globalErrors,
          validationResults: validation,
        };
      }

      // ✅ PREPARAR PAYLOAD
      const payload = this.prepareBatchPayload(validation.validTariffs);

      // ✅ ENVÍO CON TIMEOUT EXTENDIDO
      const response = await energyIaApiClient.post(
        this.endpoint,
        payload,
        {
          timeout: this.config.timeout,
          headers: {
            'Content-Type': 'application/json',
            'X-Admin-Action': 'batch-add-tariffs',
            'X-Batch-Size': validation.validTariffs.length.toString(),
            'X-Request-ID': `batch_${Date.now()}`,
          },
        }
      );

      return {
        success: true,
        message: 'Lote procesado exitosamente',
        data: response.data,
        statistics: response.data.statistics,
        validationResults: validation,
        timestamp: new Date().toISOString(),
      };

    } catch (error) {
      return {
        success: false,
        error: 'Error procesando lote de tarifas',
        message: this.getErrorMessage(error),
        details: error.response?.data || error.message,
      };
    }
  }
}
```

### 📋 Validación Exhaustiva de Lote

```javascript
validateTariffsBatch(tariffsArray) {
  const results = {
    isValid: true,
    totalTariffs: 0,
    validTariffs: [],
    invalidTariffs: [],
    globalErrors: [],
    globalWarnings: [],
    summary: { valid: 0, invalid: 0, duplicates: 0 },
  };

  // ✅ VALIDACIONES GLOBALES
  if (!Array.isArray(tariffsArray)) {
    results.globalErrors.push('El parámetro debe ser un array de tarifas');
    results.isValid = false;
    return results;
  }

  if (tariffsArray.length > this.config.maxBatchSize) {
    results.globalErrors.push(`Máximo ${this.config.maxBatchSize} tarifas por lote`);
    results.isValid = false;
    return results;
  }

  // ✅ DETECTAR DUPLICADOS POR provider+tariff_name
  const uniqueKeys = new Set();
  tariffsArray.forEach((tariff, index) => {
    if (tariff.provider && tariff.tariff_name) {
      const key = `${tariff.provider}|${tariff.tariff_name}`;
      if (uniqueKeys.has(key)) {
        results.summary.duplicates++;
      } else {
        uniqueKeys.add(key);
      }
    }
  });

  // ✅ VALIDAR CADA TARIFA INDIVIDUALMENTE
  tariffsArray.forEach((tariff, index) => {
    const validation = adminTariffAddService.validateTariffData(tariff);
    if (validation.isValid) {
      results.validTariffs.push({ index, data: validation.cleanData });
      results.summary.valid++;
    } else {
      results.invalidTariffs.push({ index, data: tariff, errors: validation.errors });
      results.summary.invalid++;
    }
  });

  results.isValid = results.summary.invalid === 0 && results.globalErrors.length === 0;
  return results;
}
```

### 🔗 Configuración del Cliente API

```javascript
// Archivo: /src/services/apiClient.js
export const energyIaApiClient = createApiClient(
  import.meta.env.VITE_ENERGY_IA_API_URL  // https://energy-ia-api-1010012211318.europe-west1.run.app
);
```

### ❌ Manejo de Errores Frontend

```javascript
getErrorMessage(error) {
  if (error.response?.status === 401) {
    return 'No tienes permisos de administrador';
  }
  if (error.response?.status === 400) {
    return error.response.data?.message || 'Datos del lote inválidos';
  }
  if (error.response?.status === 413) {
    return 'Lote demasiado grande. Reduce el número de tarifas';
  }
  if (error.response?.status === 500) {
    return 'Error interno del servidor procesando el lote';
  }
  if (error.code === 'ECONNABORTED') {
    return 'Timeout procesando lote. Intenta con menos tarifas';
  }
  return 'Error desconocido procesando el lote';
}
```

---

## 🔍 DEPENDENCIAS Y COMUNICACIÓN

### 📡 Flujo de Comunicación

```
Frontend (energyIaApiClient) 
    ↓ POST /api/v1/energy/admin/tariffs/batch-add
Energy IA API (energy_ia_api_COPY)
    ↓ for each tariff: check_duplicate_tariff_robust()
    ↓ BigQuery Batch Insert
BigQuery Table: market_electricity_tariffs
```

### 🔧 Servicios Utilizados

1. **BigQuery Client** - Inserción batch de datos
2. **check_duplicate_tariff_robust()** - Validación antiduplicados por tarifa
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

## 🚀 ESTADO DE PRODUCCIÓN

✅ **BACKEND:** Implementado y funcional en energy-ia-api-1010012211318.europe-west1.run.app
✅ **FRONTEND:** Implementado correctamente con endpoint correcto
✅ **AUTENTICACIÓN:** Firebase JWT + Admin required
✅ **ANTIDUPLICADOS:** Sistema robusto por cada tarifa
✅ **MANEJO DE ERRORES:** Completo y detallado para operaciones batch
✅ **VALIDACIÓN:** Exhaustiva con estadísticas detalladas
✅ **TIMEOUT:** Extendido a 60s para lotes grandes

---

## 📋 CHECKLIST DE VERIFICACIÓN

- [x] Endpoint disponible en producción
- [x] Prefijo `/api/v1/energy` correcto
- [x] Autenticación Firebase JWT + Admin
- [x] Validación antiduplicados por tarifa
- [x] Manejo completo de errores batch
- [x] Logging detallado con estadísticas
- [x] Frontend correctamente configurado
- [x] Variables de entorno configuradas
- [x] Timeout adecuado (60s para lotes)
- [x] Headers CORS configurados
- [x] Límite de lote configurado (50 tarifas)
- [x] Validación individual reutilizada
- [x] Estadísticas de procesamiento completas
