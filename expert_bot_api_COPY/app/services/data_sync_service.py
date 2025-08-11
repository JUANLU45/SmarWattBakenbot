# expert_bot_api_COPY/app/services/data_sync_service.py
# 🔄 SERVICIO DE SINCRONIZACIÓN DE DATOS - FIRESTORE A BIGQUERY

import logging
from flask import current_app
from google.cloud import bigquery, firestore
from google.api_core import exceptions as google_exceptions

from utils.error_handlers import AppError

logger = logging.getLogger(__name__)

class DataSyncService:
    """Servicio para la sincronización robusta de datos de usuario entre Firestore y BigQuery."""

    def __init__(self):
        try:
            self.db = firestore.Client()
            self.bq_client = bigquery.Client()
            self.project_id = current_app.config["GCP_PROJECT_ID"]
            self.dataset_id = current_app.config["BQ_DATASET_ID"]
            # TODO: VERIFICAR CAMPO - El nombre de la tabla 'users' debe coincidir con el esquema real.
            self.users_table_id = f"{self.project_id}.{self.dataset_id}.users"
        except Exception as e:
            logger.critical(f"❌ Error crítico al inicializar los clientes de Google Cloud: {str(e)}")
            raise AppError("No se pudieron inicializar los servicios de base de datos.", 500)

    def sync_user_profile_to_bigquery(self, user_id: str):
        """
        Obtiene el perfil de un usuario de Firestore y lo inserta o actualiza en BigQuery.
        Esta operación es crítica para mantener la consistencia de los datos.
        """
        if not user_id:
            logger.error("❌ Se intentó sincronizar un perfil sin user_id.")
            return

        try:
            # 1. Leer datos de Firestore
            user_ref = self.db.collection("users").document(user_id)
            user_doc = user_ref.get()

            if not user_doc.exists:
                logger.warning(f"⚠️ No se encontró el documento del usuario '{user_id}' en Firestore para sincronizar.")
                return

            user_data = user_doc.to_dict()
            if not user_data:
                logger.warning(f"⚠️ El documento del usuario '{user_id}' en Firestore está vacío.")
                return

            # 2. Preparar el registro para BigQuery
            # TODO: VERIFICAR CAMPO - Todos los campos aquí deben coincidir con el esquema real de la tabla 'users'.
            row_to_upsert = {
                "user_id": user_id,
                "email": user_data.get("email"),
                "display_name": user_data.get("displayName"),
                "created_at": user_data.get("createdAt"),
                "last_login_at": user_data.get("lastLoginAt"),
                "is_premium": user_data.get("isPremium", False),
                "data_completeness": self._calculate_completeness(user_data),
                "last_sync_at": firestore.SERVER_TIMESTAMP,
            }
            
            # 3. Realizar operación de MERGE (UPSERT) en BigQuery
            # Esta es la forma más robusta de insertar o actualizar.
            self._upsert_user_in_bigquery(row_to_upsert)

        except google_exceptions.NotFound:
             logger.error(f"❌ La colección 'users' no se encontró en Firestore para el usuario '{user_id}'.")
        except Exception as e:
            logger.error(f"❌ Error inesperado durante la sincronización del perfil del usuario '{user_id}': {str(e)}")
            # No relanzamos el error para no interrumpir el flujo principal del usuario (ej. login).
            
    def _upsert_user_in_bigquery(self, user_row: dict):
        """
        Ejecuta una consulta MERGE en BigQuery para insertar un nuevo usuario o actualizar uno existente.
        Es una operación atómica y la forma recomendada para operaciones de UPSERT.
        """
        try:
            # TODO: VERIFICAR CAMPO - Los nombres de campo en la consulta MERGE deben coincidir con el esquema.
            merge_query = f"""
            MERGE `{self.users_table_id}` T
            USING (SELECT @user_id as user_id) S
            ON T.user_id = S.user_id
            WHEN MATCHED THEN
                UPDATE SET
                    email = @email,
                    display_name = @display_name,
                    last_login_at = @last_login_at,
                    is_premium = @is_premium,
                    data_completeness = @data_completeness,
                    last_sync_at = @last_sync_at
            WHEN NOT MATCHED THEN
                INSERT (user_id, email, display_name, created_at, last_login_at, is_premium, data_completeness, last_sync_at)
                VALUES (@user_id, @email, @display_name, @created_at, @last_login_at, @is_premium, @data_completeness, @last_sync_at)
            """

            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("user_id", "STRING", user_row["user_id"]),
                    bigquery.ScalarQueryParameter("email", "STRING", user_row["email"]),
                    bigquery.ScalarQueryParameter("display_name", "STRING", user_row["display_name"]),
                    bigquery.ScalarQueryParameter("created_at", "TIMESTAMP", user_row["created_at"]),
                    bigquery.ScalarQueryParameter("last_login_at", "TIMESTAMP", user_row["last_login_at"]),
                    bigquery.ScalarQueryParameter("is_premium", "BOOLEAN", user_row["is_premium"]),
                    bigquery.ScalarQueryParameter("data_completeness", "FLOAT", user_row["data_completeness"]),
                    bigquery.ScalarQueryParameter("last_sync_at", "TIMESTAMP", user_row["last_sync_at"]),
                ]
            )

            query_job = self.bq_client.query(merge_query, job_config=job_config)
            query_job.result()  # Esperar a que el trabajo termine

            if query_job.num_dml_affected_rows > 0:
                logger.info(f"✅ Perfil del usuario '{user_row['user_id']}' sincronizado correctamente con BigQuery.")
            else:
                logger.warning(f"⚠️ No se afectaron filas al sincronizar al usuario '{user_row['user_id']}'. La consulta se ejecutó sin errores.")

        except google_exceptions.NotFound:
            logger.error(f"❌ La tabla de destino `{self.users_table_id}` no existe en BigQuery.")
        except Exception as e:
            logger.error(f"❌ Error al ejecutar la operación MERGE en BigQuery para el usuario '{user_row['user_id']}': {str(e)}")

    def _calculate_completeness(self, user_data: dict) -> float:
        """Calcula un puntaje de completitud del perfil del usuario."""
        score = 0
        total_fields = 5.0  # Número de campos que consideramos para la completitud
        
        if user_data.get("email"): score += 1
        if user_data.get("displayName"): score += 1
        if user_data.get("last_invoice_data"): score += 1
        if user_data.get("consumption"): score += 1
        if user_data.get("preferences"): score += 1

        return (score / total_fields) * 100
