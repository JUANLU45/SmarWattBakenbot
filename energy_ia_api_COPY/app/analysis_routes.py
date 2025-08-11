# energy_ia_api_COPY/app/analysis_routes.py
# 🔬 RUTAS DE ANÁLISIS CON INTELIGENCIA ARTIFICIAL

import logging
from flask import Blueprint, request, jsonify
from utils.error_handlers import AppError
from app.services.vertex_ai_service import VertexAIService
from energy_ia_api_COPY.utils.security import internal_auth_required

logger = logging.getLogger(__name__)
analysis_bp = Blueprint("analysis_routes", __name__)

@analysis_bp.route("/api/v1/analysis/sentiment", methods=["POST"])
@internal_auth_required
def analyze_sentiment_route():
    """
    Endpoint interno y seguro para realizar el análisis de sentimiento de un texto.
    Solo accesible por otros servicios de Google Cloud con un token de ID válido.
    """
    try:
        data = request.get_json()
        if not data or not data.get("message_text"):
            raise AppError("El campo 'message_text' es requerido.", 400)

        message_text = data["message_text"]
        user_id = data.get("user_id")

        logger.info(f"Recibida solicitud de análisis de sentimiento interna para el usuario: {user_id or 'desconocido'}")

        vertex_service = VertexAIService()
        sentiment_analysis = vertex_service.analyze_text_sentiment(message_text)

        return jsonify({
            "status": "success",
            "message": "Análisis de sentimiento completado exitosamente.",
            "sentiment_analysis": sentiment_analysis
        }), 200

    except AppError as e:
        logger.error(f"❌ Error de aplicación en el análisis de sentimiento: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), e.status_code
    except Exception as e:
        logger.error(f"❌ Error inesperado en el endpoint de análisis de sentimiento: {str(e)}")
        return jsonify({"status": "error", "message": "Error interno del servidor al analizar el sentimiento."}), 500
