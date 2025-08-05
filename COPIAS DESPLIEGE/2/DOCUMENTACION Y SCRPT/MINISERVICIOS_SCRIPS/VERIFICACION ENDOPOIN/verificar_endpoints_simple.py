#!/usr/bin/env python3
"""
🏢 VERIFICADOR SIMPLE DE ENDPOINTS - SMARWATT MICROSERVICIOS
==========================================================

Script simple para verificar endpoints sin dependencias complejas.
Este script se puede ejecutar directamente y genera reporte inmediato.

FUNCIONES:
✅ Verifica conectividad básica
✅ Lista todos los endpoints
✅ Documenta respuestas reales
✅ Genera reporte instantáneo

AUTOR: Sistema de Verificación Empresarial SmarWatt
FECHA: 2025-07-21
VERSIÓN: 1.0.0 - SIMPLE
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


class SimpleEndpointVerifier:
    """🔍 Verificador simple de endpoints"""

    def __init__(self):
        self.timeout = 15
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "SmarWatt-Simple-Verifier/1.0",
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )

        # Lista completa de endpoints a verificar
        self.endpoints = {
            "expert_bot_api": [
                {"path": "/health", "method": "GET", "desc": "Health check básico"},
                {
                    "path": "/health/detailed",
                    "method": "GET",
                    "desc": "Health check detallado",
                },
                {
                    "path": "/api/v1/chat/session/start",
                    "method": "POST",
                    "desc": "Iniciar sesión de chat",
                    "auth": True,
                },
                {
                    "path": "/api/v1/chat/message",
                    "method": "POST",
                    "desc": "Enviar mensaje al chat",
                    "auth": True,
                },
                {
                    "path": "/api/v1/chat/conversation/history",
                    "method": "GET",
                    "desc": "Historial de conversaciones",
                    "auth": True,
                },
                {
                    "path": "/api/v1/chat/metrics",
                    "method": "GET",
                    "desc": "Métricas de chat",
                    "auth": True,
                },
                {
                    "path": "/api/v1/energy/consumption",
                    "method": "POST",
                    "desc": "Registrar consumo",
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
                    "desc": "Perfil de usuario",
                    "auth": True,
                },
                {
                    "path": "/api/v1/energy/consumption/history",
                    "method": "GET",
                    "desc": "Historial de consumo",
                    "auth": True,
                },
                {
                    "path": "/api/v1/energy/consumption/recommendations",
                    "method": "GET",
                    "desc": "Recomendaciones",
                    "auth": True,
                },
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
            ],
            "energy_ia_api": [
                {"path": "/health", "method": "GET", "desc": "Health check IA"},
                {
                    "path": "/api/v1/info",
                    "method": "GET",
                    "desc": "Información del servicio",
                },
                {
                    "path": "/api/v1/status",
                    "method": "GET",
                    "desc": "Estado del servicio",
                },
                {"path": "/status", "method": "GET", "desc": "Estado general"},
                {
                    "path": "/api/v1/chatbot/message",
                    "method": "POST",
                    "desc": "Mensaje IA",
                    "auth": True,
                },
                {
                    "path": "/api/v1/chatbot/message/v2",
                    "method": "POST",
                    "desc": "Mensaje IA v2",
                    "auth": True,
                },
                {
                    "path": "/api/v1/chatbot/cross-service",
                    "method": "POST",
                    "desc": "Cross-service",
                    "auth": True,
                },
                {
                    "path": "/api/v1/chatbot/conversations",
                    "method": "GET",
                    "desc": "Conversaciones IA",
                    "auth": True,
                },
                {
                    "path": "/api/v1/chatbot/health",
                    "method": "GET",
                    "desc": "Health chatbot IA",
                },
            ],
        }

    def test_endpoint(self, base_url: str, endpoint: Dict[str, Any]) -> Dict[str, Any]:
        """🧪 Probar un endpoint específico"""

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
        }

        try:
            print(f"  🧪 {endpoint['method']} {endpoint['path']}")

            headers = self.session.headers.copy()
            if endpoint.get("auth"):
                headers["Authorization"] = "Bearer test-token"

            # Datos de prueba simples
            test_data = {
                "user_id": "test-user-12345",
                "message": "Test message",
                "test": True,
            }

            start_time = time.time()

            if endpoint["method"] == "GET":
                response = self.session.get(
                    full_url, headers=headers, timeout=self.timeout
                )
            elif endpoint["method"] == "POST":
                response = self.session.post(
                    full_url, headers=headers, json=test_data, timeout=self.timeout
                )
            else:
                response = self.session.request(
                    endpoint["method"], full_url, headers=headers, timeout=self.timeout
                )

            result["response_time"] = time.time() - start_time
            result["http_code"] = response.status_code

            # Evaluar respuesta
            if response.status_code == 200:
                result["status"] = "✅ SUCCESS"
                try:
                    json_response = response.json()
                    result["response_sample"] = (
                        str(json_response)[:200] + "..."
                        if len(str(json_response)) > 200
                        else json_response
                    )
                except:
                    result["response_sample"] = (
                        response.text[:200] + "..."
                        if len(response.text) > 200
                        else response.text
                    )

            elif response.status_code == 404:
                result["status"] = "🔍 NOT_FOUND"
                result["error"] = "Endpoint no encontrado"

            elif response.status_code == 401:
                result["status"] = "🔐 AUTH_REQUIRED"
                result["error"] = "Autenticación requerida"

            elif response.status_code == 403:
                result["status"] = "🚫 FORBIDDEN"
                result["error"] = "Acceso prohibido"

            else:
                result["status"] = "❌ ERROR"
                result["error"] = f"HTTP {response.status_code}: {response.text[:100]}"

        except requests.exceptions.Timeout:
            result["status"] = "⏱️ TIMEOUT"
            result["error"] = f"Timeout después de {self.timeout}s"
            result["response_time"] = self.timeout

        except requests.exceptions.RequestException as e:
            result["status"] = "💥 CONNECTION_ERROR"
            result["error"] = str(e)[:100]
            result["response_time"] = self.timeout

        return result

    def test_service_health(self, service_name: str, base_url: str) -> Dict[str, Any]:
        """🩺 Probar salud de un servicio"""

        print(f"🔍 Verificando {service_name}: {base_url}")

        try:
            start_time = time.time()
            response = self.session.get(f"{base_url}/health", timeout=self.timeout)
            response_time = time.time() - start_time

            if response.status_code == 200:
                status = "✅ HEALTHY"
                error = None
            else:
                status = "⚠️ UNHEALTHY"
                error = f"HTTP {response.status_code}"

        except requests.exceptions.RequestException as e:
            status = "❌ UNREACHABLE"
            error = str(e)[:100]
            response_time = self.timeout

        return {
            "service": service_name,
            "url": base_url,
            "status": status,
            "response_time": response_time,
            "error": error,
        }

    def verify_all_services(self):
        """🚀 Verificar todos los servicios"""

        print("🏢 VERIFICADOR SIMPLE DE ENDPOINTS - SMARWATT")
        print("=" * 60)
        print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        results = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "services": {},
            "summary": {
                "total_endpoints": 0,
                "success_count": 0,
                "error_count": 0,
                "not_found_count": 0,
                "auth_required_count": 0,
            },
        }

        # URLs a probar para cada servicio
        service_urls = {
            "expert_bot_api": [EXPERT_BOT_API_URL, LOCAL_EXPERT_BOT_URL],
            "energy_ia_api": [ENERGY_IA_API_URL, LOCAL_ENERGY_IA_URL],
        }

        for service_name, urls in service_urls.items():
            print(f"\n🔧 {service_name.upper().replace('_', ' ')}")
            print("-" * 40)

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
                    print(
                        f"  {health_result['status']} - Tiempo: {health_result['response_time']:.3f}s"
                    )
                    break
                else:
                    print(f"  {health_result['status']} - {health_result['error']}")

            if service_working and working_url:
                print(f"  🎯 Usando URL: {working_url}")
                print("  📡 Verificando endpoints:")

                service_results = {
                    "url": working_url,
                    "health": health_result,
                    "endpoints": [],
                }

                # Probar todos los endpoints del servicio
                for endpoint in self.endpoints.get(service_name, []):
                    endpoint_result = self.test_endpoint(working_url, endpoint)
                    service_results["endpoints"].append(endpoint_result)

                    # Actualizar contadores
                    results["summary"]["total_endpoints"] += 1

                    if "SUCCESS" in endpoint_result["status"]:
                        results["summary"]["success_count"] += 1
                    elif "NOT_FOUND" in endpoint_result["status"]:
                        results["summary"]["not_found_count"] += 1
                    elif "AUTH_REQUIRED" in endpoint_result["status"]:
                        results["summary"]["auth_required_count"] += 1
                    else:
                        results["summary"]["error_count"] += 1

                    print(
                        f"    {endpoint_result['status']} ({endpoint_result['response_time']:.3f}s)"
                    )

                results["services"][service_name] = service_results

            else:
                print(f"  ❌ No se pudo conectar a {service_name} en ninguna URL")
                results["services"][service_name] = {
                    "url": "N/A",
                    "health": {"status": "❌ UNREACHABLE", "error": "No disponible"},
                    "endpoints": [],
                }

        # Mostrar resumen
        print("\n" + "=" * 60)
        print("📊 RESUMEN EJECUTIVO")
        print("=" * 60)
        print(f"✅ Endpoints exitosos: {results['summary']['success_count']}")
        print(f"❌ Endpoints con error: {results['summary']['error_count']}")
        print(f"🔍 Endpoints no encontrados: {results['summary']['not_found_count']}")
        print(
            f"🔐 Endpoints que requieren auth: {results['summary']['auth_required_count']}"
        )
        print(f"📊 Total endpoints: {results['summary']['total_endpoints']}")

        if results["summary"]["total_endpoints"] > 0:
            success_rate = (
                results["summary"]["success_count"]
                / results["summary"]["total_endpoints"]
            ) * 100
            print(f"🎯 Tasa de éxito: {success_rate:.1f}%")

        # Generar reporte
        self.generate_simple_report(results)

        return results

    def generate_simple_report(self, results: Dict[str, Any]):
        """📋 Generar reporte simple"""

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = f"c:/Smarwatt_2/SmarWatt_2/backend/sevicio chatbot/servicios/Y DOCUMENTACION/MINISERVICIOS_SCRIPS/VERIFICACION ENDOPOIN/REPORTE_SIMPLE_{timestamp}.md"

        report = f"""# 🏢 REPORTE SIMPLE - ENDPOINTS SMARWATT

**Fecha:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Verificador:** Simple Endpoint Verifier v1.0

## 📊 RESUMEN

- **Total Endpoints:** {results['summary']['total_endpoints']}
- **✅ Exitosos:** {results['summary']['success_count']}
- **❌ Con Error:** {results['summary']['error_count']}
- **🔍 No Encontrados:** {results['summary']['not_found_count']}
- **🔐 Requieren Auth:** {results['summary']['auth_required_count']}

"""
        if results["summary"]["total_endpoints"] > 0:
            success_rate = (
                results["summary"]["success_count"]
                / results["summary"]["total_endpoints"]
            ) * 100
            report += f"- **🎯 Tasa de Éxito:** {success_rate:.1f}%\n"

        report += "\n## 🔧 DETALLE POR SERVICIO\n"

        for service_name, service_data in results["services"].items():
            report += f"\n### {service_name.upper().replace('_', ' ')}\n\n"
            report += f"**URL:** {service_data.get('url', 'N/A')}  \n"

            health = service_data.get("health", {})
            report += f"**Estado:** {health.get('status', 'Unknown')}  \n"

            if health.get("error"):
                report += f"**Error:** {health['error']}  \n"

            report += "\n#### Endpoints\n\n"

            for endpoint in service_data.get("endpoints", []):
                report += f"- **{endpoint['method']} {endpoint['path']}**\n"
                report += f"  - Estado: {endpoint['status']}\n"
                report += f"  - Descripción: {endpoint['description']}\n"
                report += f"  - Tiempo: {endpoint['response_time']:.3f}s\n"
                report += f"  - HTTP: {endpoint['http_code']}\n"

                if endpoint.get("error"):
                    report += f"  - Error: {endpoint['error']}\n"

                if endpoint.get("response_sample"):
                    report += (
                        f"  - Muestra: `{str(endpoint['response_sample'])[:100]}...`\n"
                    )

                report += "\n"

        report += """
## 🎯 RECOMENDACIONES

### Endpoints Exitosos
Los endpoints que responden correctamente están funcionando bien y pueden ser utilizados.

### Endpoints No Encontrados (404)
Estos endpoints pueden necesitar:
- Verificar la ruta exacta en el código
- Confirmar que el blueprint está registrado
- Revisar la configuración de URLs

### Endpoints que Requieren Autenticación
Estos endpoints están protegidos correctamente. Para usarlos necesitas:
- Token JWT válido
- Header Authorization: Bearer <token>
- Permisos de usuario adecuados

### Endpoints con Error
Revisar logs del servidor para más detalles sobre estos errores.

---

*Reporte generado automáticamente por Simple Endpoint Verifier*
"""

        try:
            with open(report_path, "w", encoding="utf-8") as f:
                f.write(report)
            print(f"\n📁 Reporte guardado en:")
            print(f"   {report_path}")
        except Exception as e:
            print(f"❌ Error guardando reporte: {e}")

        # También guardar JSON
        json_path = report_path.replace(".md", ".json")
        try:
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"   {json_path}")
        except Exception as e:
            print(f"❌ Error guardando JSON: {e}")


def main():
    """🚀 Función principal"""

    verifier = SimpleEndpointVerifier()

    try:
        results = verifier.verify_all_services()

        print("\n🎉 Verificación completada exitosamente")
        print("📁 Consulte los archivos de reporte para más detalles")

        return 0

    except Exception as e:
        print(f"\n❌ Error durante la verificación: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
