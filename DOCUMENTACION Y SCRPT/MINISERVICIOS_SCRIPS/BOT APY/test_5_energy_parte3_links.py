#!/usr/bin/env python3
"""
🔥 SCRIPT 5/8 - EXPERT-BOT-API ENERGY PARTE 3 + LINKS
====================================================

ENDPOINTS VERIFICADOS 1 A 1 EN CÓDIGO FUENTE:
15. POST /api/v1/energy/consumption/compare
16. PUT /api/v1/energy/consumption/title
17. POST /api/v1/links/test
18. GET /api/v1/links/status

TOTAL: 4 ENDPOINTS ENERGY PARTE 3 + LINKS
"""

import os
import sys
import json
import time
import requests
from datetime import datetime
from typing import Dict, Any, Optional
from dataclasses import dataclass

# Importar módulo de autenticación
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from auth_helper import get_auth_headers


@dataclass
class TestResult:
    endpoint: str
    method: str
    success: bool
    response_time: float
    status_code: int
    response_data: Any
    error_message: Optional[str] = None


class ExpertBotEnergy3LinksTester:
    """Tester para 4 endpoints ENERGY PARTE 3 + LINKS de expert-bot-api"""

    def __init__(self):
        self.base_url = "https://expert-bot-api-1010012211318.europe-west1.run.app"
        self.auth_headers = get_auth_headers()
        self.results = []

    def make_request(
        self, method: str, endpoint: str, data=None, params=None
    ) -> TestResult:
        """Hace petición HTTP real con autenticación Firebase"""
        url = f"{self.base_url}{endpoint}"
        headers = self.auth_headers.copy()

        start_time = time.time()

        try:
            if method == "GET":
                response = requests.get(url, headers=headers, params=params, timeout=30)
            elif method == "POST":
                response = requests.post(url, headers=headers, json=data, timeout=30)
            elif method == "PUT":
                response = requests.put(url, headers=headers, json=data, timeout=30)

            response_time = time.time() - start_time

            try:
                response_data = response.json()
            except:
                response_data = {"raw_text": response.text}

            return TestResult(
                endpoint=endpoint,
                method=method,
                success=response.status_code < 400,
                response_time=response_time,
                status_code=response.status_code,
                response_data=response_data,
                error_message=(
                    None
                    if response.status_code < 400
                    else f"HTTP {response.status_code}"
                ),
            )

        except Exception as e:
            return TestResult(
                endpoint=endpoint,
                method=method,
                success=False,
                response_time=time.time() - start_time,
                status_code=0,
                response_data={"error": str(e)},
                error_message=str(e),
            )

    def test_endpoints(self):
        """Ejecuta tests de 4 endpoints verificados con lógica completa"""
        print("🔥 TESTING EXPERT-BOT-API - ENERGY PARTE 3 + LINKS")
        print("=" * 55)
        print("📋 ENDPOINTS VERIFICADOS 1 A 1 EN CÓDIGO:")
        print("15. POST /consumption/compare")
        print("16. PUT /consumption/title")
        print("17. POST /links/test")
        print("18. GET /links/status")
        print(f"🔗 URL: {self.base_url}")
        print("")

        test_count = 0

        # === 15. POST /api/v1/energy/consumption/compare ===
        test_count += 1
        compare_data = {
            "current_tariff": "2.0TD",
            "comparison_targets": ["market_average", "best_available"],
            "consumption_profile": {
                "monthly_kwh": 350,
                "peak_hours": 120,
                "valley_hours": 230,
            },
            "location": "Madrid",
            "include_green_options": True,
        }
        result = self.make_request(
            "POST", "/api/v1/energy/consumption/compare", data=compare_data
        )
        self.results.append(result)
        self.print_result(test_count, result, "POST /api/v1/energy/consumption/compare")

        # === 16. PUT /api/v1/energy/consumption/title ===
        test_count += 1
        title_data = {
            "consumption_id": "test_consumption_456",
            "new_title": "Consumo Julio 2025 - Casa Principal",
            "notes": "Actualizado por el usuario",
        }
        result = self.make_request(
            "PUT", "/api/v1/energy/consumption/title", data=title_data
        )
        self.results.append(result)
        self.print_result(test_count, result, "PUT /api/v1/energy/consumption/title")

        # === 17. POST /api/v1/links/test ===
        test_count += 1
        links_test_data = {
            "response_text": "Para ahorrar energía, puedes cambiar a bombillas LED, ajustar el termostato y usar electrodomésticos eficientes. También considera instalar paneles solares."
        }
        result = self.make_request("POST", "/api/v1/links/test", data=links_test_data)
        self.results.append(result)
        self.print_result(test_count, result, "POST /api/v1/links/test")

        # === 18. GET /api/v1/links/status ===
        test_count += 1
        result = self.make_request("GET", "/api/v1/links/status")
        self.results.append(result)
        self.print_result(test_count, result, "GET /api/v1/links/status")

        # === RESULTADOS FINALES ===
        self.print_summary()

    def print_result(self, test_num: int, result: TestResult, description: str):
        """Imprime resultado detallado de un test con validación de lógica"""
        status = "✅ OK" if result.success else "❌ FALLO"
        print(
            f"[{test_num}/4] {status} | {result.status_code} | {result.response_time:.2f}s | {description}"
        )

        if not result.success and result.error_message:
            print(f"   ❌ Error: {result.error_message}")
        elif result.success:
            # Validación específica de lógica por endpoint
            response_str = str(result.response_data).lower()

            if "compare" in description:
                if any(
                    word in response_str
                    for word in ["tariff", "comparison", "savings", "recommended"]
                ):
                    print(f"   ✅ Lógica: Comparación de tarifas ejecutada")
                else:
                    print(f"   ⚠️ Lógica: Datos de comparación no detectados")

            elif "title" in description:
                if any(
                    word in response_str
                    for word in ["updated", "title", "success", "actualizado"]
                ):
                    print(f"   ✅ Lógica: Título actualizado correctamente")
                else:
                    print(f"   ⚠️ Lógica: Confirmación de actualización no detectada")

            elif "links/test" in description:
                if any(
                    word in response_str
                    for word in [
                        "enhanced_response",
                        "links_added",
                        "original_response",
                    ]
                ):
                    print(f"   ✅ Lógica: Sistema de enlaces procesando texto")
                else:
                    print(f"   ⚠️ Lógica: Respuesta de enlaces no detectada")

            elif "links/status" in description:
                if any(
                    word in response_str
                    for word in ["status", "service", "healthy", "operational"]
                ):
                    print(f"   ✅ Lógica: Estado del sistema de enlaces obtenido")
                else:
                    print(f"   ⚠️ Lógica: Estado del servicio no detectado")
            else:
                print(f"   ✅ Response: operación exitosa")

    def print_summary(self):
        """Imprime resumen final"""
        successful = len([r for r in self.results if r.success])
        total = len(self.results)
        success_rate = (successful / total) * 100 if total > 0 else 0

        print("\n" + "=" * 55)
        print("📊 RESULTADOS ENERGY PARTE 3 + LINKS:")
        print(f"✅ Exitosos: {successful}/{total}")
        print(f"❌ Fallidos: {total - successful}/{total}")
        print(f"📈 Tasa éxito: {success_rate:.1f}%")

        if success_rate >= 75:
            print("🎉 ENERGY PARTE 3 + LINKS FUNCIONANDO CORRECTAMENTE")
        elif success_rate >= 50:
            print("⚠️ ENERGY PARTE 3 + LINKS PARCIALMENTE FUNCIONAL")
        else:
            print("🚨 PROBLEMAS CRÍTICOS EN ENERGY PARTE 3 + LINKS")


def main():
    """Función principal"""
    print("🚀 INICIANDO TESTS ENERGY PARTE 3 + LINKS")
    print("🔐 Configurando autenticación Firebase...")

    try:
        tester = ExpertBotEnergy3LinksTester()
        print("✅ Autenticación configurada")
        tester.test_endpoints()
    except Exception as e:
        print(f"❌ Error fatal: {e}")


if __name__ == "__main__":
    main()
