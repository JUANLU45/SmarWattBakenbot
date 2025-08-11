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
        return Response(status=200, headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
        })

    try:
        user_profile = g.user
        user_id = user_profile.get("uid")
        logger.info("Iniciando sesión de chat para usuario: %s", user_id)

        if user_id:
            try:
                data_sync_service = DataSyncService()
                executor.submit(data_sync_service.sync_user_profile_to_bigquery, user_id)
                logger.info(f"Tarea de sincronización iniciada para el usuario {user_id}.")
            except Exception as sync_e:
                logger.error(f"Error al iniciar la tarea de sincronización para {user_id}: {sync_e}")

        chat_service = ChatService(current_app.config["ENERGY_IA_API_URL"])
        session_data = chat_service.start_session(user_profile)
        return jsonify(session_data), 200
    except Exception as e:
        logger.error("Error iniciando sesión de chat: %s", e, exc_info=True)
        raise AppError(f"Error interno iniciando sesión de chat: {str(e)}", 500) from e


@chat_bp.route("/message", methods=["POST", "OPTIONS"])
@token_required
def post_message() -> Tuple[Response, int]:
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
        
        chat_service = ChatService(current_app.config["ENERGY_IA_API_URL"])
        bot_response = chat_service.process_user_message(user_profile, json_data["message"], conversation_id)
        return jsonify(bot_response), 200
    except AppError as e:
        raise e
    except Exception as e:
        logger.error("Error procesando mensaje: %s", e, exc_info=True)
        raise AppError(f"Error interno procesando mensaje: {str(e)}", 500) from e


@chat_bp.route("/conversation/<conversation_id>", methods=["DELETE", "OPTIONS"])
@token_required
def delete_conversation(conversation_id: str) -> Tuple[Response, int]:
    if request.method == "OPTIONS":
        return Response(status=200, headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
        })
    try:
        user_id = g.user["uid"]
        logger.info("Solicitud para borrar conversación %s para usuario: %s", conversation_id, user_id)
        
        chat_service = ChatService(current_app.config["ENERGY_IA_API_URL"])
        chat_service.delete_conversation(user_id, conversation_id)

        logger.info("Conversación %s borrada correctamente para usuario: %s", conversation_id, user_id)
        # Respuesta de éxito clara y consistente según el plan de mejora.
        return jsonify({"status": "success", "message": "La conversación ha sido eliminada correctamente."}), 200
    except Exception as e:
        logger.error("Error borrando conversación %s: %s", conversation_id, e)
        raise AppError("Error interno al borrar la conversación.", 500) from e
