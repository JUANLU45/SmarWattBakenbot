# expert_bot_api_COPY/app/services/data_sync_service.py
# ⚙️ SERVICIO DE SINCRONIZACIÓN DE DATOS - FIRESTORE A BIGQUERY

import logging
from flask import current_app
from google.cloud import bigquery, firestore
from google.api_core import exceptions as google_exceptions

from utils.error_handlers import AppError

# Configuración de logging para el servicio
logger = logging.getLogger(__name__)

class DataSyncService:
    """
    Servicio robusto para garantizar la consistencia de datos de usuario
    entre Firestore (operacional) y BigQuery (analítico).
    """

    def __init__(self):
        self.bq_client = bigquery.Client()
        self.db = firestore.Client()
        self.project_id = current_app.config["GCP_PROJECT_ID"]
        self.dataset_id = current_app.config["BQ_DATASET_ID"]
        # TODO: VERIFICAR MILIMÉTRICAMENTE el nombre de esta tabla con el esquema real.
        self.users_table_id = f"{self.project_id}.{self.dataset_id}.users"

    def sync_user_profile(self, user_id: str):
        """
        Sincroniza el perfil de un usuario desde Firestore a BigQuery.
        Esta operación es crítica y se ejecuta de forma robusta.
        """
        if not user_id:
            logger.warning("sync_user_profile fue llamado sin user_id.")
            return

        try:
            # 1. Obtener datos de Firestore
            user_ref = self.db.collection("users").document(user_id)
            user_doc = user_ref.get()

            if not user_doc.exists:
                logger.warning(f"No se encontró el perfil de usuario {user_id} en Firestore para sincronizar.")
                return

            firestore_data = user_doc.to_dict()
            if not firestore_data:
                logger.warning(f"El documento del usuario {user_id} en Firestore está vacío.")
                return

            # 2. Preparar los datos para BigQuery
            # TODO: VERIFICAR MILIMÉTRICAMENTE cada campo con el esquema real de la tabla 'users'.
            bq_row = {
                "user_id": user_id,
                "email": firestore_data.get("email"),
                "display_name": firestore_data.get("displayName"),
                "created_at": firestore_data.get("createdAt"),
                "last_login_at": firestore_data.get("lastLoginAt"),
                # Añadir más campos según el esquema final de BigQuery
                "sync_timestamp": datetime.now(timezone.utc).isoformat(),
            }

            # 3. Insertar/Actualizar en BigQuery (usando MERGE para idempotencia)
            # La sentencia MERGE es la forma más robusta de hacer un "upsert".
            merge_query = f"""
            MERGE `{self.users_table_id}` T
            USING (SELECT @user_id as user_id) S
            ON T.user_id = S.user_id
            WHEN MATCHED THEN
                UPDATE SET
                    email = @email,
                    display_name = @display_name,
                    last_login_at = @last_login_at,
                    sync_timestamp = @sync_timestamp
            WHEN NOT MATCHED THEN
                INSERT (user_id, email, display_name, created_at, last_login_at, sync_timestamp)
                VALUES (@user_id, @email, @display_name, @created_at, @last_login_at, @sync_timestamp)
            """

            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("user_id", "STRING", bq_row["user_id"]),
                    bigquery.ScalarQueryParameter("email", "STRING", bq_row["email"]),
                    bigquery.ScalarQueryParameter("display_name", "STRING", bq_row["display_name"]),
                    bigquery.ScalarQueryParameter("created_at", "TIMESTAMP", bq_row["created_at"]),
                    bigquery.ScalarQueryParameter("last_login_at", "TIMESTAMP", bq_row["last_login_at"]),
                    bigquery.ScalarQueryParameter("sync_timestamp", "TIMESTAMP", bq_row["sync_timestamp"]),
                ]
            )

            query_job = self.bq_client.query(merge_query, job_config=job_config)
            query_job.result()  # Esperar a que el job termine

            logger.info(f"✅ Perfil de usuario {user_id} sincronizado exitosamente a BigQuery.")

        except google_exceptions.NotFound:
            logger.error(f"❌ La tabla {self.users_table_id} no existe en BigQuery. La sincronización no puede continuar.")
        except google_exceptions.GoogleAPICallError as e:
            logger.error(f"❌ Error de API de Google sincronizando usuario {user_id}: {str(e)}")
        except Exception as e:
            # Captura cualquier otro error para no romper el flujo de login del usuario.
            logger.error(f"❌ Error inesperado sincronizando el perfil del usuario {user_id}: {str(e)}")
