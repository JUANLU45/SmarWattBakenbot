# expert_bot_api_COPY/app/services/ai_learning_service.py
# 🏢 SERVICIO DE ORQUESTACIÓN DE APRENDIZAJE AUTOMÁTICO EMPRESARIAL

import logging
import requests
import json
import uuid
from datetime import datetime, timezone
from typing import Dict, Any
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
        Orquesta el análisis de sentimiento llamando al microservicio de IA
        y guarda el resultado en BigQuery para futuro aprendizaje.
        """
        if not all([user_id, conversation_id, message_text]):
            raise AppError("Faltan datos para el análisis de sentimiento.", 400)

        try:
            sentiment_endpoint = f"{self.energy_ia_api_url}/api/v1/analysis/sentiment"
            payload = {"user_id": user_id, "conversation_id": conversation_id, "message_text": message_text}
            headers = {"Content-Type": "application/json"} # TODO: Implementar un token seguro de servicio a servicio.
            
            response = requests.post(sentiment_endpoint, json=payload, headers=headers, timeout=15)
            response.raise_for_status()
            
            analysis_data = response.json().get("sentiment_analysis")
            if not analysis_data:
                raise AppError("Respuesta inválida del servicio de IA.", 500)

            self._log_sentiment_to_bigquery(user_id, conversation_id, message_text, analysis_data)
            return analysis_data

        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error de comunicación con energy_ia_api: {e}")
            raise AppError("El servicio de análisis no está disponible.", 503)
        except Exception as e:
            logger.error(f"❌ Error inesperado en análisis de sentimiento: {e}")
            raise AppError("Error interno al procesar el sentimiento.", 500)

    def _log_sentiment_to_bigquery(self, user_id: str, conversation_id: str, message_text: str, analysis_data: Dict[str, Any]):
        """Guarda el resultado del análisis en la tabla 'ai_sentiment_analysis'."""
        try:
            # La estructura de este registro ha sido verificada contra el esquema real de BigQuery.
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
        except Exception as e:
            logger.error(f"❌ Error inesperado al guardar el análisis de sentimiento: {e}")
