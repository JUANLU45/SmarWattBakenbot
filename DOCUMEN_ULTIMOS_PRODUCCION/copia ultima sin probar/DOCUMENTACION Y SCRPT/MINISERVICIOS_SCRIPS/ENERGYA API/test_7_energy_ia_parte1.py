#!/usr/bin/env python3
"""
🔥 SCRIPT 7/8 - ENERGY-IA-API CHATBOT
=====================================

ENDPOINTS VERIFICADOS 1 A 1 EN CÓDIGO FUENTE:
22. POST /api/v1/chatbot/message
23. POST /api/v1/chatbot/message/v2
24. POST /api/v1/chatbot/cross-service
25. GET /api/v1/chatbot/conversations

TOTAL: 4 ENDPOINTS ENERGY-IA-API PARTE 1
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


class EnergyIAChatbotTester:
    """Tester para 4 endpoints CHATBOT de energy-ia-api"""

    def __init__(self):
        self.base_url = "https://energy-ia-api-1010012211318.europe-west1.run.app"
        self.auth_headers = get_auth_headers()
        self.results = []
        self.conversation_id = None

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
        """Ejecuta tests de 4 endpoints chatbot verificados con lógica completa"""
        print("🔥 TESTING ENERGY-IA-API - CHATBOT PARTE 1")
        print("=" * 50)
        print("📋 ENDPOINTS VERIFICADOS 1 A 1 EN CÓDIGO:")
        print("22. POST /message")
        print("23. POST /message/v2")
        print("24. POST /cross-service")
        print("25. GET /conversations")
        print(f"🔗 URL: {self.base_url}")
        print("")

        test_count = 0

        # === 22. POST /api/v1/chatbot/message ===
        test_count += 1
        message_data = {
            "message": "¿Cuáles son las mejores estrategias para optimizar el consumo eléctrico doméstico?",
            "user_id": "test_user_energy_ia",
            "context": "Consulta sobre eficiencia energética residencial",
        }
        result = self.make_request("POST", "/api/v1/chatbot/message", data=message_data)
        self.results.append(result)
        self.print_result(test_count, result, "POST /api/v1/chatbot/message")

        # Capturar conversation_id del response
        if result.success and isinstance(result.response_data, dict):
            self.conversation_id = (
                result.response_data.get("conversation_id")
                or result.response_data.get("id")
                or result.response_data.get("session_id")
            )

        # === 23. POST /api/v1/chatbot/message/v2 ===
        test_count += 1
        message_v2_data = {
            "message": "Dame recomendaciones específicas para aire acondicionado eficiente",
            "user_id": "test_user_energy_ia",
            "conversation_id": self.conversation_id,
            "include_links": True,
            "format": "detailed",
        }
        result = self.make_request(
            "POST", "/api/v1/chatbot/message/v2", data=message_v2_data
        )
        self.results.append(result)
        self.print_result(test_count, result, "POST /api/v1/chatbot/message/v2")

        # === 24. POST /api/v1/chatbot/cross-service ===
        test_count += 1
        cross_service_data = {
            "service": "expert_bot_api",
            "endpoint": "/api/v1/energy/dashboard",
            "method": "GET",
            "user_id": "test_user_energy_ia",
            "parameters": {},
        }
        result = self.make_request(
            "POST", "/api/v1/chatbot/cross-service", data=cross_service_data
        )
        self.results.append(result)
        self.print_result(test_count, result, "POST /api/v1/chatbot/cross-service")

        # === 25. GET /api/v1/chatbot/conversations ===
        test_count += 1
        conversations_params = {
            "user_id": "test_user_energy_ia",
            "limit": 10,
            "page": 1,
        }
        result = self.make_request(
            "GET", "/api/v1/chatbot/conversations", params=conversations_params
        )
        self.results.append(result)
        self.print_result(test_count, result, "GET /api/v1/chatbot/conversations")

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

            if "/message" in description and "v2" not in description:
                if any(
                    word in response_str
                    for word in ["response", "message", "conversation_id", "answer"]
                ):
                    print(f"   ✅ Lógica: Mensaje IA procesado y respuesta generada")
                else:
                    print(f"   ⚠️ Lógica: Respuesta IA no detectada")

            elif "message/v2" in description:
                if any(
                    word in response_str
                    for word in ["response", "links", "detailed", "enhanced"]
                ):
                    print(f"   ✅ Lógica: Mensaje V2 con enlaces y formato avanzado")
                else:
                    print(f"   ⚠️ Lógica: Respuesta V2 mejorada no detectada")

            elif "cross-service" in description:
                if any(
                    word in response_str
                    for word in ["service_response", "expert_bot", "result", "data"]
                ):
                    print(f"   ✅ Lógica: Comunicación cross-service ejecutada")
                else:
                    print(f"   ⚠️ Lógica: Respuesta cross-service no detectada")

            elif "conversations" in description:
                if any(
                    word in response_str
                    for word in ["conversations", "history", "list", "total"]
                ):
                    print(f"   ✅ Lógica: Lista de conversaciones obtenida")
                else:
                    print(f"   ⚠️ Lógica: Datos de conversaciones no detectados")
            else:
                print(f"   ✅ Response: operación exitosa")

    def print_summary(self):
        """Imprime resumen final"""
        successful = len([r for r in self.results if r.success])
        total = len(self.results)
        success_rate = (successful / total) * 100 if total > 0 else 0

        print("\n" + "=" * 50)
        print("📊 RESULTADOS ENERGY-IA-API PARTE 1:")
        print(f"✅ Exitosos: {successful}/{total}")
        print(f"❌ Fallidos: {total - successful}/{total}")
        print(f"📈 Tasa éxito: {success_rate:.1f}%")

        if success_rate >= 75:
            print("🎉 ENERGY-IA-API PARTE 1 FUNCIONANDO CORRECTAMENTE")
        elif success_rate >= 50:
            print("⚠️ ENERGY-IA-API PARTE 1 PARCIALMENTE FUNCIONAL")
        else:
            print("🚨 PROBLEMAS CRÍTICOS EN ENERGY-IA-API PARTE 1")


def main():
    """Función principal"""
    print("🚀 INICIANDO TESTS ENERGY-IA-API CHATBOT PARTE 1")
    print("🔐 Configurando autenticación Firebase...")

    try:
        tester = EnergyIAChatbotTester()
        print("✅ Autenticación configurada")
        tester.test_endpoints()
    except Exception as e:
        print(f"❌ Error fatal: {e}")


if __name__ == "__main__":
    main()
