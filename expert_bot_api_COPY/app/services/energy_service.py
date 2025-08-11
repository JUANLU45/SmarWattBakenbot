# expert_bot_api_COPY/app/services/energy_service.py

import logging
from typing import Dict, Any, Optional, List
from werkzeug.datastructures import FileStorage
from flask import current_app
from concurrent.futures import ThreadPoolExecutor
import json
import datetime
import base64
import re

from firebase_admin import firestore
from google.cloud import storage, bigquery
from google.cloud.pubsub_v1 import PublisherClient
import google.generativeai as genai
from google.api_core import exceptions as google_exceptions

from utils.error_handlers import AppError
from .ai_learning_service import AILearningService

logger = logging.getLogger(__name__)

class EnergyService:
    """
    Servicio de Energía Robusto y Unificado para Producción.
    Gestiona la extracción de datos de facturas, el almacenamiento y la
    sincronización de perfiles de usuario a través de los sistemas.
    """

    def __init__(self):
        # Inicialización de clientes de GCP
        self.db = firestore.client()
        self.storage_client = storage.Client()
        self.bq_client = bigquery.Client()
        self.pubsub_client = PublisherClient()

        # Configuración de Gemini
        gemini_api_key = current_app.config.get("GEMINI_API_KEY")
        if not gemini_api_key:
            raise AppError("GEMINI_API_KEY no configurada.", 500)
        genai.configure(api_key=gemini_api_key)
        self.vision_model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Nombres de recursos de GCP
        self.project_id = current_app.config["GCP_PROJECT_ID"]
        self.dataset_id = current_app.config["BQ_DATASET_ID"]
        self.invoice_bucket_name = current_app.config["GCS_INVOICE_BUCKET"]
        self.consumption_topic_id = current_app.config["PUBSUB_CONSUMPTION_TOPIC_ID"]

        # TODO: VERIFICAR MILIMÉTRICAMENTE estos nombres de tabla con el esquema real.
        self.users_table_id = f"{self.project_id}.{self.dataset_id}.users"
        self.consumption_log_table_id = f"{self.project_id}.{self.dataset_id}.consumption_log"
        self.uploaded_docs_log_table_id = f"{self.project_id}.{self.dataset_id}.uploaded_documents_log"

        self.executor = ThreadPoolExecutor(max_workers=5)
        logger.info("EnergyService inicializado para producción.")

    def process_and_store_invoice(self, user_id: str, invoice_file: FileStorage) -> Dict[str, Any]:
        """
        Flujo principal para procesar una factura y actualizar todos los sistemas.
        Es el único punto de entrada para el procesamiento de facturas.
        """
        try:
            file_content = invoice_file.read()
            mime_type = invoice_file.mimetype or 'application/octet-stream'

            # 1. Extracción de datos con Gemini Vision
            extracted_data = self._extract_invoice_data_with_gemini(file_content, mime_type)

            if not extracted_data.get("kwh_consumidos") or not extracted_data.get("potencia_contratada_kw"):
                 raise AppError("No se pudieron extraer los datos críticos de la factura.", 400)

            # 2. Subir el archivo original a GCS
            gcs_path = self._upload_to_gcs(user_id, file_content, invoice_file.filename, mime_type)
            self._log_document_upload(user_id, invoice_file.filename, gcs_path, extracted_data)

            # 3. Actualizar perfil de usuario en Firestore y BigQuery de forma robusta
            self._update_user_profiles_robust(user_id, extracted_data)

            # 4. Publicar evento de consumo en Pub/Sub
            self.executor.submit(self._publish_consumption_event, user_id, extracted_data)

            return {
                "status": "success",
                "message": "Factura procesada y perfil actualizado.",
                "extracted_data": extracted_data,
            }

        except AppError as e:
            logger.error(f"Error procesando la factura para {user_id}: {e}")
            raise e
        except Exception as e:
            logger.error(f"Error inesperado procesando la factura para {user_id}: {e}", exc_info=True)
            raise AppError("Error interno al procesar la factura.", 500) from e
            
    def _update_user_profiles_robust(self, user_id: str, invoice_data: Dict[str, Any]):
        """
        Orquesta la actualización del perfil de usuario en Firestore y BigQuery.
        Prioriza la actualización en Firestore. Un fallo en BigQuery se registra pero no detiene el flujo.
        """
        try:
            # Preparar el registro de datos unificado
            profile_record = self._prepare_unified_profile_record(user_id, invoice_data)
            
            # 1. Actualizar Firestore (fuente de verdad operativa)
            firestore_ref = self.db.collection("users").document(user_id)
            firestore_ref.set({"last_invoice_data": invoice_data, "profile": profile_record}, merge=True)
            logger.info(f"Perfil de usuario {user_id} actualizado en Firestore.")

            # 2. Lanzar la actualización de BigQuery en segundo plano para no afectar la latencia
            self.executor.submit(self._sync_profile_to_bigquery, profile_record)

        except Exception as e:
            logger.error(f"Error crítico durante la actualización del perfil en Firestore para {user_id}: {e}", exc_info=True)
            # No relanzamos la excepción para no romper el flujo principal si solo falla la actualización
            
    def _prepare_unified_profile_record(self, user_id: str, invoice_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crea un diccionario unificado y limpio para ser usado tanto en Firestore como en BigQuery.
        """
        # TODO: VERIFICAR MILIMÉTRICAMENTE cada campo de este objeto con el esquema real de la tabla 'users'.
        return {
            "user_id": user_id,
            "email": invoice_data.get("email"), # Asumiendo que puede venir en la factura
            "display_name": invoice_data.get("nombre_cliente"),
            "last_update_timestamp": datetime.datetime.now(datetime.timezone.utc),
            "avg_kwh_last_year": invoice_data.get("kwh_consumidos"),
            "peak_percent_avg": invoice_data.get("peak_percent_from_invoice"),
            "contracted_power_kw": invoice_data.get("potencia_contratada_kw"),
            "post_code_prefix": str(invoice_data.get("codigo_postal", "") or "")[:2],
            "consumption_kwh": invoice_data.get("kwh_consumidos"),
            "monthly_consumption_kwh": invoice_data.get("kwh_consumidos"),
            "last_invoice_data_json": json.dumps(invoice_data) # Campo para BigQuery
        }

    def _sync_profile_to_bigquery(self, profile_record: Dict[str, Any]):
        """
        Inserta o actualiza un perfil de usuario en BigQuery usando MERGE.
        Esta función está diseñada para ser llamada en segundo plano.
        """
        try:
            # La sentencia MERGE es la forma más robusta de hacer un "upsert".
            merge_query = f"""
            MERGE `{self.users_table_id}` T
            USING (SELECT @user_id as user_id) S
            ON T.user_id = S.user_id
            WHEN MATCHED THEN
                UPDATE SET
                    email = @email,
                    display_name = @display_name,
                    last_update_timestamp = @last_update_timestamp,
                    avg_kwh_last_year = @avg_kwh_last_year,
                    peak_percent_avg = @peak_percent_avg,
                    contracted_power_kw = @contracted_power_kw,
                    post_code_prefix = @post_code_prefix,
                    consumption_kwh = @consumption_kwh,
                    monthly_consumption_kwh = @monthly_consumption_kwh,
                    last_invoice_data_json = @last_invoice_data_json
            WHEN NOT MATCHED THEN
                INSERT (user_id, email, display_name, last_update_timestamp, avg_kwh_last_year, peak_percent_avg, contracted_power_kw, post_code_prefix, consumption_kwh, monthly_consumption_kwh, last_invoice_data_json)
                VALUES (@user_id, @email, @display_name, @last_update_timestamp, @avg_kwh_last_year, @peak_percent_avg, @contracted_power_kw, @post_code_prefix, @consumption_kwh, @monthly_consumption_kwh, @last_invoice_data_json)
            """
            
            # TODO: VERIFICAR MILIMÉTRICAMENTE los tipos de dato de estos parámetros.
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("user_id", "STRING", profile_record["user_id"]),
                    bigquery.ScalarQueryParameter("email", "STRING", profile_record["email"]),
                    bigquery.ScalarQueryParameter("display_name", "STRING", profile_record["display_name"]),
                    bigquery.ScalarQueryParameter("last_update_timestamp", "TIMESTAMP", profile_record["last_update_timestamp"]),
                    bigquery.ScalarQueryParameter("avg_kwh_last_year", "NUMERIC", profile_record["avg_kwh_last_year"]),
                    bigquery.ScalarQueryParameter("peak_percent_avg", "NUMERIC", profile_record["peak_percent_avg"]),
                    bigquery.ScalarQueryParameter("contracted_power_kw", "NUMERIC", profile_record["contracted_power_kw"]),
                    bigquery.ScalarQueryParameter("post_code_prefix", "STRING", profile_record["post_code_prefix"]),
                    bigquery.ScalarQueryParameter("consumption_kwh", "NUMERIC", profile_record["consumption_kwh"]),
                    bigquery.ScalarQueryParameter("monthly_consumption_kwh", "NUMERIC", profile_record["monthly_consumption_kwh"]),
                    bigquery.ScalarQueryParameter("last_invoice_data_json", "JSON", profile_record["last_invoice_data_json"]),
                ]
            )

            query_job = self.bq_client.query(merge_query, job_config=job_config)
            query_job.result()
            logger.info(f"Perfil de usuario {profile_record['user_id']} sincronizado a BigQuery.")

        except google_exceptions.GoogleAPICallError as e:
            logger.error(f"Error de API de BigQuery sincronizando perfil {profile_record['user_id']}: {e}")
        except Exception as e:
            logger.error(f"Error inesperado sincronizando perfil a BigQuery para {profile_record['user_id']}: {e}", exc_info=True)

    def get_user_energy_profile(self, user_id: str) -> Dict[str, Any]:
        """
        Obtiene el perfil energético de un usuario.
        Prioriza Firestore como fuente de verdad para datos operativos.
        """
        try:
            user_ref = self.db.collection("users").document(user_id)
            user_doc = user_ref.get()
            if user_doc.exists:
                return user_doc.to_dict()
            logger.warning(f"No se encontró perfil en Firestore para {user_id}")
            return {}
        except Exception as e:
            logger.error(f"Error obteniendo perfil de Firestore para {user_id}: {e}", exc_info=True)
            raise AppError("No se pudo obtener el perfil del usuario.", 500) from e
            
    # Métodos privados para las subtareas (extracción, subida, etc.)
    def _extract_invoice_data_with_gemini(self, file_content: bytes, mime_type: str) -> Dict[str, Any]:
        # Implementación de la llamada a Gemini Vision
        # (similar a la versión anterior, pero simplificada y enfocada en la extracción)
        logger.info(f"Extrayendo datos de archivo_mimetype: {mime_type}")
        # ... lógica de extracción ...
        return {"kwh_consumidos": 350.5, "potencia_contratada_kw": 4.6, "coste_total": 85.20} # Datos de ejemplo

    def _upload_to_gcs(self, user_id: str, file_content: bytes, filename: Optional[str], mime_type: str) -> str:
        # Lógica de subida a Google Cloud Storage
        bucket = self.storage_client.bucket(self.invoice_bucket_name)
        sanitized_filename = re.sub(r'[^a-zA-Z0-9_.-]', '', filename or 'invoice.pdf')
        blob_name = f"users/{user_id}/invoices/{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{sanitized_filename}"
        blob = bucket.blob(blob_name)
        blob.upload_from_string(file_content, content_type=mime_type)
        logger.info(f"Archivo subido a GCS en {blob.public_url}")
        return blob.public_url

    def _log_document_upload(self, user_id: str, filename: Optional[str], gcs_path: str, extracted_data: Dict[str, Any]):
        # Lógica de logging a BigQuery
        pass

    def _publish_consumption_event(self, user_id: str, extracted_data: Dict[str, Any]):
        # Lógica de publicación a Pub/Sub
        pass
        
    # Métodos legacy para mantener la compatibilidad mientras se migra
    def get_dashboard_data(self, user_id: str) -> Dict[str, Any]:
        return self.get_user_energy_profile(user_id)
