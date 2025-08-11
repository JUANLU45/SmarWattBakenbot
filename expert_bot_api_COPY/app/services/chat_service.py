# expert_bot_api_COPY/app/services/chat_service.py
# 🏢 SERVICIO DE CHAT EMPRESARIAL - LÓGICA DE ORQUESTACIÓN SEGURA Y ROBUSTA

import logging
import uuid
import requests
from typing import Dict, Any, Optional
from flask import current_app
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor

from google.cloud import bigquery
from utils.error_handlers import AppError
from .ai_learning_service import AILearningService
from expert_bot_api_COPY.utils.auth_client import get_service_to_service_token

logger = logging.getLogger(__name__)

class ChatService:
    """
    Servicio de Chat para orquestar la conversación, delegando tareas de IA de forma segura
    y gestionando el logging a BigQuery.
    """

    def __init__(self, energy_ia_api_url: str):
        self.energy_ia_api_url = energy_ia_api_url
        self.project_id = current_app.config["GCP_PROJECT_ID"]
        self.bq_dataset_id = current_app.config["BQ_DATASET_ID"]
        self.bq_conversations_table_id = f"{self.project_id}.{self.bq_dataset_id}.{current_app.config['BQ_CONVERSATIONS_TABLE_ID']}"
        
        self.bq_client = bigquery.Client()
        self.ai_learning_service = AILearningService()
        self.executor = ThreadPoolExecutor(max_workers=5)

    def start_session(self, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Inicia una nueva sesión de chat para el usuario."""
        user_id = user_profile.get("uid")
        if not user_id:
            raise AppError("Perfil de usuario inválido, falta uid.", 400)

        session_id = str(uuid.uuid4())
        welcome_message = f"Hola {user_profile.get('name', 'usuario')}, bienvenido a SmarWatt. ¿En qué puedo ayudarte hoy?"

        self._log_conversation_turn(user_id, session_id, "system", "SESSION_START")
        return {"session_id": session_id, "welcomeMessage": welcome_message, "status": "success"}

    def process_user_message(self, user_profile: Dict[str, Any], user_message: str, conversation_id: str) -> Dict[str, Any]:
        """Procesa el mensaje del usuario y obtiene una respuesta segura del servicio de IA."""
        user_id = user_profile["uid"]
        self._log_conversation_turn(user_id, conversation_id, "user", user_message)

        try:
            self.executor.submit(self.ai_learning_service.analyze_sentiment_enterprise, user_id, conversation_id, user_message)
        except Exception as e:
            logger.error(f"Error al iniciar el análisis de sentimiento asíncrono: {e}")

        try:
            ia_endpoint = f"{self.energy_ia_api_url}/api/v1/chatbot/message"
            payload = {
                "user_id": user_id,
                "conversation_id": conversation_id,
                "message": user_message,
                "user_profile": user_profile,
            }
            
            # 🔐 OBTENCIÓN Y USO DE TOKEN DE AUTENTICACIÓN INTERNO
            auth_token = get_service_to_service_token(audience_url=self.energy_ia_api_url)
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {auth_token}"
            }
            
            response = requests.post(ia_endpoint, json=payload, headers=headers, timeout=25)
            response.raise_for_status()
            
            bot_response_data = response.json()
            bot_response_text = bot_response_data.get("response", "No he podido procesar tu solicitud.")
            self._log_conversation_turn(user_id, conversation_id, "bot", user_message, response_text=bot_response_text)
            
            return bot_response_data

        except requests.exceptions.RequestException as e:
            logger.error(f"Error de comunicación con energy_ia_api: {e}")
            raise AppError("El servicio de chatbot no está disponible en este momento.", 503)
        except Exception as e:
            logger.error(f"Error inesperado al procesar el mensaje: {e}", exc_info=True)
            raise AppError("Error interno al procesar tu mensaje.", 500)

    def delete_conversation(self, user_id: str, conversation_id: str):
        """Marca una conversación como eliminada en BigQuery (soft delete)."""
        query = f"""
        UPDATE `{self.bq_conversations_table_id}`
        SET deleted = TRUE, deleted_at = @deleted_at
        WHERE user_id = @user_id AND conversation_id = @conversation_id
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("deleted_at", "TIMESTAMP", datetime.now(timezone.utc)),
                bigquery.ScalarQueryParameter("user_id", "STRING", user_id),
                bigquery.ScalarQueryParameter("conversation_id", "STRING", conversation_id),
            ]
        )
        try:
            query_job = self.bq_client.query(query, job_config=job_config)
            query_job.result()
            logger.info(f"Conversación {conversation_id} marcada como eliminada para el usuario {user_id}.")
        except Exception as e:
            logger.error(f"Error al marcar la conversación como eliminada: {e}")
            raise AppError("No se pudo eliminar la conversación.", 500)

    def _log_conversation_turn(self, user_id: str, conversation_id: str, sender: str, message_text: str, response_text: Optional[str] = None):
        """Registra un turno de la conversación en BigQuery."""
        try:
            row = {
                "message_id": str(uuid.uuid4()),
                "conversation_id": conversation_id,
                "user_id": user_id,
                "sender": sender,
                "message_text": message_text,
                "response_text": response_text,
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "deleted": False,
            }
            errors = self.bq_client.insert_rows_json(self.bq_conversations_table_id, [row])
            if errors:
                logger.error(f"Error al insertar en BigQuery (conversations_log): {errors}")
        except Exception as e:
            logger.error(f"Error inesperado al registrar el turno de conversación: {e}")

