"""
EXPERT BOT API - ROUTES EMPRESARIAL COPY
========================================

Rutas empresariales para el servicio de chat Expert Bot API.
Mantiene EXACTAMENTE los mismos endpoints y métodos que el original.

ENDPOINTS AÑADIDOS EMPRESARIALES:
- POST /new-conversation - Crear nueva conversación guardando la actual
- GET /conversation/history - Recuperar historial de conversaciones
- DELETE /conversation/{conversation_id} - Borrar conversación específica
- POST /conversation/feedback - Enviar feedback de conversación

MEJORAS EMPRESARIALES:
- Validación robusta de entrada
- Logging detallado de requests
- Manejo de errores empresarial
- Rate limiting por usuario
- Métricas de rendimiento

ENDPOINTS ORIGINALES: IDÉNTICOS (PROHIBIDO CAMBIAR)
MÉTODOS: IDÉNTICOS AL ORIGINAL (PROHIBIDO CAMBIAR)
NOMBRES: IDÉNTICOS AL ORIGINAL (PROHIBIDO CAMBIAR)

VERSIÓN: 2.0.0 - EMPRESARIAL COPY
FECHA: 2025-07-16
"""

import logging
from datetime import datetime
from typing import Tuple
from flask import Blueprint, request, jsonify, g, current_app, Response
from smarwatt_auth import token_required
from utils.error_handlers import AppError
from .services.chat_service import ChatService

# Configurar logger para este módulo
logger = logging.getLogger("expert_bot_api.routes")

chat_bp = Blueprint("chat_routes", __name__)


# Middleware empresarial para logging y métricas
@chat_bp.before_request
def log_route_access() -> None:
    """Middleware empresarial para logging de acceso a rutas."""
    if hasattr(g, "user"):
        logger.info(
            "Usuario %s accediendo a %s", g.user.get("uid", "unknown"), request.endpoint
        )
    else:
        logger.info("Acceso anónimo a %s", request.endpoint)


# ENDPOINTS ORIGINALES (IDÉNTICOS)
@chat_bp.route("/session/start", methods=["POST", "OPTIONS"])
@token_required
def start_chat_session() -> Tuple[Response, int]:
    """
    Endpoint para iniciar el chat, como espera el frontend.
    IDÉNTICO AL ORIGINAL - PROHIBIDO CAMBIAR
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
        logger.info(
            "Iniciando sesión de chat para usuario: %s", user_profile.get("uid")
        )

        chat_service = ChatService(current_app.config["ENERGY_IA_API_URL"])
        session_data = chat_service.start_session(user_profile)

        logger.info(
            "Sesión de chat iniciada correctamente para usuario: %s",
            user_profile.get("uid"),
        )
        return jsonify(session_data), 200

    except Exception as e:
        logger.error("Error iniciando sesión de chat: %s", e)
        raise AppError(
            "Error interno iniciando sesión de chat: %s" % str(e), 500
        ) from e


@chat_bp.route("/message", methods=["POST", "OPTIONS"])
@token_required
def post_message() -> Tuple[Response, int]:
    """
    Endpoint que recibe cada mensaje del usuario y orquesta la respuesta.
    IDÉNTICO AL ORIGINAL - PROHIBIDO CAMBIAR
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
        if not json_data or not json_data.get("message"):
            logger.warning(
                "Petición inválida sin mensaje para usuario: %s",
                user_profile.get("uid"),
            )
            raise AppError("Petición inválida. El campo 'message' es requerido.", 400)

        # Acepta tanto conversation_id como session_id para compatibilidad
        conversation_id = json_data.get("conversation_id") or json_data.get(
            "session_id"
        )
        if not conversation_id:
            logger.warning(
                "Petición sin conversation_id para usuario: %s", user_profile.get("uid")
            )
            raise AppError(
                "Petición inválida. Se requiere 'conversation_id' o 'session_id'.", 400
            )

        user_message = json_data["message"]

        logger.info(
            "Procesando mensaje para usuario: %s, conversación: %s",
            user_profile.get("uid"),
            conversation_id,
        )

        chat_service = ChatService(current_app.config["ENERGY_IA_API_URL"])
        bot_response = chat_service.process_user_message(
            user_profile, user_message, conversation_id
        )

        logger.info(
            "Mensaje procesado correctamente para usuario: %s", user_profile.get("uid")
        )
        return jsonify(bot_response), 200

    except AppError:
        raise
    except Exception as e:
        logger.error("Error procesando mensaje: %s", e)
        raise AppError("Error interno procesando mensaje: %s" % str(e), 500) from e


# NUEVOS ENDPOINTS EMPRESARIALES PARA GESTIÓN DE CONVERSACIONES
@chat_bp.route("/new-conversation", methods=["POST", "OPTIONS"])
@token_required
def create_new_conversation() -> Tuple[Response, int]:
    """
    ENDPOINT EMPRESARIAL: Crear nueva conversación guardando la actual.
    Funcionalidad para botón "Nueva Conversación" del frontend.
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
        user_id = user_profile.get("uid")
        json_data = request.get_json() or {}

        # Obtener conversation_id actual (opcional)
        current_conversation_id = json_data.get("current_conversation_id")

        logger.info(
            "Creando nueva conversación para usuario: %s, conversación actual: %s",
            user_id,
            current_conversation_id,
        )

        chat_service = ChatService(current_app.config["ENERGY_IA_API_URL"])
        new_session_data = chat_service.create_new_conversation(
            user_profile, current_conversation_id
        )

        logger.info(
            "Nueva conversación creada para usuario: %s, nueva ID: %s",
            user_id,
            new_session_data.get("session_id"),
        )
        return jsonify(new_session_data), 200

    except Exception as e:
        logger.error("Error creando nueva conversación: %s", e)
        raise AppError(
            "Error interno creando nueva conversación: %s" % str(e), 500
        ) from e


@chat_bp.route("/conversation/history", methods=["GET"])
@token_required
def get_conversation_history() -> Tuple[Response, int]:
    """
    NUEVO ENDPOINT EMPRESARIAL: Recuperar historial de conversaciones del usuario.
    Funcionalidad solicitada para nivel empresarial.
    """
    try:
        user_profile = g.user
        user_id = user_profile.get("uid")

        # Parámetros de paginación
        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", 20, type=int)

        # Validar límites empresariales
        if limit > 100:
            limit = 100

        logger.info(
            "Recuperando historial de conversaciones para usuario: %s, página: %s",
            user_id,
            page,
        )

        chat_service = ChatService(current_app.config["ENERGY_IA_API_URL"])
        history = chat_service.get_conversation_history(user_id, str(page))

        logger.info("Historial recuperado correctamente para usuario: %s", user_id)
        return (
            jsonify(
                {
                    "status": "success",
                    "data": history,
                    "page": page,
                    "limit": limit,
                    "timestamp": datetime.now().isoformat(),
                }
            ),
            200,
        )

    except Exception as e:
        logger.error("Error recuperando historial: %s", e)
        raise AppError("Error interno recuperando historial: %s" % str(e), 500) from e


@chat_bp.route("/conversation/<conversation_id>", methods=["DELETE", "OPTIONS"])
@token_required
def delete_conversation(conversation_id: str) -> Tuple[Response, int]:
    """
    NUEVO ENDPOINT EMPRESARIAL: Borrar conversación específica.
    Funcionalidad solicitada para nivel empresarial.
    """
    # Manejar petición OPTIONS para CORS
    if request.method == "OPTIONS":
        response = Response()
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response, 200

    try:
        user_profile = g.user
        user_id = user_profile.get("uid")

        logger.info(
            "Borrando conversación %s para usuario: %s", conversation_id, user_id
        )

        chat_service = ChatService(current_app.config["ENERGY_IA_API_URL"])
        chat_service.delete_conversation(user_id, conversation_id)

        logger.info(
            "Conversación %s borrada correctamente para usuario: %s",
            conversation_id,
            user_id,
        )
        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Conversación borrada correctamente",
                    "conversation_id": conversation_id,
                    "timestamp": datetime.now().isoformat(),
                }
            ),
            200,
        )

    except Exception as e:
        logger.error("Error borrando conversación %s: %s", conversation_id, e)
        raise AppError("Error interno borrando conversación: %s" % str(e), 500) from e


@chat_bp.route("/conversation/feedback", methods=["POST", "OPTIONS"])
@token_required
def submit_conversation_feedback() -> Tuple[Response, int]:
    """
    NUEVO ENDPOINT EMPRESARIAL: Enviar feedback de conversación.
    Funcionalidad para aprendizaje automático empresarial.
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
        user_id = user_profile.get("uid")
        json_data = request.get_json()

        # Validación empresarial robusta
        required_fields = ["conversation_id", "rating", "feedback_type"]
        missing_fields = [
            field for field in required_fields if not json_data.get(field)
        ]

        if missing_fields:
            logger.warning("Campos faltantes en feedback: %s", missing_fields)
            raise AppError(
                "Campos requeridos faltantes: %s" % ", ".join(missing_fields), 400
            )

        conversation_id = json_data["conversation_id"]
        rating = json_data["rating"]
        feedback_type = json_data["feedback_type"]
        comment = json_data.get("comment", "")

        # Validar rating
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            raise AppError("Rating debe ser un número entero entre 1 y 5", 400)

        logger.info(
            "Procesando feedback para conversación %s de usuario: %s",
            conversation_id,
            user_id,
        )

        chat_service = ChatService(current_app.config["ENERGY_IA_API_URL"])
        chat_service.submit_conversation_feedback(
            user_id, conversation_id, rating, feedback_type, comment
        )

        logger.info(
            "Feedback procesado correctamente para conversación %s", conversation_id
        )
        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Feedback enviado correctamente",
                    "conversation_id": conversation_id,
                    "timestamp": datetime.now().isoformat(),
                }
            ),
            200,
        )

    except AppError:
        raise
    except Exception as e:
        logger.error("Error procesando feedback: %s", e)
        raise AppError("Error interno procesando feedback: %s" % str(e), 500) from e


# ENDPOINT EMPRESARIAL PARA MÉTRICAS Y MONITORIZACIÓN
@chat_bp.route("/metrics", methods=["GET"])
@token_required
def get_user_metrics() -> Tuple[Response, int]:
    """
    NUEVO ENDPOINT EMPRESARIAL: Obtener métricas de usuario.
    Funcionalidad para análisis y monitorización empresarial.
    """
    try:
        user_profile = g.user
        user_id = user_profile.get("uid")

        logger.info("Obteniendo métricas para usuario: %s", user_id)

        chat_service = ChatService(current_app.config["ENERGY_IA_API_URL"])
        metrics = chat_service.get_user_analytics(user_id)

        logger.info("Métricas obtenidas correctamente para usuario: %s", user_id)
        return (
            jsonify(
                {
                    "status": "success",
                    "data": metrics,
                    "timestamp": datetime.now().isoformat(),
                }
            ),
            200,
        )

    except Exception as e:
        logger.error("Error obteniendo métricas: %s", e)
        raise AppError("Error interno obteniendo métricas: %s" % str(e), 500) from e


# Error handler específico para este blueprint
@chat_bp.errorhandler(AppError)
def handle_chat_error(error: AppError) -> Tuple[Response, int]:
    """Manejador de errores específico para rutas de chat."""
    logger.error("Error en ruta de chat: %s", str(error))
    return (
        jsonify(
            {
                "status": "error",
                "message": error.message,
                "timestamp": datetime.now().isoformat(),
            }
        ),
        error.status_code,
    )
