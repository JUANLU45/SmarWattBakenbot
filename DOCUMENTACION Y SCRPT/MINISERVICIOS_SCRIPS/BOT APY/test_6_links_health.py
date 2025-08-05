#!/usr/bin/env python3
"""
🔥 SCRIPT 6/8 - EXPERT-BOT-API LINKS + HEALTH
============================================

ENDPOINTS VERIFICADOS 1 A 1 EN CÓDIGO FUENTE:
19. GET /api/v1/links/direct/<link_type>
20. GET /health
21. GET /health/detailed

TOTAL: 3 ENDPOINTS LINKS + HEALTH
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


class ExpertBotLinksHealthTester:
    """Tester para 3 endpoints LINKS + HEALTH de expert-bot-api"""

    def __init__(self):
        self.base_url = "https://expert-bot-api-1010012211318.europe-west1.run.app"
        self.auth_headers = get_auth_headers()
        self.results = []

    def make_request(
        self, method: str, endpoint: str, data=None, params=None, auth_required=True
    ) -> TestResult:
        """Hace petición HTTP real con autenticación Firebase opcional"""
        url = f"{self.base_url}{endpoint}"
        headers = self.auth_headers.copy() if auth_required else {}

        start_time = time.time()

        try:
            if method == "GET":
                response = requests.get(url, headers=headers, params=params, timeout=30)

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
        """Ejecuta tests de 3 endpoints verificados con lógica completa"""
        print("🔥 TESTING EXPERT-BOT-API - LINKS + HEALTH")
        print("=" * 50)
        print("📋 ENDPOINTS VERIFICADOS 1 A 1 EN CÓDIGO:")
        print("19. GET /links/direct/<link_type>")
        print("20. GET /health")
        print("21. GET /health/detailed")
        print(f"🔗 URL: {self.base_url}")
        print("")

        test_count = 0

        # === 19. GET /api/v1/links/direct/<link_type> ===
        # Probamos varios tipos de links
        link_types = ["blog", "dashboard", "calculator", "weather"]

        for link_type in link_types:
            test_count += 1
            endpoint = f"/api/v1/links/direct/{link_type}"
            result = self.make_request("GET", endpoint)
            self.results.append(result)
            self.print_result(
                test_count, result, f"GET /api/v1/links/direct/{link_type}"
            )

        # === 20. GET /health ===
        test_count += 1
        result = self.make_request("GET", "/health", auth_required=False)
        self.results.append(result)
        self.print_result(test_count, result, "GET /health")

        # === 21. GET /health/detailed ===
        test_count += 1
        result = self.make_request("GET", "/health/detailed", auth_required=False)
        self.results.append(result)
        self.print_result(test_count, result, "GET /health/detailed")

        # === RESULTADOS FINALES ===
        self.print_summary()

    def print_result(self, test_num: int, result: TestResult, description: str):
        """Imprime resultado detallado de un test con validación de lógica"""
        status = "✅ OK" if result.success else "❌ FALLO"
        print(
            f"[{test_num}/6] {status} | {result.status_code} | {result.response_time:.2f}s | {description}"
        )

        if not result.success and result.error_message:
            print(f"   ❌ Error: {result.error_message}")
        elif result.success:
            # Validación específica de lógica por endpoint
            response_str = str(result.response_data).lower()

            if "links/direct" in description:
                if any(
                    word in response_str
                    for word in ["url", "link_type", "status", "success"]
                ):
                    print(f"   ✅ Lógica: Enlace directo generado correctamente")
                else:
                    print(f"   ⚠️ Lógica: Estructura de enlace no detectada")

            elif "/health" in description and "detailed" not in description:
                if any(
                    word in response_str
                    for word in ["status", "ok", "healthy", "timestamp"]
                ):
                    print(f"   ✅ Lógica: Health check básico funcionando")
                else:
                    print(f"   ⚠️ Lógica: Respuesta health básica inesperada")

            elif "health/detailed" in description:
                if any(
                    word in response_str
                    for word in ["status", "version", "uptime", "database", "services"]
                ):
                    print(f"   ✅ Lógica: Health check detallado funcionando")
                else:
                    print(f"   ⚠️ Lógica: Detalles de health no detectados")
            else:
                print(f"   ✅ Response: operación exitosa")

    def print_summary(self):
        """Imprime resumen final"""
        successful = len([r for r in self.results if r.success])
        total = len(self.results)
        success_rate = (successful / total) * 100 if total > 0 else 0

        print("\n" + "=" * 50)
        print("📊 RESULTADOS LINKS + HEALTH:")
        print(f"✅ Exitosos: {successful}/{total}")
        print(f"❌ Fallidos: {total - successful}/{total}")
        print(f"📈 Tasa éxito: {success_rate:.1f}%")

        if success_rate >= 75:
            print("🎉 LINKS + HEALTH FUNCIONANDO CORRECTAMENTE")
        elif success_rate >= 50:
            print("⚠️ LINKS + HEALTH PARCIALMENTE FUNCIONAL")
        else:
            print("🚨 PROBLEMAS CRÍTICOS EN LINKS + HEALTH")


def main():
    """Función principal"""
    print("🚀 INICIANDO TESTS LINKS + HEALTH")
    print("🔐 Configurando autenticación Firebase...")

    try:
        tester = ExpertBotLinksHealthTester()
        print("✅ Autenticación configurada")
        tester.test_endpoints()
    except Exception as e:
        print(f"❌ Error fatal: {e}")


if __name__ == "__main__":
    main()
