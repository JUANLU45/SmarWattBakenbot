# energy_ia_api_COPY/app/config.py
# 🏢 CONFIGURACIÓN EMPRESARIAL NIVEL 2025 - ENERGY IA API COPY

import os
import logging
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de logging empresarial
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EnterpriseConfig:
    """Configuración empresarial base para el servicio de IA nivel 2025"""

    # === CONFIGURACIÓN BÁSICA EMPRESARIAL ===
    SECRET_KEY = os.environ.get("SECRET_KEY_IA")
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY_IA debe ser configurada como variable de entorno")

    CORS_ORIGINS = (os.environ.get("CORS_ORIGINS") or "http://localhost:3000").split(
        ","
    )

    # === CONFIGURACIÓN EMPRESARIAL AVANZADA ===
    ENTERPRISE_MODE = True
    API_VERSION = "2025.1.0"
    SERVICE_NAME = "energy_ia_api_copy"
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    REQUEST_TIMEOUT = 30

    # === CONFIGURACIÓN DE SEGURIDAD EMPRESARIAL ===
    SECURITY_HEADERS = {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    }

    # === CONFIGURACIÓN DE RATE LIMITING ===
    RATE_LIMIT_REQUESTS_PER_MINUTE = 60
    RATE_LIMIT_BURST = 10

    # === VARIABLES CRÍTICAS PARA GOOGLE CLOUD ===
    GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
    if not GCP_PROJECT_ID:
        raise ValueError("GCP_PROJECT_ID debe ser configurada como variable de entorno")

    GCP_LOCATION = os.environ.get("GCP_LOCATION")
    TARIFF_RECOMMENDER_ENDPOINT_ID = os.environ.get("TARIFF_RECOMMENDER_ENDPOINT_ID")

    # === VARIABLE PARA GEMINI AI ===
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

    # === VARIABLE PARA INTEGRACIÓN CON EXPERT-BOT-API ===
    EXPERT_BOT_API_URL = os.environ.get("EXPERT_BOT_API_URL")

    # === VARIABLES PARA BIGQUERY Y OTROS SERVICIOS ===
    BQ_DATASET_ID = os.environ.get("BQ_DATASET_ID")
    BQ_MARKET_TARIFFS_TABLE_ID = (
        os.environ.get("BQ_MARKET_TARIFFS_TABLE_ID") or "market_electricity_tariffs"
    )
    BQ_RECOMMENDATION_LOG_TABLE_ID = os.environ.get(
        "BQ_RECOMMENDATION_LOG_TABLE_ID", "recommendation_log"
    )
    BQ_CONSUMPTION_LOG_TABLE_ID = os.environ.get(
        "BQ_CONSUMPTION_LOG_TABLE_ID", "consumption_log"
    )
    BQ_UPLOADED_DOCS_TABLE_ID = os.environ.get(
        "BQ_UPLOADED_DOCS_TABLE_ID", "uploaded_documents_log"
    )
    BQ_CONVERSATIONS_TABLE_ID = os.environ.get(
        "BQ_CONVERSATIONS_TABLE_ID", "conversations_log"
    )
    BQ_FEEDBACK_TABLE_ID = os.environ.get("BQ_FEEDBACK_TABLE_ID", "feedback_log")
    BQ_USER_PROFILES_TABLE_ID = os.environ.get(
        "BQ_USER_PROFILES_TABLE_ID", "user_profiles_enriched"
    )
    # 🤖 CONFIGURACIÓN PARA AI_PREDICTIONS - VERTEX AI TARIFF RECOMMENDER
    BQ_AI_PREDICTIONS_TABLE_ID = os.environ.get(
        "BQ_AI_PREDICTIONS_TABLE_ID", "ai_predictions"
    )
    # 📊 CONFIGURACIÓN PARA AI_BUSINESS_METRICS - MÉTRICAS EMPRESARIALES DE IA
    BQ_AI_BUSINESS_METRICS_TABLE_ID = os.environ.get(
        "BQ_AI_BUSINESS_METRICS_TABLE_ID", "ai_business_metrics"
    )

    # 📈 CONFIGURACIÓN PARA MARKET_ANALYSIS - USA TABLA AI_BUSINESS_METRICS
    BQ_MARKET_ANALYSIS_TABLE_ID = os.environ.get(
        "BQ_MARKET_ANALYSIS_TABLE_ID", "ai_business_metrics"
    )

    # 🧠 CONFIGURACIÓN PARA AI_SENTIMENT_ANALYSIS (MISMO QUE EXPERT_BOT_API_COPY)
    BQ_AI_SENTIMENT_TABLE_ID = os.environ.get(
        "BQ_AI_SENTIMENT_TABLE_ID", "ai_sentiment_analysis"
    )

    # === VARIABLES PARA PUBSUB Y CLOUD STORAGE ===
    PUBSUB_CONSUMPTION_TOPIC_ID = os.environ.get("PUBSUB_CONSUMPTION_TOPIC_ID")
    GCS_INVOICE_BUCKET = os.environ.get("GCS_INVOICE_BUCKET")

    # === CONFIGURACIÓN DE MACHINE LEARNING EMPRESARIAL ===
    ML_MODEL_CACHE_TTL = 3600  # 1 hour
    ML_PREDICTION_TIMEOUT = 10  # seconds
    ML_BATCH_SIZE = 100
    ML_ENABLE_MONITORING = True

    # --- INTERRUPTOR EMPRESARIAL DE VERTEX AI ---
    # Por defecto está activado, pero se puede desactivar con una variable de entorno
    VERTEX_AI_ENABLED = os.environ.get("VERTEX_AI_ENABLED", "true").lower() == "true"

    # === CONFIGURACIÓN DE LOGGING EMPRESARIAL ===
    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "enterprise": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "enterprise",
                "level": "INFO",
            },
            "file": {
                "class": "logging.FileHandler",
                "filename": "logs/energy_ia_api_copy.log",
                "formatter": "enterprise",
                "level": "INFO",
            },
        },
        "loggers": {
            "energy_ia_api_copy": {
                "handlers": ["console", "file"],
                "level": "INFO",
                "propagate": False,
            }
        },
    }

    # === CONFIGURACIÓN DE CACHÉ EMPRESARIAL ===
    CACHE_CONFIG = {
        "CACHE_TYPE": "redis",
        "CACHE_REDIS_URL": os.environ.get("REDIS_URL", "redis://localhost:6379/0"),
        "CACHE_DEFAULT_TIMEOUT": 300,
        "CACHE_KEY_PREFIX": "energy_ia_api_copy:",
    }

    # === CONFIGURACIÓN DE MONITOREO EMPRESARIAL ===
    MONITORING_CONFIG = {
        "ENABLE_METRICS": True,
        "METRICS_ENDPOINT": "/metrics",
        "HEALTH_CHECK_INTERVAL": 30,
        "PERFORMANCE_TRACKING": True,
    }

    # === VALIDACIÓN ROBUSTA EMPRESARIAL ===
    _required_vars = [
        "GCP_PROJECT_ID",
        "GCP_LOCATION",
        "TARIFF_RECOMMENDER_ENDPOINT_ID",
        "BQ_DATASET_ID",
        "BQ_MARKET_TARIFFS_TABLE_ID",
        "BQ_RECOMMENDATION_LOG_TABLE_ID",
        "BQ_CONSUMPTION_LOG_TABLE_ID",
        "BQ_UPLOADED_DOCS_TABLE_ID",
        "BQ_CONVERSATIONS_TABLE_ID",
        "BQ_FEEDBACK_TABLE_ID",
        "BQ_USER_PROFILES_TABLE_ID",
        "BQ_AI_PREDICTIONS_TABLE_ID",
        "BQ_AI_BUSINESS_METRICS_TABLE_ID",
        "PUBSUB_CONSUMPTION_TOPIC_ID",
        "GCS_INVOICE_BUCKET",
    ]

    @classmethod
    def validate_configuration(cls) -> Dict[str, Any]:
        """Validación empresarial de configuración"""
        validation_result = {
            "valid": True,
            "missing_vars": [],
            "warnings": [],
            "critical_errors": [],
        }

        # Verificar variables requeridas
        for var_name in cls._required_vars:
            var_value = getattr(cls, var_name, None)
            if var_value is None:
                validation_result["missing_vars"].append(var_name)
                validation_result["valid"] = False

        # Verificar API keys críticas
        if not cls.GEMINI_API_KEY:
            validation_result["critical_errors"].append("GEMINI_API_KEY no configurada")
            validation_result["valid"] = False

        # Verificar URLs
        if cls.EXPERT_BOT_API_URL and not cls.EXPERT_BOT_API_URL.startswith(
            ("http://", "https://")
        ):
            validation_result["warnings"].append("EXPERT_BOT_API_URL formato inválido")

        # Log de resultados
        if validation_result["missing_vars"]:
            logger.warning(
                f"⚠️  Variables faltantes: {', '.join(validation_result['missing_vars'])}"
            )

        if validation_result["critical_errors"]:
            logger.error(
                f"❌ Errores críticos: {', '.join(validation_result['critical_errors'])}"
            )

        if validation_result["valid"]:
            logger.info("✅ Configuración empresarial validada exitosamente")
        else:
            logger.error("❌ Configuración empresarial inválida")

        return validation_result

    @classmethod
    def get_database_config(cls) -> Dict[str, str]:
        """Obtiene configuración de base de datos"""
        return {
            "project_id": cls.GCP_PROJECT_ID,
            "dataset_id": cls.BQ_DATASET_ID,
            "location": cls.GCP_LOCATION,
            "tables": {
                "market_electricity_tariffs": cls.BQ_MARKET_TARIFFS_TABLE_ID,
                "recommendation_log": cls.BQ_RECOMMENDATION_LOG_TABLE_ID,
                "consumption_log": cls.BQ_CONSUMPTION_LOG_TABLE_ID,
                "uploaded_docs": cls.BQ_UPLOADED_DOCS_TABLE_ID,
                "conversations": cls.BQ_CONVERSATIONS_TABLE_ID,
                "feedback": cls.BQ_FEEDBACK_TABLE_ID,
                "user_profiles": cls.BQ_USER_PROFILES_TABLE_ID,
                "ai_sentiment_analysis": cls.BQ_AI_SENTIMENT_TABLE_ID,
            },
        }

    @classmethod
    def get_ml_config(cls) -> Dict[str, Any]:
        """Obtiene configuración de Machine Learning"""
        return {
            "endpoint_id": cls.TARIFF_RECOMMENDER_ENDPOINT_ID,
            "project_id": cls.GCP_PROJECT_ID,
            "location": cls.GCP_LOCATION,
            "cache_ttl": cls.ML_MODEL_CACHE_TTL,
            "prediction_timeout": cls.ML_PREDICTION_TIMEOUT,
            "batch_size": cls.ML_BATCH_SIZE,
            "enable_monitoring": cls.ML_ENABLE_MONITORING,
        }

    @classmethod
    def get_ai_config(cls) -> Dict[str, str]:
        """Obtiene configuración de IA"""
        return {
            "gemini_api_key": cls.GEMINI_API_KEY,
            "expert_bot_url": cls.EXPERT_BOT_API_URL,
            "model_name": "gemini-1.5-flash",
            "max_tokens": 2048,
            "temperature": 0.7,
        }

    @staticmethod
    def init_app(app):
        """Inicialización empresarial de la aplicación"""
        logger.info("🏢 Inicializando configuración empresarial...")

        # Crear directorios necesarios
        os.makedirs("logs", exist_ok=True)
        os.makedirs("cache", exist_ok=True)
        os.makedirs("tmp", exist_ok=True)

        # Validar configuración
        validation = EnterpriseConfig.validate_configuration()
        if not validation["valid"]:
            logger.error(
                "❌ Configuración empresarial inválida. Revisar variables de entorno."
            )

        logger.info("✅ Configuración empresarial inicializada")


class EnterpriseDevelopmentConfig(EnterpriseConfig):
    """Configuración de desarrollo empresarial"""

    DEBUG = True
    TESTING = False

    # Configuración específica de desarrollo
    RATE_LIMIT_REQUESTS_PER_MINUTE = 120  # Más permisivo en desarrollo
    ML_MODEL_CACHE_TTL = 60  # Cache más corto en desarrollo

    @staticmethod
    def init_app(app):
        EnterpriseConfig.init_app(app)
        logger.info("🔧 Configuración de desarrollo empresarial activada")


class EnterpriseProductionConfig(EnterpriseConfig):
    """Configuración de producción empresarial"""

    DEBUG = False
    TESTING = False

    # Configuración específica de producción
    RATE_LIMIT_REQUESTS_PER_MINUTE = 60  # Más restrictivo en producción
    ML_MODEL_CACHE_TTL = 3600  # Cache más largo en producción

    # Configuración de seguridad adicional en producción
    SECURITY_HEADERS = {
        **EnterpriseConfig.SECURITY_HEADERS,
        "Content-Security-Policy": "default-src 'self'",
        "X-Permitted-Cross-Domain-Policies": "none",
    }

    @staticmethod
    def init_app(app):
        EnterpriseConfig.init_app(app)
        logger.info("🏭 Configuración de producción empresarial activada")


class EnterpriseTestingConfig(EnterpriseConfig):
    """Configuración de testing empresarial"""

    DEBUG = True
    TESTING = True

    # Configuración específica de testing
    RATE_LIMIT_REQUESTS_PER_MINUTE = 300  # Sin límites en testing
    ML_MODEL_CACHE_TTL = 1  # Cache muy corto en testing

    @staticmethod
    def init_app(app):
        EnterpriseConfig.init_app(app)
        logger.info("🧪 Configuración de testing empresarial activada")


# Diccionario de configuraciones disponibles
config = {
    "development": EnterpriseDevelopmentConfig,
    "production": EnterpriseProductionConfig,
    "testing": EnterpriseTestingConfig,
    "default": EnterpriseDevelopmentConfig,
}


# Función de utilidad para obtener configuración actual
def get_current_config(config_name: str = "default") -> EnterpriseConfig:
    """Obtiene la configuración actual"""
    return config.get(config_name, EnterpriseDevelopmentConfig)


# Función de utilidad para validar configuración al importar
def validate_on_import():
    """Valida la configuración al importar el módulo"""
    validation = EnterpriseConfig.validate_configuration()
    if not validation["valid"]:
        logger.warning("⚠️  Configuración empresarial con problemas detectados")
    return validation


# Validar configuración al importar
_validation_result = validate_on_import()
