#!/usr/bin/env python3
"""
🔥 SCRIPT 4/8 - EXPERT-BOT-API ENERGY PARTE 2
=============================================

ENDPOINTS VERIFICADOS 1 A 1 EN CÓDIGO FUENTE:
11. PUT /api/v1/energy/consumption/update
12. GET /api/v1/energy/consumption/history
13. POST /api/v1/energy/consumption/analyze
14. GET /api/v1/energy/consumption/recommendations

TOTAL: 4 ENDPOINTS ENERGY PARTE 2
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


class ExpertBotEnergy2Tester:
    """Tester para 4 endpoints ENERGY PARTE 2 de expert-bot-api"""

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
        """Ejecuta tests de 4 endpoints energy verificados con lógica completa"""
        print("🔥 TESTING EXPERT-BOT-API - ENERGY PARTE 2")
        print("=" * 50)
        print("📋 ENDPOINTS VERIFICADOS 1 A 1 EN CÓDIGO:")
        print("11. PUT /consumption/update")
        print("12. GET /consumption/history")
        print("13. POST /consumption/analyze")
        print("14. GET /consumption/recommendations")
        print(f"🔗 URL: {self.base_url}")
        print("")

        test_count = 0

        # === 11. PUT /api/v1/energy/consumption/update ===
        test_count += 1
        update_data = {
            "consumption_id": "test_consumption_123",
            "kwh": 380.5,
            "cost": 72.30,
            "period_start": "2025-06-01",
            "period_end": "2025-06-30",
            "supplier": "Endesa",
            "tariff_name": "Plan Tempo",
            "notes": "Consumo actualizado por el usuario",
        }
        result = self.make_request(
            "PUT", "/api/v1/energy/consumption/update", data=update_data
        )
        self.results.append(result)
        self.print_result(test_count, result, "PUT /api/v1/energy/consumption/update")

        # === 12. GET /api/v1/energy/consumption/history ===
        test_count += 1
        history_params = {"months": 6, "page": 1, "limit": 10}
        result = self.make_request(
            "GET", "/api/v1/energy/consumption/history", params=history_params
        )
        self.results.append(result)
        self.print_result(test_count, result, "GET /api/v1/energy/consumption/history")

        # === 13. POST /api/v1/energy/consumption/analyze ===
        test_count += 1
        analyze_data = {
            "analysis_type": "advanced",
            "period_months": 12,
            "include_predictions": True,
            "compare_market": True,
            "detailed_breakdown": True,
        }
        result = self.make_request(
            "POST", "/api/v1/energy/consumption/analyze", data=analyze_data
        )
        self.results.append(result)
        self.print_result(test_count, result, "POST /api/v1/energy/consumption/analyze")

        # === 14. GET /api/v1/energy/consumption/recommendations ===
        test_count += 1
        result = self.make_request("GET", "/api/v1/energy/consumption/recommendations")
        self.results.append(result)
        self.print_result(
            test_count, result, "GET /api/v1/energy/consumption/recommendations"
        )

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

            if "update" in description:
                if any(
                    word in response_str
                    for word in ["updated", "actualizado", "success", "modificado"]
                ):
                    print(f"   ✅ Lógica: Actualización procesada correctamente")
                else:
                    print(f"   ⚠️ Lógica: Respuesta de actualización inesperada")

            elif "history" in description:
                if any(
                    word in response_str
                    for word in ["history", "historial", "consumptions", "data"]
                ):
                    print(f"   ✅ Lógica: Historial obtenido correctamente")
                else:
                    print(f"   ⚠️ Lógica: Datos de historial no detectados")

            elif "analyze" in description:
                if any(
                    word in response_str
                    for word in ["analysis", "analytics", "insights", "patterns"]
                ):
                    print(f"   ✅ Lógica: Análisis IA generado correctamente")
                else:
                    print(f"   ⚠️ Lógica: Resultado de análisis no detectado")

            elif "recommendations" in description:
                if any(
                    word in response_str
                    for word in ["recommendations", "recomendaciones", "tips", "advice"]
                ):
                    print(f"   ✅ Lógica: Recomendaciones generadas correctamente")
                else:
                    print(f"   ⚠️ Lógica: Recomendaciones no detectadas")
            else:
                print(f"   ✅ Response: operación exitosa")

    def print_summary(self):
        """Imprime resumen final"""
        successful = len([r for r in self.results if r.success])
        total = len(self.results)
        success_rate = (successful / total) * 100 if total > 0 else 0

        print("\n" + "=" * 50)
        print("📊 RESULTADOS ENERGY PARTE 2:")
        print(f"✅ Exitosos: {successful}/{total}")
        print(f"❌ Fallidos: {total - successful}/{total}")
        print(f"📈 Tasa éxito: {success_rate:.1f}%")

        if success_rate >= 75:
            print("🎉 ENERGY PARTE 2 FUNCIONANDO CORRECTAMENTE")
        elif success_rate >= 50:
            print("⚠️ ENERGY PARTE 2 PARCIALMENTE FUNCIONAL")
        else:
            print("🚨 PROBLEMAS CRÍTICOS EN ENERGY PARTE 2")


def main():
    """Función principal"""
    print("🚀 INICIANDO TESTS ENERGY PARTE 2")
    print("🔐 Configurando autenticación Firebase...")

    try:
        tester = ExpertBotEnergy2Tester()
        print("✅ Autenticación configurada")
        tester.test_endpoints()
    except Exception as e:
        print(f"❌ Error fatal: {e}")


if __name__ == "__main__":
    main()
