# energy_ia_api_COPY/app/__init__.py
# 🏢 APLICACIÓN EMPRESARIAL NIVEL 2025 - ENERGY IA API COPY

import os
import logging
from datetime import datetime
from utils.timezone_utils import now_spanish_iso, now_spanish
from flask import Flask, request, jsonify, g
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials

from app.config import config
from utils.error_handlers import register_error_handlers

# Configuración de logging empresarial
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/energy_ia_api.log", mode="a"),
    ],
)

logger = logging.getLogger(__name__)


def create_app(config_name: str) -> Flask:
    """
    Crea la aplicación Flask con configuración empresarial nivel 2025

    Args:
        config_name: Nombre de la configuración ('development', 'production', etc.)

    Returns:
        Flask: Aplicación Flask configurada
    """
    logger.info(f"🚀 Iniciando Energy IA API COPY - Configuración: {config_name}")

    # Crear aplicación Flask
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Configuración empresarial adicional
    app.config["ENTERPRISE_MODE"] = True
    app.config["API_VERSION"] = "2025.1.0"
    app.config["START_TIME"] = now_spanish_iso()
    app.config["SERVICE_NAME"] = "energy_ia_api_copy"

    # Configurar CORS empresarial
    CORS(
        app,
        origins=app.config.get("CORS_ORIGINS", ["http://localhost:3000"]),
        supports_credentials=True,
        allow_headers=[
            "Content-Type",
            "Authorization",
            "X-Requested-With",
            "X-API-Key",
        ],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    )

    # Inicializar Firebase Admin (solo una vez)
    if not firebase_admin._apps:
        try:
            cred = credentials.ApplicationDefault()
            firebase_admin.initialize_app(
                cred, {"projectId": app.config["GCP_PROJECT_ID"]}
            )
            logger.info("✅ Firebase Admin inicializado correctamente")
        except Exception as e:
            logger.error(f"❌ Error al inicializar Firebase Admin: {str(e)}")
            raise

    # Middleware empresarial
    @app.before_request
    def before_request():
        """Middleware ejecutado antes de cada request"""
        g.start_time = now_spanish()
        g.request_id = request.headers.get(
            "X-Request-ID", f"req_{int(now_spanish().timestamp())}"
        )

        # Log de request entrante
        logger.info(f"📥 REQUEST [{g.request_id}] {request.method} {request.path}")

    @app.after_request
    def after_request(response):
        """Middleware ejecutado después de cada request"""
        if hasattr(g, "start_time"):
            duration = (now_spanish() - g.start_time).total_seconds()
            logger.info(
                f"📤 RESPONSE [{g.request_id}] {response.status_code} - {duration:.3f}s"
            )

        # Headers de seguridad empresarial
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )
        response.headers["X-API-Version"] = app.config["API_VERSION"]
        response.headers["X-Service-Name"] = app.config["SERVICE_NAME"]

        return response

    # --- REGISTRO DE BLUEPRINTS EMPRESARIALES ---

    # Importar y registrar blueprint de energy IA
    from app.routes import energy_bp

    app.register_blueprint(energy_bp, url_prefix="/api/v1/energy")
    logger.info("✅ Blueprint energy_bp registrado")

    # Registrar blueprint de chatbot
    from app.chatbot_routes import chatbot_bp

    app.register_blueprint(chatbot_bp, url_prefix="/api/v1/chatbot")
    logger.info("✅ Blueprint chatbot_bp registrado")

    # Registrar blueprint de enlaces empresariales
    from app.links_routes import links_bp

    app.register_blueprint(links_bp, url_prefix="/api/v1")
    logger.info("✅ Blueprint links_bp registrado")

    # Registrar manejadores de errores empresariales
    register_error_handlers(app)
    logger.info("✅ Manejadores de errores empresariales registrados")

    # --- ENDPOINTS EMPRESARIALES ---

    @app.route("/health")
    def health_check():
        """Endpoint de health check empresarial"""
        return (
            jsonify(
                {
                    "status": "healthy",
                    "service": app.config["SERVICE_NAME"],
                    "version": app.config["API_VERSION"],
                    "timestamp": now_spanish_iso(),
                    "uptime_seconds": (
                        now_spanish() - datetime.fromisoformat(app.config["START_TIME"])
                    ).total_seconds(),
                    "environment": config_name,
                    "enterprise_mode": app.config["ENTERPRISE_MODE"],
                }
            ),
            200,
        )

    @app.route("/api/v1/info")
    def api_info():
        """Endpoint de información de la API"""
        return (
            jsonify(
                {
                    "service_name": app.config["SERVICE_NAME"],
                    "api_version": app.config["API_VERSION"],
                    "description": "API empresarial para IA de recomendaciones de tarifas energéticas",
                    "capabilities": [
                        "energy_recommendations",
                        "tariff_analysis",
                        "consumption_optimization",
                        "chat_interface",
                        "machine_learning_integration",
                    ],
                    "endpoints": {
                        "energy": "/api/v1/energy",
                        "chatbot": "/api/v1/chatbot",
                        "health": "/health",
                        "info": "/api/v1/info",
                    },
                    "enterprise_features": [
                        "advanced_authentication",
                        "error_handling",
                        "performance_monitoring",
                        "security_headers",
                        "request_logging",
                    ],
                    "timestamp": now_spanish_iso(),
                }
            ),
            200,
        )

    @app.route("/api/v1/status")
    def service_status():
        """Endpoint de estado del servicio"""
        try:
            # Verificar componentes críticos
            firebase_status = (
                "connected" if firebase_admin._apps else "disconnected" "disconnected"
            )

            return (
                jsonify(
                    {
                        "service_status": "operational",
                        "components": {
                            "firebase_admin": firebase_status,
                            "flask_app": "running",
                            "cors": "enabled",
                            "error_handlers": "active",
                        },
                        "metrics": {
                            "start_time": app.config["START_TIME"],
                            "uptime_seconds": (
                                now_spanish()
                                - datetime.fromisoformat(app.config["START_TIME"])
                            ).total_seconds(),
                            "config_name": config_name,
                        },
                        "timestamp": now_spanish_iso(),
                    }
                ),
                200,
            )

        except Exception as e:
            logger.error(f"❌ Error en status check: {str(e)}")
            return (
                jsonify(
                    {
                        "service_status": "degraded",
                        "error": str(e),
                        "timestamp": now_spanish_iso(),
                    }
                ),
                500,
            )

    logger.info(f"🎉 Energy IA API COPY inicializada exitosamente")
    logger.info(f"📊 Configuración: {config_name}")
    logger.info(f"🔧 Versión: {app.config['API_VERSION']}")
    logger.info(f"🏢 Modo empresarial: {app.config['ENTERPRISE_MODE']}")

    return app
