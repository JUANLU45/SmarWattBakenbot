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
