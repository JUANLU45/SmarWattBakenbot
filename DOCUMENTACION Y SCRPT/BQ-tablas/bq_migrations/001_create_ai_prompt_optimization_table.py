"""
MIGRACIÓN EMPRESARIAL: Creación de tabla ai_prompt_optimization
============================================================

PROPÓSITO: Crear la tabla para almacenar datos de optimización de prompts de IA
FECHA: 2025-07-16
VERSIÓN: 1.0.0 - EMPRESARIAL

ESQUEMA DE TABLA:
- optimization_id: STRING (REQUIRED) - ID único de la optimización
- user_id: STRING (REQUIRED) - ID del usuario
- prompt_original: STRING (REQUIRED) - Prompt original
- prompt_optimized: STRING (REQUIRED) - Prompt optimizado
- optimization_score: FLOAT (REQUIRED) - Score de mejora (0-1)
- optimization_type: STRING (REQUIRED) - Tipo de optimización
- optimization_metrics: JSON (REQUIRED) - Métricas de optimización
- created_at: TIMESTAMP (REQUIRED) - Fecha de creación
- updated_at: TIMESTAMP (REQUIRED) - Fecha de actualización
- is_active: BOOLEAN (REQUIRED) - Estado activo

PARTICIÓN: Por fecha de creación (MONTHLY)
CLUSTERING: Por user_id, optimization_type
"""

from google.cloud import bigquery
from google.cloud.exceptions import NotFound, Conflict
import logging
from datetime import datetime
from typing import Dict, Any


def upgrade(
    client: bigquery.Client, project_id: str, dataset_id: str
) -> Dict[str, Any]:
    """
    Crear tabla ai_prompt_optimization si no existe.

    Args:
        client: Cliente BigQuery
        project_id: ID del proyecto GCP
        dataset_id: ID del dataset

    Returns:
        Dict con resultado de la migración
    """
    table_id = "ai_prompt_optimization"
    table_ref = client.dataset(dataset_id).table(table_id)

    try:
        # Verificar si la tabla ya existe
        client.get_table(table_ref)
        logging.info(f"Tabla {table_id} ya existe. Saltando creación.")
        return {
            "status": "skipped",
            "message": f"Tabla {table_id} ya existe",
            "table_id": table_id,
        }
    except NotFound:
        # La tabla no existe, crearla
        pass

    # Definir esquema empresarial robusto
    schema = [
        bigquery.SchemaField("optimization_id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("user_id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("prompt_original", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("prompt_optimized", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("optimization_score", "FLOAT", mode="REQUIRED"),
        bigquery.SchemaField("optimization_type", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("optimization_metrics", "JSON", mode="REQUIRED"),
        bigquery.SchemaField("created_at", "TIMESTAMP", mode="REQUIRED"),
        bigquery.SchemaField("updated_at", "TIMESTAMP", mode="REQUIRED"),
        bigquery.SchemaField("is_active", "BOOLEAN", mode="REQUIRED"),
    ]

    # Configuración de tabla empresarial
    table = bigquery.Table(table_ref, schema=schema)

    # Partición mensual por fecha de creación
    table.time_partitioning = bigquery.TimePartitioning(
        type_=bigquery.TimePartitioningType.MONTH, field="created_at"
    )

    # Clustering para optimización de consultas
    table.clustering_fields = ["user_id", "optimization_type"]

    # Configuración de expiración (2 años)
    table.time_partitioning.expiration_ms = 63072000000  # 2 años en ms

    # Descripción empresarial
    table.description = (
        "Tabla empresarial para almacenar optimizaciones de prompts de IA. "
        "Particionada mensualmente por created_at. "
        "Clustering por user_id y optimization_type para optimización de consultas."
    )

    try:
        # Crear tabla con configuración empresarial
        table = client.create_table(table, exists_ok=False)
        logging.info(f"Tabla {table_id} creada exitosamente.")

        return {
            "status": "created",
            "message": f"Tabla {table_id} creada exitosamente",
            "table_id": table_id,
            "schema_fields": len(schema),
            "partitioning": "MONTHLY",
            "clustering": ["user_id", "optimization_type"],
        }

    except Conflict:
        logging.warning(f"Tabla {table_id} ya existe (conflicto de concurrencia).")
        return {
            "status": "exists",
            "message": f"Tabla {table_id} ya existe",
            "table_id": table_id,
        }
    except Exception as e:
        logging.error(f"Error creando tabla {table_id}: {str(e)}")
        raise


def downgrade(
    client: bigquery.Client, project_id: str, dataset_id: str
) -> Dict[str, Any]:
    """
    Eliminar tabla ai_prompt_optimization (solo para desarrollo).

    Args:
        client: Cliente BigQuery
        project_id: ID del proyecto GCP
        dataset_id: ID del dataset

    Returns:
        Dict con resultado de la migración
    """
    table_id = "ai_prompt_optimization"
    table_ref = client.dataset(dataset_id).table(table_id)

    try:
        client.delete_table(table_ref, not_found_ok=True)
        logging.info(f"Tabla {table_id} eliminada exitosamente.")
        return {
            "status": "deleted",
            "message": f"Tabla {table_id} eliminada exitosamente",
            "table_id": table_id,
        }
    except Exception as e:
        logging.error(f"Error eliminando tabla {table_id}: {str(e)}")
        raise


if __name__ == "__main__":
    """Ejecutar migración manualmente para pruebas."""
    import os

    # Configuración desde variables de entorno
    project_id = os.environ.get("GCP_PROJECT_ID", "smatwatt")
    dataset_id = os.environ.get("BQ_DATASET_ID", "smartwatt_data")

    # Inicializar cliente BigQuery
    client = bigquery.Client(project=project_id)

    # Ejecutar migración
    result = upgrade(client, project_id, dataset_id)
    print(f"Resultado migración: {result}")
