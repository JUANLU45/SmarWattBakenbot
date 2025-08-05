"""
MIGRACIÓN EMPRESARIAL: Creación de tabla worker_metrics

Esta migración crea la tabla worker_metrics para el almacenamiento de métricas
de rendimiento de workers asíncronos con análisis detallado.

Autor: Sistema de Migraciones Empresariales
Fecha: 2025-07-16
Versión: 1.0

IMPORTANTE: Esta tabla es crítica para el monitoreo de AsyncProcessingService.
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
    🏢 CREAR TABLA worker_metrics

    Crear tabla worker_metrics si no existe.
    Esta tabla almacena métricas de rendimiento de workers asíncronos.
    """
    try:
        client = get_bigquery_client()
        dataset_id = get_dataset_id()
        table_id = "worker_metrics"

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
                "worker_id",
                "STRING",
                mode="REQUIRED",
                description="ID único del worker",
            ),
            bigquery.SchemaField(
                "worker_name",
                "STRING",
                mode="NULLABLE",
                description="Nombre descriptivo del worker",
            ),
            bigquery.SchemaField(
                "status",
                "STRING",
                mode="REQUIRED",
                description="Estado del worker (idle, processing, error, offline)",
            ),
            bigquery.SchemaField(
                "current_task",
                "STRING",
                mode="NULLABLE",
                description="ID de la tarea actual",
            ),
            bigquery.SchemaField(
                "tasks_processed",
                "INTEGER",
                mode="REQUIRED",
                description="Número total de tareas procesadas",
            ),
            bigquery.SchemaField(
                "tasks_failed",
                "INTEGER",
                mode="REQUIRED",
                description="Número total de tareas fallidas",
            ),
            bigquery.SchemaField(
                "avg_processing_time_ms",
                "FLOAT",
                mode="NULLABLE",
                description="Tiempo promedio de procesamiento en ms",
            ),
            bigquery.SchemaField(
                "total_processing_time_ms",
                "INTEGER",
                mode="NULLABLE",
                description="Tiempo total de procesamiento en ms",
            ),
            bigquery.SchemaField(
                "memory_usage_mb",
                "FLOAT",
                mode="NULLABLE",
                description="Uso actual de memoria en MB",
            ),
            bigquery.SchemaField(
                "max_memory_usage_mb",
                "FLOAT",
                mode="NULLABLE",
                description="Uso máximo de memoria en MB",
            ),
            bigquery.SchemaField(
                "cpu_usage_percent",
                "FLOAT",
                mode="NULLABLE",
                description="Uso actual de CPU en porcentaje",
            ),
            bigquery.SchemaField(
                "max_cpu_usage_percent",
                "FLOAT",
                mode="NULLABLE",
                description="Uso máximo de CPU en porcentaje",
            ),
            bigquery.SchemaField(
                "queue_size",
                "INTEGER",
                mode="NULLABLE",
                description="Tamaño actual de la cola",
            ),
            bigquery.SchemaField(
                "success_rate",
                "FLOAT",
                mode="NULLABLE",
                description="Tasa de éxito (0.0-1.0)",
            ),
            bigquery.SchemaField(
                "error_rate",
                "FLOAT",
                mode="NULLABLE",
                description="Tasa de error (0.0-1.0)",
            ),
            bigquery.SchemaField(
                "throughput_tasks_per_minute",
                "FLOAT",
                mode="NULLABLE",
                description="Rendimiento en tareas por minuto",
            ),
            bigquery.SchemaField(
                "last_activity",
                "TIMESTAMP",
                mode="NULLABLE",
                description="Timestamp de última actividad",
            ),
            bigquery.SchemaField(
                "last_error",
                "STRING",
                mode="NULLABLE",
                description="Último mensaje de error",
            ),
            bigquery.SchemaField(
                "health_status",
                "STRING",
                mode="NULLABLE",
                description="Estado de salud (healthy, degraded, unhealthy)",
            ),
            bigquery.SchemaField(
                "uptime_seconds",
                "INTEGER",
                mode="NULLABLE",
                description="Tiempo de actividad en segundos",
            ),
            bigquery.SchemaField(
                "worker_version",
                "STRING",
                mode="NULLABLE",
                description="Versión del worker",
            ),
            bigquery.SchemaField(
                "host_info",
                "JSON",
                mode="NULLABLE",
                description="Información del host donde corre el worker",
            ),
            bigquery.SchemaField(
                "created_at",
                "TIMESTAMP",
                mode="REQUIRED",
                description="Timestamp de creación del worker",
            ),
            bigquery.SchemaField(
                "recorded_at",
                "TIMESTAMP",
                mode="REQUIRED",
                description="Timestamp de registro de la métrica",
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
            "🏢 TABLA EMPRESARIAL: Métricas de rendimiento de workers asíncronos"
        )

        # Configurar particionamiento por fecha de registro
        table.time_partitioning = bigquery.TimePartitioning(
            type_=bigquery.TimePartitioningType.DAY,
            field="recorded_at",
            expiration_ms=None,  # Sin expiración automática
        )

        # Configurar clustering para optimizar consultas
        table.clustering_fields = ["worker_id", "status", "health_status"]

        # Crear tabla
        table = client.create_table(table)

        logging.info(f"✅ Tabla {table_id} creada exitosamente")
        logging.info(
            f"📍 Ubicación: {table.project}.{table.dataset_id}.{table.table_id}"
        )
        logging.info(f"🏢 Particionamiento: Por fecha de registro")
        logging.info(f"🔍 Clustering: worker_id, status, health_status")

        return True

    except Exception as e:
        logging.error(f"❌ Error creando tabla worker_metrics: {e}")
        raise


def downgrade():
    """
    🗑️ ELIMINAR TABLA worker_metrics

    Eliminar tabla worker_metrics (solo para desarrollo).
    ⚠️ CUIDADO: Esta operación es irreversible.
    """
    try:
        client = get_bigquery_client()
        dataset_id = get_dataset_id()
        table_id = "worker_metrics"

        # Referencia completa de la tabla
        table_ref = client.dataset(dataset_id).table(table_id)

        # Eliminar tabla
        client.delete_table(table_ref, not_found_ok=True)
        logging.info(f"🗑️ Tabla {table_id} eliminada exitosamente")

    except Exception as e:
        logging.error(f"❌ Error eliminando tabla worker_metrics: {e}")
        raise


if __name__ == "__main__":
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    print("🏢 MIGRACIÓN EMPRESARIAL: worker_metrics")
    print("=" * 50)

    # Ejecutar usando las variables del entorno
    from google.cloud import bigquery
    import os

    client = bigquery.Client(project="smatwatt")
    project_id = "smatwatt"
    dataset_id = "smartwatt_data"

    upgrade(client, project_id, dataset_id)
    print("✅ Migración completada exitosamente")
