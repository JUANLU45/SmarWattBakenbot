"""
MIGRACIÓN EMPRESARIAL: Creación de tabla ai_predictions

Esta migración crea la tabla ai_predictions para el almacenamiento de predicciones
de IA con metadata empresarial completo.

Autor: Sistema de Migraciones Empresariales
Fecha: 2025-07-16
Versión: 1.0

IMPORTANTE: Esta tabla es crítica para el funcionamiento del AILearningService.
"""

from google.cloud import bigquery
from google.cloud.exceptions import NotFound
import logging
import os
from datetime import datetime, timezone


def get_bigquery_client() -> bigquery.Client:
    """Obtener cliente BigQuery configurado"""
    project_id = os.environ.get("GCP_PROJECT_ID", "smatwatt")
    return bigquery.Client(project=project_id)


def get_dataset_id() -> str:
    """Obtener ID del dataset"""
    return os.environ.get("BQ_DATASET_ID", "smartwatt_data")


def upgrade(client: bigquery.Client, project_id: str, dataset_id: str) -> bool:
    """
    🏢 CREAR TABLA ai_predictions

    Crear tabla ai_predictions si no existe.
    Esta tabla almacena predicciones de IA con metadata empresarial.
    """
    try:
        # Usar los parámetros pasados o los valores por defecto
        if client is None:
            client = get_bigquery_client()
        if dataset_id is None:
            dataset_id = get_dataset_id()

        table_id = "ai_predictions"

        # Referencia completa de la tabla
        table_ref = client.dataset(dataset_id).table(table_id)

        # Verificar si la tabla ya existe
        try:
            client.get_table(table_ref)
            logging.info("✅ Tabla %s ya existe - saltando creación", table_id)
            return True
        except NotFound:
            logging.info("📋 Creando tabla %s...", table_id)

        # Definir esquema empresarial
        schema = [
            bigquery.SchemaField(
                "prediction_id",
                "STRING",
                mode="REQUIRED",
                description="ID único de la predicción",
            ),
            bigquery.SchemaField(
                "user_id",
                "STRING",
                mode="REQUIRED",
                description="ID del usuario que generó la predicción",
            ),
            bigquery.SchemaField(
                "conversation_id",
                "STRING",
                mode="REQUIRED",
                description="ID de la conversación asociada",
            ),
            bigquery.SchemaField(
                "prediction_type",
                "STRING",
                mode="REQUIRED",
                description="Tipo de predicción (consumption, cost, tariff, etc.)",
            ),
            bigquery.SchemaField(
                "predicted_value",
                "JSON",
                mode="REQUIRED",
                description="Valor predicho en formato JSON",
            ),
            bigquery.SchemaField(
                "confidence_score",
                "FLOAT",
                mode="REQUIRED",
                description="Puntuación de confianza (0.0-1.0)",
            ),
            bigquery.SchemaField(
                "actual_outcome",
                "JSON",
                mode="NULLABLE",
                description="Resultado real para validación",
            ),
            bigquery.SchemaField(
                "prediction_accuracy",
                "FLOAT",
                mode="NULLABLE",
                description="Precisión de la predicción validada",
            ),
            bigquery.SchemaField(
                "business_value",
                "FLOAT",
                mode="NULLABLE",
                description="Valor comercial estimado de la predicción",
            ),
            bigquery.SchemaField(
                "model_version",
                "STRING",
                mode="NULLABLE",
                description="Versión del modelo utilizado",
            ),
            bigquery.SchemaField(
                "input_features",
                "JSON",
                mode="NULLABLE",
                description="Características de entrada utilizadas",
            ),
            bigquery.SchemaField(
                "processing_time_ms",
                "INTEGER",
                mode="NULLABLE",
                description="Tiempo de procesamiento en milisegundos",
            ),
            bigquery.SchemaField(
                "created_at",
                "TIMESTAMP",
                mode="REQUIRED",
                description="Timestamp de creación",
            ),
            bigquery.SchemaField(
                "validated_at",
                "TIMESTAMP",
                mode="NULLABLE",
                description="Timestamp de validación",
            ),
            bigquery.SchemaField(
                "last_updated",
                "TIMESTAMP",
                mode="NULLABLE",
                description="Timestamp de última actualización",
            ),
        ]

        # Configurar tabla con particionamiento por fecha
        table = bigquery.Table(table_ref, schema=schema)
        table.description = (
            "🏢 TABLA EMPRESARIAL: Predicciones de IA con metadata completo"
        )

        # Configurar particionamiento por fecha de creación
        table.time_partitioning = bigquery.TimePartitioning(
            type_=bigquery.TimePartitioningType.DAY,
            field="created_at",
            expiration_ms=None,  # Sin expiración automática
        )

        # Configurar clustering para optimizar consultas
        table.clustering_fields = ["user_id", "prediction_type", "conversation_id"]

        # Crear tabla
        table = client.create_table(table)

        logging.info("✅ Tabla %s creada exitosamente", table_id)
        logging.info(
            "📍 Ubicación: %s.%s.%s",
            table.project,
            table.dataset_id,
            table.table_id,
        )
        logging.info("🏢 Particionamiento: Por fecha de creación")
        logging.info("🔍 Clustering: user_id, prediction_type, conversation_id")

        return True

    except Exception as e:
        logging.error("❌ Error creando tabla ai_predictions: %s", e)
        raise


def downgrade() -> None:
    """
    🗑️ ELIMINAR TABLA ai_predictions

    Eliminar tabla ai_predictions (solo para desarrollo).
    ⚠️ CUIDADO: Esta operación es irreversible.
    """
    try:
        client = get_bigquery_client()
        dataset_id: str = get_dataset_id()
        table_id = "ai_predictions"

        # Referencia completa de la tabla
        table_ref = client.dataset(dataset_id).table(table_id)

        # Eliminar tabla
        client.delete_table(table_ref, not_found_ok=True)
        logging.info(f"🗑️ Tabla {table_id} eliminada exitosamente")

    except Exception as e:
        logging.error(f"❌ Error eliminando tabla ai_predictions: {e}")
        raise


if __name__ == "__main__":
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    print("🏢 MIGRACIÓN EMPRESARIAL: ai_predictions")
    print("=" * 50)

    # Ejecutar usando las variables del entorno
    from google.cloud import bigquery
    import os

    client = bigquery.Client(project="smatwatt")
    bq_project_id = "smatwatt"
    dataset_id = "smartwatt_data"

    upgrade(client, bq_project_id, dataset_id)
    print("✅ Migración completada exitosamente")
