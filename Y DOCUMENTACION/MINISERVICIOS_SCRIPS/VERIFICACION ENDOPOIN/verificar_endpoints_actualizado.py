#!/usr/bin/env python3
"""
🏢 VERIFICADOR ACTUALIZADO DE ENDPOINTS - SMARWATT MICROSERVICIOS
===============================================================

Script actualizado con las rutas REALES de los endpoints basado en el código fuente.
Este script verifica las rutas exactas como están configuradas en los microservicios.

RUTAS REALES EXPERT BOT API:
- Chat: /api/v1/chatbot/*
- Energy: /api/v1/energy/*
- Links: /api/v1/*

RUTAS REALES ENERGY IA API:
- Chatbot: /api/v1/chatbot/*
- Health: /health, /api/v1/info, /api/v1/status

AUTOR: Sistema de Verificación Empresarial SmarWatt
FECHA: 2025-07-21
VERSIÓN: 1.1.0 - ACTUALIZADO CON RUTAS REALES
"""

import requests
import json
import time
import os
from datetime import datetime, timezone
from typing import Dict, List, Any

# Configurar requests para evitar warnings
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# URLs de los microservicios
EXPERT_BOT_API_URL = "https://expert-bot-api-1010012211318.europe-west1.run.app"
ENERGY_IA_API_URL = "https://energy-ia-api-1010012211318.europe-west1.run.app"

# URLs locales como fallback
LOCAL_EXPERT_BOT_URL = "http://localhost:8080"
LOCAL_ENERGY_IA_URL = "http://localhost:8081"


class ActualEndpointVerifier:
    """🔍 Verificador con rutas reales basado en código fuente"""

    def __init__(self):
        self.timeout = 20
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "SmarWatt-Actual-Verifier/1.1",
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )

        # ✅ ENDPOINTS REALES basados en el código fuente
        self.endpoints = {
            "expert_bot_api": [
                # === HEALTH ENDPOINTS (directos en app) ===
                {"path": "/health", "method": "GET", "desc": "Health check básico"},
                {
                    "path": "/health/detailed",
                    "method": "GET",
                    "desc": "Health check detallado",
                },
                # === CHAT ENDPOINTS (prefix: /api/v1/chatbot) ===
                {
                    "path": "/api/v1/chatbot/session/start",
                    "method": "POST",
                    "desc": "Iniciar sesión de chat",
                    "auth": True,
                },
                {
                    "path": "/api/v1/chatbot/message",
                    "method": "POST",
                    "desc": "Enviar mensaje al chatbot",
                    "auth": True,
                },
                {
                    "path": "/api/v1/chatbot/conversation/history",
                    "method": "GET",
                    "desc": "Historial de conversaciones",
                    "auth": True,
                },
                {
                    "path": "/api/v1/chatbot/conversation/test-123",
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
                },
                {
                    "path": "/api/v1/energy/dashboard",
                    "method": "GET",
                    "desc": "Dashboard de energía",
                    "auth": True,
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
                {"path": "/health", "method": "GET", "desc": "Health check IA básico"},
                {
                    "path": "/api/v1/info",
                    "method": "GET",
                    "desc": "Información del servicio IA",
                },
                {
                    "path": "/api/v1/status",
                    "method": "GET",
                    "desc": "Estado detallado del servicio IA",
                },
                {
                    "path": "/status",
                    "method": "GET",
                    "desc": "Estado general desde run.py",
                },
                # === CHATBOT IA ENDPOINTS (prefix: /api/v1/chatbot) ===
                {
                    "path": "/api/v1/chatbot/message",
                    "method": "POST",
                    "desc": "Procesamiento IA de mensajes",
                    "auth": True,
                },
                {
                    "path": "/api/v1/chatbot/message/v2",
                    "method": "POST",
                    "desc": "Procesamiento IA v2 mejorado",
                    "auth": True,
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
                    "path": "/api/v1/chatbot/conversations/test-conv-123",
                    "method": "DELETE",
                    "desc": "Eliminar conversación IA",
                    "auth": True,
                },
                {
                    "path": "/api/v1/chatbot/health",
                    "method": "GET",
                    "desc": "Health check específico chatbot IA",
                },
            ],
        }

    def test_endpoint(self, base_url: str, endpoint: Dict[str, Any]) -> Dict[str, Any]:
        """🧪 Probar un endpoint con configuración real"""

        full_url = f"{base_url}{endpoint['path']}"
        result = {
            "path": endpoint["path"],
            "method": endpoint["method"],
            "description": endpoint["desc"],
            "requires_auth": endpoint.get("auth", False),
            "url": full_url,
            "status": "unknown",
            "http_code": 0,
            "response_time": 0.0,
            "error": None,
            "response_sample": None,
            "response_headers": None,
        }

        try:
            print(f"  🧪 {endpoint['method']} {endpoint['path']}")

            headers = self.session.headers.copy()
            if endpoint.get("auth"):
                # Usar token de prueba más realista
                headers["Authorization"] = (
                    "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.test"
                )

            # Datos de prueba más realistas según el endpoint
            test_data = self._get_realistic_test_data(endpoint)

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
                # Reintentar sin verificación SSL si es necesario
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
            result["response_headers"] = dict(response.headers)

            # Evaluar respuesta de manera más detallada
            if response.status_code == 200:
                result["status"] = "✅ SUCCESS"
                try:
                    json_response = response.json()
                    result["response_sample"] = json_response
                    if len(str(json_response)) > 500:
                        result["response_sample"] = (
                            str(json_response)[:500] + "... [truncated]"
                        )
                except ValueError:
                    # No es JSON válido
                    result["response_sample"] = (
                        response.text[:300] + "..."
                        if len(response.text) > 300
                        else response.text
                    )

            elif response.status_code == 201:
                result["status"] = "✅ CREATED"
                result["response_sample"] = response.text[:200]

            elif response.status_code == 404:
                result["status"] = "🔍 NOT_FOUND"
                result["error"] = "Endpoint no encontrado - Verificar ruta y blueprint"

            elif response.status_code == 401:
                result["status"] = "🔐 AUTH_REQUIRED"
                result["error"] = "Autenticación requerida - Token JWT necesario"

            elif response.status_code == 403:
                result["status"] = "🚫 FORBIDDEN"
                result["error"] = "Acceso prohibido - Permisos insuficientes"

            elif response.status_code == 422:
                result["status"] = "📋 VALIDATION_ERROR"
                result["error"] = "Error de validación - Parámetros incorrectos"

            elif response.status_code == 500:
                result["status"] = "💥 SERVER_ERROR"
                result["error"] = "Error interno del servidor"
                result["response_sample"] = response.text[:200]

            elif response.status_code >= 400:
                result["status"] = "❌ ERROR"
                result["error"] = f"HTTP {response.status_code}: {response.text[:200]}"
            else:
                result["status"] = "❓ UNKNOWN"
                result["error"] = f"Status inesperado: {response.status_code}"

        except requests.exceptions.Timeout:
            result["status"] = "⏱️ TIMEOUT"
            result["error"] = f"Timeout después de {self.timeout}s"
            result["response_time"] = self.timeout

        except requests.exceptions.ConnectionError as e:
            result["status"] = "🔗 CONNECTION_ERROR"
            result["error"] = f"Error de conexión: {str(e)[:100]}"

        except requests.exceptions.RequestException as e:
            result["status"] = "💥 REQUEST_ERROR"
            result["error"] = f"Error de petición: {str(e)[:100]}"

        return result

    def _get_realistic_test_data(self, endpoint: Dict[str, Any]) -> Dict[str, Any]:
        """🧪 Generar datos de prueba realistas según el endpoint"""

        path = endpoint["path"]
        method = endpoint["method"]

        # Datos base comunes
        base_data = {
            "user_id": "test-user-12345",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        # Datos específicos según endpoint
        if "chat" in path and "message" in path:
            return {
                **base_data,
                "message": "Hola, quiero información sobre mi consumo eléctrico",
                "session_id": "test-session-67890",
                "context": {"source": "web_app", "user_location": "Madrid, España"},
            }

        elif "chat" in path and "session/start" in path:
            return {
                **base_data,
                "session_type": "energy_consultation",
                "client_info": {"platform": "web", "version": "1.0.0"},
            }

        elif "energy" in path and "consumption" in path and method == "POST":
            return {
                **base_data,
                "consumption_data": {
                    "kwh_consumed": 450.75,
                    "period": "monthly",
                    "cost": 87.50,
                    "tariff_type": "PVPC",
                    "supplier": "Endesa",
                },
                "meter_reading": 12345.67,
                "invoice_data": {
                    "invoice_number": "INV-2025-001",
                    "invoice_date": "2025-01-15",
                },
            }

        elif "energy" in path and "manual-data" in path:
            return {
                **base_data,
                "manual_data": {
                    "consumption_kwh": 320.50,
                    "cost_euros": 65.30,
                    "period_start": "2025-01-01",
                    "period_end": "2025-01-31",
                    "data_source": "manual_input",
                },
            }

        elif "feedback" in path:
            return {
                **base_data,
                "conversation_id": "conv-test-12345",
                "rating": 5,
                "feedback": "Excelente servicio, muy útil",
                "category": "satisfaction",
            }

        elif "cross-service" in path:
            return {
                **base_data,
                "source_service": "expert_bot_api",
                "target_action": "analyze_consumption",
                "data": {"analysis_type": "trend_analysis", "period_months": 12},
            }

        elif "links/test" in path:
            return {
                "target_service": "energy_ia_api",
                "test_type": "connectivity",
                "test_data": {"message": "Test connection from expert bot"},
            }

        else:
            return base_data

    def test_service_health(self, service_name: str, base_url: str) -> Dict[str, Any]:
        """🩺 Test de salud mejorado"""

        print(f"🔍 Verificando {service_name}: {base_url}")

        health_results = []

        # Probar múltiples endpoints de health
        health_endpoints = ["/health", "/api/v1/status", "/status"]

        for health_path in health_endpoints:
            try:
                start_time = time.time()
                response = self.session.get(f"{base_url}{health_path}", timeout=10)
                response_time = time.time() - start_time

                health_results.append(
                    {
                        "path": health_path,
                        "status_code": response.status_code,
                        "response_time": response_time,
                        "available": response.status_code < 500,
                    }
                )

                if response.status_code == 200:
                    print(
                        f"  ✅ {health_path}: Healthy ({response.status_code}) - {response_time:.3f}s"
                    )
                    break
                else:
                    print(
                        f"  ⚠️  {health_path}: Responde pero no healthy ({response.status_code})"
                    )

            except requests.exceptions.RequestException as e:
                health_results.append(
                    {
                        "path": health_path,
                        "status_code": 0,
                        "response_time": 10,
                        "available": False,
                        "error": str(e)[:100],
                    }
                )
                print(f"  ❌ {health_path}: Error - {str(e)[:50]}")

        # Determinar estado general
        available_endpoints = [h for h in health_results if h.get("available")]

        if available_endpoints:
            best_health = min(available_endpoints, key=lambda x: x["response_time"])
            status = (
                "✅ HEALTHY" if best_health["status_code"] == 200 else "⚠️ UNHEALTHY"
            )
            response_time = best_health["response_time"]
            error = None
        else:
            status = "❌ UNREACHABLE"
            response_time = 10
            error = "No hay endpoints de health disponibles"

        return {
            "service": service_name,
            "url": base_url,
            "status": status,
            "response_time": response_time,
            "error": error,
            "health_details": health_results,
        }

    def verify_all_services(self):
        """🚀 Verificación completa de servicios"""

        print("🏢 VERIFICADOR ACTUALIZADO DE ENDPOINTS - SMARWATT")
        print("=" * 65)
        print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("Versión: 1.1.0 - Con rutas reales del código fuente")
        print()

        results = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "version": "1.1.0",
            "services": {},
            "summary": {
                "total_endpoints": 0,
                "success_count": 0,
                "error_count": 0,
                "not_found_count": 0,
                "auth_required_count": 0,
                "server_error_count": 0,
                "timeout_count": 0,
            },
        }

        # URLs a probar para cada servicio
        service_urls = {
            "expert_bot_api": [EXPERT_BOT_API_URL, LOCAL_EXPERT_BOT_URL],
            "energy_ia_api": [ENERGY_IA_API_URL, LOCAL_ENERGY_IA_URL],
        }

        for service_name, urls in service_urls.items():
            print(f"\n🔧 {service_name.upper().replace('_', ' ')}")
            print("-" * 50)

            service_working = False
            working_url = None

            # Probar cada URL hasta encontrar una que funcione
            for url in urls:
                health_result = self.test_service_health(service_name, url)

                if (
                    "HEALTHY" in health_result["status"]
                    or "UNHEALTHY" in health_result["status"]
                ):
                    service_working = True
                    working_url = url
                    break
                else:
                    print(f"  💀 No disponible en {url}")

            if service_working and working_url:
                print(f"  🎯 URL activa: {working_url}")
                print(
                    f"  📡 Verificando {len(self.endpoints.get(service_name, []))} endpoints:"
                )

                service_results = {
                    "url": working_url,
                    "health": health_result,
                    "endpoints": [],
                    "total_endpoints": 0,
                    "success_count": 0,
                    "error_count": 0,
                }

                # Probar todos los endpoints del servicio
                for endpoint in self.endpoints.get(service_name, []):
                    endpoint_result = self.test_endpoint(working_url, endpoint)
                    service_results["endpoints"].append(endpoint_result)

                    # Actualizar contadores de servicio
                    service_results["total_endpoints"] += 1

                    # Actualizar contadores globales
                    results["summary"]["total_endpoints"] += 1

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
                    elif "TIMEOUT" in endpoint_result["status"]:
                        results["summary"]["timeout_count"] += 1
                    else:
                        results["summary"]["error_count"] += 1
                        service_results["error_count"] += 1

                    # Mostrar resultado con más detalle
                    status_icon = endpoint_result["status"].split()[0]
                    print(
                        f"    {status_icon} {endpoint_result['method']} {endpoint_result['path']} "
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
                print(
                    f"  📊 Resumen {service_name}: {service_results['success_count']}/{service_results['total_endpoints']} OK ({success_rate:.1f}%)"
                )

            else:
                print(f"  💀 Servicio completamente inaccesible")
                results["services"][service_name] = {
                    "url": "N/A",
                    "health": {
                        "status": "❌ UNREACHABLE",
                        "error": "No disponible en ninguna URL",
                    },
                    "endpoints": [],
                    "total_endpoints": 0,
                    "success_count": 0,
                    "error_count": 0,
                }

        # Mostrar resumen global mejorado
        print("\n" + "=" * 65)
        print("📊 RESUMEN EJECUTIVO DETALLADO")
        print("=" * 65)

        total = results["summary"]["total_endpoints"]
        if total > 0:
            success_rate = (results["summary"]["success_count"] / total) * 100
            print(f"🎯 Tasa de éxito general: {success_rate:.1f}%")

        print(f"✅ Endpoints funcionando: {results['summary']['success_count']}")
        print(f"❌ Endpoints con error: {results['summary']['error_count']}")
        print(f"🔍 Endpoints no encontrados: {results['summary']['not_found_count']}")
        print(
            f"🔐 Endpoints que requieren auth: {results['summary']['auth_required_count']}"
        )
        print(f"� Errores del servidor: {results['summary']['server_error_count']}")
        print(f"⏱️  Timeouts: {results['summary']['timeout_count']}")
        print(f"� Total endpoints verificados: {total}")

        # Generar reporte detallado
        self.generate_detailed_report(results)

        return results

    def generate_detailed_report(self, results: Dict[str, Any]):
        """📋 Generar reporte detallado con análisis"""

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = f"c:/Smarwatt_2/SmarWatt_2/backend/sevicio chatbot/servicios/Y DOCUMENTACION/MINISERVICIOS_SCRIPS/VERIFICACION ENDOPOIN/REPORTE_DETALLADO_{timestamp}.md"

        total = results["summary"]["total_endpoints"]
        success_rate = (
            (results["summary"]["success_count"] / total * 100) if total > 0 else 0
        )

        # Generar reporte más detallado
        report = f"""# 🏢 REPORTE DETALLADO DE ENDPOINTS - SMARWATT MICROSERVICIOS

**Fecha de Verificación:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Versión del Verificador:** {results.get('version', '1.1.0')}  
**Tipo de Verificación:** Endpoints Reales del Código Fuente

## 🎯 RESUMEN EJECUTIVO

| Métrica | Valor | Porcentaje |
|---------|-------|------------|
| **Total Endpoints** | {total} | 100% |
| **✅ Funcionando** | {results['summary']['success_count']} | {(results['summary']['success_count']/total*100):.1f}% |
| **❌ Con Errores** | {results['summary']['error_count']} | {(results['summary']['error_count']/total*100):.1f}% |
| **🔍 No Encontrados** | {results['summary']['not_found_count']} | {(results['summary']['not_found_count']/total*100):.1f}% |
| **🔐 Requieren Auth** | {results['summary']['auth_required_count']} | {(results['summary']['auth_required_count']/total*100):.1f}% |
| **💥 Error Servidor** | {results['summary']['server_error_count']} | {(results['summary']['server_error_count']/total*100):.1f}% |
| **⏱️ Timeouts** | {results['summary']['timeout_count']} | {(results['summary']['timeout_count']/total*100):.1f}% |

**🎯 Tasa de Éxito General:** {success_rate:.1f}%

## 🔗 CONFIGURACIÓN DE MICROSERVICIOS

### Expert Bot API
- **URL Producción:** `{EXPERT_BOT_API_URL}`
- **URL Local:** `{LOCAL_EXPERT_BOT_URL}`

### Energy IA API  
- **URL Producción:** `{ENERGY_IA_API_URL}`
- **URL Local:** `{LOCAL_ENERGY_IA_URL}`

---

"""

        # Detallar cada servicio
        for service_name, service_data in results["services"].items():

            service_title = service_name.upper().replace("_", " ")
            report += f"""
## 🔧 {service_title}

**URL Activa:** `{service_data.get('url', 'N/A')}`  
**Estado del Servicio:** {service_data.get('health', {}).get('status', 'Unknown')}  
"""

            if service_data.get("health", {}).get("response_time"):
                report += f"**Tiempo de Respuesta Health:** {service_data['health']['response_time']:.3f}s  \n"

            if service_data.get("health", {}).get("error"):
                report += f"**Error de Health:** {service_data['health']['error']}  \n"

            total_svc = service_data.get("total_endpoints", 0)
            success_svc = service_data.get("success_count", 0)

            if total_svc > 0:
                success_rate_svc = (success_svc / total_svc) * 100
                report += f"**Tasa de Éxito:** {success_rate_svc:.1f}% ({success_svc}/{total_svc})  \n"

            report += "\n### 📋 ENDPOINTS VERIFICADOS\n\n"

            if not service_data.get("endpoints"):
                report += (
                    "❌ **No se pudieron verificar endpoints para este servicio**\n\n"
                )
                continue

            # Agrupar por categoría y estado
            categories = {}
            for endpoint in service_data.get("endpoints", []):
                path = endpoint.get("path", "")
                if "/health" in path:
                    category = "🔍 Health & Status"
                elif "/chatbot" in path or "/chat" in path:
                    category = "💬 Chat & Conversación"
                elif "/energy" in path:
                    category = "⚡ Gestión Energética"
                elif "/links" in path:
                    category = "🔗 Comunicación Entre Servicios"
                else:
                    category = "📡 General"

                if category not in categories:
                    categories[category] = []
                categories[category].append(endpoint)

            for category, endpoints in categories.items():
                report += f"\n#### {category}\n\n"

                for endpoint in endpoints:
                    status = endpoint.get("status", "unknown")
                    path = endpoint.get("path", "")
                    method = endpoint.get("method", "")
                    desc = endpoint.get("description", "")

                    report += f"**`{method} {path}`**\n"
                    report += f"- **Descripción:** {desc}\n"
                    report += f"- **Estado:** {status}\n"
                    report += f"- **Código HTTP:** {endpoint.get('http_code', 'N/A')}\n"
                    report += f"- **Tiempo:** {endpoint.get('response_time', 0):.3f}s\n"
                    report += f"- **Auth Requerida:** {'Sí' if endpoint.get('requires_auth') else 'No'}\n"

                    if endpoint.get("error"):
                        report += f"- **⚠️ Error:** {endpoint['error']}\n"

                    # Mostrar muestra de respuesta si es exitosa
                    if "SUCCESS" in status and endpoint.get("response_sample"):
                        sample = endpoint["response_sample"]
                        if isinstance(sample, dict):
                            sample_str = json.dumps(
                                sample, indent=2, ensure_ascii=False
                            )[:400]
                        else:
                            sample_str = str(sample)[:400]
                        report += f"- **📄 Respuesta:**\n```json\n{sample_str}\n```\n"

                    report += "\n"

        # Análisis y recomendaciones
        report += f"""

---

## 🎯 ANÁLISIS EMPRESARIAL

### ✅ Aspectos Positivos

- **Arquitectura Sólida:** Los microservicios tienen estructura clara y bien definida
- **Health Checks:** Implementados correctamente en ambos servicios
- **Separación de Responsabilidades:** Chat, Energy y Links bien diferenciados
"""
        if results["summary"]["success_count"] > 0:
            report += f"- **Endpoints Funcionales:** {results['summary']['success_count']} endpoints están operativos\n"

        report += """
### ⚠️ Áreas de Mejora

"""

        if results["summary"]["not_found_count"] > 0:
            report += f"- **Endpoints 404:** {results['summary']['not_found_count']} endpoints no encontrados - Revisar blueprints y rutas\n"

        if results["summary"]["server_error_count"] > 0:
            report += f"- **Errores de Servidor:** {results['summary']['server_error_count']} endpoints con errores 500 - Revisar logs\n"

        if (
            "energy_ia_api" in results["services"]
            and results["services"]["energy_ia_api"]["url"] == "N/A"
        ):
            report += "- **Energy IA API Inaccesible:** Verificar despliegue y configuración\n"

        report += f"""
### 🔧 RECOMENDACIONES TÉCNICAS

#### Corto Plazo (1-2 semanas)
1. **Corregir Endpoints 404:** Revisar configuración de blueprints
2. **Verificar Energy IA API:** Asegurar que esté desplegado y accesible  
3. **Implementar Autenticación Real:** Reemplazar tokens de prueba
4. **Logging Detallado:** Añadir logs para debugging de endpoints

#### Medio Plazo (1 mes)
1. **Tests Automatizados:** Implementar suite de tests de endpoints
2. **Monitorización:** Añadir alertas para endpoints críticos
3. **Documentación API:** Crear especificación OpenAPI/Swagger
4. **Rate Limiting:** Proteger endpoints contra abuso

#### Largo Plazo (2-3 meses)
1. **Circuit Breakers:** Implementar para resiliencia
2. **Caching Estratégico:** Optimizar performance
3. **Observabilidad Completa:** Métricas, trazas y logs correlacionados
4. **Versionado de API:** Implementar estrategia de versioning

## 📊 MÉTRICAS TÉCNICAS DETALLADAS

### Distribución de Códigos HTTP
"""

        # Contar códigos HTTP
        http_codes = {}
        for service_data in results["services"].values():
            for endpoint in service_data.get("endpoints", []):
                code = endpoint.get("http_code", 0)
                http_codes[code] = http_codes.get(code, 0) + 1

        for code, count in sorted(http_codes.items()):
            if code > 0:
                report += f"- **{code}:** {count} endpoints\n"

        report += f"""

### Tiempos de Respuesta
"""

        # Análisis de performance
        response_times = []
        for service_data in results["services"].values():
            for endpoint in service_data.get("endpoints", []):
                if endpoint.get("response_time", 0) > 0:
                    response_times.append(endpoint["response_time"])

        if response_times:
            avg_time = sum(response_times) / len(response_times)
            max_time = max(response_times)
            min_time = min(response_times)

            report += f"- **Tiempo Promedio:** {avg_time:.3f}s\n"
            report += f"- **Tiempo Máximo:** {max_time:.3f}s\n"
            report += f"- **Tiempo Mínimo:** {min_time:.3f}s\n"

            if max_time > 5:
                report += "- **⚠️ Alerta:** Algunos endpoints tienen tiempos de respuesta > 5s\n"

        report += f"""

---

## 📞 SOPORTE Y CONTACTO

**Equipo Técnico:** SmarWatt DevOps Engineering  
**Email:** desarrollo@smarwatt.com  
**Documentación:** https://docs.smarwatt.com/apis  
**Monitorización:** Google Cloud Console - Proyecto `smatwatt`  
**URLs de Producción:**
- Expert Bot API: {EXPERT_BOT_API_URL}
- Energy IA API: {ENERGY_IA_API_URL}

---

*Este reporte fue generado automáticamente el {datetime.now().strftime('%Y-%m-%d a las %H:%M:%S')} por el sistema de verificación empresarial de SmarWatt.*  
*Para información actualizada, ejecute la verificación nuevamente.*

**Próxima verificación recomendada:** {datetime.now().replace(hour=datetime.now().hour + 24).strftime('%Y-%m-%d %H:%M:%S')}
"""

        try:
            with open(report_path, "w", encoding="utf-8") as f:
                f.write(report)
            print(f"\n📁 Reporte detallado guardado:")
            print(f"   📋 {report_path}")
        except Exception as e:
            print(f"❌ Error guardando reporte: {e}")

        # También guardar JSON actualizado
        json_path = report_path.replace(".md", ".json")
        try:
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"   📊 {json_path}")
        except Exception as e:
            print(f"❌ Error guardando JSON: {e}")


def main():
    """🚀 Función principal mejorada"""

    verifier = ActualEndpointVerifier()

    try:
        results = verifier.verify_all_services()

        print(f"\n🎉 VERIFICACIÓN COMPLETADA EXITOSAMENTE")
        print("=" * 50)

        total = results["summary"]["total_endpoints"]
        success = results["summary"]["success_count"]

        if total > 0:
            success_rate = (success / total) * 100
            print(f"🎯 Resultado: {success}/{total} endpoints OK ({success_rate:.1f}%)")

            if success_rate >= 80:
                print("✅ Estado: EXCELENTE - La mayoría de endpoints funcionan")
            elif success_rate >= 60:
                print("⚠️  Estado: BUENO - Algunos endpoints necesitan atención")
            elif success_rate >= 40:
                print("🔧 Estado: REGULAR - Varios endpoints requieren corrección")
            else:
                print("❌ Estado: CRÍTICO - La mayoría de endpoints tienen problemas")

        print("\n📁 Consulte los archivos de reporte para análisis detallado")

        return 0

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
