#!/usr/bin/env python3
"""
🔥 SCRIPT 1/8 - EXPERT-BOT-API CHATBOT PARTE 1
==============================================

ENDPOINTS VERIFICADOS 1 A 1 EN CÓDIGO FUENTE:
1. POST /api/v1/chatbot/session/start
2. POST /api/v1/chatbot/message
3. GET /api/v1/chatbot/conversation/history
4. DELETE /api/v1/chatbot/conversation/<conversation_id>

TOTAL: 4 ENDPOINTS CHATBOT PARTE 1
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


class ExpertBotChatbot1Tester:
    """Tester para 4 endpoints CHATBOT PARTE 1 de expert-bot-api"""

    def __init__(self):
        self.base_url = "https://expert-bot-api-1010012211318.europe-west1.run.app"
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
        """Ejecuta tests de 4 endpoints chatbot verificados"""
        print("🔥 TESTING EXPERT-BOT-API - CHATBOT PARTE 1")
        print("=" * 50)
        print("📋 ENDPOINTS VERIFICADOS 1 A 1 EN CÓDIGO:")
        print("1. POST /session/start")
        print("2. POST /message")
        print("3. GET /conversation/history")
        print("4. DELETE /conversation/<conversation_id>")
        print(f"🔗 URL: {self.base_url}")
        print("")

        test_count = 0

        # === 1. POST /api/v1/chatbot/session/start ===
        test_count += 1
        session_data = {
            "user_id": "test_user_real",
            "context": "Usuario solicita información sobre ahorro energético",
        }
        result = self.make_request(
            "POST", "/api/v1/chatbot/session/start", data=session_data
        )
        self.results.append(result)
        self.print_result(test_count, result, "POST /api/v1/chatbot/session/start")

        # Capturar conversation_id del response real
        if result.success and isinstance(result.response_data, dict):
            self.conversation_id = (
                result.response_data.get("conversation_id")
                or result.response_data.get("session_id")
                or result.response_data.get("id")
            )
            if self.conversation_id:
                print(f"   📋 conversation_id: {self.conversation_id}")

        # === 2. POST /api/v1/chatbot/message ===
        test_count += 1
        message_data = {
            "message": "¿Cuáles son las mejores formas de reducir el consumo eléctrico en el hogar?",
            "conversation_id": self.conversation_id,
            "user_id": "test_user_real",
        }
        result = self.make_request("POST", "/api/v1/chatbot/message", data=message_data)
        self.results.append(result)
        self.print_result(test_count, result, "POST /api/v1/chatbot/message")

        # === 3. GET /api/v1/chatbot/conversation/history ===
        test_count += 1
        params = {"user_id": "test_user_real", "limit": 5}
        result = self.make_request(
            "GET", "/api/v1/chatbot/conversation/history", params=params
        )
        self.results.append(result)
        self.print_result(
            test_count, result, "GET /api/v1/chatbot/conversation/history"
        )

        # === 4. DELETE /api/v1/chatbot/conversation/<conversation_id> ===
        test_count += 1
        if self.conversation_id:
            delete_endpoint = f"/api/v1/chatbot/conversation/{self.conversation_id}"
            result = self.make_request("DELETE", delete_endpoint)
            self.results.append(result)
            self.print_result(test_count, result, f"DELETE {delete_endpoint}")
        else:
            print(
                f"[{test_count}/4] ⚠️ SKIP | Sin conversation_id | DELETE /api/v1/chatbot/conversation/<id>"
            )

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
            if "conversation_id" in str(result.response_data):
                print(f"   ✅ Response: conversation_id detectado")
            elif "response" in str(result.response_data):
                print(f"   ✅ Response: mensaje generado")
            elif "conversations" in str(result.response_data):
                print(f"   ✅ Response: historial obtenido")
            else:
                print(f"   ✅ Response: operación exitosa")

    def print_summary(self):
        """Imprime resumen final"""
        successful = len([r for r in self.results if r.success])
        total = len(self.results)
        success_rate = (successful / total) * 100 if total > 0 else 0

        print("\n" + "=" * 50)
        print("📊 RESULTADOS CHATBOT PARTE 1:")
        print(f"✅ Exitosos: {successful}/{total}")
        print(f"❌ Fallidos: {total - successful}/{total}")
        print(f"📈 Tasa éxito: {success_rate:.1f}%")

        if success_rate >= 75:
            print("🎉 CHATBOT PARTE 1 FUNCIONANDO CORRECTAMENTE")
        elif success_rate >= 50:
            print("⚠️ CHATBOT PARTE 1 PARCIALMENTE FUNCIONAL")
        else:
            print("🚨 PROBLEMAS CRÍTICOS EN CHATBOT PARTE 1")


def main():
    """Función principal"""
    print("🚀 INICIANDO TESTS CHATBOT PARTE 1")
    print("🔐 Configurando autenticación Firebase...")

    try:
        tester = ExpertBotChatbot1Tester()
        print("✅ Autenticación configurada")
        tester.test_endpoints()
    except Exception as e:
        print(f"❌ Error fatal: {e}")


if __name__ == "__main__":
    main()
