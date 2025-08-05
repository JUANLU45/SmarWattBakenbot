#!/usr/bin/env python
"""
🔍 DIAGNÓSTICO DETALLADO ESIOS API
Análisis profundo del problema con indicador 1001
"""

import requests
import json
import os
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class ESIOSConfig:
    """📋 Configuración ESIOS API"""

    api_key: str
    api_base_url: str = "https://api.esios.ree.es/v1"
    indicators_endpoint: str = "/indicators"
    pvpc_indicator_id: int = 1001  # Precio PVPC oficial
    request_timeout: int = 30
    max_retries: int = 3
    retry_delay: int = 2


class ESIOSDetailedDiagnoser:
    """🔬 Diagnóstico detallado ESIOS"""

    def __init__(self, api_key: str):
        self.config = ESIOSConfig(api_key=api_key)
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/json; application/vnd.esios-api-v1+json",
                "Content-Type": "application/json",
                "Host": "api.esios.ree.es",
                "Authorization": f"Token token={self.config.api_key}",
                "X-Requested-With": "XMLHttpRequest",
            }
        )

    def test_api_connectivity(self) -> Dict[str, Any]:
        """🌐 Probar conectividad básica"""

        print("🔍 1. PROBANDO CONECTIVIDAD BÁSICA...")

        try:
            response = self.session.get(
                f"{self.config.api_base_url}/archives",
                timeout=self.config.request_timeout,
            )

            result = {
                "status_code": response.status_code,
                "success": response.status_code == 200,
                "headers": dict(response.headers),
                "response_size": len(response.content),
            }

            if response.status_code == 200:
                print("✅ Conectividad OK")
            else:
                print(f"❌ Error HTTP {response.status_code}")
                print(f"Response: {response.text[:500]}")

            return result

        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            return {"success": False, "error": str(e)}

    def test_indicator_exists(self, indicator_id: int) -> Dict[str, Any]:
        """🔍 Verificar si el indicador existe"""

        print(f"🔍 2. VERIFICANDO INDICADOR {indicator_id}...")

        try:
            # Obtener información del indicador sin datos
            url = f"{self.config.api_base_url}{self.config.indicators_endpoint}/{indicator_id}"

            response = self.session.get(url, timeout=self.config.request_timeout)

            result = {
                "status_code": response.status_code,
                "success": response.status_code == 200,
                "response_size": len(response.content),
            }

            if response.status_code == 200:
                data = response.json()
                indicator_info = data.get("indicator", {})

                result.update(
                    {
                        "indicator_name": indicator_info.get("name"),
                        "indicator_short_name": indicator_info.get("short_name"),
                        "indicator_id": indicator_info.get("id"),
                        "data_type": indicator_info.get("data_type"),
                        "step_type": indicator_info.get("step_type"),
                        "time_granularity": indicator_info.get("time_granularity"),
                    }
                )

                print(f"✅ Indicador encontrado: {result['indicator_name']}")
                print(f"   ID: {result['indicator_id']}")
                print(f"   Nombre corto: {result['indicator_short_name']}")
                print(f"   Tipo: {result['data_type']}")

            else:
                print(f"❌ Indicador no encontrado - HTTP {response.status_code}")
                result["error_response"] = response.text[:500]

            return result

        except Exception as e:
            print(f"❌ Error verificando indicador: {e}")
            return {"success": False, "error": str(e)}

    def test_data_fetch(self, indicator_id: int, days_back: int = 1) -> Dict[str, Any]:
        """📊 Probar obtención de datos reales"""

        print(f"🔍 3. PROBANDO OBTENCIÓN DE DATOS (últimos {days_back} días)...")

        try:
            # Fechas para obtener datos recientes
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)

            start_date_str = start_date.strftime("%Y-%m-%dT00:00")
            end_date_str = end_date.strftime("%Y-%m-%dT23:59")

            url = f"{self.config.api_base_url}{self.config.indicators_endpoint}/{indicator_id}"
            params = {
                "start_date": start_date_str,
                "end_date": end_date_str,
                "time_trunc": "hour",
            }

            print(f"   URL: {url}")
            print(f"   Parámetros: {params}")

            response = self.session.get(
                url, params=params, timeout=self.config.request_timeout
            )

            result = {
                "status_code": response.status_code,
                "success": response.status_code == 200,
                "url": response.url,
                "params_used": params,
            }

            if response.status_code == 200:
                data = response.json()
                indicator = data.get("indicator", {})
                values = indicator.get("values", [])

                result.update(
                    {
                        "total_values": len(values),
                        "first_value": values[0] if values else None,
                        "last_value": values[-1] if values else None,
                        "indicator_info": {
                            "name": indicator.get("name"),
                            "id": indicator.get("id"),
                            "data_type": indicator.get("data_type"),
                        },
                    }
                )

                print(f"✅ Datos obtenidos: {len(values)} valores")
                if values:
                    print(f"   Primer valor: {values[0]}")
                    print(f"   Último valor: {values[-1]}")
                else:
                    print("⚠️ No hay valores en el rango solicitado")

            else:
                print(f"❌ Error obteniendo datos - HTTP {response.status_code}")
                result["error_response"] = response.text[:1000]

            return result

        except Exception as e:
            print(f"❌ Error obteniendo datos: {e}")
            return {"success": False, "error": str(e)}

    def comprehensive_diagnosis(self) -> Dict[str, Any]:
        """🔬 Diagnóstico completo"""

        print("=" * 60)
        print("🔬 DIAGNÓSTICO DETALLADO ESIOS API")
        print("=" * 60)

        results = {}

        # Test 1: Conectividad
        results["connectivity"] = self.test_api_connectivity()

        # Test 2: Indicador existe
        results["indicator_check"] = self.test_indicator_exists(
            self.config.pvpc_indicator_id
        )

        # Test 3: Obtención de datos
        results["data_fetch"] = self.test_data_fetch(self.config.pvpc_indicator_id)

        # Resumen
        print("\n" + "=" * 60)
        print("📋 RESUMEN DEL DIAGNÓSTICO")
        print("=" * 60)

        connectivity_ok = results["connectivity"].get("success", False)
        indicator_ok = results["indicator_check"].get("success", False)
        data_ok = results["data_fetch"].get("success", False)

        print(f"🌐 Conectividad API: {'✅ OK' if connectivity_ok else '❌ FALLO'}")
        print(f"🔍 Indicador 1001: {'✅ EXISTE' if indicator_ok else '❌ NO EXISTE'}")
        print(f"📊 Obtención datos: {'✅ OK' if data_ok else '❌ FALLO'}")

        # Análisis del problema
        if not connectivity_ok:
            print("\n🚨 PROBLEMA: No hay conectividad con ESIOS API")
        elif not indicator_ok:
            print("\n🚨 PROBLEMA: El indicador 1001 no existe o no es accesible")
        elif not data_ok:
            print("\n🚨 PROBLEMA: El indicador existe pero no se pueden obtener datos")

            if results["data_fetch"].get("status_code") == 404:
                print("   - Posible causa: Indicador sin datos en el rango solicitado")
            elif results["data_fetch"].get("status_code") == 401:
                print("   - Posible causa: API Key inválida o sin permisos")
            elif results["data_fetch"].get("status_code") == 429:
                print("   - Posible causa: Rate limit excedido")
        else:
            print("\n✅ TODO FUNCIONA CORRECTAMENTE")
            total_values = results["data_fetch"].get("total_values", 0)
            print(f"   - Se obtuvieron {total_values} valores correctamente")

        return results


def main():
    """🚀 Ejecutar diagnóstico"""

    # Obtener API key
    api_key = os.getenv("ESIOS_API_KEY")

    if not api_key:
        print("❌ ERROR: Variable ESIOS_API_KEY no encontrada")
        print("💡 Configurar con: $env:ESIOS_API_KEY='tu_api_key'")
        return

    print(f"🔑 Usando API Key: {api_key[:10]}...{api_key[-4:]}")

    # Ejecutar diagnóstico
    diagnoser = ESIOSDetailedDiagnoser(api_key)
    results = diagnoser.comprehensive_diagnosis()

    # Guardar resultados
    with open("esios_diagnosis_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Resultados guardados en: esios_diagnosis_results.json")


if __name__ == "__main__":
    main()
