# energy_ia_api_COPY/app/__init__.py
# 🏢 APLICACIÓN EMPRESARIAL NIVEL 2025 - ENERGY IA API COPY

import logging
from flask import Flask
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials

from app.config import config
from utils.error_handlers import register_error_handlers

def create_app(config_name: str) -> Flask:
    """Crea y configura una instancia de la aplicación Flask."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Configurar CORS
    CORS(app, origins=app.config.get("CORS_ORIGINS", "*"))

    # Inicializar Firebase Admin
    if not firebase_admin._apps:
        try:
            cred = credentials.ApplicationDefault()
            firebase_admin.initialize_app(cred, {"projectId": app.config["GCP_PROJECT_ID"]})
            logging.info("✅ Firebase Admin inicializado correctamente.")
        except Exception as e:
            logging.critical(f"❌ Error fatal al inicializar Firebase Admin: {e}")
            # En un entorno de producción, esto debería detener el arranque.
            raise e

    # Registrar Blueprints
    from .routes import energy_bp
    from .chatbot_routes import chatbot_bp
    from .analysis_routes import analysis_bp
    from .links_routes import links_bp
    from .weather_routes import weather_bp # Importar el nuevo blueprint

    app.register_blueprint(energy_bp, url_prefix="/api/v1/energy")
    app.register_blueprint(chatbot_bp, url_prefix="/api/v1/chatbot")
    app.register_blueprint(analysis_bp, url_prefix="/api/v1/analysis")
    app.register_blueprint(links_bp, url_prefix="/api/v1/links")
    app.register_blueprint(weather_bp, url_prefix="/api/v1/weather") # Registrar el nuevo blueprint
    
    # Registrar manejadores de errores
    register_error_handlers(app)

    @app.route("/health")
    def health_check():
        return {"status": "healthy"}, 200

    logging.info(f"🎉 Energy IA API COPY ({config_name}) inicializada exitosamente.")
    return app
