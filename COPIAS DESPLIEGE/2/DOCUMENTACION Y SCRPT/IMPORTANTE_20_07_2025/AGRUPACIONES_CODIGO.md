# AGRUPACIONES DE CÓDIGO - ANÁLISIS EXACTO
## Solo Código Fuente, Zero BigQuery, Zero Inventos

### 🎯 OBJETIVO:
Documentar exactamente qué datos necesita cada endpoint y cada IA según el CÓDIGO REAL.


## 📁 MICROSERVICIO: ENERGY_IA_API_COPY

### 🔗 ENDPOINTS Y SUS NECESIDADES DE DATOS:


#### 📍 `/tariffs/recommendations` - `get_tariff_recommendations_route()`

**Archivo:** `routes.py`

**Datos que NECESITA del código:**
- **Campos accedidos:** `last_invoice_data`, `data`, `uid`
- **Variables config:** 
- **HTTP calls:** 
- **Métodos llamados:** `json`, `info`


#### 📍 `/tariffs/market-data` - `get_market_data()`

**Archivo:** `routes.py`

**Datos que NECESITA del código:**
- **Campos accedidos:** `green_energy_percentage`, `last_updated`, `discriminated_hourly`, `promotion_discount_percentage`
- **Variables config:** 
- **HTTP calls:** 
- **Métodos llamados:** `get_market_tariffs`


#### 📍 `/admin/tariffs/add` - `add_tariff_data()`

**Archivo:** `routes.py`

**Datos que NECESITA del código:**
- **Campos accedidos:** `valley_price`, `peak_hours`, `peak_price`
- **Variables config:** 
- **HTTP calls:** 
- **Métodos llamados:** `get_json`


#### 📍 `/admin/tariffs/batch-add` - `batch_add_tariffs()`

**Archivo:** `routes.py`

**Datos que NECESITA del código:**
- **Campos accedidos:** 
- **Variables config:** 
- **HTTP calls:** 
- **Métodos llamados:** `get_json`, `append`


#### 📍 `/tariffs/compare` - `compare_tariffs()`

**Archivo:** `routes.py`

**Datos que NECESITA del código:**
- **Campos accedidos:** `uid`
- **Variables config:** 
- **HTTP calls:** 
- **Métodos llamados:** `get_json`, `append`, `get_market_tariffs`


### 🤖 MÉTODOS IA Y SUS NECESIDADES DE DATOS:


#### 🧠 `_initialize_vertex_ai_client()`

**Archivo:** `vertex_ai_service.py`

**Datos que NECESITA del código:**
- **Campos accedidos:** `VERTEX_AI_LOCATION`, `GCP_PROJECT_ID`
- **Consultas tablas:** 
- **Variables config:** 


#### 🧠 `get_enterprise_tariff_recommendation()`

**Archivo:** `vertex_ai_service.py`

**Datos que NECESITA del código:**
- **Campos accedidos:** `user_id`
- **Consultas tablas:** 
- **Variables config:** 


#### 🧠 `_analyze_market_statistics()`

**Archivo:** `vertex_ai_service.py`

**Datos que NECESITA del código:**
- **Campos accedidos:** `fixed_monthly_fee`, `kwh_price_peak`, `kwh_price_valley`
- **Consultas tablas:** 
- **Variables config:** 


#### 🧠 `_analyze_user_position_in_market()`

**Archivo:** `vertex_ai_service.py`

**Datos que NECESITA del código:**
- **Campos accedidos:** `avg_kwh`, `peak_percent`
- **Consultas tablas:** 
- **Variables config:** 


#### 🧠 `_get_market_based_recommendations()`

**Archivo:** `vertex_ai_service.py`

**Datos que NECESITA del código:**
- **Campos accedidos:** 
- **Consultas tablas:** 
- **Variables config:** 


#### 🧠 `_get_recommendation_reason()`

**Archivo:** `vertex_ai_service.py`

**Datos que NECESITA del código:**
- **Campos accedidos:** `avg_kwh`, `peak_percent`
- **Consultas tablas:** 
- **Variables config:** 


## 📁 MICROSERVICIO: EXPERT_BOT_API_COPY

### 🔗 ENDPOINTS Y SUS NECESIDADES DE DATOS:


#### 📍 `/session/start` - `start_chat_session()`

**Archivo:** `routes.py`

**Datos que NECESITA del código:**
- **Campos accedidos:** `uid`
- **Variables config:** `ENERGY_IA_API_URL`
- **HTTP calls:** 
- **Métodos llamados:** `start_session`, `error`, `route`, `info`


#### 📍 `/message` - `post_message()`

**Archivo:** `routes.py`

**Datos que NECESITA del código:**
- **Campos accedidos:** `uid`, `conversation_id`, `message`
- **Variables config:** 
- **HTTP calls:** 
- **Métodos llamados:** `get_json`, `warning`


#### 📍 `/conversation/history` - `get_conversation_history()`

**Archivo:** `routes.py`

**Datos que NECESITA del código:**
- **Campos accedidos:** `limit`, `page`, `uid`
- **Variables config:** `ENERGY_IA_API_URL`
- **HTTP calls:** 
- **Métodos llamados:** `get_conversation_history`, `info`


#### 📍 `/conversation/<conversation_id>` - `delete_conversation()`

**Archivo:** `routes.py`

**Datos que NECESITA del código:**
- **Campos accedidos:** `uid`
- **Variables config:** `ENERGY_IA_API_URL`
- **HTTP calls:** 
- **Métodos llamados:** `isoformat`, `delete_conversation`, `info`


#### 📍 `/conversation/feedback` - `submit_conversation_feedback()`

**Archivo:** `routes.py`

**Datos que NECESITA del código:**
- **Campos accedidos:** `comment`, `uid`
- **Variables config:** 
- **HTTP calls:** 
- **Métodos llamados:** `get_json`, `join`, `warning`


#### 📍 `/metrics` - `get_user_metrics()`

**Archivo:** `routes.py`

**Datos que NECESITA del código:**
- **Campos accedidos:** `uid`
- **Variables config:** `ENERGY_IA_API_URL`
- **HTTP calls:** 
- **Métodos llamados:** `isoformat`, `error`, `info`, `get_user_analytics`


#### 📍 `/consumption` - `upload_consumption_data()`

**Archivo:** `energy_routes.py`

**Datos que NECESITA del código:**
- **Campos accedidos:** 
- **Variables config:** 
- **HTTP calls:** 
- **Métodos llamados:** 


#### 📍 `/dashboard` - `get_dashboard_data()`

**Archivo:** `energy_routes.py`

**Datos que NECESITA del código:**
- **Campos accedidos:** `email`, `name`
- **Variables config:** 
- **HTTP calls:** 
- **Métodos llamados:** `error`, `get_dashboard_data`, `info`


#### 📍 `/users/profile` - `get_user_profile()`

**Archivo:** `energy_routes.py`

**Datos que NECESITA del código:**
- **Campos accedidos:** 
- **Variables config:** 
- **HTTP calls:** 
- **Métodos llamados:** `_get_user_energy_profile`, `error`, `route`, `info`


#### 📍 `/manual-data` - `add_manual_energy_data()`

**Archivo:** `energy_routes.py`

**Datos que NECESITA del código:**
- **Campos accedidos:** 
- **Variables config:** 
- **HTTP calls:** 
- **Métodos llamados:** `join`, `items`, `append`, `get_json`


#### 📍 `/consumption/update` - `update_consumption_data()`

**Archivo:** `energy_routes.py`

**Datos que NECESITA del código:**
- **Campos accedidos:** 
- **Variables config:** 
- **HTTP calls:** 
- **Métodos llamados:** `isoformat`, `update_consumption_data`, `info`, `process_consumption_update_patterns`, `get_json`


#### 📍 `/consumption/history` - `get_consumption_history()`

**Archivo:** `energy_routes.py`

**Datos que NECESITA del código:**
- **Campos accedidos:** `limit`, `months`, `page`
- **Variables config:** 
- **HTTP calls:** 
- **Métodos llamados:** `get_consumption_history`, `info`


#### 📍 `/consumption/analyze` - `analyze_consumption()`

**Archivo:** `energy_routes.py`

**Datos que NECESITA del código:**
- **Campos accedidos:** 
- **Variables config:** 
- **HTTP calls:** 
- **Métodos llamados:** `isoformat`, `error`, `generate_consumption_insights`, `info`, `get_json`, `analyze_consumption_patterns`


#### 📍 `/consumption/recommendations` - `get_consumption_recommendations()`

**Archivo:** `energy_routes.py`

**Datos que NECESITA del código:**
- **Campos accedidos:** 
- **Variables config:** 
- **HTTP calls:** 
- **Métodos llamados:** `get_personalized_recommendations`, `isoformat`, `error`, `generate_smart_recommendations`, `info`


#### 📍 `/consumption/compare` - `compare_tariffs()`

**Archivo:** `energy_routes.py`

**Datos que NECESITA del código:**
- **Campos accedidos:** 
- **Variables config:** 
- **HTTP calls:** 
- **Métodos llamados:** `isoformat`, `compare_electricity_tariffs`, `error`, `info`, `get_json`, `enhance_tariff_comparison`


#### 📍 `/consumption/title` - `update_consumption_title()`

**Archivo:** `energy_routes.py`

**Datos que NECESITA del código:**
- **Campos accedidos:** `new_title`, `consumption_id`
- **Variables config:** 
- **HTTP calls:** 
- **Métodos llamados:** `isoformat`, `update_consumption_title`, `info`, `get_json`


### 🤖 MÉTODOS IA Y SUS NECESIDADES DE DATOS:


#### 🧠 `_ensure_enterprise_ai_tables_exist()`

**Archivo:** `ai_learning_service.py`

**Datos que NECESITA del código:**
- **Campos accedidos:** 
- **Consultas tablas:** 
- **Variables config:** 


#### 🧠 `_log_to_bigquery_ai_with_auto_schema()`

**Archivo:** `ai_learning_service.py`

**Datos que NECESITA del código:**
- **Campos accedidos:** 
- **Consultas tablas:** 
- **Variables config:** 


#### 🧠 `analyze_sentiment_enterprise()`

**Archivo:** `ai_learning_service.py`

**Datos que NECESITA del código:**
- **Campos accedidos:** 
- **Consultas tablas:** 
- **Variables config:** 


#### 🧠 `_analyze_context_multipliers()`

**Archivo:** `ai_learning_service.py`

**Datos que NECESITA del código:**
- **Campos accedidos:** 
- **Consultas tablas:** 
- **Variables config:** 


#### 🧠 `_analyze_risk_factors()`

**Archivo:** `ai_learning_service.py`

**Datos que NECESITA del código:**
- **Campos accedidos:** `urgency_level`, `frustration_level`, `caps_usage`, `question_intensity`
- **Consultas tablas:** 
- **Variables config:** 


## 🔄 ANÁLISIS DE FLUJO DE DATOS ENTRE SERVICIOS:

### 📊 CAMPOS MÁS UTILIZADOS POR SERVICIO:


#### ENERGY_IA_API_COPY:
**Endpoints por campo:**
- `last_invoice_data`: 1 endpoints
- `data`: 1 endpoints
- `uid`: 2 endpoints
- `green_energy_percentage`: 1 endpoints
- `last_updated`: 1 endpoints
- `discriminated_hourly`: 1 endpoints
- `promotion_discount_percentage`: 1 endpoints
- `valley_price`: 1 endpoints
- `peak_hours`: 1 endpoints
- `peak_price`: 1 endpoints

**Necesidades de IA:**
- `_initialize_vertex_ai_client`: 2 campos, 0 consultas
- `get_enterprise_tariff_recommendation`: 1 campos, 0 consultas
- `_analyze_market_statistics`: 3 campos, 0 consultas
- `_analyze_user_position_in_market`: 2 campos, 0 consultas
- `_get_market_based_recommendations`: 0 campos, 0 consultas
- `_get_recommendation_reason`: 2 campos, 0 consultas


#### EXPERT_BOT_API_COPY:
**Endpoints por campo:**
- `uid`: 6 endpoints
- `conversation_id`: 1 endpoints
- `message`: 1 endpoints
- `limit`: 2 endpoints
- `page`: 2 endpoints
- `comment`: 1 endpoints
- `email`: 1 endpoints
- `name`: 1 endpoints
- `months`: 1 endpoints
- `new_title`: 1 endpoints
- `consumption_id`: 1 endpoints

**Necesidades de IA:**
- `_ensure_enterprise_ai_tables_exist`: 0 campos, 0 consultas
- `_log_to_bigquery_ai_with_auto_schema`: 0 campos, 0 consultas
- `analyze_sentiment_enterprise`: 0 campos, 0 consultas
- `_analyze_context_multipliers`: 0 campos, 0 consultas
- `_analyze_risk_factors`: 4 campos, 0 consultas


### 🚨 CONCLUSIONES DE AGRUPACIONES:

1. **DATOS CRÍTICOS**: Los campos más accedidos son los que necesitan estar perfectamente unificados
2. **DEPENDENCIAS**: Los endpoints que más datos necesitan son los más críticos
3. **IA REQUIREMENTS**: Los métodos de IA tienen patrones específicos de acceso a datos

⚡ **SIGUIENTE PASO**: Agrupar los datos según estas necesidades reales del código.
