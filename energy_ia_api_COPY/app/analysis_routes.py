# energy_ia_api_COPY/app/analysis_routes.py
# 🔬 RUTAS DE ANÁLISIS CON INTELIGENCIA ARTIFICIAL

import logging
from flask import Blueprint, request, jsonify
from utils.error_handlers import AppError
from app.services.vertex_ai_service import VertexAIService

logger = logging.getLogger(__name__)
analysis_bp = Blueprint("analysis_routes", __name__)

@analysis_bp.route("/api/v1/analysis/sentiment", methods=["POST"])
def analyze_sentiment_route():
    """
    Endpoint para realizar el análisis de sentimiento de un texto utilizando Vertex AI.
    Este es un endpoint interno llamado por otros microservicios.
    """
    try:
        data = request.get_json()
        if not data or not data.get("message_text"):
            raise AppError("El campo 'message_text' es requerido.", 400)

        message_text = data["message_text"]
        user_id = data.get("user_id") # Opcional, para logging y contexto futuro

        logger.info(f"Recibida solicitud de análisis de sentimiento para el usuario: {user_id or 'desconocido'}")

        # Instanciar el servicio de Vertex AI
        vertex_service = VertexAIService()

        # Llamar al método de análisis de sentimiento real
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
