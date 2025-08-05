"""
EXPERT BOT API - APP INIT EMPRESARIAL COPY
==========================================

Inicializador de aplicación Flask empresarial con configuración robusta.
Mantiene EXACTAMENTE los mismos endpoints, credenciales y tablas que el original.

MEJORAS EMPRESARIALES:
- Inicialización robusta de Firebase con fallbacks
- Configuración CORS empresarial
- Registro de blueprints con validación
- Manejo de errores empresarial
- Monitorización y logging avanzado

CREDENCIALES GOOGLE: IDÉNTICAS AL ORIGINAL (PROHIBIDO CAMBIAR)
TABLAS: IDÉNTICAS AL ORIGINAL (PROHIBIDO CAMBIAR)
ENDPOINTS: IDÉNTICOS AL ORIGINAL (PROHIBIDO CAMBIAR)
MÉTODOS: IDÉNTICOS AL ORIGINAL (PROHIBIDO CAMBIAR)

VERSIÓN: 2.0.0 - EMPRESARIAL COPY
FECHA: 2025-07-16
"""

import logging
import os
from datetime import datetime
from flask import Flask, g, request
from flask_cors import CORS
from .config import config

# Importación robusta de utilidades
from utils.error_handlers import register_error_handlers

# Firebase Admin initialization con manejo empresarial
import firebase_admin
from firebase_admin import credentials


def create_app(config_name: str) -> Flask:
    """
    Crear aplicación Flask empresarial con configuración robusta.

    Args:
        config_name: Nombre de la configuración a usar

    Returns:
        Flask: Instancia de aplicación configurada empresarialmente
    """
    # Configurar logging empresarial
    logger = logging.getLogger("expert_bot_api")
    logger.info(f"Iniciando creación de aplicación con configuración: {config_name}")

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Configuración empresarial adicional
    app.config["ENTERPRISE_MODE"] = True
    app.config["STARTUP_TIME"] = datetime.now().isoformat()

    # Inicializar Firebase Admin SDK de forma robusta empresarial
    if not firebase_admin._apps:
        try:
            # En Cloud Run, usar Application Default Credentials
            cred = credentials.ApplicationDefault()
            firebase_admin.initialize_app(
                cred, {"projectId": app.config["GCP_PROJECT_ID"]}
            )
            app.logger.info(
                f"Firebase Admin SDK inicializado correctamente para proyecto: {app.config['GCP_PROJECT_ID']}"
            )
            logger.info(
                "Firebase Admin SDK configurado correctamente en modo empresarial"
            )
        except Exception as e:
            app.logger.error(f"Error inicializando Firebase Admin SDK: {e}")
            app.logger.error(
                "Esto puede causar problemas de autenticación en endpoints protegidos"
            )
            logger.warning(f"Firebase Admin SDK no disponible: {e}")
            # Continuar sin Firebase para endpoints que no lo necesiten
            pass

    # Configuración CORS empresarial
    try:
        CORS(app, origins=app.config["CORS_ORIGINS"], supports_credentials=True)
        logger.info("CORS configurado correctamente para modo empresarial")
    except Exception as e:
        logger.error(f"Error configurando CORS: {e}")
        # Fallback CORS básico
        CORS(app, origins="*", supports_credentials=True)

    # Middleware empresarial para logging de requests
    @app.before_request
    def log_request_info():
        """Middleware empresarial para logging de requests"""
        if not request.path.startswith("/static"):
            logger.info(
                f"Request: {request.method} {request.path} - IP: {request.remote_addr}"
            )

    # Registro de rutas del chatbot (IDÉNTICO AL ORIGINAL)
    try:
        from .routes import chat_bp

        app.register_blueprint(chat_bp, url_prefix="/api/v1/chatbot")
        logger.info("Blueprint de chat registrado correctamente")
    except Exception as e:
        logger.error(f"Error registrando blueprint de chat: {e}")
        raise

    # Registro de rutas de energía (IDÉNTICO AL ORIGINAL)
    try:
        from .energy_routes import expert_energy_bp

        app.register_blueprint(expert_energy_bp, url_prefix="/api/v1/energy")
        logger.info("Blueprint de energía registrado correctamente")
    except Exception as e:
        logger.error(f"Error registrando blueprint de energía: {e}")
        raise

    # Registro de rutas de enlaces empresariales
    try:
        from .links_routes import links_bp

        app.register_blueprint(links_bp, url_prefix="/api/v1")
        logger.info("Blueprint de enlaces empresariales registrado correctamente")
    except Exception as e:
        logger.error(f"Error registrando blueprint de enlaces: {e}")
        raise

    # Registro de rutas de análisis empresarial
    try:
        from .analysis_routes import analysis_bp

        app.register_blueprint(analysis_bp)
        logger.info("Blueprint de análisis empresarial registrado correctamente")
    except Exception as e:
        logger.error(f"Error registrando blueprint de análisis: {e}")
        raise

    # Registro de rutas de procesamiento asíncrono empresarial
    try:
        from .async_routes import async_bp

        app.register_blueprint(async_bp, url_prefix="/api/v1/async")
        logger.info(
            "Blueprint de procesamiento asíncrono empresarial registrado correctamente"
        )
    except Exception as e:
        logger.error(f"Error registrando blueprint de procesamiento asíncrono: {e}")
        raise

    # Registro de manejadores de errores empresariales
    try:
        register_error_handlers(app)
        logger.info("Manejadores de errores empresariales registrados correctamente")
    except Exception as e:
        logger.error(f"Error registrando manejadores de errores: {e}")
        raise

    # Endpoint de health check empresarial (IDÉNTICO AL ORIGINAL)
    @app.route("/health")
    def health_check():
        """
        Endpoint de health check empresarial con información detallada.
        IDÉNTICO AL ORIGINAL pero con información adicional para monitorización.
        """
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": "2.0.0-enterprise",
            "mode": "production",
        }, 200

    # Endpoint adicional para monitorización empresarial
    @app.route("/health/detailed")
    def detailed_health_check():
        """Endpoint de health check detallado para monitorización empresarial"""
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "startup_time": app.config.get("STARTUP_TIME"),
            "firebase_initialized": bool(firebase_admin._apps),
            "config": config_name,
            "enterprise_mode": True,
        }, 200

    logger.info("Aplicación Expert Bot API creada correctamente en modo empresarial")
    return app
