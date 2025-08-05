#!/usr/bin/env python3
"""
🔥 SCRIPT 2/8 - EXPERT-BOT-API CHATBOT PARTE 2
==============================================

ENDPOINTS VERIFICADOS 1 A 1 EN CÓDIGO FUENTE:
5. POST /api/v1/chatbot/conversation/feedback
6. GET /api/v1/chatbot/metrics

TOTAL: 2 ENDPOINTS CHATBOT PARTE 2
"""

import os
import sys
import json
import time
import requests
from datetime import datetime
from typing import Dict, Any, Optional
from dataclasses import dataclass
import uuid

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


class ExpertBotChatbot2Tester:
    """Tester para 2 endpoints CHATBOT PARTE 2 de expert-bot-api"""

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
        """Ejecuta tests de 2 endpoints chatbot verificados"""
        print("🔥 TESTING EXPERT-BOT-API - CHATBOT PARTE 2")
        print("=" * 50)
        print("📋 ENDPOINTS VERIFICADOS 1 A 1 EN CÓDIGO:")
        print("5. POST /conversation/feedback")
        print("6. GET /metrics")
        print(f"🔗 URL: {self.base_url}")
        print("")

        test_count = 0

        # === 5. POST /api/v1/chatbot/conversation/feedback ===
        test_count += 1
        feedback_data = {
            "conversation_id": "test_conv_123",
            "rating": 5,
            "feedback_type": "positive",
            "feedback": "Respuesta muy útil y precisa",
            "user_id": "test_user_real",
        }
        result = self.make_request(
            "POST", "/api/v1/chatbot/conversation/feedback", data=feedback_data
        )
        self.results.append(result)
        self.print_result(
            test_count, result, "POST /api/v1/chatbot/conversation/feedback"
        )

        # === 6. GET /api/v1/chatbot/metrics ===
        test_count += 1
        result = self.make_request("GET", "/api/v1/chatbot/metrics")
        self.results.append(result)
        self.print_result(test_count, result, "GET /api/v1/chatbot/metrics")

        # === RESULTADOS FINALES ===
        self.print_summary()

    def print_result(self, test_num: int, result: TestResult, description: str):
        """Imprime resultado detallado de un test"""
        status = "✅ OK" if result.success else "❌ FALLO"
        print(
            f"[{test_num}/2] {status} | {result.status_code} | {result.response_time:.2f}s | {description}"
        )

        if not result.success and result.error_message:
            print(f"   ❌ Error: {result.error_message}")
        elif result.success:
            if "feedback" in str(result.response_data):
                print(f"   ✅ Response: feedback procesado")
            elif "metrics" in str(result.response_data):
                print(f"   ✅ Response: métricas obtenidas")
            else:
                print(f"   ✅ Response: operación exitosa")

    def print_summary(self):
        """Imprime resumen final"""
        successful = len([r for r in self.results if r.success])
        total = len(self.results)
        success_rate = (successful / total) * 100 if total > 0 else 0

        print("\n" + "=" * 50)
        print("📊 RESULTADOS CHATBOT PARTE 2:")
        print(f"✅ Exitosos: {successful}/{total}")
        print(f"❌ Fallidos: {total - successful}/{total}")
        print(f"📈 Tasa éxito: {success_rate:.1f}%")

        if success_rate >= 75:
            print("🎉 CHATBOT PARTE 2 FUNCIONANDO CORRECTAMENTE")
        elif success_rate >= 50:
            print("⚠️ CHATBOT PARTE 2 PARCIALMENTE FUNCIONAL")
        else:
            print("🚨 PROBLEMAS CRÍTICOS EN CHATBOT PARTE 2")


def main():
    """Función principal"""
    print("🚀 INICIANDO TESTS CHATBOT PARTE 2")
    print("🔐 Configurando autenticación Firebase...")

    try:
        tester = ExpertBotChatbot2Tester()
        print("✅ Autenticación configurada")
        tester.test_endpoints()
    except Exception as e:
        print(f"❌ Error fatal: {e}")


if __name__ == "__main__":
    main()
