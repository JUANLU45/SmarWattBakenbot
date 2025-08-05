# 🧠 DOCUMENTACIÓN TÉCNICA: ENDPOINT ANÁLISIS SENTIMENT EMPRESARIAL

## ENDPOINT: `/api/v1/analysis/sentiment`

**MICROSERVICIO:** expert_bot_api_COPY  
**ARCHIVO:** `app/analysis_routes.py`  
**FECHA CREACIÓN:** 2025-01-03  
**ESTADO:** ✅ IMPLEMENTADO Y VERIFICADO  
**PROPÓSITO:** El mejor chatbot energético del mundo requiere análisis de sentiment empresarial para personalizar respuestas según el estado emocional del usuario.

---

## 📋 ESPECIFICACIONES TÉCNICAS

### MÉTODO HTTP

- **Tipo:** POST
- **Ruta:** `/api/v1/analysis/sentiment`
- **Autenticación:** `@token_required` (Firebase JWT)
- **CORS:** Habilitado con OPTIONS

### FUNCIÓN PRINCIPAL

```python
@analysis_bp.route('/sentiment', methods=['POST', 'OPTIONS'])
@token_required
def analyze_sentiment():
```

### VALIDACIONES DE ENTRADA

#### DATOS REQUERIDOS (JSON)

```json
{
  "message_text": "string OBLIGATORIO",
  "user_id": "string OPCIONAL",
  "conversation_id": "string OPCIONAL"
}
```

#### REGLAS DE VALIDACIÓN

- `message_text`: OBLIGATORIO, no vacío, máximo 5000 caracteres
- Formato JSON válido requerido
- Content-Type: application/json

### PROCESAMIENTO INTERNO

#### SERVICIO UTILIZADO

- **Clase:** `AILearningService`
- **Método:** `analyze_sentiment_enterprise(message_text)`
- **Ubicación:** `app/services/ai_learning_service.py`

#### ALGORITMO

- Análisis lexical específico del sector energético
- Detección de patrones emocionales
- Cálculo de métricas de engagement
- Identificación de factores de riesgo

---

## 📊 DATOS DE SALIDA

### ESTRUCTURA COMPLETA DE RESPUESTA

```json
{
  "status": "success",
  "sentiment_analysis": {
    "sentiment_score": -1.0,
    "sentiment_label": "very_negative",
    "confidence": 0.95,
    "emotional_indicators": {
      "frustration_level": 8,
      "satisfaction_level": 1,
      "urgency_level": 9,
      "technical_engagement": 3,
      "question_intensity": 7,
      "excitement_level": 0,
      "caps_usage": 15,
      "message_length": 150,
      "word_count": 25,
      "complexity_score": 0.7,
      "energy_domain_relevance": 8
    },
    "personalization_hints": [
      "use_empathetic_tone",
      "provide_step_by_step_guidance",
      "offer_immediate_support",
      "prioritize_problem_solving"
    ],
    "risk_factors": [
      "high_frustration_risk",
      "confusion_abandonment_risk",
      "escalation_risk"
    ],
    "engagement_level": "very_high"
  },
  "request_info": {
    "user_id": "user_12345",
    "conversation_id": "conv_67890",
    "message_length": 150,
    "processed_at": "2025-01-03T10:30:00.000Z"
  },
  "enterprise_metrics": {
    "processing_successful": true,
    "analysis_type": "advanced_enterprise",
    "ai_service_version": "2.0.0"
  }
}
```

### CÓDIGOS DE SENTIMENT

- `"very_negative"`: -1.0 a -0.6
- `"negative"`: -0.6 a -0.2
- `"neutral"`: -0.2 a 0.2
- `"positive"`: 0.2 a 0.6
- `"very_positive"`: 0.6 a 1.0

### NIVELES DE ENGAGEMENT

- `"very_low"`: Usuario desconectado
- `"low"`: Participación mínima
- `"medium"`: Engagement estándar
- `"high"`: Usuario comprometido
- `"very_high"`: Máximo nivel de interacción

---

## 🗄️ LOGGING AUTOMÁTICO BIGQUERY

### TABLA: `ai_sentiment_analysis`

#### CAMPOS ALMACENADOS

```sql
CREATE TABLE ai_sentiment_analysis (
    interaction_id STRING,
    conversation_id STRING,
    user_id STRING,
    message_text STRING,
    sentiment_score FLOAT64,
    sentiment_label STRING,
    confidence FLOAT64,
    emotional_indicators JSON,
    analyzed_at TIMESTAMP
);
```

#### DATOS ESCRITOS AUTOMÁTICAMENTE

- **interaction_id:** UUID único generado
- **conversation_id:** ID de conversación (si se proporciona)
- **user_id:** UID del usuario (si se proporciona)
- **message_text:** Texto original del mensaje
- **sentiment_score:** Puntuación numérica (-1.0 a 1.0)
- **sentiment_label:** Etiqueta categórica
- **confidence:** Nivel de confianza (0.0 a 1.0)
- **emotional_indicators:** JSON completo con métricas
- **analyzed_at:** Timestamp UTC del análisis

---

## 🔌 COMUNICACIÓN ENTRE MICROSERVICIOS

### CONSUMIDOR: energy_ia_api_COPY

#### ARCHIVO CONSUMIDOR

`energy_ia_api_COPY/app/services/generative_chat_service.py`

#### FUNCIÓN CONSUMIDORA

```python
def _analyze_message_sentiment(self, message_text: str, user_id: str = None) -> Dict:
    """
    Línea aproximada: 350
    """
```

#### CONFIGURACIÓN HTTP

- **URL:** `{EXPERT_BOT_API_BASE_URL}/api/v1/analysis/sentiment`
- **TIMEOUT:** 10 segundos
- **MÉTODO:** POST
- **HEADERS:** Authorization Bearer + Content-Type JSON

#### MANEJO DE ERRORES

```python
try:
    response = requests.post(url, json=payload, headers=headers, timeout=10)
    return response.json()
except requests.exceptions.RequestException:
    # Fallback a análisis básico local
    return self._basic_sentiment_analysis(message_text)
```

---

## ⚠️ MANEJO DE ERRORES

### ERRORES HTTP DEVUELTOS

#### 400 - Bad Request

```json
{
  "error": "message_text is required",
  "status": "error",
  "error_code": "MISSING_MESSAGE_TEXT"
}
```

#### 413 - Request Entity Too Large

```json
{
  "error": "Message text too long. Maximum 5000 characters allowed",
  "status": "error",
  "error_code": "MESSAGE_TOO_LONG"
}
```

#### 401 - Unauthorized

```json
{
  "error": "Authentication required",
  "status": "error",
  "error_code": "UNAUTHORIZED"
}
```

#### 500 - Internal Server Error

```json
{
  "error": "Analysis service temporarily unavailable",
  "status": "error",
  "error_code": "ANALYSIS_SERVICE_ERROR"
}
```

---

## 🧪 EJEMPLOS DE USO

### CASO 1: Usuario Frustrado

**ENTRADA:**

```json
{
  "message_text": "¡¡¡ESTOY HARTO DE ESTAS FACTURAS TAN ALTAS!!! ¿POR QUÉ NO FUNCIONA NADA?",
  "user_id": "user_angry_123",
  "conversation_id": "conv_escalation_456"
}
```

**SALIDA:**

```json
{
  "sentiment_analysis": {
    "sentiment_score": -0.9,
    "sentiment_label": "very_negative",
    "confidence": 0.98,
    "emotional_indicators": {
      "frustration_level": 10,
      "caps_usage": 70,
      "urgency_level": 9
    },
    "personalization_hints": ["immediate_escalation", "empathetic_response"],
    "risk_factors": ["abandonment_risk", "escalation_risk"]
  }
}
```

### CASO 2: Usuario Satisfecho

**ENTRADA:**

```json
{
  "message_text": "Gracias por la recomendación de tarifa, he ahorrado mucho dinero",
  "user_id": "user_happy_789"
}
```

**SALIDA:**

```json
{
  "sentiment_analysis": {
    "sentiment_score": 0.8,
    "sentiment_label": "very_positive",
    "confidence": 0.92,
    "emotional_indicators": {
      "satisfaction_level": 9,
      "energy_domain_relevance": 8
    },
    "personalization_hints": [
      "maintain_positive_tone",
      "offer_additional_tips"
    ],
    "engagement_level": "high"
  }
}
```

---

## 🔧 CONFIGURACIÓN Y DESPLIEGUE

### VARIABLES DE ENTORNO REQUERIDAS

- `EXPERT_BOT_API_BASE_URL`: URL base del microservicio
- `FIREBASE_PROJECT_ID`: ID del proyecto Firebase
- `GOOGLE_CLOUD_PROJECT`: Proyecto de BigQuery

### DEPENDENCIAS

- `flask`
- `smarwatt_auth`
- `AILearningService`
- `AppError` (utils.error_handlers)

### COMPILACIÓN VERIFICADA

```bash
python -c "from app.analysis_routes import *"
```

✅ RESULTADO: Sin errores de importación

---

## 📈 MÉTRICAS Y MONITOREO

### MÉTRICAS AUTOMÁTICAS BIGQUERY

- Total de análisis realizados por día
- Distribución de sentiment scores
- Tiempo promedio de procesamiento
- Tasa de éxito/fallo por usuario

### LOGS EMPRESARIALES

- Cada solicitud genera entrada en BigQuery
- Logs estructurados para análisis posterior
- Trazabilidad completa por conversation_id

---

## 🎯 CASOS DE USO EMPRESARIALES

### 1. PERSONALIZACIÓN DE RESPUESTAS

El chatbot adapta su tono según el sentiment detectado:

- **Negativo:** Tono empático, soluciones inmediatas
- **Positivo:** Mantenimiento del mood, ofertas adicionales
- **Neutral:** Información directa y clara

### 2. ESCALAMIENTO AUTOMÁTICO

Sentiment muy negativo + alta frustración = Escalamiento a humano

### 3. ANÁLISIS DE SATISFACCIÓN

Métricas agregadas para medir satisfacción del usuario por conversación

### 4. MEJORA CONTINUA

Análisis de patrones para optimizar respuestas del chatbot

---

**ENDPOINT VERIFICADO Y DOCUMENTADO COMPLETAMENTE** ✅  
**FECHA:** 2025-01-03  
**VERSIÓN:** 1.0.0  
**ESTADO:** PRODUCCIÓN READY
