"""
EXPERT BOT API - VERSIÓN EMPRESARIAL COPY
========================================

Servidor principal para el servicio Expert Bot API con configuración empresarial robusta.
Mantiene EXACTAMENTE los mismos nombres, credenciales y tablas que el original.

MEJORAS EMPRESARIALES:
- Logging empresarial completo
- Manejo robusto de errores
- Configuración de producción optimizada
- Monitorización de rendimiento
- Validación de entorno empresarial

CREDENCIALES Y TABLAS: IDÉNTICAS AL ORIGINAL (PROHIBIDO CAMBIAR)
ENDPOINTS: IDÉNTICOS AL ORIGINAL (PROHIBIDO CAMBIAR)
MÉTODOS: IDÉNTICOS AL ORIGINAL (PROHIBIDO CAMBIAR)

VERSIÓN: 2.0.0 - EMPRESARIAL COPY
FECHA: 2025-07-16
"""

import os
import sys
import logging
from datetime import datetime
from app import create_app


# Configuración de logging empresarial
def setup_enterprise_logging():
    """Configuración de logging empresarial robusto"""
    log_level = os.getenv("LOG_LEVEL", "INFO")
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(
                f'expert_bot_api_{datetime.now().strftime("%Y%m%d")}.log'
            ),
        ],
    )

    # Logger específico para la aplicación
    app_logger = logging.getLogger("expert_bot_api")
    app_logger.info("Sistema de logging empresarial iniciado correctamente")
    return app_logger


# Validación de entorno empresarial
def validate_enterprise_environment():
    """Validación robusta del entorno empresarial"""
    logger = logging.getLogger("expert_bot_api")

    required_vars = ["GCP_PROJECT_ID", "FLASK_CONFIG"]

    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        logger.warning(
            "Variables de entorno faltantes (usando defaults): %s", missing_vars
        )
    else:
        logger.info("Todas las variables de entorno requeridas están configuradas")

    return True


# Inicialización empresarial
def initialize_enterprise_app():
    """Inicialización empresarial robusta de la aplicación"""
    logger = logging.getLogger("expert_bot_api")

    try:
        # Validar entorno
        validate_enterprise_environment()

        # Crear aplicación con configuración empresarial
        config_name = os.getenv("FLASK_CONFIG", "production")
        logger.info("Iniciando aplicación con configuración: %s", config_name)

        app = create_app(config_name)

        # Configuración adicional empresarial
        app.config["ENTERPRISE_MODE"] = True
        app.config["STARTUP_TIME"] = datetime.now().isoformat()

        logger.info(
            "Aplicación Expert Bot API inicializada correctamente en modo empresarial"
        )
        return app

    except Exception as e:
        logger.error("Error crítico en inicialización empresarial: %s", e)
        sys.exit(1)


# Configuración empresarial
setup_enterprise_logging()
app = initialize_enterprise_app()

if __name__ == "__main__":
    logger = logging.getLogger("expert_bot_api")

    # Configuración del servidor empresarial
    host = os.getenv("HOST", "0.0.0.0")
    port_str = os.getenv("PORT", "8081")
    try:
        port = int(port_str)
    except ValueError:
        logger.warning("Valor de PORT inválido: %s, usando 8081", port_str)
        port = 8081
    debug = os.getenv("FLASK_DEBUG", "False").lower() == "true"

    logger.info("Iniciando servidor empresarial en %s:%d", host, port)
    logger.info("Modo debug: %s", debug)

    try:
        # Solo usar app.run() en desarrollo local
        # En producción (Docker) Gunicorn maneja la aplicación
        if os.getenv("FLASK_ENV") != "production":
            app.run(
                host=host,
                port=port,
                debug=debug,
                threaded=True,
                use_reloader=False,  # Desactivado en producción
            )
        else:
            logger.info(
                "Modo producción detectado - esperando que Gunicorn maneje la aplicación"
            )
    except Exception as e:
        logger.error("Error crítico en servidor: %s", e)
        sys.exit(1)
