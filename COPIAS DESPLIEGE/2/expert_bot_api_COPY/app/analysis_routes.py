"""
EXPERT BOT API - ANALYSIS ROUTES EMPRESARIAL COPY
=================================================

Rutas empresariales para servicios de análisis avanzado.
Mantiene EXACTAMENTE el mismo patrón y estructura que los otros endpoints.

ENDPOINTS EMPRESARIALES:
- POST /api/v1/analysis/sentiment - Análisis de sentiment empresarial

MEJORAS EMPRESARIALES:
- Validación robusta de entrada
- Logging detallado de requests
- Manejo de errores empresarial
- Rate limiting por usuario
- Métricas de rendimiento

VERSIÓN: 2.0.0 - EMPRESARIAL COPY
FECHA: 2025-08-03
"""

import logging
from datetime import datetime, timezone
from typing import Tuple
from flask import Blueprint, request, jsonify, g, Response
from smarwatt_auth import token_required
from utils.error_handlers import AppError
from .services.ai_learning_service import AILearningService

# Configurar logger para este módulo
logger = logging.getLogger("expert_bot_api.analysis_routes")

analysis_bp = Blueprint("analysis_routes", __name__)


# Middleware empresarial para logging y métricas
@analysis_bp.before_request
def log_route_access() -> None:
    """Middleware empresarial para logging de acceso a rutas."""
    if hasattr(g, "user"):
        logger.info(
            "Usuario %s accediendo a %s", g.user.get("uid", "unknown"), request.endpoint
        )
    else:
        logger.info("Acceso anónimo a %s", request.endpoint)


@analysis_bp.route("/api/v1/analysis/sentiment", methods=["POST", "OPTIONS"])
@token_required
def analyze_sentiment() -> Tuple[Response, int]:
    """
    Endpoint empresarial para análisis de sentiment avanzado.
    Expone el método analyze_sentiment_enterprise vía HTTP para microservicios independientes.
    """
    # Manejar petición OPTIONS para CORS
    if request.method == "OPTIONS":
        response = Response()
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response, 200

    try:
        user_profile = g.user
        json_data = request.get_json()

        # Validación empresarial robusta
        if not json_data:
            logger.warning(
                "Petición inválida sin datos JSON para usuario: %s",
                user_profile.get("uid"),
            )
            raise AppError("Petición inválida. Se requieren datos JSON.", 400)

        if not json_data.get("message_text"):
            logger.warning(
                "Petición inválida sin message_text para usuario: %s",
                user_profile.get("uid"),
            )
            raise AppError(
                "Petición inválida. El campo 'message_text' es requerido.", 400
            )

        # Validar longitud del mensaje
        message_text = json_data["message_text"]
        if not message_text.strip():
            logger.warning(
                "Mensaje vacío recibido de usuario: %s", user_profile.get("uid")
            )
            raise AppError("El mensaje no puede estar vacío.", 400)

        if len(message_text) > 5000:
            logger.warning(
                "Mensaje demasiado largo (%d caracteres) de usuario: %s",
                len(message_text),
                user_profile.get("uid"),
            )
            raise AppError("El mensaje no puede exceder 5000 caracteres.", 400)

        # Extraer parámetros opcionales
        conversation_id = json_data.get("conversation_id", "default_conversation")
        user_id = json_data.get("user_id", user_profile.get("uid"))

        logger.info(
            "Analizando sentiment para usuario: %s, conversación: %s, longitud mensaje: %d",
            user_profile.get("uid"),
            conversation_id,
            len(message_text),
        )

        # Inicializar servicio de AI Learning
        ai_learning_service = AILearningService()

        # Realizar análisis de sentiment empresarial
        sentiment_analysis = ai_learning_service.analyze_sentiment_enterprise(
            user_id, conversation_id, message_text
        )

        # Preparar respuesta empresarial
        response_data = {
            "status": "success",
            "sentiment_analysis": {
                "sentiment_score": sentiment_analysis.sentiment_score,
                "sentiment_label": sentiment_analysis.sentiment_label,
                "confidence": sentiment_analysis.confidence,
                "emotional_indicators": sentiment_analysis.emotional_indicators,
                "personalization_hints": sentiment_analysis.personalization_hints,
                "risk_factors": sentiment_analysis.risk_factors,
                "engagement_level": sentiment_analysis.engagement_level,
            },
            "request_info": {
                "user_id": user_id,
                "conversation_id": conversation_id,
                "message_length": len(message_text),
                "processed_at": datetime.now().isoformat(),
            },
            "enterprise_metrics": {
                "processing_successful": True,
                "analysis_type": "advanced_enterprise",
                "ai_service_version": "2.0.0",
            },
        }

        logger.info(
            "Análisis de sentiment completado para usuario: %s, score: %.3f, label: %s",
            user_profile.get("uid"),
            sentiment_analysis.sentiment_score,
            sentiment_analysis.sentiment_label,
        )

        return jsonify(response_data), 200

    except AppError:
        raise
    except Exception as e:
        logger.error(
            "Error interno en análisis de sentiment para usuario %s: %s",
            g.user.get("uid", "unknown"),
            str(e),
        )
        raise AppError(
            "Error interno procesando análisis de sentiment: %s" % str(e), 500
        ) from e


# Error handler específico para este blueprint
@analysis_bp.errorhandler(AppError)
def handle_analysis_error(error: AppError) -> Tuple[Response, int]:
    """Manejador de errores específico para rutas de análisis."""
    logger.error("Error en ruta de análisis: %s", str(error))
    return (
        jsonify(
            {
                "status": "error",
                "message": error.message,
                "timestamp": datetime.now().isoformat(),
                "error_type": "analysis_error",
            }
        ),
        error.status_code,
    )


@analysis_bp.route("/api/v1/analysis/sentiment/internal", methods=["POST", "OPTIONS"])
def analyze_sentiment_internal() -> Tuple[Response, int]:
    """
    🔒 ENDPOINT INTERNO PARA ANÁLISIS DE SENTIMENT ENTRE MICROSERVICIOS

    Endpoint específico para comunicación service-to-service.
    NO requiere autenticación Firebase para evitar conflictos arquitectónicos.
    Incluye validación de origen interno para mantener seguridad.

    USADO POR: energy-ia-api para análisis de sentiment en conversaciones
    SEGURIDAD: Validación User-Agent + red interna Cloud Run
    """
    # Manejar petición OPTIONS para CORS
    if request.method == "OPTIONS":
        response = Response()
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response, 200

    try:
        # Validación de origen interno - Solo servicios Python internos
        user_agent = request.headers.get("User-Agent", "")
        if "python-requests" not in user_agent:
            logger.warning("Request no interno detectado: %s", user_agent)
            raise AppError(
                "Endpoint exclusivo para comunicación interna entre servicios", 403
            )

        # Validación de payload
        json_data = request.get_json()
        if not json_data or not json_data.get("message_text"):
            raise AppError("Campo 'message_text' es obligatorio", 400)

        # Simular contexto de usuario interno para compatibilidad con analyze_sentiment()
        # Esto permite reutilizar la lógica existente sin duplicar código
        g.user = {
            "uid": "internal_service_energy_ia",
            "email": "internal@smarwatt.com",
            "display_name": "Energy IA Internal Service",
        }

        logger.info(
            "Procesando análisis de sentiment interno: %s caracteres",
            len(json_data["message_text"]),
        )

        # Ejecutar lógica empresarial directa SIN decorador @token_required
        # Inicializar servicio de AI Learning
        ai_learning_service = AILearningService()

        # Realizar análisis de sentiment empresarial
        sentiment_analysis = ai_learning_service.analyze_sentiment_enterprise(
            g.user.get("uid") or "internal_service_energy_ia", 
            json_data.get("conversation_id", "internal_conversation"),
            json_data["message_text"]
        )

        # Preparar respuesta empresarial
        response_data = {
            "status": "success",
            "data": {
                "sentiment_analysis": sentiment_analysis,
                "user_id": g.user.get("uid"),
                "conversation_id": json_data.get("conversation_id", "internal_conversation"),
                "processed_message_length": len(json_data["message_text"]),
                "analysis_timestamp": datetime.now(timezone.utc).isoformat(),
            },
            "service": "expert_bot_api",
            "endpoint": "internal_sentiment_analysis"
        }

        logger.info(f"✅ Sentiment analysis interno completado exitosamente")
        return jsonify(response_data), 200

    except AppError:
        raise
    except Exception as e:
        logger.error("Error crítico en sentiment analysis interno: %s", str(e))
        raise AppError(f"Error interno del servicio: {str(e)}", 500) from e
