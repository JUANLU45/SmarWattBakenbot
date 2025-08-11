"""
EXPERT BOT API - ROUTES EMPRESARIAL COPY
========================================

Rutas empresariales para el servicio de chat Expert Bot API.
Mantiene EXACTAMENTE los mismos endpoints y métodos que el original.
"""

import logging
from datetime import datetime
from typing import Tuple
from flask import Blueprint, request, jsonify, g, current_app, Response
from smarwatt_auth import token_required
from utils.error_handlers import AppError
from .services.chat_service import ChatService
from .services.data_sync_service import DataSyncService
from concurrent.futures import ThreadPoolExecutor

# Configurar logger para este módulo
logger = logging.getLogger("expert_bot_api.routes")

chat_bp = Blueprint("chat_routes", __name__)
executor = ThreadPoolExecutor(max_workers=2)


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
    Endpoint para iniciar el chat.
    Ahora incluye la sincronización de datos asíncrona a BigQuery.
    """
    if request.method == "OPTIONS":
        # Manejo de CORS pre-flight
        return Response(status=200, headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
        })

    try:
        user_profile = g.user
        user_id = user_profile.get("uid")
        logger.info("Iniciando sesión de chat para usuario: %s", user_id)

        # 🚀 SINCRONIZACIÓN ASÍNCRONA 🚀
        if user_id:
            try:
                data_sync_service = DataSyncService()
                executor.submit(data_sync_service.sync_user_profile_to_bigquery, user_id)
                logger.info(f"Tarea de sincronización iniciada para el usuario {user_id}.")
            except Exception as sync_e:
                logger.error(f"Error al iniciar la tarea de sincronización para {user_id}: {sync_e}")

        chat_service = ChatService(current_app.config["ENERGY_IA_API_URL"])
        session_data = chat_service.start_session(user_profile)

        logger.info("Sesión de chat iniciada correctamente para usuario: %s", user_id)
        return jsonify(session_data), 200

    except Exception as e:
        logger.error("Error iniciando sesión de chat: %s", e, exc_info=True)
        raise AppError(f"Error interno iniciando sesión de chat: {str(e)}", 500) from e


@chat_bp.route("/message", methods=["POST", "OPTIONS"])
@token_required
def post_message() -> Tuple[Response, int]:
    """
    Endpoint que recibe cada mensaje del usuario y orquesta la respuesta.
    """
    if request.method == "OPTIONS":
        return Response(status=200, headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
        })

    try:
        user_profile = g.user
        json_data = request.get_json()

        if not json_data or not json_data.get("message"):
            raise AppError("El campo 'message' es requerido.", 400)

        conversation_id = json_data.get("conversation_id") or json_data.get("session_id")
        if not conversation_id:
            raise AppError("Se requiere 'conversation_id' o 'session_id'.", 400)

        user_message = json_data["message"]
        
        chat_service = ChatService(current_app.config["ENERGY_IA_API_URL"])
        bot_response = chat_service.process_user_message(user_profile, user_message, conversation_id)

        return jsonify(bot_response), 200

    except AppError as e:
        raise e
    except Exception as e:
        logger.error("Error procesando mensaje: %s", e, exc_info=True)
        raise AppError(f"Error interno procesando mensaje: {str(e)}", 500) from e

# ... (El resto de los endpoints permanecen sin cambios)
