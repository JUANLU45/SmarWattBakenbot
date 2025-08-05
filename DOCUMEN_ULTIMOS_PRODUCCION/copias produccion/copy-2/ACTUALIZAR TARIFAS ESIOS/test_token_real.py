#!/usr/bin/env python3
"""
🔍 VERIFICACIÓN REAL DEL TOKEN ESIOS
==================================
Prueba que el token funciona REALMENTE con la API oficial
"""

import requests
import json


def test_esios_token():
    """Probar el token REAL con la API ESIOS oficial"""

    # Token correcto proporcionado por el usuario
    token = "ac5c7863608aae858a07e6e31cc9497275ecbe4a5d57f6fa769abd9bee350c94"

    print("🔍 VERIFICANDO TOKEN ESIOS REAL...")
    print(f"Token: {token[:20]}...")

    try:
        # Headers exactos según documentación ESIOS
        headers = {
            "Accept": "application/json; application/vnd.esios-api-v1+json",
            "Content-Type": "application/json",
            "Host": "api.esios.ree.es",
            "x-api-key": token,
        }

        # Hacer petición REAL al indicador 1001 (PVPC)
        url = "https://api.esios.ree.es/indicators/1001"
        print(f"URL: {url}")

        response = requests.get(url, headers=headers, timeout=10)

        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            indicator = data.get("indicator", {})
            values = indicator.get("values", [])

            print("✅ TOKEN VÁLIDO - CONEXIÓN EXITOSA")
            print(f'✅ Indicador: {indicator.get("name", "N/A")}')
            print(f"✅ Valores disponibles: {len(values)}")
            print(f'✅ ID del indicador: {indicator.get("id", "N/A")}')

            if values:
                print(f'✅ Último valor: {values[-1].get("value", "N/A")} €/MWh')
                print(f'✅ Fecha último valor: {values[-1].get("datetime", "N/A")}')

            print("🎉 EL TOKEN FUNCIONA PERFECTAMENTE")
            return True

        elif response.status_code == 403:
            print("❌ HTTP 403 - Token inválido o sin permisos")
            print(f"Respuesta: {response.text[:200]}")
            return False

        else:
            print(f"❌ Error HTTP {response.status_code}")
            print(f"Respuesta: {response.text[:200]}")
            return False

    except requests.exceptions.Timeout:
        print("❌ Timeout - La API ESIOS no responde")
        return False

    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión - Verificar internet")
        return False

    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False


if __name__ == "__main__":
    success = test_esios_token()
    if success:
        print("\n🚀 LISTO PARA DESPLEGAR - El token funciona")
    else:
        print("\n🛑 NO DESPLEGAR - Hay problemas con el token")
