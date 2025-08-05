"""
MIGRACIÓN EMPRESARIAL: Creación de tabla ai_business_metrics

Esta migración crea la tabla ai_business_metrics para el almacenamiento de métricas
empresariales de IA con análisis de tendencias.

Autor: Sistema de Migraciones Empresariales
Fecha: 2025-07-16
Versión: 1.0

IMPORTANTE: Esta tabla es crítica para el análisis de rendimiento empresarial.
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
    🏢 CREAR TABLA ai_business_metrics

    Crear tabla ai_business_metrics si no existe.
    Esta tabla almacena métricas empresariales de IA con análisis de tendencias.
    """
    try:
        client = get_bigquery_client()
        dataset_id = get_dataset_id()
        table_id = "ai_business_metrics"

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
                "metric_id",
                "STRING",
                mode="REQUIRED",
                description="ID único de la métrica",
            ),
            bigquery.SchemaField(
                "metric_type",
                "STRING",
                mode="REQUIRED",
                description="Tipo de métrica (engagement, conversion, efficiency, etc.)",
            ),
            bigquery.SchemaField(
                "metric_value",
                "FLOAT",
                mode="REQUIRED",
                description="Valor numérico de la métrica",
            ),
            bigquery.SchemaField(
                "metric_metadata",
                "JSON",
                mode="NULLABLE",
                description="Metadata adicional de la métrica",
            ),
            bigquery.SchemaField(
                "user_segment",
                "STRING",
                mode="NULLABLE",
                description="Segmento de usuario asociado",
            ),
            bigquery.SchemaField(
                "time_period",
                "STRING",
                mode="NULLABLE",
                description="Período de tiempo de la métrica",
            ),
            bigquery.SchemaField(
                "trend_direction",
                "STRING",
                mode="NULLABLE",
                description="Dirección de tendencia (up, down, stable)",
            ),
            bigquery.SchemaField(
                "business_impact",
                "STRING",
                mode="NULLABLE",
                description="Impacto empresarial (high, medium, low)",
            ),
            bigquery.SchemaField(
                "category",
                "STRING",
                mode="NULLABLE",
                description="Categoría de la métrica",
            ),
            bigquery.SchemaField(
                "subcategory",
                "STRING",
                mode="NULLABLE",
                description="Subcategoría de la métrica",
            ),
            bigquery.SchemaField(
                "aggregation_level",
                "STRING",
                mode="NULLABLE",
                description="Nivel de agregación (daily, weekly, monthly)",
            ),
            bigquery.SchemaField(
                "baseline_value",
                "FLOAT",
                mode="NULLABLE",
                description="Valor de referencia para comparación",
            ),
            bigquery.SchemaField(
                "threshold_min",
                "FLOAT",
                mode="NULLABLE",
                description="Umbral mínimo aceptable",
            ),
            bigquery.SchemaField(
                "threshold_max",
                "FLOAT",
                mode="NULLABLE",
                description="Umbral máximo aceptable",
            ),
            bigquery.SchemaField(
                "alert_triggered",
                "BOOLEAN",
                mode="NULLABLE",
                description="Si se disparó una alerta",
            ),
            bigquery.SchemaField(
                "data_source",
                "STRING",
                mode="NULLABLE",
                description="Fuente de datos original",
            ),
            bigquery.SchemaField(
                "calculation_method",
                "STRING",
                mode="NULLABLE",
                description="Método de cálculo utilizado",
            ),
            bigquery.SchemaField(
                "recorded_at",
                "TIMESTAMP",
                mode="REQUIRED",
                description="Timestamp de registro",
            ),
            bigquery.SchemaField(
                "created_at",
                "TIMESTAMP",
                mode="REQUIRED",
                description="Timestamp de creación",
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
            "🏢 TABLA EMPRESARIAL: Métricas de negocio de IA con análisis de tendencias"
        )

        # Configurar particionamiento por fecha de registro
        table.time_partitioning = bigquery.TimePartitioning(
            type_=bigquery.TimePartitioningType.DAY,
            field="recorded_at",
            expiration_ms=None,  # Sin expiración automática
        )

        # Configurar clustering para optimizar consultas
        table.clustering_fields = ["metric_type", "user_segment", "business_impact"]

        # Crear tabla
        table = client.create_table(table)

        logging.info(f"✅ Tabla {table_id} creada exitosamente")
        logging.info(
            f"📍 Ubicación: {table.project}.{table.dataset_id}.{table.table_id}"
        )
        logging.info(f"🏢 Particionamiento: Por fecha de registro")
        logging.info(f"🔍 Clustering: metric_type, user_segment, business_impact")

        return True

    except Exception as e:
        logging.error(f"❌ Error creando tabla ai_business_metrics: {e}")
        raise


def downgrade():
    """
    🗑️ ELIMINAR TABLA ai_business_metrics

    Eliminar tabla ai_business_metrics (solo para desarrollo).
    ⚠️ CUIDADO: Esta operación es irreversible.
    """
    try:
        client = get_bigquery_client()
        dataset_id = get_dataset_id()
        table_id = "ai_business_metrics"

        # Referencia completa de la tabla
        table_ref = client.dataset(dataset_id).table(table_id)

        # Eliminar tabla
        client.delete_table(table_ref, not_found_ok=True)
        logging.info(f"🗑️ Tabla {table_id} eliminada exitosamente")

    except Exception as e:
        logging.error(f"❌ Error eliminando tabla ai_business_metrics: {e}")
        raise


if __name__ == "__main__":
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    print("🏢 MIGRACIÓN EMPRESARIAL: ai_business_metrics")
    print("=" * 50)

    # Ejecutar usando las variables del entorno
    from google.cloud import bigquery
    import os

    client = bigquery.Client(project="smatwatt")
    project_id = "smatwatt"
    dataset_id = "smartwatt_data"

    upgrade(client, project_id, dataset_id)
    print("✅ Migración completada exitosamente")
