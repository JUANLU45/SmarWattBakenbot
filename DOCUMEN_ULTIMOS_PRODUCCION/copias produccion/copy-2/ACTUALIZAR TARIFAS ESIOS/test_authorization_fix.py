#!/usr/bin/env python
"""
🔧 TEST ESPECÍFICO: VERIFICAR CORRECCIÓN DE AUTHORIZATION HEADER
"""

import requests
import os


def test_esios_authorization_fixed():
    """🔍 Probar con el formato de autorización correcto"""

    api_key = os.getenv(
        "ESIOS_API_KEY",
        "ac5c7863608aae858a07e6e31cc9497275ecbe4a5d57f66fa769abd9bee350c94",
    )

    print("🔧 PROBANDO CORRECCIÓN DE AUTHORIZATION HEADER")
    print("=" * 50)

    # Configurar headers como en el código corregido
    session = requests.Session()
    session.headers.update(
        {
            "Accept": "application/json; application/vnd.esios-api-v1+json",
            "Content-Type": "application/json",
            "Authorization": f"Token token={api_key}",  # FORMATO CORRECTO
            "User-Agent": "SmarWatt-ESIOS-Updater/1.0",
        }
    )

    # Probar endpoint básico
    url = "https://api.esios.ree.es/v1/indicators/1001"

    print(f"🌐 URL: {url}")
    print(f"🔑 Authorization: Token token={api_key[:10]}...{api_key[-4:]}")

    try:
        response = session.get(url, timeout=30)

        print(f"\n📊 RESULTADO:")
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            print("✅ CORRECCIÓN EXITOSA - API KEY FUNCIONA")
            data = response.json()
            indicator = data.get("indicator", {})
            print(f"   Indicador: {indicator.get('name', 'N/A')}")
            print(f"   ID: {indicator.get('id', 'N/A')}")
            print(f"   Tipo: {indicator.get('data_type', 'N/A')}")

        elif response.status_code == 401:
            print("❌ TODAVÍA ERROR 401 - API key inválida")

        elif response.status_code == 403:
            print("❌ TODAVÍA ERROR 403 - Sin permisos")

        else:
            print(f"❌ ERROR HTTP {response.status_code}")

        print(f"\nRespuesta: {response.text[:300]}")

    except Exception as e:
        print(f"❌ Error de conexión: {e}")


if __name__ == "__main__":
    test_esios_authorization_fixed()
