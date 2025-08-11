# energy_ia_api_COPY/app/chatbot_routes.py
# 🏢 CHATBOT EMPRESARIAL UNIFICADO - COMUNICACIÓN SEGURA Y ROBUSTA

import logging
from flask import Blueprint, request, jsonify, g
from smarwatt_auth import token_required
from utils.error_handlers import AppError
from app.services.generative_chat_service import get_enterprise_chat_service
from energy_ia_api_COPY.utils.security import internal_auth_required

logger = logging.getLogger(__name__)
chatbot_bp = Blueprint("chatbot_routes", __name__)

@chatbot_bp.route("/message", methods=["POST"])
@internal_auth_required # 🔐 Endpoint protegido para llamadas internas
def send_chat_message():
    """
    Endpoint principal para chat, ahora protegido para ser llamado únicamente
    por el microservicio expert_bot_api de forma segura.
    """
    try:
        json_data = request.get_json()
        if not json_data or "message" not in json_data:
            raise AppError("Petición inválida. Se requiere 'message'.", 400)

        user_message = json_data["message"]
        chat_history = json_data.get("history", [])
        user_context = json_data.get("user_profile", {}) # El perfil ahora viene en el payload

        service = get_enterprise_chat_service()
        result = service.send_message(
            chat_session=service.start_new_chat(),
            user_message=user_message,
            user_context=user_context
        )
        
        return jsonify(result), 200

    except AppError as e:
        logger.error(f"❌ Error en chat: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), e.status_code
    except Exception as e:
        logger.error(f"❌ Error inesperado en chat: {str(e)}", exc_info=True)
        return jsonify({"status": "error", "message": "Error interno del servicio de chat."}), 500
