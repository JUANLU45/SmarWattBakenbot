#!/usr/bin/env python3
"""
🔥 SCRIPT 2/4 - EXPERT-BOT-API ENERGY ROUTES
==========================================

ENDPOINTS ENERGY (/api/v1/energy/*):
1. GET /api/v1/energy/dashboard
2. GET /api/v1/energy/users/profile
3. POST /api/v1/energy/consumption
4. POST /api/v1/energy/manual-data
5. PUT /api/v1/energy/consumption/update
6. GET /api/v1/energy/consumption/history
7. POST /api/v1/energy/consumption/analyze
8. GET /api/v1/energy/consumption/recommendations
9. POST /api/v1/energy/consumption/compare
10. PUT /api/v1/energy/consumption/title

TOTAL: 10 ENDPOINTS ENERGY
"""

import os
import sys
import json
import time
import requests
from datetime import datetime, timedelta
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


class ExpertBotEnergyTester:
    """Tester para endpoints ENERGY de expert-bot-api"""

    def __init__(self):
        self.base_url = "https://expert-bot-api-1010012211318.europe-west1.run.app"
        self.auth_headers = get_auth_headers()
        self.results = []

    def make_request(
        self, method: str, endpoint: str, data=None, params=None, files=None
    ) -> TestResult:
        """Hace petición HTTP real con autenticación Firebase"""
        url = f"{self.base_url}{endpoint}"
        headers = self.auth_headers.copy()

        if files and "Content-Type" in headers:
            del headers["Content-Type"]

        start_time = time.time()

        try:
            if method == "GET":
                response = requests.get(url, headers=headers, params=params, timeout=30)
            elif method == "POST":
                if files:
                    auth_headers = {
                        k: v for k, v in headers.items() if k == "Authorization"
                    }
                    response = requests.post(
                        url, headers=auth_headers, files=files, data=data, timeout=30
                    )
                else:
                    response = requests.post(
                        url, headers=headers, json=data, timeout=30
                    )
            elif method == "PUT":
                response = requests.put(url, headers=headers, json=data, timeout=30)
            elif method == "DELETE":
                response = requests.delete(url, headers=headers, timeout=30)

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

    def test_energy_endpoints(self):
        """Ejecuta todos los tests de endpoints energy"""
        print("🔥 TESTING EXPERT-BOT-API - ENERGY ROUTES")
        print("=" * 50)
        print(f"🔗 URL: {self.base_url}")
        print("")

        test_count = 0

        # === 1. GET /api/v1/energy/dashboard ===
        test_count += 1
        result = self.make_request("GET", "/api/v1/energy/dashboard")
        self.results.append(result)
        self.print_result(test_count, result, "GET /api/v1/energy/dashboard")

        # === 2. GET /api/v1/energy/users/profile ===
        test_count += 1
        result = self.make_request("GET", "/api/v1/energy/users/profile")
        self.results.append(result)
        self.print_result(test_count, result, "GET /api/v1/energy/users/profile")

        # === 3. POST /api/v1/energy/consumption ===
        test_count += 1
        consumption_data = {
            "consumption_kwh": 350.5,
            "billing_period_start": "2025-06-01",
            "billing_period_end": "2025-06-30",
            "cost_euros": 89.75,
            "tariff_type": "discriminacion_horaria",
        }
        result = self.make_request(
            "POST", "/api/v1/energy/consumption", data=consumption_data
        )
        self.results.append(result)
        self.print_result(test_count, result, "POST /api/v1/energy/consumption")

        # === 4. POST /api/v1/energy/manual-data ===
        test_count += 1
        manual_data = {
            "consumption_kwh": 420.3,
            "cost": 95.50,
            "period_start": "2025-07-01",
            "period_end": "2025-07-20",
            "source": "manual_entry",
        }
        result = self.make_request(
            "POST", "/api/v1/energy/manual-data", data=manual_data
        )
        self.results.append(result)
        self.print_result(test_count, result, "POST /api/v1/energy/manual-data")

        # === 5. PUT /api/v1/energy/consumption/update ===
        test_count += 1
        update_data = {
            "consumption_id": "test_consumption_id",
            "consumption_kwh": 375.0,
            "cost_euros": 92.25,
            "notes": "Consumo actualizado desde test",
        }
        result = self.make_request(
            "PUT", "/api/v1/energy/consumption/update", data=update_data
        )
        self.results.append(result)
        self.print_result(test_count, result, "PUT /api/v1/energy/consumption/update")

        # === 6. GET /api/v1/energy/consumption/history ===
        test_count += 1
        params = {"limit": 12, "period": "monthly"}
        result = self.make_request(
            "GET", "/api/v1/energy/consumption/history", params=params
        )
        self.results.append(result)
        self.print_result(test_count, result, "GET /api/v1/energy/consumption/history")

        # === 7. POST /api/v1/energy/consumption/analyze ===
        test_count += 1
        analyze_data = {
            "analysis_type": "efficiency_trends",
            "period_months": 6,
            "include_recommendations": True,
        }
        result = self.make_request(
            "POST", "/api/v1/energy/consumption/analyze", data=analyze_data
        )
        self.results.append(result)
        self.print_result(test_count, result, "POST /api/v1/energy/consumption/analyze")

        # === 8. GET /api/v1/energy/consumption/recommendations ===
        test_count += 1
        result = self.make_request("GET", "/api/v1/energy/consumption/recommendations")
        self.results.append(result)
        self.print_result(
            test_count, result, "GET /api/v1/energy/consumption/recommendations"
        )

        # === 9. POST /api/v1/energy/consumption/compare ===
        test_count += 1
        compare_data = {
            "comparison_targets": ["similar_homes", "market_average"],
            "period": "last_3_months",
        }
        result = self.make_request(
            "POST", "/api/v1/energy/consumption/compare", data=compare_data
        )
        self.results.append(result)
        self.print_result(test_count, result, "POST /api/v1/energy/consumption/compare")

        # === 10. PUT /api/v1/energy/consumption/title ===
        test_count += 1
        title_data = {
            "consumption_id": "test_consumption_id",
            "title": "Consumo Julio 2025 - Test",
            "description": "Periodo de prueba para validación",
        }
        result = self.make_request(
            "PUT", "/api/v1/energy/consumption/title", data=title_data
        )
        self.results.append(result)
        self.print_result(test_count, result, "PUT /api/v1/energy/consumption/title")

        # === RESULTADOS FINALES ===
        self.print_summary()

    def print_result(self, test_num: int, result: TestResult, description: str):
        """Imprime resultado de un test"""
        status = "✅ OK" if result.success else "❌ FALLO"
        print(
            f"[{test_num}/10] {status} | {result.status_code} | {result.response_time:.2f}s | {description}"
        )
        if not result.success and result.error_message:
            print(f"   Error: {result.error_message}")
        if result.success and result.response_data:
            # Mostrar datos relevantes
            if "dashboard" in description.lower():
                print(f"   ✅ Dashboard data disponible")
            elif "consumption" in description.lower():
                print(f"   ✅ Consumption data procesada")

    def print_summary(self):
        """Imprime resumen final"""
        successful = len([r for r in self.results if r.success])
        total = len(self.results)
        success_rate = (successful / total) * 100

        print("\n" + "=" * 50)
        print("📊 RESULTADOS FINALES ENERGY:")
        print(f"✅ Exitosos: {successful}/{total}")
        print(f"❌ Fallidos: {total - successful}/{total}")
        print(f"📈 Tasa éxito: {success_rate:.1f}%")

        if success_rate >= 70:
            print("🎉 ENDPOINTS ENERGY FUNCIONANDO")
        else:
            print("⚠️ PROBLEMAS EN ENDPOINTS ENERGY")


def main():
    """Función principal"""
    print("🚀 INICIANDO TESTS ENERGY - EXPERT-BOT-API")
    print("🔐 Configurando autenticación Firebase...")

    try:
        tester = ExpertBotEnergyTester()
        print("✅ Autenticación configurada")
        tester.test_energy_endpoints()
    except Exception as e:
        print(f"❌ Error fatal: {e}")


if __name__ == "__main__":
    main()
