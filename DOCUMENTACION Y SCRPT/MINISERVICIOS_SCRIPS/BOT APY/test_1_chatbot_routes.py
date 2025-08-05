#!/usr/bin/env python3
"""
🔥 SCRIPT 1/4 - EXPERT-BOT-API CHATBOT ROUTES
============================================

ENDPOINTS CHATBOT (/api/v1/chatbot/*):
1. POST /api/v1/chatbot/session/start
2. POST /api/v1/chatbot/message
3. GET /api/v1/chatbot/conversation/history
4. DELETE /api/v1/chatbot/conversation/<id>
5. POST /api/v1/chatbot/conversation/feedback
6. GET /api/v1/chatbot/metrics

TOTAL: 6 ENDPOINTS CHATBOT
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


class ExpertBotChatbotTester:
    """Tester para endpoints CHATBOT de expert-bot-api"""

    def __init__(self):
        self.base_url = "https://expert-bot-api-1010012211318.europe-west1.run.app"
        self.auth_headers = get_auth_headers()
        self.results = []
        self.conversation_id = None

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
                response = requests.post(url, headers=headers, json=data, timeout=30)
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

    def test_chatbot_endpoints(self):
        """Ejecuta todos los tests de endpoints chatbot"""
        print("🔥 TESTING EXPERT-BOT-API - CHATBOT ROUTES")
        print("=" * 50)
        print(f"🔗 URL: {self.base_url}")
        print("")

        test_count = 0

        # === 1. POST /api/v1/chatbot/session/start ===
        test_count += 1
        session_data = {
            "user_id": "test_user_chatbot",
            "context": "Quiero información sobre ahorro energético",
        }
        result = self.make_request(
            "POST", "/api/v1/chatbot/session/start", data=session_data
        )
        self.results.append(result)
        self.print_result(test_count, result, "POST /api/v1/chatbot/session/start")

        # Capturar conversation_id si está disponible
        if result.success and isinstance(result.response_data, dict):
            self.conversation_id = result.response_data.get(
                "conversation_id"
            ) or result.response_data.get("session_id")
            if self.conversation_id:
                print(f"   ✅ Conversation ID capturado: {self.conversation_id}")

        # === 2. POST /api/v1/chatbot/message ===
        test_count += 1
        message_data = {
            "message": "¿Cómo puedo reducir mi consumo eléctrico?",
            "conversation_id": self.conversation_id,
            "user_id": "test_user_chatbot",
        }
        result = self.make_request("POST", "/api/v1/chatbot/message", data=message_data)
        self.results.append(result)
        self.print_result(test_count, result, "POST /api/v1/chatbot/message")

        # === 3. GET /api/v1/chatbot/conversation/history ===
        test_count += 1
        params = {"user_id": "test_user_chatbot", "limit": 10}
        result = self.make_request(
            "GET", "/api/v1/chatbot/conversation/history", params=params
        )
        self.results.append(result)
        self.print_result(
            test_count, result, "GET /api/v1/chatbot/conversation/history"
        )

        # === 4. POST /api/v1/chatbot/conversation/feedback ===
        test_count += 1
        feedback_data = {
            "conversation_id": self.conversation_id,
            "rating": 5,
            "feedback": "Respuesta muy útil y detallada",
            "user_id": "test_user_chatbot",
        }
        result = self.make_request(
            "POST", "/api/v1/chatbot/conversation/feedback", data=feedback_data
        )
        self.results.append(result)
        self.print_result(
            test_count, result, "POST /api/v1/chatbot/conversation/feedback"
        )

        # === 5. GET /api/v1/chatbot/metrics ===
        test_count += 1
        result = self.make_request("GET", "/api/v1/chatbot/metrics")
        self.results.append(result)
        self.print_result(test_count, result, "GET /api/v1/chatbot/metrics")

        # === 6. DELETE /api/v1/chatbot/conversation/<id> ===
        test_count += 1
        if self.conversation_id:
            delete_endpoint = f"/api/v1/chatbot/conversation/{self.conversation_id}"
            result = self.make_request("DELETE", delete_endpoint)
            self.results.append(result)
            self.print_result(test_count, result, f"DELETE {delete_endpoint}")
        else:
            print(
                f"[{test_count}/6] ⚠️ SKIP | No conversation_id | DELETE /api/v1/chatbot/conversation/<id>"
            )

        # === RESULTADOS FINALES ===
        self.print_summary()

    def print_result(self, test_num: int, result: TestResult, description: str):
        """Imprime resultado de un test"""
        status = "✅ OK" if result.success else "❌ FALLO"
        print(
            f"[{test_num}/6] {status} | {result.status_code} | {result.response_time:.2f}s | {description}"
        )
        if not result.success and result.error_message:
            print(f"   Error: {result.error_message}")
        if result.success and result.response_data:
            # Mostrar datos relevantes
            if "conversation_id" in str(result.response_data):
                print(f"   ✅ Datos: conversation_id encontrado")
            elif "response" in str(result.response_data):
                print(f"   ✅ Datos: response generada")

    def print_summary(self):
        """Imprime resumen final"""
        successful = len([r for r in self.results if r.success])
        total = len(self.results)
        success_rate = (successful / total) * 100

        print("\n" + "=" * 50)
        print("📊 RESULTADOS FINALES CHATBOT:")
        print(f"✅ Exitosos: {successful}/{total}")
        print(f"❌ Fallidos: {total - successful}/{total}")
        print(f"📈 Tasa éxito: {success_rate:.1f}%")

        if success_rate >= 70:
            print("🎉 ENDPOINTS CHATBOT FUNCIONANDO")
        else:
            print("⚠️ PROBLEMAS EN ENDPOINTS CHATBOT")


def main():
    """Función principal"""
    print("🚀 INICIANDO TESTS CHATBOT - EXPERT-BOT-API")
    print("🔐 Configurando autenticación Firebase...")

    try:
        tester = ExpertBotChatbotTester()
        print("✅ Autenticación configurada")
        tester.test_chatbot_endpoints()
    except Exception as e:
        print(f"❌ Error fatal: {e}")


if __name__ == "__main__":
    main()
