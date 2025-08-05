#!/usr/bin/env python3
"""
📊 TEST CONSULTA MERCADO - SIN PERMISOS ADMIN
============================================

Prueba específica del endpoint de consulta de tarifas
que no requiere permisos de administrador.

ENDPOINT A PROBAR:
- GET /tariffs/market-data (Consulta pública)
"""

import sys
import os
import requests
import json
import time
from datetime import datetime, timezone

# Añadir ruta del módulo de autenticación
sys.path.append(os.path.dirname(__file__))
from auth_helper import SmarWattAuth


def test_market_data_public():
    """Test del endpoint público de datos de mercado"""
    print("📊 TEST: GET /tariffs/market-data (CONSULTA PÚBLICA)")
    print("=" * 55)

    energy_ia_url = "https://energy-ia-api-1010012211318.europe-west1.run.app"
    auth_helper = SmarWattAuth()

    # Obtener token de usuario normal (no admin) - usar un usuario real existente
    user_token = auth_helper.get_production_user_token(
        "56bE1dNrjef8kO0Erg1qKQytKAq2"
    )  # Tomates Juanlu como usuario

    headers = {
        "Authorization": f"Bearer {user_token}",
        "Content-Type": "application/json",
        "User-Agent": "SmarWatt-Market-Test/1.0",
    }

    url = f"{energy_ia_url}/tariffs/market-data"

    try:
        start_time = time.time()
        response = requests.get(url, headers=headers)
        duration = time.time() - start_time

        print(f"🔗 URL: {url}")
        print(f"⏱️ Tiempo: {duration:.2f}s")
        print(f"📊 Status: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print(f"✅ ÉXITO: Datos de mercado obtenidos")

            # Análisis de los datos
            if isinstance(result, dict):
                if "tariffs" in result:
                    tariffs = result["tariffs"]
                    print(f"📈 Total tarifas disponibles: {len(tariffs)}")

                    # Análisis por tipo de tarifa
                    types = {}
                    suppliers = set()

                    for tariff in tariffs:
                        tariff_type = tariff.get("tariff_type", "Unknown")
                        types[tariff_type] = types.get(tariff_type, 0) + 1
                        suppliers.add(tariff.get("supplier_name", "Unknown"))

                    print(f"📊 Distribución por tipo:")
                    for t_type, count in types.items():
                        print(f"   - {t_type}: {count} tarifas")

                    print(f"🏢 Total proveedores: {len(suppliers)}")

                    # Mostrar algunas tarifas de ejemplo
                    print(f"📋 Ejemplos de tarifas:")
                    for i, tariff in enumerate(tariffs[:3]):
                        print(
                            f"   {i+1}. {tariff.get('supplier_name', 'N/A')} - {tariff.get('tariff_name', 'N/A')}"
                        )
                        print(
                            f"      Tipo: {tariff.get('tariff_type', 'N/A')} | Precio fijo: {tariff.get('fixed_term_price', 'N/A')}€"
                        )

                if "statistics" in result:
                    stats = result["statistics"]
                    print(f"📈 Estadísticas del mercado:")
                    print(f"{json.dumps(stats, indent=2)}")

            return True

        elif response.status_code == 403:
            print(f"❌ ERROR 403: Sin permisos")
            print(f"🔍 Respuesta: {response.text}")
            return False

        elif response.status_code == 404:
            print(f"❌ ERROR 404: Endpoint no encontrado")
            print(f"🔍 Respuesta: {response.text}")
            return False

        else:
            print(f"❌ ERROR {response.status_code}: {response.text}")
            return False

    except requests.exceptions.ConnectionError as e:
        print(f"❌ ERROR DE CONEXIÓN: {e}")
        return False
    except Exception as e:
        print(f"❌ EXCEPCIÓN: {e}")
        return False


def test_market_data_no_auth():
    """Test del endpoint sin autenticación"""
    print(f"\n📊 TEST: GET /tariffs/market-data (SIN AUTENTICACIÓN)")
    print("=" * 55)

    energy_ia_url = "https://energy-ia-api-1010012211318.europe-west1.run.app"

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "SmarWatt-Market-Test-NoAuth/1.0",
    }

    url = f"{energy_ia_url}/tariffs/market-data"

    try:
        start_time = time.time()
        response = requests.get(url, headers=headers)
        duration = time.time() - start_time

        print(f"🔗 URL: {url}")
        print(f"⏱️ Tiempo: {duration:.2f}s")
        print(f"📊 Status: {response.status_code}")

        if response.status_code == 200:
            print(f"✅ ÉXITO: Endpoint público accesible sin autenticación")
            return True
        elif response.status_code == 401:
            print(f"🔐 INFO: Endpoint requiere autenticación (esperado)")
            return True  # Es esperado que requiera auth
        else:
            print(f"❌ ERROR {response.status_code}: {response.text}")
            return False

    except Exception as e:
        print(f"❌ EXCEPCIÓN: {e}")
        return False


if __name__ == "__main__":
    print("🚀 INICIANDO TEST DE CONSULTA DE MERCADO")
    print("=" * 50)
    print(f"🕐 Fecha: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")

    results = []

    # Test 1: Con autenticación de usuario
    results.append(test_market_data_public())

    # Test 2: Sin autenticación
    results.append(test_market_data_no_auth())

    # Resumen
    print(f"\n📊 RESUMEN FINAL:")
    print(f"✅ Tests exitosos: {sum(results)}/{len(results)}")
    print(f"❌ Tests fallidos: {len(results) - sum(results)}/{len(results)}")

    if all(results):
        print(f"🎉 ENDPOINT DE CONSULTA DE MERCADO FUNCIONANDO CORRECTAMENTE")
    else:
        print(f"⚠️ PROBLEMAS DETECTADOS EN CONSULTA DE MERCADO")
