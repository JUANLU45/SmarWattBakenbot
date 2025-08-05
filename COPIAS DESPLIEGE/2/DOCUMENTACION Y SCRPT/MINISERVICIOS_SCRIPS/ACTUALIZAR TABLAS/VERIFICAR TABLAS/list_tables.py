#!/usr/bin/env python3
"""
📋 LISTADOR DE TABLAS BIGQUERY - SMARWATT
=========================================

Lista todas las tablas disponibles en el dataset de BigQuery.
Perfecto para exploración rápida del estado actual.

USO:
    python list_tables.py

AUTOR: Sistema de verificación empresarial
FECHA: 2025-08-03
"""

from google.cloud import bigquery
from google.oauth2 import service_account
import os
from datetime import datetime


def list_all_tables():
    """📋 Lista todas las tablas del dataset BigQuery"""

    # CONFIGURAR CREDENCIALES - MISMA RUTA QUE EL SCRIPT ANTERIOR
    credentials_path = r"C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\DOCUMENTACION Y SCRPT\MINISERVICIOS_SCRIPS\ESCRIP ADMIN\firebase-adminsdk-fbsvc-key.json"

    if not os.path.exists(credentials_path):
        print(
            f"❌ ERROR: No se encontró el archivo de credenciales en: {credentials_path}"
        )
        return False

    print(f"🔑 Usando credenciales desde: {credentials_path}")
    print(f"📅 Iniciando exploración: {datetime.now().isoformat()}")

    # Configurar cliente BigQuery
    try:
        credentials = service_account.Credentials.from_service_account_file(
            credentials_path
        )
        client = bigquery.Client(credentials=credentials, project="smatwatt")
        print("✅ Cliente BigQuery configurado correctamente")
    except Exception as e:
        print(f"❌ ERROR configurando credenciales: {str(e)}")
        return False

    project_id = "smatwatt"
    dataset_id = "smartwatt_data"

    print(f"\n{'='*60}")
    print(f"📊 EXPLORANDO DATASET: {project_id}.{dataset_id}")
    print(f"{'='*60}")

    try:
        # Obtener referencia al dataset
        dataset_ref = client.dataset(dataset_id)

        # Listar todas las tablas
        tables = list(client.list_tables(dataset_ref))

        if not tables:
            print("⚠️  No se encontraron tablas en el dataset")
            return True

        print(f"✅ ENCONTRADAS {len(tables)} TABLAS:")
        print(f"\n{'='*60}")

        for i, table in enumerate(tables, 1):
            # Obtener información detallada de la tabla
            table_ref = dataset_ref.table(table.table_id)
            table_info = client.get_table(table_ref)

            print(f"📋 {i:2d}. {table.table_id}")
            print(f"    🆔 ID completo: {table_info.full_table_id}")
            print(f"    📊 Campos: {len(table_info.schema)} columnas")

            if table_info.num_rows is not None:
                print(f"    📈 Registros: {table_info.num_rows:,}")
            else:
                print(f"    📈 Registros: N/A")

            if table_info.created:
                print(
                    f"    📅 Creada: {table_info.created.strftime('%Y-%m-%d %H:%M:%S')}"
                )

            if table_info.modified:
                print(
                    f"    🔄 Modificada: {table_info.modified.strftime('%Y-%m-%d %H:%M:%S')}"
                )

            print(f"    💾 Tamaño: {table_info.num_bytes / (1024*1024):.2f} MB")
            print("")

        print(f"{'='*60}")
        print(f"📊 RESUMEN FINAL:")
        print(f"   • Dataset: {dataset_id}")
        print(f"   • Total tablas: {len(tables)}")
        print(f"   • Proyecto: {project_id}")
        print(f"{'='*60}")

        return True

    except Exception as e:
        print(f"❌ ERROR listando tablas: {str(e)}")
        return False


if __name__ == "__main__":
    print("📋 EXPLORADOR DE TABLAS BIGQUERY - SMARWATT")
    print("=" * 50)

    success = list_all_tables()

    if success:
        print("✅ EXPLORACIÓN COMPLETADA EXITOSAMENTE")
    else:
        print("❌ ERROR DURANTE LA EXPLORACIÓN")
