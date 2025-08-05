#!/usr/bin/env python3
"""
🔥 SCRIPT 8/8 - ENERGY-IA-API FINAL
===================================

ENDPOINTS VERIFICADOS 1 A 1 EN CÓDIGO FUENTE:
26. DELETE /api/v1/chatbot/conversations/<conversation_id>
27. GET /api/v1/chatbot/health
28. GET /health

TOTAL: 3 ENDPOINTS ENERGY-IA-API FINAL
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


class EnergyIAFinalTester:
    """Tester para 3 endpoints FINALES de energy-ia-api"""

    def __init__(self):
        self.base_url = "https://energy-ia-api-1010012211318.europe-west1.run.app"
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

    def test_endpoints(self):
        """Ejecuta tests de 3 endpoints finales verificados con lógica completa"""
        print("🔥 TESTING ENERGY-IA-API - ENDPOINTS FINALES")
        print("=" * 50)
        print("📋 ENDPOINTS VERIFICADOS 1 A 1 EN CÓDIGO:")
        print("26. DELETE /conversations/<conversation_id>")
        print("27. GET /chatbot/health")
        print("28. GET /health")
        print(f"🔗 URL: {self.base_url}")
        print("")

        test_count = 0

        # === 26. DELETE /api/v1/chatbot/conversations/<conversation_id> ===
        test_count += 1
        # Usamos un ID de prueba ya que es para testing
        test_conversation_id = "test_conversation_delete_123"
        delete_endpoint = f"/api/v1/chatbot/conversations/{test_conversation_id}"
        result = self.make_request("DELETE", delete_endpoint)
        self.results.append(result)
        self.print_result(
            test_count,
            result,
            f"DELETE /api/v1/chatbot/conversations/{test_conversation_id}",
        )

        # === 27. GET /api/v1/chatbot/health ===
        test_count += 1
        result = self.make_request("GET", "/api/v1/chatbot/health")
        self.results.append(result)
        self.print_result(test_count, result, "GET /api/v1/chatbot/health")

        # === 28. GET /health ===
        test_count += 1
        result = self.make_request("GET", "/health", auth_required=False)
        self.results.append(result)
        self.print_result(test_count, result, "GET /health")

        # === RESULTADOS FINALES ===
        self.print_summary()

    def print_result(self, test_num: int, result: TestResult, description: str):
        """Imprime resultado detallado de un test con validación de lógica"""
        status = "✅ OK" if result.success else "❌ FALLO"
        print(
            f"[{test_num}/3] {status} | {result.status_code} | {result.response_time:.2f}s | {description}"
        )

        if not result.success and result.error_message:
            print(f"   ❌ Error: {result.error_message}")
        elif result.success:
            # Validación específica de lógica por endpoint
            response_str = str(result.response_data).lower()

            if "DELETE" in description and "conversations" in description:
                if any(
                    word in response_str
                    for word in ["deleted", "removed", "success", "eliminado"]
                ):
                    print(f"   ✅ Lógica: Conversación eliminada correctamente")
                elif "not found" in response_str or "404" in response_str:
                    print(
                        f"   ✅ Lógica: Conversación no encontrada (comportamiento esperado)"
                    )
                else:
                    print(f"   ⚠️ Lógica: Respuesta de eliminación inesperada")

            elif "chatbot/health" in description:
                if any(
                    word in response_str
                    for word in ["status", "healthy", "ok", "service", "operational"]
                ):
                    print(f"   ✅ Lógica: Health check del chatbot funcionando")
                else:
                    print(f"   ⚠️ Lógica: Estado del chatbot no detectado")

            elif "/health" in description and "chatbot" not in description:
                if any(
                    word in response_str
                    for word in ["status", "healthy", "ok", "timestamp", "uptime"]
                ):
                    print(f"   ✅ Lógica: Health check general funcionando")
                else:
                    print(f"   ⚠️ Lógica: Estado general del servicio no detectado")
            else:
                print(f"   ✅ Response: operación exitosa")

    def print_summary(self):
        """Imprime resumen final"""
        successful = len([r for r in self.results if r.success])
        total = len(self.results)
        success_rate = (successful / total) * 100 if total > 0 else 0

        print("\n" + "=" * 50)
        print("📊 RESULTADOS ENERGY-IA-API FINAL:")
        print(f"✅ Exitosos: {successful}/{total}")
        print(f"❌ Fallidos: {total - successful}/{total}")
        print(f"📈 Tasa éxito: {success_rate:.1f}%")

        if success_rate >= 75:
            print("🎉 ENERGY-IA-API FINAL FUNCIONANDO CORRECTAMENTE")
        elif success_rate >= 50:
            print("⚠️ ENERGY-IA-API FINAL PARCIALMENTE FUNCIONAL")
        else:
            print("🚨 PROBLEMAS CRÍTICOS EN ENERGY-IA-API FINAL")

        print("\n🏁 TESTING COMPLETO DE TODOS LOS 30+ ENDPOINTS")
        print("=" * 50)


def main():
    """Función principal"""
    print("🚀 INICIANDO TESTS ENERGY-IA-API FINAL")
    print("🔐 Configurando autenticación Firebase...")

    try:
        tester = EnergyIAFinalTester()
        print("✅ Autenticación configurada")
        tester.test_endpoints()
    except Exception as e:
        print(f"❌ Error fatal: {e}")


if __name__ == "__main__":
    main()
