#!/usr/bin/env python3
"""
🔥 SCRIPT 3/8 - EXPERT-BOT-API ENERGY PARTE 1
=============================================

ENDPOINTS VERIFICADOS 1 A 1 EN CÓDIGO FUENTE:
7. POST /api/v1/energy/consumption
8. GET /api/v1/energy/dashboard
9. GET /api/v1/energy/users/profile
10. POST /api/v1/energy/manual-data

TOTAL: 4 ENDPOINTS ENERGY PARTE 1
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


class ExpertBotEnergy1Tester:
    """Tester para 4 endpoints ENERGY PARTE 1 de expert-bot-api"""

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
        """Ejecuta tests de 4 endpoints energy verificados"""
        print("🔥 TESTING EXPERT-BOT-API - ENERGY PARTE 1")
        print("=" * 50)
        print("📋 ENDPOINTS VERIFICADOS 1 A 1 EN CÓDIGO:")
        print("7. POST /consumption")
        print("8. GET /dashboard")
        print("9. GET /users/profile")
        print("10. POST /manual-data")
        print(f"🔗 URL: {self.base_url}")
        print("")

        test_count = 0

        # === 7. POST /api/v1/energy/consumption - CON FACTURA REAL ===
        test_count += 1
        factura_path = r"C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\Y DOCUMENTACION\MINISERVICIOS_SCRIPS\factura_prueba.pdf"

        if os.path.exists(factura_path):
            with open(factura_path, "rb") as f:
                files = {"file": ("factura_prueba.pdf", f, "application/pdf")}
                form_data = {"user_id": "test_user_real"}
                result = self.make_request(
                    "POST", "/api/v1/energy/consumption", data=form_data, files=files
                )
        else:
            # Fallback con datos JSON si no hay factura
            consumption_data = {
                "kwh": 450,
                "cost": 85.50,
                "period": "monthly",
                "date": "2025-07-01",
            }
            result = self.make_request(
                "POST", "/api/v1/energy/consumption", data=consumption_data
            )

        self.results.append(result)
        self.print_result(test_count, result, "POST /api/v1/energy/consumption")

        # === 8. GET /api/v1/energy/dashboard ===
        test_count += 1
        result = self.make_request("GET", "/api/v1/energy/dashboard")
        self.results.append(result)
        self.print_result(test_count, result, "GET /api/v1/energy/dashboard")

        # === 9. GET /api/v1/energy/users/profile ===
        test_count += 1
        result = self.make_request("GET", "/api/v1/energy/users/profile")
        self.results.append(result)
        self.print_result(test_count, result, "GET /api/v1/energy/users/profile")

        # === 10. POST /api/v1/energy/manual-data ===
        test_count += 1
        manual_data = {
            "consumption_kwh": 320.5,
            "billing_amount": 65.75,
            "billing_period_start": "2025-06-01",
            "billing_period_end": "2025-06-30",
            "supplier": "Iberdrola",
            "tariff_type": "2.0TD",
        }
        result = self.make_request(
            "POST", "/api/v1/energy/manual-data", data=manual_data
        )
        self.results.append(result)
        self.print_result(test_count, result, "POST /api/v1/energy/manual-data")

        # === RESULTADOS FINALES ===
        self.print_summary()

    def print_result(self, test_num: int, result: TestResult, description: str):
        """Imprime resultado detallado de un test"""
        status = "✅ OK" if result.success else "❌ FALLO"
        print(
            f"[{test_num}/4] {status} | {result.status_code} | {result.response_time:.2f}s | {description}"
        )

        if not result.success and result.error_message:
            print(f"   ❌ Error: {result.error_message}")
        elif result.success:
            if "dashboard" in str(result.response_data):
                print(f"   ✅ Response: dashboard data obtenido")
            elif "profile" in str(result.response_data):
                print(f"   ✅ Response: perfil usuario obtenido")
            elif "consumption" in str(result.response_data):
                print(f"   ✅ Response: consumo procesado")
            else:
                print(f"   ✅ Response: operación exitosa")

    def print_summary(self):
        """Imprime resumen final"""
        successful = len([r for r in self.results if r.success])
        total = len(self.results)
        success_rate = (successful / total) * 100 if total > 0 else 0

        print("\n" + "=" * 50)
        print("📊 RESULTADOS ENERGY PARTE 1:")
        print(f"✅ Exitosos: {successful}/{total}")
        print(f"❌ Fallidos: {total - successful}/{total}")
        print(f"📈 Tasa éxito: {success_rate:.1f}%")

        if success_rate >= 75:
            print("🎉 ENERGY PARTE 1 FUNCIONANDO CORRECTAMENTE")
        elif success_rate >= 50:
            print("⚠️ ENERGY PARTE 1 PARCIALMENTE FUNCIONAL")
        else:
            print("🚨 PROBLEMAS CRÍTICOS EN ENERGY PARTE 1")


def main():
    """Función principal"""
    print("🚀 INICIANDO TESTS ENERGY PARTE 1")
    print("🔐 Configurando autenticación Firebase...")

    try:
        tester = ExpertBotEnergy1Tester()
        print("✅ Autenticación configurada")
        tester.test_endpoints()
    except Exception as e:
        print(f"❌ Error fatal: {e}")


if __name__ == "__main__":
    main()
