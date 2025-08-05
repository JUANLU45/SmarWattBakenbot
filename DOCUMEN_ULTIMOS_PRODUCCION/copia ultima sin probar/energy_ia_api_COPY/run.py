# energy_ia_api_COPY/run.py
# 🏢 APLICACIÓN EMPRESARIAL NIVEL 2025 - ENERGY IA API COPY

import os
import sys
import logging
from datetime import datetime
from flask import Flask
from app import create_app
from utils.timezone_utils import now_spanish_iso

# Configuración de logging empresarial
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/energy_ia_api.log", mode="a"),
    ],
)

logger = logging.getLogger(__name__)


def create_enterprise_app():
    """
    Crea la aplicación Flask con configuración empresarial
    """
    try:
        # Configuración empresarial del entorno
        config_name = os.getenv("FLASK_CONFIG", "production")

        # Crear la aplicación
        app = create_app(config_name)

        # Configuración adicional empresarial
        app.config["ENTERPRISE_MODE"] = True
        app.config["API_VERSION"] = "2025.1.0"
        app.config["START_TIME"] = now_spanish_iso()

        # Logging empresarial
        logger.info(f"🚀 Energy IA API COPY iniciada en modo empresarial")
        logger.info(f"📊 Configuración: {config_name}")
        logger.info(f"🔧 Versión: {app.config['API_VERSION']}")
        logger.info(f"⏰ Inicio: {app.config['START_TIME']}")

        return app

    except Exception as e:
        logger.error(f"❌ Error al crear la aplicación empresarial: {str(e)}")
        raise


# Crear la aplicación empresarial
app = create_enterprise_app()


# ENDPOINTS ÚNICOS EN RUN.PY (NO DUPLICAR CON __init__.py)


@app.route("/status")
def status_check():
    """Endpoint de estado empresarial"""
    return {
        "service": "energy_ia_api_copy",
        "version": app.config.get("API_VERSION", "2025.1.0"),
        "start_time": app.config.get("START_TIME"),
        "current_time": now_spanish_iso(),
        "enterprise_features": {
            "tariff_recommendations": True,
            "machine_learning": True,
            "robust_communication": True,
            "enterprise_security": True,
        },
    }


if __name__ == "__main__":
    try:
        # Configuración del servidor empresarial
        host = os.environ.get("HOST", "0.0.0.0")
        port = int(os.environ.get("PORT", 8080))
        debug = os.environ.get("FLASK_DEBUG", "False").lower() == "true"

        logger.info(f"🌐 Servidor iniciando en {host}:{port}")
        logger.info(f"🔍 Debug mode: {debug}")

        # Solo usar app.run() en desarrollo local
        # En producción (Docker) Gunicorn maneja la aplicación
        if os.environ.get("FLASK_ENV") != "production":
            app.run(
                host=host, port=port, debug=debug, threaded=True, use_reloader=False
            )
        else:
            logger.info(
                "🏭 Modo producción detectado - esperando que Gunicorn maneje la aplicación"
            )

    except Exception as e:
        logger.error(f"❌ Error al iniciar el servidor: {str(e)}")
        sys.exit(1)
