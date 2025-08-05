#!/usr/bin/env python3
"""
📊 EXPLORADOR DETALLADO DE ESQUEMAS BIGQUERY - SMARWATT
======================================================

Genera un reporte completo con todos los campos de todas las tablas.
Guarda la información en un archivo de texto para consulta posterior.

USO:
    python explore_schemas.py

SALIDA:
    - Archivo: bigquery_schemas_report.txt
    - Información completa de cada tabla y sus campos

AUTOR: Sistema de verificación empresarial
FECHA: 2025-08-03
"""

from google.cloud import bigquery
from google.oauth2 import service_account
import os
from datetime import datetime


def explore_all_schemas():
    """📊 Explora y documenta todos los esquemas de BigQuery"""

    # CONFIGURAR CREDENCIALES - MISMA RUTA QUE EL SCRIPT ANTERIOR
    credentials_path = r"C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\DOCUMENTACION Y SCRPT\MINISERVICIOS_SCRIPS\ESCRIP ADMIN\firebase-adminsdk-fbsvc-key.json"

    if not os.path.exists(credentials_path):
        print(
            f"❌ ERROR: No se encontró el archivo de credenciales en: {credentials_path}"
        )
        return False

    print(f"🔑 Usando credenciales desde: {credentials_path}")
    print(f"📅 Iniciando exploración detallada: {datetime.now().isoformat()}")

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

    # Archivo de salida
    output_file = "bigquery_schemas_report.txt"

    print(f"\n{'='*60}")
    print(f"📊 GENERANDO REPORTE DETALLADO: {dataset_id}")
    print(f"📄 Archivo de salida: {output_file}")
    print(f"{'='*60}")

    try:
        # Obtener referencia al dataset
        dataset_ref = client.dataset(dataset_id)

        # Listar todas las tablas
        tables = list(client.list_tables(dataset_ref))

        if not tables:
            print("⚠️  No se encontraron tablas en el dataset")
            return True

        # Abrir archivo para escribir
        with open(output_file, "w", encoding="utf-8") as f:
            # Escribir encabezado
            f.write("=" * 80 + "\\n")
            f.write("📊 REPORTE COMPLETO DE ESQUEMAS BIGQUERY - SMARWATT\\n")
            f.write("=" * 80 + "\\n")
            f.write(f"📅 Generado: {datetime.now().isoformat()}\\n")
            f.write(f"🗂️  Dataset: {project_id}.{dataset_id}\\n")
            f.write(f"📋 Total tablas: {len(tables)}\\n")
            f.write("=" * 80 + "\\n\\n")

            print(f"✅ PROCESANDO {len(tables)} TABLAS...")

            for i, table in enumerate(tables, 1):
                print(f"   📋 {i}/{len(tables)}: {table.table_id}")

                # Obtener información detallada de la tabla
                table_ref = dataset_ref.table(table.table_id)
                table_info = client.get_table(table_ref)

                # Escribir información de la tabla
                f.write(f"📋 TABLA {i}: {table.table_id.upper()}\\n")
                f.write("-" * 60 + "\\n")
                f.write(f"🆔 ID Completo: {table_info.full_table_id}\\n")
                f.write(f"📊 Total Campos: {len(table_info.schema)}\\n")

                if table_info.num_rows is not None:
                    f.write(f"📈 Registros: {table_info.num_rows:,}\\n")
                else:
                    f.write("📈 Registros: N/A\\n")

                if table_info.created:
                    f.write(
                        f"📅 Creada: {table_info.created.strftime('%Y-%m-%d %H:%M:%S')}\\n"
                    )

                if table_info.modified:
                    f.write(
                        f"🔄 Modificada: {table_info.modified.strftime('%Y-%m-%d %H:%M:%S')}\\n"
                    )

                f.write(f"💾 Tamaño: {table_info.num_bytes / (1024*1024):.2f} MB\\n")
                f.write("\\n")

                # Escribir esquema detallado
                f.write("🔧 ESQUEMA DETALLADO:\\n")
                f.write("-" * 40 + "\\n")

                for j, field in enumerate(table_info.schema, 1):
                    f.write(f"  {j:2d}. {field.name}\\n")
                    f.write(f"      📝 Tipo: {field.field_type}\\n")
                    f.write(f"      🔒 Modo: {field.mode}\\n")

                    if field.description:
                        f.write(f"      📋 Descripción: {field.description}\\n")
                    else:
                        f.write("      📋 Descripción: (Sin descripción)\\n")

                    # Información adicional para campos específicos
                    if field.field_type == "RECORD" and field.fields:
                        f.write(f"      🏗️  Subcampos: {len(field.fields)}\\n")
                        for subfield in field.fields:
                            f.write(
                                f"         • {subfield.name} ({subfield.field_type})\\n"
                            )

                    f.write("\\n")

                f.write("=" * 80 + "\\n\\n")

            # Escribir resumen final
            f.write("📊 RESUMEN FINAL\\n")
            f.write("=" * 40 + "\\n")
            f.write(f"📋 Total tablas procesadas: {len(tables)}\\n")

            total_fields = sum(
                len(client.get_table(dataset_ref.table(table.table_id)).schema)
                for table in tables
            )
            f.write(f"🔧 Total campos en dataset: {total_fields}\\n")

            f.write(f"📅 Reporte generado: {datetime.now().isoformat()}\\n")
            f.write("=" * 80 + "\\n")

        print(f"\\n✅ REPORTE GENERADO EXITOSAMENTE")
        print(f"📄 Archivo: {os.path.abspath(output_file)}")
        print(f"📊 {len(tables)} tablas documentadas")

        return True

    except Exception as e:
        print(f"❌ ERROR generando reporte: {str(e)}")
        return False


if __name__ == "__main__":
    print("📊 EXPLORADOR DETALLADO DE ESQUEMAS BIGQUERY - SMARWATT")
    print("=" * 60)

    success = explore_all_schemas()

    if success:
        print("\\n🎉 EXPLORACIÓN DETALLADA COMPLETADA EXITOSAMENTE")
        print("📋 Consulta el archivo generado para ver todos los detalles")
    else:
        print("\\n❌ ERROR DURANTE LA EXPLORACIÓN DETALLADA")
