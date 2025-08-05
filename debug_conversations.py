#!/usr/bin/env python3
"""
🔍 VERIFICACIÓN MILIMÉTRICAMENTE PERFECTA DE CONVERSACIONES
Script para identificar exactamente por qué las conversaciones devuelven 0 resultados
"""

import os
import sys
import json
import requests
from datetime import datetime
from google.cloud import bigquery

# Configuración de variables de entorno
os.environ.update(
    {
        "GCP_PROJECT_ID": "smatwatt",
        "BQ_DATASET_ID": "smartwatt_data",
        "BQ_CONVERSATIONS_TABLE_ID": "conversations_log",
        "GOOGLE_APPLICATION_CREDENTIALS": "C:/Smarwatt_2/SmarWatt_2/backend/sevicio chatbot/servicios/energy_ia_api_COPY/config/google-credentials.json",
    }
)


def check_bigquery_table():
    """🔍 Verificar estructura y contenido de la tabla BigQuery"""
    try:
        print("🔍 VERIFICANDO TABLA BIGQUERY...")

        project_id = os.getenv("GCP_PROJECT_ID")
        dataset_id = os.getenv("BQ_DATASET_ID")
        table_id = os.getenv("BQ_CONVERSATIONS_TABLE_ID")

        client = bigquery.Client(project=project_id)
        full_table_id = f"{project_id}.{dataset_id}.{table_id}"

        # 1. Verificar que la tabla existe
        try:
            table = client.get_table(full_table_id)
            print(f"✅ Tabla encontrada: {full_table_id}")
            print(f"📊 Total de filas: {table.num_rows}")
        except Exception as e:
            print(f"❌ Error accediendo a tabla: {e}")
            return False

        # 2. Verificar estructura de la tabla
        print("\n📋 ESTRUCTURA DE LA TABLA:")
        for field in table.schema:
            print(f"   {field.name}: {field.field_type}")

        # 3. Verificar datos recientes
        query = f"""
        SELECT 
            user_id,
            conversation_id,
            message_text,
            response_text,
            timestamp_utc,
            deleted
        FROM `{full_table_id}`
        ORDER BY timestamp_utc DESC
        LIMIT 10
        """

        print(f"\n🔎 EJECUTANDO QUERY:")
        print(query)

        query_job = client.query(query)
        results = query_job.result()

        rows = list(results)
        print(f"\n📊 RESULTADOS ENCONTRADOS: {len(rows)}")

        if rows:
            print("\n📝 PRIMERAS 5 FILAS:")
            for i, row in enumerate(rows[:5]):
                print(f"   {i+1}. user_id: {row.user_id}")
                print(f"      conversation_id: {row.conversation_id}")
                print(
                    f"      message: {row.message_text[:50] if row.message_text else 'None'}..."
                )
                print(f"      timestamp: {row.timestamp_utc}")
                print(f"      deleted: {row.deleted}")
                print()
        else:
            print("⚠️  No hay datos en la tabla")

        # 4. Contar por user_id
        count_query = f"""
        SELECT 
            user_id,
            COUNT(*) as conversation_count
        FROM `{full_table_id}`
        WHERE deleted IS NULL OR deleted = false
        GROUP BY user_id
        ORDER BY conversation_count DESC
        LIMIT 10
        """

        print(f"\n📊 CONTEO POR USUARIO:")
        count_job = client.query(count_query)
        count_results = count_job.result()

        for row in count_results:
            print(f"   User: {row.user_id} → {row.conversation_count} conversaciones")

        return True

    except Exception as e:
        print(f"❌ Error verificando BigQuery: {e}")
        return False


def test_conversations_endpoint():
    """🔍 Probar el endpoint de conversaciones directamente"""
    try:
        print("\n🌐 PROBANDO ENDPOINT DE CONVERSACIONES...")

        # Usar un user_id de prueba (puedes cambiar esto)
        test_user_id = "test_user_123"

        # URL del endpoint
        url = "http://localhost:8080/api/v1/chatbot/conversations"

        # Headers con token de prueba (ajustar según tu auth)
        headers = {
            "Authorization": "Bearer test_token",
            "Content-Type": "application/json",
        }

        print(f"📡 Haciendo request a: {url}")
        print(f"🔑 Headers: {headers}")

        response = requests.get(url, headers=headers, timeout=10)

        print(f"📊 Status Code: {response.status_code}")
        print(f"📋 Response:")
        print(json.dumps(response.json(), indent=2))

        return response.status_code == 200

    except requests.exceptions.ConnectionError:
        print(
            "❌ No se puede conectar al servidor - ¿está ejecutándose en puerto 8080?"
        )
        return False
    except Exception as e:
        print(f"❌ Error probando endpoint: {e}")
        return False


def main():
    """🎯 Verificación completa del sistema de conversaciones"""
    print("🚀 INICIANDO VERIFICACIÓN COMPLETA DE CONVERSACIONES")
    print("=" * 60)

    # 1. Verificar BigQuery
    bq_ok = check_bigquery_table()

    # 2. Verificar endpoint
    # endpoint_ok = test_conversations_endpoint()

    print("\n" + "=" * 60)
    print("📋 RESUMEN DE VERIFICACIÓN:")
    print(f"   BigQuery: {'✅ OK' if bq_ok else '❌ FALLA'}")
    # print(f"   Endpoint: {'✅ OK' if endpoint_ok else '❌ FALLA'}")

    if bq_ok:
        print("\n💡 RECOMENDACIONES:")
        print(
            "   1. Verificar que el user_id en el frontend coincida con los datos en BigQuery"
        )
        print("   2. Comprobar que el token de autenticación sea válido")
        print("   3. Verificar logs del servidor para errores específicos")
        print(
            "   4. Confirmar que las variables de entorno estén configuradas correctamente"
        )


if __name__ == "__main__":
    main()
