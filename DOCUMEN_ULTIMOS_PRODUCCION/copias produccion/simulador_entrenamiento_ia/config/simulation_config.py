# config/simulation_config.py
# Control de Costes y Autonomía - Adaptado a Producción Real

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# === CONFIGURACIÓN DE EJECUCIÓN AUTÓNOMA ===

# Si True, el script se ejecutará en un bucle continuo
AUTONOMOUS_MODE = True

# Intervalo entre ejecuciones autónomas para evitar picos de carga
# Ejemplo: 24 horas para simular un ciclo de actividad diario
EXECUTION_INTERVAL_HOURS = 24

# === PARÁMETROS DE SIMULACIÓN Y CONTROL DE GASTOS ===
# 🔥 CONFIGURACIÓN OPTIMIZADA PARA PRESUPUESTO €5/MES MÁXIMO 🔥

# EJECUCIÓN CADA 72 HORAS para control de costes
EXECUTION_INTERVAL_HOURS = 72  # 10 ejecuciones/mes en lugar de 30

# Número de usuarios sintéticos por ejecución (REDUCIDO para presupuesto)
# 25 usuarios × 10 interacciones × 10 ejecuciones/mes = 2,500 llamadas/mes
NUM_USERS_PER_RUN = 25

# Número de interacciones por usuario (MANTENIDO ROBUSTO)
# NO recortamos el aprendizaje, solo la frecuencia
API_CALLS_PER_USER = 10

# Porcentaje de usuarios que simularán una subida de factura
# MANTENIDO COMPLETO para entrenar OCR y Pub/Sub robustamente
INVOICE_UPLOAD_RATE = 0.20  # 20% de los usuarios

# Porcentaje de usuarios que simularán una petición de recomendación
# MANTENIDO COMPLETO para entrenar algoritmo de recomendaciones
RECOMMENDATION_REQUEST_RATE = 0.50  # 50% de los usuarios

# === CONFIGURACIÓN DE PRODUCCIÓN REAL ===

# URLs de los microservicios desplegados en Google Cloud Run
EXPERT_BOT_API_URL = os.getenv(
    "EXPERT_BOT_API_URL", "https://expert-bot-api-1010012211318.europe-west1.run.app"
)
ENERGY_IA_API_URL = os.getenv(
    "ENERGY_IA_API_URL", "https://energy-ia-api-1010012211318.europe-west1.run.app"
)

# Token de autenticación Firebase (DEBE ser un token real y válido)
AUTH_TOKEN = os.getenv("AUTH_TOKEN")

# Configuración de Google Cloud
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "smatwatt")
BQ_DATASET_ID = os.getenv("BQ_DATASET_ID", "smartwatt_data")

# === TABLAS BIGQUERY REALES EN PRODUCCIÓN ===
# ✅ VERIFICADAS CONTRA comamdos_desplige_variables_reales.md
BQ_CONVERSATIONS_TABLE_ID = os.getenv("BQ_CONVERSATIONS_TABLE_ID", "conversations_log")
BQ_CONSUMPTION_LOG_TABLE_ID = os.getenv(
    "BQ_CONSUMPTION_LOG_TABLE_ID", "consumption_log"
)
BQ_USER_PROFILES_TABLE_ID = os.getenv(
    "BQ_USER_PROFILES_TABLE_ID", "user_profiles_enriched"
)
BQ_MARKET_TARIFFS_TABLE_ID = os.getenv(
    "BQ_MARKET_TARIFFS_TABLE_ID", "market_electricity_tariffs"
)
BQ_RECOMMENDATION_LOG_TABLE_ID = os.getenv(
    "BQ_RECOMMENDATION_LOG_TABLE_ID", "recommendation_log"
)
BQ_UPLOADED_DOCS_TABLE_ID = os.getenv(
    "BQ_UPLOADED_DOCS_TABLE_ID", "uploaded_documents_log"
)
BQ_FEEDBACK_TABLE_ID = os.getenv("BQ_FEEDBACK_TABLE_ID", "feedback_log")

# === TABLAS ADICIONALES DE IA (DE EXPERT_BOT_API) ===
BQ_AI_SENTIMENT_TABLE_ID = os.getenv(
    "BQ_AI_SENTIMENT_TABLE_ID", "ai_sentiment_analysis"
)
BQ_AI_PATTERNS_TABLE_ID = os.getenv("BQ_AI_PATTERNS_TABLE_ID", "ai_user_patterns")
BQ_AI_OPTIMIZATION_TABLE_ID = os.getenv(
    "BQ_AI_OPTIMIZATION_TABLE_ID", "ai_prompt_optimization"
)
BQ_AI_PREDICTIONS_TABLE_ID = os.getenv("BQ_AI_PREDICTIONS_TABLE_ID", "ai_predictions")
BQ_AI_BUSINESS_METRICS_TABLE_ID = os.getenv(
    "BQ_AI_BUSINESS_METRICS_TABLE_ID", "ai_business_metrics"
)
BQ_ASYNC_TASKS_TABLE_ID = os.getenv("BQ_ASYNC_TASKS_TABLE_ID", "async_tasks")
BQ_WORKER_METRICS_TABLE_ID = os.getenv("BQ_WORKER_METRICS_TABLE_ID", "worker_metrics")

# === CONTROL DE COSTES Y LÍMITES ===
# 🔒 LÍMITES ESTRICTOS PARA PRESUPUESTO €5/MES 🔒

# Máximo número de llamadas API por hora (REDUCIDO para control de costes)
MAX_API_CALLS_PER_HOUR = int(os.getenv("MAX_API_CALLS_PER_HOUR", "500"))

# Máximo coste estimado por día en USD (AJUSTADO a €5/mes = ~$5.50/mes = $0.18/día)
MAX_DAILY_COST_USD = float(os.getenv("MAX_DAILY_COST_USD", "0.20"))

# NUEVO: Límite mensual estricto en USD (~€5 = $5.50)
MAX_MONTHLY_COST_USD = float(os.getenv("MAX_MONTHLY_COST_USD", "5.50"))

# NUEVO: Límite total de llamadas API por mes
MAX_MONTHLY_API_CALLS = int(os.getenv("MAX_MONTHLY_API_CALLS", "2500"))

# Timeout para peticiones HTTP (segundos)
HTTP_TIMEOUT = 30

# Reintentos máximos para peticiones fallidas
MAX_RETRIES = 3

# Tiempo de espera entre reintentos (segundos)
RETRY_DELAY = 5

# === CONFIGURACIÓN DE LOGGING ===
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "simulador_entrenamiento.log")


# === VALIDACIÓN DE CONFIGURACIÓN ===
def validate_configuration():
    """Valida que todas las configuraciones críticas estén presentes."""
    errors = []

    if not AUTH_TOKEN:
        errors.append("AUTH_TOKEN es requerido en el archivo .env")

    if not EXPERT_BOT_API_URL.startswith("https://"):
        errors.append("EXPERT_BOT_API_URL debe ser una URL HTTPS válida")

    if not ENERGY_IA_API_URL.startswith("https://"):
        errors.append("ENERGY_IA_API_URL debe ser una URL HTTPS válida")

    if NUM_USERS_PER_RUN <= 0:
        errors.append("NUM_USERS_PER_RUN debe ser mayor que 0")

    if API_CALLS_PER_USER <= 0:
        errors.append("API_CALLS_PER_USER debe ser mayor que 0")

    if errors:
        raise ValueError(
            "Errores de configuración:\n" + "\n".join(f"- {error}" for error in errors)
        )

    return True


# === ESTIMACIÓN DE COSTES ===
def estimate_daily_cost():
    """Estima el coste diario basado en la configuración actual."""
    daily_executions = 24 / EXECUTION_INTERVAL_HOURS
    daily_users = NUM_USERS_PER_RUN * daily_executions
    daily_api_calls = daily_users * API_CALLS_PER_USER

    # Costes estimados por llamada (USD) - ACTUALIZADOS 2025
    cost_per_api_call = 0.003  # $0.003 por llamada API (incluye Gemini)
    cost_per_bigquery_query = 0.002  # $0.002 por query BigQuery
    cost_per_firebase_auth = 0.001  # $0.001 por autenticación Firebase

    estimated_cost = (
        (daily_api_calls * cost_per_api_call)
        + (daily_api_calls * 2 * cost_per_bigquery_query)
        + (daily_api_calls * cost_per_firebase_auth)
    )

    return {
        "daily_executions": daily_executions,
        "daily_users": daily_users,
        "daily_api_calls": daily_api_calls,
        "estimated_cost_usd": round(estimated_cost, 3),
        "estimated_monthly_cost_usd": round(estimated_cost * 30, 2),
        "estimated_monthly_cost_eur": round(estimated_cost * 30 * 0.91, 2),  # USD a EUR
        "within_budget": (estimated_cost * 30) <= MAX_MONTHLY_COST_USD,
    }


def estimate_monthly_cost():
    """Estima el coste mensual completo."""
    monthly_executions = (30 * 24) / EXECUTION_INTERVAL_HOURS
    monthly_users = NUM_USERS_PER_RUN * monthly_executions
    monthly_api_calls = monthly_users * API_CALLS_PER_USER

    # Costes totales mensuales
    cost_per_api_call = 0.003
    cost_per_bigquery_query = 0.002
    cost_per_firebase_auth = 0.001

    total_monthly_cost = (
        (monthly_api_calls * cost_per_api_call)
        + (monthly_api_calls * 2 * cost_per_bigquery_query)
        + (monthly_api_calls * cost_per_firebase_auth)
    )

    return {
        "monthly_executions": monthly_executions,
        "monthly_users": monthly_users,
        "monthly_api_calls": monthly_api_calls,
        "total_monthly_cost_usd": round(total_monthly_cost, 2),
        "total_monthly_cost_eur": round(total_monthly_cost * 0.91, 2),
        "within_budget": total_monthly_cost <= MAX_MONTHLY_COST_USD,
        "budget_usage_percentage": round(
            (total_monthly_cost / MAX_MONTHLY_COST_USD) * 100, 1
        ),
    }


# Ejecutar validación al importar
if __name__ == "__main__":
    validate_configuration()
    daily_cost = estimate_daily_cost()
    monthly_cost = estimate_monthly_cost()

    print("🔥 CONFIGURACIÓN OPTIMIZADA PARA PRESUPUESTO €5/MES 🔥")
    print("=" * 60)
    print(f"📊 ESTIMACIÓN DIARIA:")
    print(f"   • Ejecuciones: {daily_cost['daily_executions']}")
    print(f"   • Usuarios: {daily_cost['daily_users']}")
    print(f"   • Llamadas API: {daily_cost['daily_api_calls']}")
    print(
        f"   • Coste: ${daily_cost['estimated_cost_usd']} USD / €{daily_cost['estimated_monthly_cost_eur']}"
    )
    print()
    print(f"📊 ESTIMACIÓN MENSUAL:")
    print(f"   • Ejecuciones totales: {monthly_cost['monthly_executions']}")
    print(f"   • Usuarios totales: {monthly_cost['monthly_users']}")
    print(f"   • Llamadas API totales: {monthly_cost['monthly_api_calls']}")
    print(f"   • Coste total: ${monthly_cost['total_monthly_cost_usd']} USD")
    print(f"   • Coste total: €{monthly_cost['total_monthly_cost_eur']} EUR")
    print(f"   • Uso del presupuesto: {monthly_cost['budget_usage_percentage']}%")
    print(
        f"   • Dentro del presupuesto: {'✅ SÍ' if monthly_cost['within_budget'] else '❌ NO'}"
    )
    print("=" * 60)
