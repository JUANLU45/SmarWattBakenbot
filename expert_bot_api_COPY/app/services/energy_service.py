# expert_bot_api_COPY/app/services/energy_service.py
# 🏢 SERVICIO DE ENERGÍA - LÓGICA DE PROCESAMIENTO DE DATOS PARA PRODUCCIÓN

import logging
import json
import re
import datetime
from typing import Dict, Any, Optional
from werkzeug.datastructures import FileStorage
from flask import current_app
from concurrent.futures import ThreadPoolExecutor

from firebase_admin import firestore
from google.cloud import storage, bigquery, pubsub_v1
import google.generativeai as genai

from utils.error_handlers import AppError

logger = logging.getLogger(__name__)

class EnergyService:
    """
    Gestiona la extracción de datos de facturas, el almacenamiento robusto 
    y la sincronización de perfiles de usuario a través de Firestore y BigQuery.
    """

    def __init__(self):
        self.db = firestore.client()
        self.storage_client = storage.Client()
        self.bq_client = bigquery.Client()
        self.pubsub_client = pubsub_v1.PublisherClient()

        # Configuración de Gemini
        gemini_api_key = current_app.config.get("GEMINI_API_KEY")
        if not gemini_api_key:
            raise AppError("GEMINI_API_KEY no configurada.", 500)
        genai.configure(api_key=gemini_api_key)
        self.vision_model = genai.GenerativeModel("gemini-1.5-flash")

        self.project_id = current_app.config["GCP_PROJECT_ID"]
        self.dataset_id = current_app.config["BQ_DATASET_ID"]
        self.invoice_bucket_name = current_app.config["GCS_INVOICE_BUCKET"]
        self.consumption_topic_name = f"projects/{self.project_id}/topics/{current_app.config['PUBSUB_CONSUMPTION_TOPIC_ID']}"
        self.users_table_id = f"{self.project_id}.{self.dataset_id}.user_profiles_enriched"
        self.consumption_log_table_id = f"{self.project_id}.{self.dataset_id}.consumption_log"
        self.uploaded_docs_log_table_id = f"{self.project_id}.{self.dataset_id}.uploaded_documents_log"

        self.executor = ThreadPoolExecutor(max_workers=3)
        logger.info("EnergyService inicializado para producción con Gemini Vision real.")

    def process_and_store_invoice(self, user_id: str, invoice_file: FileStorage) -> Dict[str, Any]:
        """Flujo principal para procesar una factura con IA real y actualizar todos los sistemas."""
        try:
            file_content = invoice_file.read()
            mime_type = invoice_file.mimetype or 'application/octet-stream'

            extracted_data = self._extract_invoice_data_with_gemini(file_content, mime_type)
            if extracted_data.get("error"):
                raise AppError(f"Error de IA al procesar la factura: {extracted_data['error']}", 400)
            if not extracted_data.get("kwh_consumidos") or not extracted_data.get("potencia_contratada_kw"):
                raise AppError("Datos críticos (kWh o potencia) no pudieron ser extraídos. La factura puede ser ilegible o de un formato no soportado.", 400)

            self._update_user_profiles_robust(user_id, extracted_data)
            
            self.executor.submit(self._upload_to_gcs_and_log, user_id, file_content, invoice_file.filename, mime_type)
            self.executor.submit(self._publish_consumption_event, user_id, extracted_data)

            return extracted_data
        except AppError as e:
            logger.error(f"Error procesando la factura para {user_id}: {e}")
            raise e
        except Exception as e:
            logger.error(f"Error inesperado procesando la factura para {user_id}: {e}", exc_info=True)
            raise AppError("Error interno del servidor al procesar la factura.", 500)

    def _extract_invoice_data_with_gemini(self, file_content: bytes, mime_type: str) -> Dict[str, Any]:
        """
        Llama a la IA de Gemini para extraer datos de una factura de forma robusta y espectacular.
        Esta es la implementación 100% real para producción.
        """
        logger.info(f"Iniciando extracción de datos con Gemini Vision (MIME type: {mime_type})...")
        
        prompt = """
        Eres un experto en OCR especializado en facturas de electricidad de España.
        Tu tarea es extraer los siguientes campos de la imagen y devolverlos en un formato JSON estricto.
        Si un campo no se encuentra o es ilegible, devuélvelo como null.
        Si la imagen es completamente ilegible o no es una factura, devuelve un JSON con una única clave "error".

        Campos a extraer:
        - kwh_consumidos (número)
        - potencia_contratada_kw (número)
        - coste_total (número)
        - peak_percent_from_invoice (número, porcentaje de consumo en punta si está disponible)
        - nombre_cliente (string)
        - codigo_postal (string)
        - comercializadora (string)
        - tarifa_contratada (string)
        - fecha_emision (string, en formato YYYY-MM-DD)

        Ejemplo de respuesta exitosa:
        {"kwh_consumidos": 350.5, "potencia_contratada_kw": 4.6, "coste_total": 85.20, "peak_percent_from_invoice": 45.0, "nombre_cliente": "Juan Pérez", "codigo_postal": "28080", "comercializadora": "Iberdrola", "tarifa_contratada": "Plan Estable", "fecha_emision": "2024-07-28"}

        Ejemplo de respuesta de error:
        {"error": "La imagen no es una factura de electricidad o es completamente ilegible."}
        """
        
        try:
            image_part = {"mime_type": mime_type, "data": file_content}
            response = self.vision_model.generate_content([prompt, image_part])
            
            # Limpiar la respuesta de Gemini para obtener un JSON válido
            cleaned_response = response.text.strip().replace("```json", "").replace("```", "").strip()
            
            return json.loads(cleaned_response)

        except Exception as e:
            logger.error(f"Error en la llamada a la API de Gemini: {e}", exc_info=True)
            raise AppError("El servicio de inteligencia artificial no pudo procesar la factura.", 503)

    # El resto de los métodos del servicio permanecen igual, ya que su lógica es robusta.
    def process_manual_data(self, user_id: str, manual_data: Dict[str, Any]) -> Dict[str, Any]:
        self._update_user_profiles_robust(user_id, manual_data)
        self.executor.submit(self._publish_consumption_event, user_id, manual_data)
        return manual_data

    def get_user_energy_profile_enterprise(self, user_id: str) -> Dict[str, Any]:
        try:
            user_doc = self.db.collection("users").document(user_id).get()
            return user_doc.to_dict() if user_doc.exists else {}
        except Exception as e:
            logger.error(f"Error obteniendo perfil de Firestore para {user_id}: {e}", exc_info=True)
            raise AppError("No se pudo obtener el perfil del usuario.", 500)

    def _update_user_profiles_robust(self, user_id: str, invoice_data: Dict[str, Any]):
        try:
            profile_record = self._prepare_unified_profile_record(user_id, invoice_data)
            firestore_ref = self.db.collection("users").document(user_id)
            firestore_ref.set(profile_record, merge=True)
            self.executor.submit(self._sync_profile_to_bigquery, profile_record)
        except Exception as e:
            logger.error(f"Error crítico al actualizar perfil en Firestore para {user_id}: {e}")

    def _prepare_unified_profile_record(self, user_id: str, invoice_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "user_id": user_id,
            "last_update_timestamp": datetime.datetime.now(datetime.timezone.utc),
            "monthly_consumption_kwh": float(invoice_data.get("kwh_consumidos", 0)),
            "peak_consumption_percent": float(invoice_data.get("peak_percent_from_invoice", 0)),
            "contracted_power_kw": float(invoice_data.get("potencia_contratada_kw", 0)),
            "last_invoice_data_json": json.dumps(invoice_data)
        }

    def _sync_profile_to_bigquery(self, profile_record: Dict[str, Any]):
        try:
            user_id = profile_record['user_id']
            merge_query = f"""
            MERGE `{self.users_table_id}` T
            USING (SELECT @user_id as user_id) S ON T.user_id = S.user_id
            WHEN MATCHED THEN
                UPDATE SET last_update_timestamp = @last_update_timestamp, monthly_consumption_kwh = @monthly_consumption_kwh, peak_consumption_percent = @peak_consumption_percent, contracted_power_kw = @contracted_power_kw, last_invoice_data_json = @last_invoice_data_json
            WHEN NOT MATCHED THEN
                INSERT (user_id, last_update_timestamp, monthly_consumption_kwh, peak_consumption_percent, contracted_power_kw, last_invoice_data_json)
                VALUES (@user_id, @last_update_timestamp, @monthly_consumption_kwh, @peak_consumption_percent, @contracted_power_kw, @last_invoice_data_json)
            """
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("user_id", "STRING", user_id),
                    bigquery.ScalarQueryParameter("last_update_timestamp", "TIMESTAMP", profile_record["last_update_timestamp"]),
                    bigquery.ScalarQueryParameter("monthly_consumption_kwh", "NUMERIC", profile_record["monthly_consumption_kwh"]),
                    bigquery.ScalarQueryParameter("peak_consumption_percent", "NUMERIC", profile_record["peak_consumption_percent"]),
                    bigquery.ScalarQueryParameter("contracted_power_kw", "NUMERIC", profile_record["contracted_power_kw"]),
                    bigquery.ScalarQueryParameter("last_invoice_data_json", "JSON", profile_record["last_invoice_data_json"]),
                ]
            )
            query_job = self.bq_client.query(merge_query, job_config=job_config)
            query_job.result()
            if query_job.num_dml_affected_rows > 0:
                logger.info(f"Perfil de usuario {user_id} sincronizado a BigQuery.")
        except Exception as e:
            logger.error(f"Error en _sync_profile_to_bigquery para {profile_record.get('user_id')}: {e}")

    def _upload_to_gcs_and_log(self, user_id: str, file_content: bytes, filename: Optional[str], mime_type: str):
        try:
            bucket = self.storage_client.bucket(self.invoice_bucket_name)
            sanitized_filename = re.sub(r'[^a-zA-Z0-9_.-]', '', filename or 'file')
            blob_name = f"invoices/{user_id}/{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{sanitized_filename}"
            blob = bucket.blob(blob_name)
            blob.upload_from_string(file_content, content_type=mime_type)
            logger.info(f"Archivo de {user_id} subido a GCS: {blob.name}")
        except Exception as e:
            logger.error(f"Error al subir archivo a GCS para {user_id}: {e}")

    def _publish_consumption_event(self, user_id: str, extracted_data: Dict[str, Any]):
        try:
            event_data = {
                "user_id": user_id,
                "event_type": "consumption_update",
                "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "data": extracted_data
            }
            message_payload = json.dumps(event_data).encode("utf-8")
            future = self.pubsub_client.publish(self.consumption_topic_name, message_payload)
            future.result()
            logger.info(f"Evento de consumo para {user_id} publicado en Pub/Sub.")
        except Exception as e:
            logger.error(f"Error al publicar evento en Pub/Sub para {user_id}: {e}")
