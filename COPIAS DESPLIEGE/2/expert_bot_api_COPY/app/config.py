"""
EXPERT BOT API - CONFIG EMPRESARIAL COPY
========================================

Configuración empresarial robusta para Expert Bot API.
Mantiene EXACTAMENTE las mismas credenciales, tablas y configuraciones que el original.

MEJORAS EMPRESARIALES:
- Validación robusta de variables de entorno
- Configuración de logging empresarial
- Manejo de errores en configuración
- Configuración de cache empresarial
- Configuración de monitorización

CREDENCIALES GOOGLE: IDÉNTICAS AL ORIGINAL (PROHIBIDO CAMBIAR)
TABLAS: IDÉNTICAS AL ORIGINAL (PROHIBIDO CAMBIAR)
NOMBRES: IDÉNTICOS AL ORIGINAL (PROHIBIDO CAMBIAR)

VERSIÓN: 2.0.0 - EMPRESARIAL COPY
FECHA: 2025-07-16
"""

import os
import logging
from typing import Any
from dotenv import load_dotenv

# Carga las variables de entorno desde un archivo .env si existe
load_dotenv()


class Config:
    """Configuraciones base completas para el servicio principal empresarial."""

    # --- CONFIGURACIONES EXISTENTES (INTACTAS) ---
    SECRET_KEY = os.environ.get("SECRET_KEY")
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY debe ser configurada como variable de entorno")

    CORS_ORIGINS = (os.environ.get("CORS_ORIGINS") or "http://localhost:3000").split(
        ","
    )

    # URL para la comunicación con el microservicio de IA
    ENV = os.environ.get("FLASK_CONFIG", "production").lower()
    ENERGY_IA_API_URL = os.environ.get("ENERGY_IA_API_URL")

    # Validación empresarial: ENERGY_IA_API_URL es obligatorio en producción
    if not ENERGY_IA_API_URL:
        raise ValueError(
            "ENERGY_IA_API_URL debe ser configurada como variable de entorno"
        )

    # --- NUEVAS VARIABLES PARA LA INTEGRACIÓN CON GOOGLE CLOUD ---
    # Leídas desde el archivo .env que configuramos previamente.

    # Variables críticas para la conexión con Google Cloud (IDÉNTICAS AL ORIGINAL)
    GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
    if not GCP_PROJECT_ID:
        raise ValueError("GCP_PROJECT_ID debe ser configurada como variable de entorno")

    GCP_LOCATION = os.environ.get("GCP_LOCATION", "eu")

    # --- VARIABLE PARA GEMINI VISION OCR ---
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

    # --- VARIABLES PARA BIGQUERY, PUBSUB Y CLOUD STORAGE ---
    BQ_DATASET_ID = os.environ.get("BQ_DATASET_ID", "smartwatt_data")
    BQ_CONVERSATIONS_TABLE_ID = os.environ.get(
        "BQ_CONVERSATIONS_TABLE_ID", "conversations_log"
    )
    BQ_FEEDBACK_TABLE_ID = os.environ.get("BQ_FEEDBACK_TABLE_ID", "feedback_log")
    BQ_CONSUMPTION_LOG_TABLE_ID = os.environ.get(
        "BQ_CONSUMPTION_LOG_TABLE_ID", "consumption_log"
    )
    BQ_UPLOADED_DOCS_TABLE_ID = os.environ.get(
        "BQ_UPLOADED_DOCS_TABLE_ID", "uploaded_documents_log"
    )
    BQ_USER_PROFILES_TABLE_ID = os.environ.get(
        "BQ_USER_PROFILES_TABLE_ID", "user_profiles_enriched"
    )
    BQ_RECOMMENDATION_LOG_TABLE_ID = os.environ.get(
        "BQ_RECOMMENDATION_LOG_TABLE_ID", "recommendation_log"
    )
    BQ_MARKET_TARIFFS_TABLE_ID = os.environ.get(
        "BQ_MARKET_TARIFFS_TABLE_ID", "market_electricity_tariffs"
    )
    PUBSUB_CONSUMPTION_TOPIC_ID = os.environ.get(
        "PUBSUB_CONSUMPTION_TOPIC_ID", "consumption_topic"
    )
    GCS_INVOICE_BUCKET = os.environ.get("GCS_INVOICE_BUCKET", "smarwatt-invoices")

    # 🧠 NUEVAS VARIABLES PARA APRENDIZAJE AUTOMÁTICO
    AI_LEARNING_ENABLED = (
        os.environ.get("AI_LEARNING_ENABLED", "true").lower() == "true"
    )
    BQ_AI_SENTIMENT_TABLE_ID = os.environ.get(
        "BQ_AI_SENTIMENT_TABLE_ID", "ai_sentiment_analysis"
    )
    BQ_AI_PATTERNS_TABLE_ID = os.environ.get(
        "BQ_AI_PATTERNS_TABLE_ID", "ai_user_patterns"
    )

    # 🏢 TABLAS EMPRESARIALES DE IA (IMPLEMENTADAS CON MIGRACIONES)
    BQ_AI_OPTIMIZATION_TABLE_ID = os.environ.get(
        "BQ_AI_OPTIMIZATION_TABLE_ID", "ai_prompt_optimization"
    )
    BQ_AI_PREDICTIONS_TABLE_ID = os.environ.get(
        "BQ_AI_PREDICTIONS_TABLE_ID", "ai_predictions"
    )
    BQ_AI_BUSINESS_METRICS_TABLE_ID = os.environ.get(
        "BQ_AI_BUSINESS_METRICS_TABLE_ID", "ai_business_metrics"
    )

    # 🏢 TABLAS DE PROCESAMIENTO ASÍNCRONO (IMPLEMENTADAS CON MIGRACIONES)
    BQ_ASYNC_TASKS_TABLE_ID = os.environ.get("BQ_ASYNC_TASKS_TABLE_ID", "async_tasks")
    BQ_WORKER_METRICS_TABLE_ID = os.environ.get(
        "BQ_WORKER_METRICS_TABLE_ID", "worker_metrics"
    )

    # 🏢 NUEVAS CONFIGURACIONES EMPRESARIALES
    ENTERPRISE_MODE = True
    CACHE_ENABLED = os.environ.get("CACHE_ENABLED", "true").lower() == "true"
    CACHE_TIMEOUT = int(os.environ.get("CACHE_TIMEOUT", "300"))  # 5 minutos

    # Configuración de logging empresarial
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
    LOG_FORMAT = os.environ.get(
        "LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Configuración de monitorización
    MONITORING_ENABLED = os.environ.get("MONITORING_ENABLED", "true").lower() == "true"
    METRICS_ENABLED = os.environ.get("METRICS_ENABLED", "true").lower() == "true"

    # Configuración de rate limiting empresarial
    RATE_LIMIT_ENABLED = os.environ.get("RATE_LIMIT_ENABLED", "true").lower() == "true"
    RATE_LIMIT_PER_MINUTE = int(os.environ.get("RATE_LIMIT_PER_MINUTE", "60"))

    # Configuración de timeouts empresariales
    REQUEST_TIMEOUT = int(os.environ.get("REQUEST_TIMEOUT", "30"))
    BIGQUERY_TIMEOUT = int(os.environ.get("BIGQUERY_TIMEOUT", "60"))

    # Validación robusta para las nuevas variables (IDÉNTICA AL ORIGINAL)
    @classmethod
    def validate_gcp_variables(cls) -> bool:
        """Valida que todas las variables críticas de GCP estén configuradas."""
        required_vars = {
            "GCP_PROJECT_ID": cls.GCP_PROJECT_ID,
            "GCP_LOCATION": cls.GCP_LOCATION,
            "GEMINI_API_KEY": cls.GEMINI_API_KEY,
            "BQ_DATASET_ID": cls.BQ_DATASET_ID,
            "BQ_CONVERSATIONS_TABLE_ID": cls.BQ_CONVERSATIONS_TABLE_ID,
            "BQ_FEEDBACK_TABLE_ID": cls.BQ_FEEDBACK_TABLE_ID,
            "BQ_CONSUMPTION_LOG_TABLE_ID": cls.BQ_CONSUMPTION_LOG_TABLE_ID,
            "BQ_UPLOADED_DOCS_TABLE_ID": cls.BQ_UPLOADED_DOCS_TABLE_ID,
            "BQ_USER_PROFILES_TABLE_ID": cls.BQ_USER_PROFILES_TABLE_ID,
            "BQ_AI_SENTIMENT_TABLE_ID": cls.BQ_AI_SENTIMENT_TABLE_ID,
            "BQ_AI_PATTERNS_TABLE_ID": cls.BQ_AI_PATTERNS_TABLE_ID,
            "BQ_AI_OPTIMIZATION_TABLE_ID": cls.BQ_AI_OPTIMIZATION_TABLE_ID,
            "BQ_AI_PREDICTIONS_TABLE_ID": cls.BQ_AI_PREDICTIONS_TABLE_ID,
            "BQ_AI_BUSINESS_METRICS_TABLE_ID": cls.BQ_AI_BUSINESS_METRICS_TABLE_ID,
            "BQ_ASYNC_TASKS_TABLE_ID": cls.BQ_ASYNC_TASKS_TABLE_ID,
            "BQ_WORKER_METRICS_TABLE_ID": cls.BQ_WORKER_METRICS_TABLE_ID,
            "BQ_MARKET_TARIFFS_TABLE_ID": cls.BQ_MARKET_TARIFFS_TABLE_ID,
            "PUBSUB_CONSUMPTION_TOPIC_ID": cls.PUBSUB_CONSUMPTION_TOPIC_ID,
            "GCS_INVOICE_BUCKET": cls.GCS_INVOICE_BUCKET,
        }

        missing_vars = [name for name, value in required_vars.items() if not value]
        if missing_vars:
            print(
                f"ADVERTENCIA: Faltan variables de entorno de GCP: {', '.join(missing_vars)}"
            )
            print("La ingesta de datos podría fallar en producción.")

        return len(missing_vars) == 0

    @classmethod
    def validate_enterprise_config(cls) -> bool:
        """Validación empresarial adicional de configuraciones."""
        logger = logging.getLogger("expert_bot_api")

        # Validar configuraciones críticas
        if not cls.SECRET_KEY:
            logger.error("SECRET_KEY no configurado")
            return False

        if not cls.ENERGY_IA_API_URL:
            logger.error("ENERGY_IA_API_URL no configurado")
            return False

        # Validar configuraciones de GCP
        gcp_valid = cls.validate_gcp_variables()

        if gcp_valid:
            logger.info(
                "Todas las configuraciones empresariales validadas correctamente"
            )
        else:
            logger.warning("Algunas configuraciones de GCP no están disponibles")

        return True

    @staticmethod
    def init_app(app: Any) -> None:
        """Inicialización empresarial de la aplicación."""
        logger = logging.getLogger("expert_bot_api")

        # Configurar logging
        logging.basicConfig(
            level=getattr(logging, app.config.get("LOG_LEVEL", "INFO")),
            format=app.config.get("LOG_FORMAT"),
        )

        # Validar configuraciones
        if app.config.get("ENTERPRISE_MODE"):
            app.config["VALIDATE_CONFIG"] = Config.validate_enterprise_config()

        logger.info("Configuración empresarial inicializada correctamente")


class DevelopmentConfig(Config):
    """Configuración de desarrollo empresarial."""

    DEBUG = True
    LOG_LEVEL = "DEBUG"
    CACHE_TIMEOUT = 60  # 1 minuto en desarrollo
    RATE_LIMIT_PER_MINUTE = 120  # Más permisivo en desarrollo


class ProductionConfig(Config):
    """Configuración de producción empresarial."""

    DEBUG = False
    LOG_LEVEL = "INFO"
    CACHE_TIMEOUT = 300  # 5 minutos en producción
    RATE_LIMIT_PER_MINUTE = 60  # Más restrictivo en producción

    # Configuraciones adicionales de seguridad para producción
    SECURITY_HEADERS = True
    FORCE_HTTPS = True


class TestingConfig(Config):
    """Configuración de testing empresarial."""

    TESTING = True
    DEBUG = True
    LOG_LEVEL = "DEBUG"
    CACHE_ENABLED = False
    RATE_LIMIT_ENABLED = False


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
