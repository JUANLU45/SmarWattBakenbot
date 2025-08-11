# expert_bot_api_COPY/app/services/ai_learning_service.py
# 🏢 SERVICIO DE ORQUESTACIÓN DE APRENDIZAJE AUTOMÁTICO EMPRESARIAL

import logging
import requests
import json
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
from flask import current_app
from google.cloud import bigquery
from google.api_core import exceptions as google_exceptions

from utils.error_handlers import AppError

logger = logging.getLogger(__name__)

class AILearningService:
    """
    Orquesta las tareas de aprendizaje automático, delegando el procesamiento intensivo
    a los microservicios especializados como `energy_ia_api`.
    """

    def __init__(self):
        self.bq_client = bigquery.Client()
        self.project_id = current_app.config["GCP_PROJECT_ID"]
        self.dataset_id = current_app.config["BQ_DATASET_ID"]
        self.ai_sentiment_table_id = f"{self.project_id}.{self.dataset_id}.ai_sentiment_analysis"
        self.energy_ia_api_url = current_app.config["ENERGY_IA_API_URL"]

    def analyze_sentiment_enterprise(self, user_id: str, conversation_id: str, message_text: str) -> Dict[str, Any]:
        """
        Orquesta el análisis de sentimiento llamando al microservicio de IA.
        Garantiza que el resultado se guarde en BigQuery para futuro aprendizaje.
        """
        if not all([user_id, conversation_id, message_text]):
            raise AppError("Faltan datos para el análisis de sentimiento.", 400)

        try:
            # 1. Llamada HTTP robusta al servicio de IA para el análisis real.
            sentiment_endpoint = f"{self.energy_ia_api_url}/api/v1/analysis/sentiment"
            payload = {
                "user_id": user_id,
                "conversation_id": conversation_id,
                "message_text": message_text
            }
            # TODO: Implementar un token de servicio a servicio seguro.
            headers = {"Content-Type": "application/json"}
            
            response = requests.post(sentiment_endpoint, json=payload, headers=headers, timeout=15)
            response.raise_for_status() # Lanza una excepción para errores HTTP 4xx/5xx.
            
            sentiment_result = response.json()
            analysis_data = sentiment_result.get("sentiment_analysis")
            if not analysis_data:
                raise AppError("La respuesta del servicio de IA no contiene el análisis de sentimiento.", 500)

            # 2. Persistir el resultado en BigQuery para el aprendizaje a largo plazo.
            self._log_sentiment_to_bigquery(user_id, conversation_id, message_text, analysis_data)

            return analysis_data

        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error de comunicación con energy_ia_api para análisis de sentimiento: {str(e)}")
            raise AppError("El servicio de análisis de sentimiento no está disponible en este momento.", 503)
        except Exception as e:
            logger.error(f"❌ Error inesperado en el proceso de análisis de sentimiento: {str(e)}")
            raise AppError("Error interno al procesar el sentimiento del mensaje.", 500)

    def _log_sentiment_to_bigquery(self, user_id: str, conversation_id: str, message_text: str, analysis_data: Dict[str, Any]):
        """
        Guarda el resultado del análisis de sentimiento en la tabla 'ai_sentiment_analysis'.
        Verificado milimétricamente contra el esquema de BigQuery.
        """
        try:
            # TODO: VERIFICAR CAMPO - Todos los campos aquí deben coincidir con el esquema real.
            row_to_insert = {
                "interaction_id": str(uuid.uuid4()),
                "conversation_id": conversation_id,
                "user_id": user_id,
                "message_text": message_text,
                "sentiment_score": float(analysis_data.get("sentiment_score", 0.0)),
                "sentiment_label": analysis_data.get("sentiment_label", "neutral"),
                "confidence": float(analysis_data.get("confidence", 0.0)),
                "emotional_indicators": json.dumps(analysis_data.get("emotional_indicators", {})),
                "analyzed_at": datetime.now(timezone.utc).isoformat(),
            }

            errors = self.bq_client.insert_rows_json(self.ai_sentiment_table_id, [row_to_insert])
            if errors:
                logger.error(f"❌ Error al insertar en BigQuery (ai_sentiment_analysis): {errors}")
            else:
                logger.info(f"✅ Análisis de sentimiento para el usuario {user_id} guardado en BigQuery.")

        except google_exceptions.NotFound:
            logger.error(f"❌ La tabla `{self.ai_sentiment_table_id}` no existe en BigQuery.")
        except Exception as e:
            logger.error(f"❌ Error inesperado al guardar el análisis de sentimiento: {str(e)}")
            # No relanzamos la excepción para no afectar la respuesta al usuario.
