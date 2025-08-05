"""
MIGRACIÓN EMPRESARIAL: Creación de tabla async_tasks

Esta migración crea la tabla async_tasks para el almacenamiento de tareas
asíncronas con tracking completo del estado y rendimiento.

Autor: Sistema de Migraciones Empresariales
Fecha: 2025-07-16
Versión: 1.0

IMPORTANTE: Esta tabla es crítica para el AsyncProcessingService.
"""

from google.cloud import bigquery
from google.cloud.exceptions import NotFound
import logging
import os
from datetime import datetime, timezone


def get_bigquery_client():
    """Obtener cliente BigQuery configurado"""
    project_id = os.environ.get("GCP_PROJECT_ID", "smatwatt")
    return bigquery.Client(project=project_id)


def get_dataset_id():
    """Obtener ID del dataset"""
    return os.environ.get("BQ_DATASET_ID", "smartwatt_data")


def upgrade(client: bigquery.Client, project_id: str, dataset_id: str):
    """
    🏢 CREAR TABLA async_tasks

    Crear tabla async_tasks si no existe.
    Esta tabla almacena tareas asíncronas con tracking completo.
    """
    try:
        client = get_bigquery_client()
        dataset_id = get_dataset_id()
        table_id = "async_tasks"

        # Referencia completa de la tabla
        table_ref = client.dataset(dataset_id).table(table_id)

        # Verificar si la tabla ya existe
        try:
            client.get_table(table_ref)
            logging.info(f"✅ Tabla {table_id} ya existe - saltando creación")
            return
        except NotFound:
            logging.info(f"📋 Creando tabla {table_id}...")

        # Definir esquema empresarial
        schema = [
            bigquery.SchemaField(
                "task_id", "STRING", mode="REQUIRED", description="ID único de la tarea"
            ),
            bigquery.SchemaField(
                "task_type",
                "STRING",
                mode="REQUIRED",
                description="Tipo de tarea (invoice_processing, ai_analysis, etc.)",
            ),
            bigquery.SchemaField(
                "status",
                "STRING",
                mode="REQUIRED",
                description="Estado de la tarea (pending, processing, completed, failed)",
            ),
            bigquery.SchemaField(
                "priority",
                "INTEGER",
                mode="REQUIRED",
                description="Prioridad de la tarea (1-10)",
            ),
            bigquery.SchemaField(
                "user_id",
                "STRING",
                mode="NULLABLE",
                description="ID del usuario asociado",
            ),
            bigquery.SchemaField(
                "worker_id",
                "STRING",
                mode="NULLABLE",
                description="ID del worker que procesó la tarea",
            ),
            bigquery.SchemaField(
                "task_data",
                "JSON",
                mode="NULLABLE",
                description="Datos de entrada de la tarea",
            ),
            bigquery.SchemaField(
                "task_result",
                "JSON",
                mode="NULLABLE",
                description="Resultado de la tarea",
            ),
            bigquery.SchemaField(
                "error_message",
                "STRING",
                mode="NULLABLE",
                description="Mensaje de error si falló",
            ),
            bigquery.SchemaField(
                "error_traceback",
                "STRING",
                mode="NULLABLE",
                description="Traceback completo del error",
            ),
            bigquery.SchemaField(
                "retry_count",
                "INTEGER",
                mode="NULLABLE",
                description="Número de reintentos",
            ),
            bigquery.SchemaField(
                "max_retries",
                "INTEGER",
                mode="NULLABLE",
                description="Máximo número de reintentos permitidos",
            ),
            bigquery.SchemaField(
                "execution_time_ms",
                "INTEGER",
                mode="NULLABLE",
                description="Tiempo de ejecución en milisegundos",
            ),
            bigquery.SchemaField(
                "queue_time_ms",
                "INTEGER",
                mode="NULLABLE",
                description="Tiempo en cola en milisegundos",
            ),
            bigquery.SchemaField(
                "memory_usage_mb",
                "FLOAT",
                mode="NULLABLE",
                description="Uso de memoria en MB",
            ),
            bigquery.SchemaField(
                "cpu_usage_percent",
                "FLOAT",
                mode="NULLABLE",
                description="Uso de CPU en porcentaje",
            ),
            bigquery.SchemaField(
                "created_at",
                "TIMESTAMP",
                mode="REQUIRED",
                description="Timestamp de creación",
            ),
            bigquery.SchemaField(
                "started_at",
                "TIMESTAMP",
                mode="NULLABLE",
                description="Timestamp de inicio de procesamiento",
            ),
            bigquery.SchemaField(
                "completed_at",
                "TIMESTAMP",
                mode="NULLABLE",
                description="Timestamp de finalización",
            ),
            bigquery.SchemaField(
                "updated_at",
                "TIMESTAMP",
                mode="NULLABLE",
                description="Timestamp de última actualización",
            ),
        ]

        # Configurar tabla con particionamiento por fecha
        table = bigquery.Table(table_ref, schema=schema)
        table.description = (
            "🏢 TABLA EMPRESARIAL: Tareas asíncronas con tracking completo"
        )

        # Configurar particionamiento por fecha de creación
        table.time_partitioning = bigquery.TimePartitioning(
            type_=bigquery.TimePartitioningType.DAY,
            field="created_at",
            expiration_ms=None,  # Sin expiración automática
        )

        # Configurar clustering para optimizar consultas
        table.clustering_fields = ["task_type", "status", "user_id"]

        # Crear tabla
        table = client.create_table(table)

        logging.info(f"✅ Tabla {table_id} creada exitosamente")
        logging.info(
            f"📍 Ubicación: {table.project}.{table.dataset_id}.{table.table_id}"
        )
        logging.info(f"🏢 Particionamiento: Por fecha de creación")
        logging.info(f"🔍 Clustering: task_type, status, user_id")

        return True

    except Exception as e:
        logging.error(f"❌ Error creando tabla async_tasks: {e}")
        raise


def downgrade():
    """
    🗑️ ELIMINAR TABLA async_tasks

    Eliminar tabla async_tasks (solo para desarrollo).
    ⚠️ CUIDADO: Esta operación es irreversible.
    """
    try:
        client = get_bigquery_client()
        dataset_id = get_dataset_id()
        table_id = "async_tasks"

        # Referencia completa de la tabla
        table_ref = client.dataset(dataset_id).table(table_id)

        # Eliminar tabla
        client.delete_table(table_ref, not_found_ok=True)
        logging.info(f"🗑️ Tabla {table_id} eliminada exitosamente")

    except Exception as e:
        logging.error(f"❌ Error eliminando tabla async_tasks: {e}")
        raise


if __name__ == "__main__":
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    print("🏢 MIGRACIÓN EMPRESARIAL: async_tasks")
    print("=" * 50)

    # Ejecutar usando las variables del entorno
    from google.cloud import bigquery
    import os

    client = bigquery.Client(project="smatwatt")
    project_id = "smatwatt"
    dataset_id = "smartwatt_data"

    upgrade(client, project_id, dataset_id)
    print("✅ Migración completada exitosamente")
