# 🏢 TABLAS BIGQUERY EMPRESARIALES ACTUALIZADAS

## TABLAS EXISTENTES EN BIGQUERY

```
ai_sentiment_analysis
ai_user_patterns
consumption_log
conversations_log
electricity_consumption_log
feedback_log
market_electricity_tariffs
ml_training_20250711_062334
model_feedback_log
recommendation_log
uploaded_documents_log
user_profiles_enriched
```

## 🆕 TABLAS NUEVAS IMPLEMENTADAS CON MIGRACIONES

```
ai_prompt_optimization      # Migración 001
ai_predictions             # Migración 002
ai_business_metrics        # Migración 003
async_tasks               # Migración 004
worker_metrics            # Migración 005
```

## 🚀 COMANDOS DE DEPLOY ACTUALIZADOS

### BOT_API (EXPERT-BOT-API)

```bash
gcloud run deploy expert-bot-api \
--source . \
--platform managed \
--region europe-west1 \
--allow-unauthenticated \
--service-account="firebase-adminsdk-fbsvc@smatwatt.iam.gserviceaccount.com" \
--memory="4Gi" \
--cpu="2" \
--max-instances="5" \
--timeout="900s" \
--set-secrets="/secrets/expert-bot-api-sa-key=expert-bot-api-sa-key:1,/credentials/firebase-adminsdk-key=firebase-adminsdk-key:1" \
--set-env-vars="FLASK_CONFIG=production,GCP_PROJECT_ID=smatwatt,GCP_LOCATION=eu,BQ_DATASET_ID=smartwatt_data,GCS_INVOICE_BUCKET=smatwatt-model-exports-smatwatt-final,BQ_UPLOADED_DOCS_TABLE_ID=uploaded_documents_log,BQ_CONSUMPTION_LOG_TABLE_ID=consumption_log,BQ_CONVERSATIONS_TABLE_ID=conversations_log,BQ_FEEDBACK_TABLE_ID=feedback_log,BQ_USER_PROFILES_TABLE_ID=user_profiles_enriched,PUBSUB_CONSUMPTION_TOPIC_ID=consumption-topic,GEMINI_API_KEY=AIzaSyCONKtpEAWHM5xtq-C3YTX8xsmFnHo0goE,ENERGY_IA_API_URL=https://energy-ia-api-1010012211318.europe-west1.run.app,OPENWEATHER_API_KEY=8f91cb80de36de44e701ff196ea256e8,CORS_ORIGINS=https://smarwatt.com,AI_LEARNING_ENABLED=true,BQ_AI_SENTIMENT_TABLE_ID=ai_sentiment_analysis,BQ_AI_PATTERNS_TABLE_ID=ai_user_patterns,BQ_AI_OPTIMIZATION_TABLE_ID=ai_prompt_optimization,BQ_AI_PREDICTIONS_TABLE_ID=ai_predictions,BQ_AI_BUSINESS_METRICS_TABLE_ID=ai_business_metrics,BQ_ASYNC_TASKS_TABLE_ID=async_tasks,BQ_WORKER_METRICS_TABLE_ID=worker_metrics,SECRET_KEY=MTvrA_NDjZ11l6wCEFcxVr6A7R1iI8AAeyQG6oRUv2I"
```

### ENERGIA-API (ENERGY-IA-API)

```bash
gcloud run deploy energy-ia-api \
--source . \
--platform managed \
--region europe-west1 \
--allow-unauthenticated \
--service-account="firebase-adminsdk-fbsvc@smatwatt.iam.gserviceaccount.com" \
--memory="4Gi" \
--cpu="2" \
--max-instances="5" \
--timeout="900s" \
--set-secrets="/secrets/expert-bot-api-sa-key=expert-bot-api-sa-key:1,/credentials/firebase-adminsdk-key=firebase-adminsdk-key:1" \
--set-env-vars="FLASK_CONFIG=production,GCP_PROJECT_ID=smatwatt,GCP_LOCATION=eu,EXPERT_BOT_API_URL=https://expert-bot-api-1010012211318.europe-west1.run.app,BQ_DATASET_ID=smartwatt_data,TARIFF_RECOMMENDER_ENDPOINT_ID=1334169399375953920,BQ_MARKET_TARIFFS_TABLE_ID=market_electricity_tariffs,BQ_RECOMMENDATION_LOG_TABLE_ID=recommendation_log,BQ_USER_PROFILES_TABLE_ID=user_profiles_enriched,BQ_CONSUMPTION_LOG_TABLE_ID=consumption_log,BQ_UPLOADED_DOCS_TABLE_ID=uploaded_documents_log,BQ_CONVERSATIONS_TABLE_ID=conversations_log,BQ_FEEDBACK_TABLE_ID=feedback_log,PUBSUB_CONSUMPTION_TOPIC_ID=consumption-topic,GCS_INVOICE_BUCKET=smatwatt-model-exports-smatwatt-final,GEMINI_API_KEY=AIzaSyCONKtpEAWHM5xtq-C3YTX8xsmFnHo0goE,OPENWEATHER_API_KEY=8f91cb80de36de44e701ff196ea256e8,CORS_ORIGINS=https://smarwatt.com,SECRET_KEY=MTvrA_NDjZ11l6wCEFcxVr6A7R1iI8AAeyQG6oRUv2I"
```

## 📋 INSTRUCCIONES DE IMPLEMENTACIÓN

### 1. Ejecutar migraciones ANTES del deploy

```bash
cd bq_migrations
python run_migrations.py
```

### 2. Verificar tablas creadas

```bash
bq ls smartwatt_data
```

### 3. Hacer deploy con las nuevas variables

```bash
# Usar los comandos actualizados arriba
```

## 🔧 CONFIGURACIÓN DE VARIABLES

### Variables nuevas añadidas

- `BQ_AI_OPTIMIZATION_TABLE_ID=ai_prompt_optimization`
- `BQ_AI_PREDICTIONS_TABLE_ID=ai_predictions`
- `BQ_AI_BUSINESS_METRICS_TABLE_ID=ai_business_metrics`
- `BQ_ASYNC_TASKS_TABLE_ID=async_tasks`
- `BQ_WORKER_METRICS_TABLE_ID=worker_metrics`

## ✅ VERIFICACIÓN POST-DEPLOY

### Verificar que todas las tablas existen

```sql
SELECT table_name, table_type, creation_time
FROM `smatwatt.smartwatt_data.INFORMATION_SCHEMA.TABLES`
WHERE table_name IN (
    'ai_prompt_optimization',
    'ai_predictions',
    'ai_business_metrics',
    'async_tasks',
    'worker_metrics'
)
ORDER BY table_name;
```

### Verificar esquemas de tablas

```sql
SELECT table_name, column_name, data_type, is_nullable
FROM `smatwatt.smartwatt_data.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name IN (
    'ai_prompt_optimization',
    'ai_predictions',
    'ai_business_metrics',
    'async_tasks',
    'worker_metrics'
)
ORDER BY table_name, ordinal_position;
```

## 🚨 NOTAS IMPORTANTES

1. **EJECUTAR MIGRACIONES PRIMERO**: Las migraciones deben ejecutarse antes del deploy
2. **VERIFICAR PERMISOS**: Asegurarse de que la service account tenga permisos para crear tablas
3. **BACKUP**: Hacer backup de BigQuery antes de ejecutar migraciones en producción
4. **TESTING**: Probar migraciones en entorno de desarrollo primero
5. **MONITORING**: Monitorear logs después del deploy para verificar que todo funciona

## 🔄 ROLLBACK

Si algo falla, usar las funciones `downgrade()` de cada migración:

```bash
python -c "from 001_create_ai_prompt_optimization_table import downgrade; downgrade()"
# Repetir para cada migración
```
