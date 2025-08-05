#!/usr/bin/env python3
"""
🏢 VERIFICADOR LOCAL DE ENDPOINTS - SMARWATT MICROSERVICIOS
=========================================================

Este script verifica LOCALMENTE los endpoints de ambos microservicios
ejecutándose en tu ordenador ANTES de desplegarlos.

PROPÓSITO:
✅ Probar cambios localmente antes del despliegue
✅ Verificar que todos los endpoints funcionen correctamente
✅ Detectar problemas antes de ir a producción
✅ Generar reporte de endpoints locales

URLs LOCALES:
- Expert Bot API: http://localhost:8080
- Energy IA API: http://localhost:8081

INSTRUCCIONES DE USO:
1. Asegúrate de tener ambos servicios ejecutándose localmente
2. Expert Bot API en puerto 8080: python run.py
3. Energy IA API en puerto 8081: python run.py
4. Ejecuta este script: python verificar_endpoints_local.py

AUTOR: Sistema de Verificación Local SmarWatt
FECHA: 2025-07-21
VERSIÓN: 1.0.0 - VERIFICACIÓN LOCAL
"""

import requests
import json
import time
import os
import subprocess
import socket
from datetime import datetime, timezone
from typing import Dict, List, Any, Tuple
from pathlib import Path

# Configurar requests para evitar warnings
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# URLs LOCALES de los microservicios
EXPERT_BOT_LOCAL_URL = "http://localhost:8080"
ENERGY_IA_LOCAL_URL = "http://localhost:8081"


class LocalEndpointVerifier:
    """🔍 Verificador de endpoints locales"""

    def __init__(self):
        self.timeout = 10
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "SmarWatt-Local-Verifier/1.0",
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )

        # ✅ ENDPOINTS REALES basados en el código fuente LOCAL
        self.endpoints = {
            "expert_bot_api": [
                # === HEALTH ENDPOINTS ===
                {
                    "path": "/health",
                    "method": "GET",
                    "desc": "Health check básico",
                    "critical": True,
                },
                {
                    "path": "/health/detailed",
                    "method": "GET",
                    "desc": "Health check detallado",
                    "critical": True,
                },
                # === CHAT ENDPOINTS (prefix: /api/v1/chatbot) ===
                {
                    "path": "/api/v1/chatbot/session/start",
                    "method": "POST",
                    "desc": "Iniciar sesión de chat",
                    "auth": True,
                    "critical": True,
                },
                {
                    "path": "/api/v1/chatbot/message",
                    "method": "POST",
                    "desc": "Enviar mensaje al chatbot",
                    "auth": True,
                    "critical": True,
                },
                {
                    "path": "/api/v1/chatbot/conversation/history",
                    "method": "GET",
                    "desc": "Historial de conversaciones",
                    "auth": True,
                },
                {
                    "path": "/api/v1/chatbot/conversation/test-conv-123",
                    "method": "DELETE",
                    "desc": "Eliminar conversación",
                    "auth": True,
                },
                {
                    "path": "/api/v1/chatbot/conversation/feedback",
                    "method": "POST",
                    "desc": "Feedback de conversación",
                    "auth": True,
                },
                {
                    "path": "/api/v1/chatbot/metrics",
                    "method": "GET",
                    "desc": "Métricas de chat",
                    "auth": True,
                },
                # === ENERGY ENDPOINTS (prefix: /api/v1/energy) ===
                {
                    "path": "/api/v1/energy/consumption",
                    "method": "POST",
                    "desc": "Registrar consumo energético",
                    "auth": True,
                    "critical": True,
                },
                {
                    "path": "/api/v1/energy/dashboard",
                    "method": "GET",
                    "desc": "Dashboard de energía",
                    "auth": True,
                    "critical": True,
                },
                {
                    "path": "/api/v1/energy/users/profile",
                    "method": "GET",
                    "desc": "Perfil energético usuario",
                    "auth": True,
                },
                {
                    "path": "/api/v1/energy/manual-data",
                    "method": "POST",
                    "desc": "Ingreso manual de datos",
                    "auth": True,
                },
                {
                    "path": "/api/v1/energy/consumption/update",
                    "method": "PUT",
                    "desc": "Actualizar consumo",
                    "auth": True,
                },
                {
                    "path": "/api/v1/energy/consumption/history",
                    "method": "GET",
                    "desc": "Historial de consumo",
                    "auth": True,
                },
                {
                    "path": "/api/v1/energy/consumption/analyze",
                    "method": "POST",
                    "desc": "Análisis de consumo",
                    "auth": True,
                },
                {
                    "path": "/api/v1/energy/consumption/recommendations",
                    "method": "GET",
                    "desc": "Recomendaciones energéticas",
                    "auth": True,
                },
                {
                    "path": "/api/v1/energy/consumption/compare",
                    "method": "POST",
                    "desc": "Comparar consumos",
                    "auth": True,
                },
                {
                    "path": "/api/v1/energy/consumption/title",
                    "method": "PUT",
                    "desc": "Actualizar título",
                    "auth": True,
                },
                # === LINKS ENDPOINTS (prefix: /api/v1) ===
                {
                    "path": "/api/v1/links/test",
                    "method": "POST",
                    "desc": "Test de conectividad",
                },
                {
                    "path": "/api/v1/links/status",
                    "method": "GET",
                    "desc": "Estado de conexiones",
                },
                {
                    "path": "/api/v1/links/direct/energy-service",
                    "method": "GET",
                    "desc": "Acceso directo a servicios",
                    "auth": True,
                },
            ],
            "energy_ia_api": [
                # === HEALTH ENDPOINTS ===
                {
                    "path": "/health",
                    "method": "GET",
                    "desc": "Health check IA básico",
                    "critical": True,
                },
                {
                    "path": "/api/v1/info",
                    "method": "GET",
                    "desc": "Información del servicio IA",
                    "critical": True,
                },
                {
                    "path": "/api/v1/status",
                    "method": "GET",
                    "desc": "Estado detallado del servicio IA",
                    "critical": True,
                },
                {
                    "path": "/status",
                    "method": "GET",
                    "desc": "Estado general desde run.py",
                    "critical": True,
                },
                # === CHATBOT IA ENDPOINTS (prefix: /api/v1/chatbot) ===
                {
                    "path": "/api/v1/chatbot/message",
                    "method": "POST",
                    "desc": "Procesamiento IA de mensajes",
                    "auth": True,
                    "critical": True,
                },
                {
                    "path": "/api/v1/chatbot/message/v2",
                    "method": "POST",
                    "desc": "Procesamiento IA v2 mejorado",
                    "auth": True,
                    "critical": True,
                },
                {
                    "path": "/api/v1/chatbot/cross-service",
                    "method": "POST",
                    "desc": "Comunicación inter-servicios",
                    "auth": True,
                },
                {
                    "path": "/api/v1/chatbot/conversations",
                    "method": "GET",
                    "desc": "Listar conversaciones IA",
                    "auth": True,
                },
                {
                    "path": "/api/v1/chatbot/conversations/test-conv-456",
                    "method": "DELETE",
                    "desc": "Eliminar conversación IA",
                    "auth": True,
                },
                {
                    "path": "/api/v1/chatbot/health",
                    "method": "GET",
                    "desc": "Health check específico chatbot IA",
                    "critical": True,
                },
            ],
        }

    def check_port_open(self, host: str, port: int) -> bool:
        """🔍 Verificar si un puerto está abierto"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(2)
                result = sock.connect_ex((host, port))
                return result == 0
        except:
            return False

    def get_service_status(self, service_name: str, base_url: str) -> Dict[str, Any]:
        """🩺 Obtener estado completo del servicio local"""

        port = int(base_url.split(":")[-1])
        host = base_url.split("://")[1].split(":")[0]

        print(f"🔍 Verificando {service_name} en {base_url}")

        # Verificar si el puerto está abierto
        port_open = self.check_port_open(host, port)
        if not port_open:
            print(f"  ❌ Puerto {port} no está abierto")
            return {
                "service": service_name,
                "url": base_url,
                "port_open": False,
                "status": "❌ SERVICE_DOWN",
                "error": f"Puerto {port} no está accesible",
                "response_time": 0,
            }

        print(f"  ✅ Puerto {port} está abierto")

        # Intentar health check
        try:
            start_time = time.time()
            response = self.session.get(f"{base_url}/health", timeout=5)
            response_time = time.time() - start_time

            if response.status_code == 200:
                status = "✅ RUNNING_HEALTHY"
                error = None
                print(
                    f"  ✅ Servicio healthy - {response.status_code} ({response_time:.3f}s)"
                )

                # Intentar obtener información adicional
                try:
                    health_data = response.json()
                    print(f"  📊 Info: {health_data.get('status', 'N/A')}")
                except:
                    pass

            elif response.status_code == 404:
                status = "⚠️ RUNNING_NO_HEALTH"
                error = "Servicio ejecutándose pero sin endpoint /health"
                print(f"  ⚠️  Servicio responde pero sin /health")
            else:
                status = "⚠️ RUNNING_UNHEALTHY"
                error = f"Health check retorna {response.status_code}"
                print(f"  ⚠️  Health check: {response.status_code}")

        except requests.exceptions.ConnectionError:
            status = "❌ CONNECTION_REFUSED"
            error = "Conexión rechazada - El servicio no está ejecutándose"
            response_time = 5
            print(f"  ❌ Conexión rechazada")

        except requests.exceptions.Timeout:
            status = "⏱️ TIMEOUT"
            error = "Timeout - El servicio responde muy lento"
            response_time = 5
            print(f"  ⏱️  Timeout")

        except Exception as e:
            status = "💥 ERROR"
            error = f"Error inesperado: {str(e)[:100]}"
            response_time = 5
            print(f"  💥 Error: {str(e)[:50]}")

        return {
            "service": service_name,
            "url": base_url,
            "port_open": port_open,
            "status": status,
            "error": error,
            "response_time": response_time,
        }

    def test_endpoint_local(
        self, base_url: str, endpoint: Dict[str, Any]
    ) -> Dict[str, Any]:
        """🧪 Probar un endpoint local con datos realistas"""

        full_url = f"{base_url}{endpoint['path']}"
        result = {
            "path": endpoint["path"],
            "method": endpoint["method"],
            "description": endpoint["desc"],
            "requires_auth": endpoint.get("auth", False),
            "is_critical": endpoint.get("critical", False),
            "url": full_url,
            "status": "unknown",
            "http_code": 0,
            "response_time": 0.0,
            "error": None,
            "response_sample": None,
            "local_test": True,
        }

        try:
            print(f"  🧪 {endpoint['method']} {endpoint['path']}")

            headers = self.session.headers.copy()
            if endpoint.get("auth"):
                # Token JWT de prueba más realista para desarrollo local
                headers["Authorization"] = (
                    "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoidGVzdC11c2VyLTEyMzQ1IiwiaWF0IjoxNjQyNjgwMDAwfQ.local-test-token"
                )

            # Datos de prueba específicos para desarrollo local
            test_data = self._get_local_test_data(endpoint)

            start_time = time.time()

            try:
                if endpoint["method"] == "GET":
                    # Para GETs con auth, añadir user_id como query param
                    params = (
                        {"user_id": "test-user-12345"} if endpoint.get("auth") else {}
                    )
                    response = self.session.get(
                        full_url, headers=headers, params=params, timeout=self.timeout
                    )

                elif endpoint["method"] == "POST":
                    response = self.session.post(
                        full_url, headers=headers, json=test_data, timeout=self.timeout
                    )

                elif endpoint["method"] == "PUT":
                    response = self.session.put(
                        full_url, headers=headers, json=test_data, timeout=self.timeout
                    )

                elif endpoint["method"] == "DELETE":
                    response = self.session.delete(
                        full_url, headers=headers, timeout=self.timeout
                    )

                else:
                    response = self.session.request(
                        endpoint["method"],
                        full_url,
                        headers=headers,
                        json=test_data,
                        timeout=self.timeout,
                    )

            except requests.exceptions.SSLError:
                # Para desarrollo local, ignorar SSL
                self.session.verify = False
                if endpoint["method"] == "GET":
                    params = (
                        {"user_id": "test-user-12345"} if endpoint.get("auth") else {}
                    )
                    response = self.session.get(
                        full_url, headers=headers, params=params, timeout=self.timeout
                    )
                else:
                    response = self.session.request(
                        endpoint["method"],
                        full_url,
                        headers=headers,
                        json=test_data,
                        timeout=self.timeout,
                    )

            result["response_time"] = time.time() - start_time
            result["http_code"] = response.status_code

            # Evaluar respuesta específicamente para desarrollo local
            if response.status_code == 200:
                result["status"] = "✅ SUCCESS"
                try:
                    json_response = response.json()
                    result["response_sample"] = json_response
                    if len(str(json_response)) > 300:
                        result["response_sample"] = (
                            str(json_response)[:300] + "... [truncated]"
                        )
                except ValueError:
                    result["response_sample"] = (
                        response.text[:200] + "..."
                        if len(response.text) > 200
                        else response.text
                    )

            elif response.status_code == 201:
                result["status"] = "✅ CREATED"
                result["response_sample"] = response.text[:200]

            elif response.status_code == 404:
                result["status"] = "🔍 NOT_FOUND"
                result["error"] = "Endpoint no encontrado - Verificar blueprint y rutas"

            elif response.status_code == 401:
                result["status"] = "🔐 AUTH_REQUIRED"
                result["error"] = "Autenticación requerida - Implementar JWT local"

            elif response.status_code == 403:
                result["status"] = "🚫 FORBIDDEN"
                result["error"] = "Acceso prohibido - Verificar permisos"

            elif response.status_code == 422:
                result["status"] = "📋 VALIDATION_ERROR"
                result["error"] = "Error de validación - Ajustar parámetros de prueba"

            elif response.status_code == 500:
                result["status"] = "💥 SERVER_ERROR"
                result["error"] = "Error interno - Revisar logs del servidor local"
                result["response_sample"] = response.text[:300]

            elif response.status_code >= 400:
                result["status"] = "❌ ERROR"
                result["error"] = f"HTTP {response.status_code}: {response.text[:100]}"
            else:
                result["status"] = "❓ UNKNOWN"
                result["error"] = f"Status inesperado: {response.status_code}"

        except requests.exceptions.Timeout:
            result["status"] = "⏱️ TIMEOUT"
            result["error"] = f"Timeout después de {self.timeout}s"
            result["response_time"] = self.timeout

        except requests.exceptions.ConnectionError:
            result["status"] = "🔗 CONNECTION_ERROR"
            result["error"] = "Error de conexión - Servicio no está ejecutándose"

        except requests.exceptions.RequestException as e:
            result["status"] = "💥 REQUEST_ERROR"
            result["error"] = f"Error de petición: {str(e)[:100]}"

        return result

    def _get_local_test_data(self, endpoint: Dict[str, Any]) -> Dict[str, Any]:
        """🧪 Generar datos de prueba para desarrollo local"""

        path = endpoint["path"]
        method = endpoint["method"]

        # Datos base para desarrollo local
        base_data = {
            "user_id": "local-test-user-12345",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "local_test": True,
            "environment": "development",
        }

        # Datos específicos para desarrollo local
        if "chat" in path and "message" in path:
            return {
                **base_data,
                "message": "¡Hola! Soy un mensaje de prueba local. ¿Puedes ayudarme con mi factura eléctrica?",
                "session_id": "local-session-67890",
                "context": {
                    "source": "local_development",
                    "user_location": "Madrid, España",
                    "test_mode": True,
                },
            }

        elif "chat" in path and "session/start" in path:
            return {
                **base_data,
                "session_type": "local_test_consultation",
                "client_info": {
                    "platform": "local_development",
                    "version": "dev-1.0.0",
                    "user_agent": "Local-Test-Agent",
                },
            }

        elif "energy" in path and "consumption" in path and method == "POST":
            return {
                **base_data,
                "consumption_data": {
                    "kwh_consumed": 250.75,
                    "period": "monthly",
                    "cost": 65.25,
                    "tariff_type": "PVPC",
                    "supplier": "Endesa",
                    "local_test": True,
                },
                "meter_reading": 98765.43,
                "invoice_data": {
                    "invoice_number": "LOCAL-TEST-001",
                    "invoice_date": "2025-01-15",
                    "test_invoice": True,
                },
            }

        elif "energy" in path and "manual-data" in path:
            return {
                **base_data,
                "manual_data": {
                    "consumption_kwh": 180.25,
                    "cost_euros": 45.60,
                    "period_start": "2025-01-01",
                    "period_end": "2025-01-31",
                    "data_source": "local_test_input",
                },
            }

        elif "feedback" in path:
            return {
                **base_data,
                "conversation_id": "local-conv-test-12345",
                "rating": 5,
                "feedback": "Prueba local exitosa - Excelente funcionamiento",
                "category": "local_test_satisfaction",
            }

        elif "cross-service" in path:
            return {
                **base_data,
                "source_service": "expert_bot_api_local",
                "target_action": "local_test_analyze_consumption",
                "data": {
                    "analysis_type": "local_trend_analysis",
                    "period_months": 3,
                    "test_mode": True,
                },
            }

        elif "links/test" in path:
            return {
                "target_service": "energy_ia_api_local",
                "test_type": "local_connectivity",
                "test_data": {
                    "message": "Test local connection from expert bot",
                    "local_development": True,
                },
            }

        else:
            return base_data

    def provide_startup_instructions(self):
        """📋 Proporcionar instrucciones para iniciar servicios localmente"""

        print("🏢 VERIFICADOR LOCAL DE ENDPOINTS - SMARWATT")
        print("=" * 60)
        print(
            "Para usar este verificador, necesitas tener ambos servicios ejecutándose localmente:\n"
        )

        print("📁 EXPERT BOT API (Puerto 8080):")
        print(
            "   1. cd c:\\Smarwatt_2\\SmarWatt_2\\backend\\sevicio chatbot\\servicios\\expert_bot_api_COPY"
        )
        print("   2. python run.py")
        print("   3. El servicio debería estar en http://localhost:8080\n")

        print("📁 ENERGY IA API (Puerto 8081):")
        print(
            "   1. cd c:\\Smarwatt_2\\SmarWatt_2\\backend\\sevicio chatbot\\servicios\\energy_ia_api_COPY"
        )
        print("   2. python run.py")
        print("   3. El servicio debería estar en http://localhost:8081\n")

        print("⚠️  IMPORTANTE:")
        print("   - Asegúrate de tener todas las variables de entorno configuradas")
        print("   - Los servicios deben tener acceso a Firebase y BigQuery")
        print("   - Si hay errores de autenticación, configura credenciales locales")
        print("\n" + "=" * 60 + "\n")

    def verify_local_services(self):
        """🚀 Verificar servicios localmente"""

        self.provide_startup_instructions()

        results = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "environment": "local_development",
            "version": "1.0.0",
            "services": {},
            "summary": {
                "total_endpoints": 0,
                "success_count": 0,
                "error_count": 0,
                "not_found_count": 0,
                "auth_required_count": 0,
                "server_error_count": 0,
                "connection_error_count": 0,
                "critical_endpoints_working": 0,
                "critical_endpoints_total": 0,
            },
        }

        # Servicios locales a verificar
        services = {
            "expert_bot_api": EXPERT_BOT_LOCAL_URL,
            "energy_ia_api": ENERGY_IA_LOCAL_URL,
        }

        for service_name, base_url in services.items():
            print(f"🔧 {service_name.upper().replace('_', ' ')}")
            print("-" * 50)

            # Verificar estado del servicio
            service_status = self.get_service_status(service_name, base_url)

            if "RUNNING" in service_status["status"]:
                print(f"  🎯 Servicio detectado en {base_url}")
                print(
                    f"  📡 Verificando {len(self.endpoints.get(service_name, []))} endpoints:"
                )

                service_results = {
                    "url": base_url,
                    "service_status": service_status,
                    "endpoints": [],
                    "total_endpoints": 0,
                    "success_count": 0,
                    "error_count": 0,
                    "critical_working": 0,
                    "critical_total": 0,
                }

                # Probar todos los endpoints del servicio
                for endpoint in self.endpoints.get(service_name, []):
                    endpoint_result = self.test_endpoint_local(base_url, endpoint)
                    service_results["endpoints"].append(endpoint_result)

                    # Contadores del servicio
                    service_results["total_endpoints"] += 1

                    # Contadores globales
                    results["summary"]["total_endpoints"] += 1

                    # Contadores de endpoints críticos
                    if endpoint.get("critical"):
                        service_results["critical_total"] += 1
                        results["summary"]["critical_endpoints_total"] += 1

                        if (
                            "SUCCESS" in endpoint_result["status"]
                            or "CREATED" in endpoint_result["status"]
                        ):
                            service_results["critical_working"] += 1
                            results["summary"]["critical_endpoints_working"] += 1

                    # Clasificar resultado
                    if (
                        "SUCCESS" in endpoint_result["status"]
                        or "CREATED" in endpoint_result["status"]
                    ):
                        results["summary"]["success_count"] += 1
                        service_results["success_count"] += 1
                    elif "NOT_FOUND" in endpoint_result["status"]:
                        results["summary"]["not_found_count"] += 1
                    elif "AUTH_REQUIRED" in endpoint_result["status"]:
                        results["summary"]["auth_required_count"] += 1
                    elif "SERVER_ERROR" in endpoint_result["status"]:
                        results["summary"]["server_error_count"] += 1
                    elif "CONNECTION_ERROR" in endpoint_result["status"]:
                        results["summary"]["connection_error_count"] += 1
                    else:
                        results["summary"]["error_count"] += 1
                        service_results["error_count"] += 1

                    # Mostrar resultado con indicador crítico
                    critical_indicator = "🔴" if endpoint.get("critical") else "🔵"
                    status_icon = endpoint_result["status"].split()[0]
                    print(
                        f"    {critical_indicator} {status_icon} {endpoint_result['method']} {endpoint_result['path']} "
                        f"({endpoint_result['response_time']:.3f}s)"
                    )

                    if endpoint_result.get("error"):
                        print(f"      └─ {endpoint_result['error']}")

                results["services"][service_name] = service_results

                # Mostrar resumen del servicio
                success_rate = (
                    service_results["success_count"]
                    / service_results["total_endpoints"]
                ) * 100
                critical_rate = (
                    service_results["critical_working"]
                    / max(service_results["critical_total"], 1)
                ) * 100

                print(f"  📊 Resumen {service_name}:")
                print(
                    f"      Total: {service_results['success_count']}/{service_results['total_endpoints']} OK ({success_rate:.1f}%)"
                )
                print(
                    f"      Críticos: {service_results['critical_working']}/{service_results['critical_total']} OK ({critical_rate:.1f}%)"
                )

            else:
                print(
                    f"  💀 {service_status['status']}: {service_status.get('error', 'No disponible')}"
                )
                results["services"][service_name] = {
                    "url": base_url,
                    "service_status": service_status,
                    "endpoints": [],
                    "total_endpoints": 0,
                    "success_count": 0,
                    "error_count": 0,
                    "critical_working": 0,
                    "critical_total": 0,
                }

        # Mostrar resumen global
        self._show_local_summary(results)

        # Generar reporte local
        self._generate_local_report(results)

        return results

    def _show_local_summary(self, results: Dict[str, Any]):
        """📊 Mostrar resumen de verificación local"""

        print("\n" + "=" * 60)
        print("📊 RESUMEN DE VERIFICACIÓN LOCAL")
        print("=" * 60)

        total = results["summary"]["total_endpoints"]
        if total > 0:
            success_rate = (results["summary"]["success_count"] / total) * 100
            print(f"🎯 Tasa de éxito general: {success_rate:.1f}%")

        # Resumen de endpoints críticos
        critical_total = results["summary"]["critical_endpoints_total"]
        critical_working = results["summary"]["critical_endpoints_working"]
        if critical_total > 0:
            critical_rate = (critical_working / critical_total) * 100
            print(
                f"🔴 Endpoints críticos: {critical_working}/{critical_total} OK ({critical_rate:.1f}%)"
            )

        print(f"✅ Endpoints funcionando: {results['summary']['success_count']}")
        print(f"❌ Endpoints con error: {results['summary']['error_count']}")
        print(f"🔍 Endpoints no encontrados: {results['summary']['not_found_count']}")
        print(
            f"🔐 Endpoints que requieren auth: {results['summary']['auth_required_count']}"
        )
        print(f"💥 Errores del servidor: {results['summary']['server_error_count']}")
        print(f"🔗 Errores de conexión: {results['summary']['connection_error_count']}")
        print(f"📊 Total endpoints verificados: {total}")

        # Evaluación de estado para desarrollo
        if critical_total > 0:
            if critical_rate >= 100:
                print("\n✅ ESTADO: EXCELENTE - Todos los endpoints críticos funcionan")
            elif critical_rate >= 80:
                print("\n⚠️  ESTADO: BUENO - La mayoría de endpoints críticos funcionan")
            elif critical_rate >= 50:
                print("\n🔧 ESTADO: REGULAR - Algunos endpoints críticos fallan")
            else:
                print("\n❌ ESTADO: CRÍTICO - Muchos endpoints críticos fallan")

        print("\n🔍 PRÓXIMOS PASOS:")
        if results["summary"]["not_found_count"] > 0:
            print("  1. Corregir endpoints 404 - Verificar blueprints y rutas")
        if results["summary"]["server_error_count"] > 0:
            print("  2. Revisar logs para endpoints con error 500")
        if results["summary"]["auth_required_count"] > 0:
            print("  3. Implementar autenticación para endpoints protegidos")
        if results["summary"]["connection_error_count"] > 0:
            print("  4. Verificar que ambos servicios estén ejecutándose")

        print("\n🚀 Cuando todo funcione localmente, ¡listo para desplegar!")

    def _generate_local_report(self, results: Dict[str, Any]):
        """📋 Generar reporte de verificación local"""

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = f"c:/Smarwatt_2/SmarWatt_2/backend/sevicio chatbot/servicios/Y DOCUMENTACION/MINISERVICIOS_SCRIPS/VERIFICACION ENDOPOIN/REPORTE_LOCAL_{timestamp}.md"

        total = results["summary"]["total_endpoints"]
        success_rate = (
            (results["summary"]["success_count"] / total * 100) if total > 0 else 0
        )
        critical_total = results["summary"]["critical_endpoints_total"]
        critical_working = results["summary"]["critical_endpoints_working"]
        critical_rate = (
            (critical_working / critical_total * 100) if critical_total > 0 else 0
        )

        report = f"""# 🏢 REPORTE DE VERIFICACIÓN LOCAL - SMARWATT MICROSERVICIOS

**Fecha de Verificación:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Tipo de Verificación:** Desarrollo Local  
**Entorno:** Local Development  
**Versión del Verificador:** 1.0.0

## 🎯 RESUMEN EJECUTIVO LOCAL

| Métrica | Valor | Porcentaje |
|---------|-------|------------|
| **Total Endpoints** | {total} | 100% |
| **✅ Funcionando** | {results['summary']['success_count']} | {(results['summary']['success_count']/total*100) if total > 0 else 0:.1f}% |
| **🔴 Endpoints Críticos** | {critical_working}/{critical_total} | {critical_rate:.1f}% |
| **❌ Con Errores** | {results['summary']['error_count']} | {(results['summary']['error_count']/total*100) if total > 0 else 0:.1f}% |
| **🔍 No Encontrados** | {results['summary']['not_found_count']} | {(results['summary']['not_found_count']/total*100) if total > 0 else 0:.1f}% |
| **🔐 Requieren Auth** | {results['summary']['auth_required_count']} | {(results['summary']['auth_required_count']/total*100) if total > 0 else 0:.1f}% |
| **💥 Error Servidor** | {results['summary']['server_error_count']} | {(results['summary']['server_error_count']/total*100) if total > 0 else 0:.1f}% |
| **🔗 Error Conexión** | {results['summary']['connection_error_count']} | {(results['summary']['connection_error_count']/total*100) if total > 0 else 0:.1f}% |

**🎯 Tasa de Éxito General:** {success_rate:.1f}%  
**🔴 Tasa de Éxito Críticos:** {critical_rate:.1f}%

## 🔗 CONFIGURACIÓN LOCAL

### Expert Bot API
- **URL Local:** `{EXPERT_BOT_LOCAL_URL}`
- **Puerto:** 8080
- **Comando:** `cd expert_bot_api_COPY && python run.py`

### Energy IA API  
- **URL Local:** `{ENERGY_IA_LOCAL_URL}`
- **Puerto:** 8081  
- **Comando:** `cd energy_ia_api_COPY && python run.py`

---

"""

        # Detallar cada servicio
        for service_name, service_data in results["services"].items():

            service_title = service_name.upper().replace("_", " ")
            report += f"""
## 🔧 {service_title}

**URL Local:** `{service_data.get('url', 'N/A')}`  
"""

            service_status = service_data.get("service_status", {})
            report += f"**Estado del Servicio:** {service_status.get('status', 'Unknown')}  \n"

            if service_status.get("response_time"):
                report += f"**Tiempo de Respuesta:** {service_status['response_time']:.3f}s  \n"

            if service_status.get("error"):
                report += f"**Error:** {service_status['error']}  \n"

            total_svc = service_data.get("total_endpoints", 0)
            success_svc = service_data.get("success_count", 0)
            critical_svc = service_data.get("critical_working", 0)
            critical_total_svc = service_data.get("critical_total", 0)

            if total_svc > 0:
                success_rate_svc = (success_svc / total_svc) * 100
                report += f"**Tasa de Éxito:** {success_rate_svc:.1f}% ({success_svc}/{total_svc})  \n"

            if critical_total_svc > 0:
                critical_rate_svc = (critical_svc / critical_total_svc) * 100
                report += f"**Críticos Funcionando:** {critical_rate_svc:.1f}% ({critical_svc}/{critical_total_svc})  \n"

            report += "\n### 📋 ENDPOINTS VERIFICADOS\n\n"

            if not service_data.get("endpoints"):
                report += (
                    "❌ **Servicio no disponible o sin endpoints verificables**\n\n"
                )
                continue

            # Agrupar por estado y criticidad
            critical_endpoints = [
                e for e in service_data.get("endpoints", []) if e.get("is_critical")
            ]
            normal_endpoints = [
                e for e in service_data.get("endpoints", []) if not e.get("is_critical")
            ]

            if critical_endpoints:
                report += "\n#### 🔴 ENDPOINTS CRÍTICOS\n\n"
                for endpoint in critical_endpoints:
                    status = endpoint.get("status", "unknown")
                    path = endpoint.get("path", "")
                    method = endpoint.get("method", "")
                    desc = endpoint.get("description", "")

                    report += f"**`{method} {path}`** 🔴\n"
                    report += f"- **Descripción:** {desc}\n"
                    report += f"- **Estado:** {status}\n"
                    report += f"- **Código HTTP:** {endpoint.get('http_code', 'N/A')}\n"
                    report += f"- **Tiempo:** {endpoint.get('response_time', 0):.3f}s\n"

                    if endpoint.get("error"):
                        report += f"- **⚠️ Error:** {endpoint['error']}\n"

                    if "SUCCESS" in status and endpoint.get("response_sample"):
                        sample = endpoint["response_sample"]
                        if isinstance(sample, dict):
                            sample_str = json.dumps(
                                sample, indent=2, ensure_ascii=False
                            )[:300]
                        else:
                            sample_str = str(sample)[:300]
                        report += (
                            f"- **📄 Respuesta Local:**\n```json\n{sample_str}\n```\n"
                        )

                    report += "\n"

            if normal_endpoints:
                report += "\n#### 🔵 ENDPOINTS NORMALES\n\n"
                for endpoint in normal_endpoints:
                    status = endpoint.get("status", "unknown")
                    path = endpoint.get("path", "")
                    method = endpoint.get("method", "")
                    desc = endpoint.get("description", "")

                    report += f"**`{method} {path}`**\n"
                    report += f"- **Estado:** {status}\n"
                    report += f"- **Descripción:** {desc}\n"
                    report += f"- **Tiempo:** {endpoint.get('response_time', 0):.3f}s\n"

                    if endpoint.get("error"):
                        report += f"- **⚠️ Error:** {endpoint['error']}\n"

                    report += "\n"

        # Análisis específico para desarrollo local
        report += f"""

---

## 🛠️ ANÁLISIS PARA DESARROLLO LOCAL

### ✅ Aspectos Positivos

- **Servicios Locales:** Los microservicios se pueden ejecutar localmente
- **Health Checks:** Los endpoints de salud están implementados
- **Arquitectura:** La estructura de microservicios es sólida
"""
        if critical_rate >= 80:
            report += "- **Endpoints Críticos:** La mayoría de funcionalidades críticas funcionan\n"

        if results["summary"]["success_count"] > 0:
            report += f"- **Endpoints Funcionales:** {results['summary']['success_count']} endpoints están operativos\n"

        report += """
### ⚠️ Problemas Identificados en Desarrollo

"""

        if results["summary"]["connection_error_count"] > 0:
            report += f"- **Servicios No Ejecutándose:** {results['summary']['connection_error_count']} servicios no están disponibles\n"

        if results["summary"]["not_found_count"] > 0:
            report += f"- **Endpoints 404:** {results['summary']['not_found_count']} endpoints no encontrados - Verificar blueprints\n"

        if results["summary"]["server_error_count"] > 0:
            report += f"- **Errores 500:** {results['summary']['server_error_count']} endpoints con errores internos - Revisar configuración\n"

        if results["summary"]["auth_required_count"] > 0:
            report += f"- **Autenticación:** {results['summary']['auth_required_count']} endpoints requieren tokens JWT válidos\n"

        report += f"""
### 🔧 PLAN DE ACCIÓN LOCAL

#### 1. ANTES DE CONTINUAR DESARROLLO
- [ ] Asegurar que ambos servicios se ejecuten sin errores
- [ ] Corregir todos los endpoints críticos que fallan
- [ ] Implementar autenticación JWT básica para desarrollo
- [ ] Verificar configuración de variables de entorno locales

#### 2. CORRECCIONES INMEDIATAS
"""

        if results["summary"]["not_found_count"] > 0:
            report += "- [ ] Registrar blueprints faltantes en app/__init__.py\n"

        if results["summary"]["server_error_count"] > 0:
            report += "- [ ] Revisar logs de errores 500 y corregir configuración\n"

        if results["summary"]["connection_error_count"] > 0:
            report += "- [ ] Iniciar servicios que no están ejecutándose\n"

        report += f"""
#### 3. VALIDACIÓN ANTES DE DESPLIEGUE
- [ ] Tasa de éxito de endpoints críticos >= 90%
- [ ] Tasa de éxito general >= 80%
- [ ] Todos los servicios health check OK
- [ ] Sin errores 500 en endpoints críticos

#### 4. CONFIGURACIÓN PARA DESPLIEGUE
- [ ] Verificar variables de entorno para producción
- [ ] Configurar credenciales de Google Cloud correctamente
- [ ] Verificar configuración de BigQuery y Firebase
- [ ] Probar autenticación con tokens reales

## 📊 COMANDOS ÚTILES PARA DESARROLLO

### Iniciar Expert Bot API
```bash
cd c:\\Smarwatt_2\\SmarWatt_2\\backend\\sevicio chatbot\\servicios\\expert_bot_api_COPY
python run.py
```

### Iniciar Energy IA API
```bash
cd c:\\Smarwatt_2\\SmarWatt_2\\backend\\sevicio chatbot\\servicios\\energy_ia_api_COPY  
python run.py
```

### Verificar Endpoints Localmente
```bash
cd "c:\\...\\VERIFICACION ENDOPOIN"
python verificar_endpoints_local.py
```

### Ver Logs en Tiempo Real
```bash
# En la carpeta de cada servicio
tail -f logs/*.log
```

---

## 📞 SOPORTE DE DESARROLLO

**Equipo:** SmarWatt Development Team  
**Documentación Local:** Ver README.md en cada microservicio  
**Logs:** Disponibles en carpeta logs/ de cada servicio  
**Configuración:** Ver archivos config.py en cada servicio  

---

*Reporte de desarrollo local generado automáticamente el {datetime.now().strftime('%Y-%m-%d a las %H:%M:%S')}*  
*Para verificar cambios después de modificaciones, ejecute este script nuevamente.*

**Estado para Despliegue:** {'✅ LISTO' if critical_rate >= 90 and success_rate >= 80 else '❌ NO LISTO - Corregir errores primero'}
"""

        try:
            with open(report_path, "w", encoding="utf-8") as f:
                f.write(report)
            print(f"\n📁 Reporte local guardado:")
            print(f"   📋 {report_path}")
        except Exception as e:
            print(f"❌ Error guardando reporte: {e}")

        # También guardar JSON
        json_path = report_path.replace(".md", ".json")
        try:
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"   📊 {json_path}")
        except Exception as e:
            print(f"❌ Error guardando JSON: {e}")


def main():
    """🚀 Función principal para verificación local"""

    verifier = LocalEndpointVerifier()

    try:
        results = verifier.verify_local_services()

        total = results["summary"]["total_endpoints"]
        success = results["summary"]["success_count"]
        critical_working = results["summary"]["critical_endpoints_working"]
        critical_total = results["summary"]["critical_endpoints_total"]

        print(f"\n🎉 VERIFICACIÓN LOCAL COMPLETADA")
        print("=" * 50)

        if total > 0:
            success_rate = (success / total) * 100
            print(
                f"🎯 Resultado General: {success}/{total} endpoints OK ({success_rate:.1f}%)"
            )

            if critical_total > 0:
                critical_rate = (critical_working / critical_total) * 100
                print(
                    f"🔴 Endpoints Críticos: {critical_working}/{critical_total} OK ({critical_rate:.1f}%)"
                )

                # Evaluación para despliegue
                if critical_rate >= 90 and success_rate >= 80:
                    print("\n✅ ESTADO: LISTO PARA DESPLEGAR")
                    print("   Los endpoints críticos funcionan correctamente")
                elif critical_rate >= 70:
                    print("\n⚠️  ESTADO: CASI LISTO - Corregir algunos problemas")
                    print("   La mayoría de endpoints críticos funcionan")
                else:
                    print("\n❌ ESTADO: NO LISTO PARA DESPLEGAR")
                    print(
                        "   Muchos endpoints críticos fallan - Corregir antes de desplegar"
                    )

        print("\n📁 Consulte el reporte detallado para más información")

        return 0 if (critical_working / max(critical_total, 1)) >= 0.9 else 1

    except KeyboardInterrupt:
        print("\n⏹️  Verificación cancelada por el usuario")
        return 1

    except Exception as e:
        print(f"\n💥 Error durante la verificación: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
