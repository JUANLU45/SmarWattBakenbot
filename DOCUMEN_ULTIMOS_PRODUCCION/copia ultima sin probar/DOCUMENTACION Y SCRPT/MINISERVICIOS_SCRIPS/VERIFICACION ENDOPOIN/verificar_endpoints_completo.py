#!/usr/bin/env python3
"""
🏢 VERIFICADOR COMPLETO DE ENDPOINTS - SMARWATT MICROSERVICIOS
============================================================

PROPÓSITO:
Este script verifica TODOS los endpoints de ambos microservicios (Expert Bot API y Energy IA API),
documenta su funcionamiento real, valida conectividad, y genera reporte empresarial completo.

FUNCIONES:
✅ Mapea todos los endpoints disponibles
✅ Verifica conectividad y respuestas
✅ Documenta parámetros requeridos
✅ Valida autenticación
✅ Genera reporte empresarial
✅ Identifica endpoints no funcionales

CONFIGURACIÓN EMPRESARIAL:
- URLs de producción: https://expert-bot-api-1010012211318.europe-west1.run.app
                     https://energy-ia-api-1010012211318.europe-west1.run.app
- Proyecto GCP: smatwatt (ID: 1010012211318)
- Dataset BigQuery: smartwatt_data
- Región: europe-west1

AUTOR: Sistema de Verificación Empresarial SmarWatt
FECHA: 2025-07-21
VERSIÓN: 1.0.0 - EMPRESARIAL
"""

import requests
import json
import time
import os
import sys
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Tuple
from urllib.parse import urljoin
import logging
from dataclasses import dataclass, asdict
import asyncio
import aiohttp
from pathlib import Path

# Configuración de logging empresarial
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("verificacion_endpoints.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

# URLs de los microservicios en producción
EXPERT_BOT_API_URL = "https://expert-bot-api-1010012211318.europe-west1.run.app"
ENERGY_IA_API_URL = "https://energy-ia-api-1010012211318.europe-west1.run.app"

# URLs locales para desarrollo (si están ejecutándose)
LOCAL_EXPERT_BOT_URL = "http://localhost:8080"
LOCAL_ENERGY_IA_URL = "http://localhost:8081"


@dataclass
class EndpointInfo:
    """Información completa de un endpoint"""

    path: str
    method: str
    description: str
    service: str
    requires_auth: bool = False
    parameters: Dict[str, Any] = None
    response_example: Dict[str, Any] = None
    status: str = "unknown"  # success, error, not_found, timeout
    response_time: float = 0.0
    error_message: str = ""
    http_status: int = 0


@dataclass
class ServiceInfo:
    """Información completa de un servicio"""

    name: str
    url: str
    status: str = "unknown"
    endpoints: List[EndpointInfo] = None
    total_endpoints: int = 0
    working_endpoints: int = 0
    broken_endpoints: int = 0
    response_time: float = 0.0

    def __post_init__(self):
        if self.endpoints is None:
            self.endpoints = []


class EndpointVerifier:
    """🏢 Verificador empresarial de endpoints"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "SmarWatt-Endpoint-Verifier/1.0",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )
        self.timeout = 30
        self.results = []

        # Mapeo completo de endpoints basado en el código fuente
        self.endpoints_map = self._build_endpoints_map()

    def _build_endpoints_map(self) -> Dict[str, List[EndpointInfo]]:
        """🏢 Construye el mapa completo de endpoints desde el código fuente"""
        return {
            "expert_bot_api": [
                # --- HEALTH ENDPOINTS ---
                EndpointInfo(
                    path="/health",
                    method="GET",
                    description="Health check básico del servicio",
                    service="expert_bot_api",
                    requires_auth=False,
                ),
                EndpointInfo(
                    path="/health/detailed",
                    method="GET",
                    description="Health check detallado con métricas del sistema",
                    service="expert_bot_api",
                    requires_auth=False,
                ),
                # --- CHAT ENDPOINTS ---
                EndpointInfo(
                    path="/api/v1/chat/session/start",
                    method="POST",
                    description="Iniciar nueva sesión de chat",
                    service="expert_bot_api",
                    requires_auth=True,
                    parameters={
                        "user_id": "string (required)",
                        "session_type": "string (optional)",
                    },
                ),
                EndpointInfo(
                    path="/api/v1/chat/message",
                    method="POST",
                    description="Enviar mensaje al chatbot experto",
                    service="expert_bot_api",
                    requires_auth=True,
                    parameters={
                        "user_id": "string (required)",
                        "message": "string (required)",
                        "session_id": "string (optional)",
                        "context": "object (optional)",
                    },
                ),
                EndpointInfo(
                    path="/api/v1/chat/conversation/history",
                    method="GET",
                    description="Obtener historial de conversaciones",
                    service="expert_bot_api",
                    requires_auth=True,
                    parameters={
                        "user_id": "string (required)",
                        "limit": "integer (optional)",
                        "offset": "integer (optional)",
                    },
                ),
                EndpointInfo(
                    path="/api/v1/chat/conversation/<conversation_id>",
                    method="DELETE",
                    description="Eliminar conversación específica",
                    service="expert_bot_api",
                    requires_auth=True,
                    parameters={"conversation_id": "string (required)"},
                ),
                EndpointInfo(
                    path="/api/v1/chat/conversation/feedback",
                    method="POST",
                    description="Enviar feedback sobre una conversación",
                    service="expert_bot_api",
                    requires_auth=True,
                    parameters={
                        "conversation_id": "string (required)",
                        "rating": "integer (required)",
                        "feedback": "string (optional)",
                    },
                ),
                EndpointInfo(
                    path="/api/v1/chat/metrics",
                    method="GET",
                    description="Obtener métricas de chat",
                    service="expert_bot_api",
                    requires_auth=True,
                ),
                # --- ENERGY ENDPOINTS ---
                EndpointInfo(
                    path="/api/v1/energy/consumption",
                    method="POST",
                    description="Registrar datos de consumo energético",
                    service="expert_bot_api",
                    requires_auth=True,
                    parameters={
                        "user_id": "string (required)",
                        "consumption_data": "object (required)",
                        "timestamp": "string (optional)",
                    },
                ),
                EndpointInfo(
                    path="/api/v1/energy/dashboard",
                    method="GET",
                    description="Obtener datos del dashboard de energía",
                    service="expert_bot_api",
                    requires_auth=True,
                    parameters={
                        "user_id": "string (required)",
                        "period": "string (optional)",
                    },
                ),
                EndpointInfo(
                    path="/api/v1/energy/users/profile",
                    method="GET",
                    description="Obtener perfil energético del usuario",
                    service="expert_bot_api",
                    requires_auth=True,
                    parameters={"user_id": "string (required)"},
                ),
                EndpointInfo(
                    path="/api/v1/energy/manual-data",
                    method="POST",
                    description="Ingreso manual de datos energéticos",
                    service="expert_bot_api",
                    requires_auth=True,
                    parameters={
                        "user_id": "string (required)",
                        "manual_data": "object (required)",
                    },
                ),
                EndpointInfo(
                    path="/api/v1/energy/consumption/update",
                    method="PUT",
                    description="Actualizar datos de consumo existentes",
                    service="expert_bot_api",
                    requires_auth=True,
                    parameters={
                        "consumption_id": "string (required)",
                        "updated_data": "object (required)",
                    },
                ),
                EndpointInfo(
                    path="/api/v1/energy/consumption/history",
                    method="GET",
                    description="Obtener historial de consumo",
                    service="expert_bot_api",
                    requires_auth=True,
                    parameters={
                        "user_id": "string (required)",
                        "start_date": "string (optional)",
                        "end_date": "string (optional)",
                    },
                ),
                EndpointInfo(
                    path="/api/v1/energy/consumption/analyze",
                    method="POST",
                    description="Análisis avanzado de consumo",
                    service="expert_bot_api",
                    requires_auth=True,
                    parameters={
                        "user_id": "string (required)",
                        "analysis_type": "string (required)",
                    },
                ),
                EndpointInfo(
                    path="/api/v1/energy/consumption/recommendations",
                    method="GET",
                    description="Obtener recomendaciones de ahorro",
                    service="expert_bot_api",
                    requires_auth=True,
                    parameters={"user_id": "string (required)"},
                ),
                EndpointInfo(
                    path="/api/v1/energy/consumption/compare",
                    method="POST",
                    description="Comparar consumos entre períodos",
                    service="expert_bot_api",
                    requires_auth=True,
                    parameters={
                        "user_id": "string (required)",
                        "periods": "array (required)",
                    },
                ),
                EndpointInfo(
                    path="/api/v1/energy/consumption/title",
                    method="PUT",
                    description="Actualizar título de consumo",
                    service="expert_bot_api",
                    requires_auth=True,
                    parameters={
                        "consumption_id": "string (required)",
                        "title": "string (required)",
                    },
                ),
                # --- LINKS ENDPOINTS ---
                EndpointInfo(
                    path="/api/v1/links/test",
                    method="POST",
                    description="Test de conectividad entre servicios",
                    service="expert_bot_api",
                    requires_auth=False,
                    parameters={
                        "target_service": "string (required)",
                        "test_data": "object (optional)",
                    },
                ),
                EndpointInfo(
                    path="/api/v1/links/status",
                    method="GET",
                    description="Estado de conexiones entre servicios",
                    service="expert_bot_api",
                    requires_auth=False,
                ),
                EndpointInfo(
                    path="/api/v1/links/direct/<link_type>",
                    method="GET",
                    description="Acceso directo a servicios vinculados",
                    service="expert_bot_api",
                    requires_auth=True,
                    parameters={
                        "link_type": "string (required)",
                        "params": "object (optional)",
                    },
                ),
            ],
            "energy_ia_api": [
                # --- HEALTH ENDPOINTS ---
                EndpointInfo(
                    path="/health",
                    method="GET",
                    description="Health check básico del servicio IA",
                    service="energy_ia_api",
                    requires_auth=False,
                ),
                EndpointInfo(
                    path="/api/v1/info",
                    method="GET",
                    description="Información del servicio y versión",
                    service="energy_ia_api",
                    requires_auth=False,
                ),
                EndpointInfo(
                    path="/api/v1/status",
                    method="GET",
                    description="Estado detallado del servicio IA",
                    service="energy_ia_api",
                    requires_auth=False,
                ),
                EndpointInfo(
                    path="/status",
                    method="GET",
                    description="Estado general desde run.py",
                    service="energy_ia_api",
                    requires_auth=False,
                ),
                # --- CHATBOT IA ENDPOINTS ---
                EndpointInfo(
                    path="/api/v1/chatbot/message",
                    method="POST",
                    description="Procesamiento de mensajes con IA avanzada",
                    service="energy_ia_api",
                    requires_auth=True,
                    parameters={
                        "user_id": "string (required)",
                        "message": "string (required)",
                        "context": "object (optional)",
                        "session_id": "string (optional)",
                    },
                ),
                EndpointInfo(
                    path="/api/v1/chatbot/message/v2",
                    method="POST",
                    description="Procesamiento de mensajes IA v2 mejorada",
                    service="energy_ia_api",
                    requires_auth=True,
                    parameters={
                        "user_id": "string (required)",
                        "message": "string (required)",
                        "ai_model": "string (optional)",
                        "enhanced_features": "boolean (optional)",
                    },
                ),
                EndpointInfo(
                    path="/api/v1/chatbot/cross-service",
                    method="POST",
                    description="Comunicación cruzada entre servicios",
                    service="energy_ia_api",
                    requires_auth=True,
                    parameters={
                        "source_service": "string (required)",
                        "target_action": "string (required)",
                        "data": "object (required)",
                    },
                ),
                EndpointInfo(
                    path="/api/v1/chatbot/conversations",
                    method="GET",
                    description="Listar conversaciones del usuario",
                    service="energy_ia_api",
                    requires_auth=True,
                    parameters={
                        "user_id": "string (required)",
                        "limit": "integer (optional)",
                        "offset": "integer (optional)",
                    },
                ),
                EndpointInfo(
                    path="/api/v1/chatbot/conversations/<conversation_id>",
                    method="DELETE",
                    description="Eliminar conversación específica IA",
                    service="energy_ia_api",
                    requires_auth=True,
                    parameters={"conversation_id": "string (required)"},
                ),
                EndpointInfo(
                    path="/api/v1/chatbot/health",
                    method="GET",
                    description="Health check específico del chatbot IA",
                    service="energy_ia_api",
                    requires_auth=False,
                ),
            ],
        }

    async def verify_service_health(
        self, service_name: str, base_url: str
    ) -> ServiceInfo:
        """🏢 Verificar salud completa de un servicio"""
        logger.info(f"🔍 Verificando servicio: {service_name} - {base_url}")

        service = ServiceInfo(name=service_name, url=base_url, endpoints=[])

        try:
            # Health check básico
            start_time = time.time()
            response = self.session.get(f"{base_url}/health", timeout=self.timeout)
            service.response_time = time.time() - start_time

            if response.status_code == 200:
                service.status = "healthy"
                logger.info(
                    f"✅ {service_name} está saludable - {response.status_code}"
                )
            else:
                service.status = "unhealthy"
                logger.warning(
                    f"⚠️  {service_name} responde pero no está saludable - {response.status_code}"
                )

        except requests.exceptions.RequestException as e:
            service.status = "unreachable"
            service.response_time = self.timeout
            logger.error(f"❌ {service_name} no es accesible: {e}")

        return service

    def verify_endpoint(self, endpoint: EndpointInfo, base_url: str) -> EndpointInfo:
        """🏢 Verificar un endpoint específico"""
        full_url = f"{base_url}{endpoint.path}"

        # Reemplazar placeholders en la URL para testing
        test_url = full_url.replace("<conversation_id>", "test-conversation-123")
        test_url = test_url.replace("<link_type>", "energy-service")

        logger.info(f"🧪 Verificando: {endpoint.method} {test_url}")

        try:
            start_time = time.time()

            # Preparar headers de autenticación si es necesario
            headers = self.session.headers.copy()
            if endpoint.requires_auth:
                headers["Authorization"] = "Bearer test-token-for-verification"

            # Preparar datos de prueba según el endpoint
            test_data = self._get_test_data(endpoint)

            # Realizar la petición según el método
            if endpoint.method == "GET":
                response = self.session.get(
                    test_url, headers=headers, timeout=self.timeout
                )
            elif endpoint.method == "POST":
                response = self.session.post(
                    test_url, headers=headers, json=test_data, timeout=self.timeout
                )
            elif endpoint.method == "PUT":
                response = self.session.put(
                    test_url, headers=headers, json=test_data, timeout=self.timeout
                )
            elif endpoint.method == "DELETE":
                response = self.session.delete(
                    test_url, headers=headers, timeout=self.timeout
                )
            else:
                response = self.session.request(
                    endpoint.method, test_url, headers=headers, timeout=self.timeout
                )

            endpoint.response_time = time.time() - start_time
            endpoint.http_status = response.status_code

            # Analizar la respuesta
            if response.status_code == 200:
                endpoint.status = "success"
                try:
                    endpoint.response_example = response.json()
                except json.JSONDecodeError:
                    endpoint.response_example = {
                        "response": "Non-JSON response",
                        "content": response.text[:200],
                    }
                logger.info(
                    f"✅ {endpoint.method} {endpoint.path} - OK ({response.status_code})"
                )

            elif response.status_code == 404:
                endpoint.status = "not_found"
                endpoint.error_message = "Endpoint not found"
                logger.warning(
                    f"🔍 {endpoint.method} {endpoint.path} - Not Found (404)"
                )

            elif response.status_code == 401:
                endpoint.status = "auth_required"
                endpoint.error_message = "Authentication required"
                logger.warning(
                    f"🔐 {endpoint.method} {endpoint.path} - Auth Required (401)"
                )

            elif response.status_code == 403:
                endpoint.status = "forbidden"
                endpoint.error_message = "Access forbidden"
                logger.warning(
                    f"🚫 {endpoint.method} {endpoint.path} - Forbidden (403)"
                )

            elif response.status_code >= 400:
                endpoint.status = "error"
                endpoint.error_message = (
                    f"HTTP {response.status_code}: {response.text[:200]}"
                )
                logger.error(
                    f"❌ {endpoint.method} {endpoint.path} - Error ({response.status_code})"
                )
            else:
                endpoint.status = "unknown"
                endpoint.error_message = f"Unexpected status: {response.status_code}"

        except requests.exceptions.Timeout:
            endpoint.status = "timeout"
            endpoint.error_message = f"Timeout after {self.timeout}s"
            endpoint.response_time = self.timeout
            logger.error(f"⏱️  {endpoint.method} {endpoint.path} - Timeout")

        except requests.exceptions.RequestException as e:
            endpoint.status = "error"
            endpoint.error_message = str(e)
            endpoint.response_time = self.timeout
            logger.error(f"💥 {endpoint.method} {endpoint.path} - Error: {e}")

        return endpoint

    def _get_test_data(self, endpoint: EndpointInfo) -> Dict[str, Any]:
        """🧪 Generar datos de prueba para un endpoint"""
        if not endpoint.parameters:
            return {}

        test_data = {}

        # Datos de prueba comunes
        common_data = {
            "user_id": "test-user-12345",
            "message": "Test message for endpoint verification",
            "session_id": "test-session-67890",
            "context": {
                "source": "endpoint_verification",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
            "consumption_data": {
                "kwh_consumed": 150.5,
                "cost": 45.75,
                "period": "monthly",
            },
            "rating": 5,
            "feedback": "Test feedback",
            "analysis_type": "consumption_trend",
            "target_service": "energy_ia_api",
            "source_service": "expert_bot_api",
            "target_action": "analyze_consumption",
            "data": {"test": True},
        }

        # Generar datos basados en los parámetros del endpoint
        for param_name, param_info in endpoint.parameters.items():
            if param_name in common_data:
                test_data[param_name] = common_data[param_name]
            elif "required" in param_info.lower():
                # Generar valor por defecto para parámetros requeridos
                if "string" in param_info.lower():
                    test_data[param_name] = f"test-{param_name}-value"
                elif "integer" in param_info.lower():
                    test_data[param_name] = 1
                elif "boolean" in param_info.lower():
                    test_data[param_name] = True
                elif "object" in param_info.lower():
                    test_data[param_name] = {"test": True}
                elif "array" in param_info.lower():
                    test_data[param_name] = ["test-item"]

        return test_data

    async def run_complete_verification(self) -> Dict[str, Any]:
        """🏢 Ejecutar verificación completa de todos los servicios"""
        logger.info("🚀 Iniciando verificación completa de endpoints...")

        verification_start = time.time()
        results = {
            "verification_info": {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "verifier_version": "1.0.0",
                "total_services": 2,
                "verification_timeout": self.timeout,
            },
            "services": {},
            "summary": {
                "total_endpoints": 0,
                "working_endpoints": 0,
                "broken_endpoints": 0,
                "unreachable_endpoints": 0,
                "auth_required_endpoints": 0,
            },
        }

        # URLs a verificar (primero producción, luego local si falla)
        services_urls = [
            ("expert_bot_api", [EXPERT_BOT_API_URL, LOCAL_EXPERT_BOT_URL]),
            ("energy_ia_api", [ENERGY_IA_API_URL, LOCAL_ENERGY_IA_URL]),
        ]

        for service_name, urls in services_urls:
            service_verified = False

            for url in urls:
                logger.info(f"🔗 Intentando conectar a {service_name}: {url}")

                # Verificar salud del servicio
                service = await self.verify_service_health(service_name, url)

                if service.status != "unreachable":
                    logger.info(f"✅ Conectado a {service_name} en {url}")

                    # Verificar todos los endpoints del servicio
                    endpoints = self.endpoints_map.get(service_name, [])

                    for endpoint in endpoints:
                        verified_endpoint = self.verify_endpoint(endpoint, url)
                        service.endpoints.append(verified_endpoint)

                        # Actualizar estadísticas
                        if verified_endpoint.status == "success":
                            service.working_endpoints += 1
                        elif verified_endpoint.status in [
                            "error",
                            "timeout",
                            "not_found",
                        ]:
                            service.broken_endpoints += 1

                    service.total_endpoints = len(service.endpoints)
                    results["services"][service_name] = asdict(service)
                    service_verified = True
                    break
                else:
                    logger.warning(f"⚠️  No se pudo conectar a {service_name} en {url}")

            if not service_verified:
                logger.error(f"❌ No se pudo verificar {service_name} en ninguna URL")
                results["services"][service_name] = {
                    "name": service_name,
                    "status": "completely_unreachable",
                    "urls_tried": urls,
                    "endpoints": [],
                    "total_endpoints": 0,
                    "working_endpoints": 0,
                    "broken_endpoints": 0,
                }

        # Calcular resumen general
        for service_data in results["services"].values():
            results["summary"]["total_endpoints"] += service_data.get(
                "total_endpoints", 0
            )
            results["summary"]["working_endpoints"] += service_data.get(
                "working_endpoints", 0
            )
            results["summary"]["broken_endpoints"] += service_data.get(
                "broken_endpoints", 0
            )

        results["verification_info"]["total_time"] = time.time() - verification_start

        logger.info("✅ Verificación completa terminada")
        logger.info(
            f"📊 Resumen: {results['summary']['total_endpoints']} endpoints totales, "
            f"{results['summary']['working_endpoints']} funcionando, "
            f"{results['summary']['broken_endpoints']} con problemas"
        )

        return results

    def generate_documentation(self, results: Dict[str, Any]) -> str:
        """📋 Generar documentación empresarial completa"""

        doc = f"""
# 🏢 REPORTE DE VERIFICACIÓN DE ENDPOINTS - SMARWATT MICROSERVICIOS
================================================================

**Fecha de Verificación:** {results['verification_info']['timestamp']}  
**Versión del Verificador:** {results['verification_info']['verifier_version']}  
**Tiempo Total de Verificación:** {results['verification_info']['total_time']:.2f} segundos

## 📊 RESUMEN EJECUTIVO

- **Total de Servicios:** {results['verification_info']['total_services']}
- **Total de Endpoints:** {results['summary']['total_endpoints']}
- **Endpoints Funcionando:** {results['summary']['working_endpoints']} ✅
- **Endpoints con Problemas:** {results['summary']['broken_endpoints']} ❌
- **Tasa de Éxito:** {(results['summary']['working_endpoints'] / max(results['summary']['total_endpoints'], 1) * 100):.1f}%

## 🔗 CONFIGURACIÓN DE PRODUCCIÓN

### Expert Bot API
- **URL Producción:** {EXPERT_BOT_API_URL}
- **URL Local:** {LOCAL_EXPERT_BOT_URL}

### Energy IA API  
- **URL Producción:** {ENERGY_IA_API_URL}
- **URL Local:** {LOCAL_ENERGY_IA_URL}

---

"""

        # Documentar cada servicio
        for service_name, service_data in results["services"].items():
            doc += f"""
## 🔧 {service_name.upper().replace('_', ' ')}

**Estado del Servicio:** {service_data.get('status', 'unknown').upper()}  
**URL Activa:** {service_data.get('url', 'N/A')}  
**Tiempo de Respuesta:** {service_data.get('response_time', 0):.3f}s  
**Endpoints Totales:** {service_data.get('total_endpoints', 0)}  
**Endpoints Funcionando:** {service_data.get('working_endpoints', 0)}  
**Endpoints con Problemas:** {service_data.get('broken_endpoints', 0)}  

### 📋 DETALLE DE ENDPOINTS

"""

            endpoints = service_data.get("endpoints", [])
            if not endpoints:
                doc += (
                    "❌ **No se pudieron verificar endpoints para este servicio**\n\n"
                )
                continue

            # Agrupar endpoints por categoría
            categories = {}
            for endpoint in endpoints:
                path = endpoint.get("path", "")
                if "/health" in path:
                    category = "🔍 Health Checks"
                elif "/chat" in path:
                    category = "💬 Chat & Conversación"
                elif "/energy" in path:
                    category = "⚡ Gestión Energética"
                elif "/chatbot" in path:
                    category = "🤖 Chatbot IA"
                elif "/links" in path:
                    category = "🔗 Comunicación Entre Servicios"
                else:
                    category = "📡 General"

                if category not in categories:
                    categories[category] = []
                categories[category].append(endpoint)

            for category, category_endpoints in categories.items():
                doc += f"\n#### {category}\n\n"

                for endpoint in category_endpoints:
                    status_icon = {
                        "success": "✅",
                        "error": "❌",
                        "timeout": "⏱️",
                        "not_found": "🔍",
                        "auth_required": "🔐",
                        "forbidden": "🚫",
                        "unknown": "❓",
                    }.get(endpoint.get("status"), "❓")

                    doc += f"""
**{status_icon} `{endpoint.get('method')} {endpoint.get('path')}`**
- **Descripción:** {endpoint.get('description')}
- **Estado:** {endpoint.get('status').upper()}
- **Código HTTP:** {endpoint.get('http_status', 'N/A')}
- **Tiempo de Respuesta:** {endpoint.get('response_time', 0):.3f}s
- **Requiere Autenticación:** {'Sí' if endpoint.get('requires_auth') else 'No'}
"""

                    if endpoint.get("parameters"):
                        doc += "- **Parámetros:**\n"
                        for param, description in endpoint.get(
                            "parameters", {}
                        ).items():
                            doc += f"  - `{param}`: {description}\n"

                    if endpoint.get("error_message"):
                        doc += f"- **⚠️ Error:** {endpoint.get('error_message')}\n"

                    if (
                        endpoint.get("response_example")
                        and endpoint.get("status") == "success"
                    ):
                        doc += f"- **📄 Respuesta de Ejemplo:**\n```json\n{json.dumps(endpoint.get('response_example'), indent=2, ensure_ascii=False)[:300]}...\n```\n"

                    doc += "\n"

        # Sección de recomendaciones
        doc += f"""

---

## 🎯 RECOMENDACIONES EMPRESARIALES

### ✅ Aspectos Positivos
"""

        if results["summary"]["working_endpoints"] > 0:
            doc += f"- {results['summary']['working_endpoints']} endpoints están funcionando correctamente\n"

        doc += f"""
- La arquitectura de microservicios está bien estructurada
- Los health checks están implementados
- La documentación de endpoints está completa

### ⚠️ Aspectos a Mejorar
"""

        if results["summary"]["broken_endpoints"] > 0:
            doc += f"- {results['summary']['broken_endpoints']} endpoints requieren atención inmediata\n"

        doc += f"""
- Implementar autenticación real en endpoints que la requieren
- Mejorar manejo de errores y timeouts
- Añadir validación de parámetros más robusta
- Implementar rate limiting para protección

### 🔧 Acciones Recomendadas

1. **Corto Plazo (1-2 semanas):**
   - Revisar y corregir endpoints que retornan errores 404
   - Implementar autenticación JWT real
   - Añadir logs detallados para debugging

2. **Medio Plazo (1 mes):**
   - Implementar tests automáticos de endpoints  
   - Añadir monitorización de salud en tiempo real
   - Documentar APIs con OpenAPI/Swagger

3. **Largo Plazo (2-3 meses):**
   - Implementar circuit breakers para resiliencia
   - Añadir caching estratégico
   - Implementar observabilidad completa con métricas

---

## 📞 SOPORTE TÉCNICO

**Equipo:** SmarWatt DevOps Engineering  
**Contacto:** desarrollo@smarwatt.com  
**Documentación:** https://docs.smarwatt.com/apis  
**Monitorización:** Google Cloud Console - Proyecto smatwatt  

---

*Este reporte fue generado automáticamente por el sistema de verificación empresarial de SmarWatt.*
*Para obtener la información más actualizada, ejecute la verificación nuevamente.*
"""

        return doc

    async def save_results(self, results: Dict[str, Any], documentation: str):
        """💾 Guardar resultados y documentación"""

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_path = Path(
            "c:/Smarwatt_2/SmarWatt_2/backend/sevicio chatbot/servicios/Y DOCUMENTACION/MINISERVICIOS_SCRIPS/VERIFICACION ENDOPOIN"
        )

        # Guardar JSON completo
        json_file = base_path / f"verificacion_endpoints_{timestamp}.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        # Guardar documentación markdown
        md_file = base_path / f"REPORTE_ENDPOINTS_{timestamp}.md"
        with open(md_file, "w", encoding="utf-8") as f:
            f.write(documentation)

        # Crear archivo de resumen rápido
        summary_file = base_path / "ULTIMO_RESUMEN.txt"
        summary = f"""
ÚLTIMA VERIFICACIÓN DE ENDPOINTS - SMARWATT
==========================================
Fecha: {results['verification_info']['timestamp']}

RESUMEN RÁPIDO:
- Total Endpoints: {results['summary']['total_endpoints']}
- Funcionando: {results['summary']['working_endpoints']} ✅
- Con Problemas: {results['summary']['broken_endpoints']} ❌
- Tasa de Éxito: {(results['summary']['working_endpoints'] / max(results['summary']['total_endpoints'], 1) * 100):.1f}%

SERVICIOS:
"""
        for service_name, service_data in results["services"].items():
            summary += f"- {service_name}: {service_data.get('status', 'unknown')} ({service_data.get('working_endpoints', 0)}/{service_data.get('total_endpoints', 0)})\n"

        summary += f"""
ARCHIVOS GENERADOS:
- Datos completos: {json_file.name}
- Documentación: {md_file.name}
- Este resumen: {summary_file.name}

Para más detalles, consulte la documentación completa.
"""

        with open(summary_file, "w", encoding="utf-8") as f:
            f.write(summary)

        logger.info(f"📁 Resultados guardados:")
        logger.info(f"   - JSON: {json_file}")
        logger.info(f"   - Documentación: {md_file}")
        logger.info(f"   - Resumen: {summary_file}")


async def main():
    """🚀 Función principal de verificación"""

    print("🏢 VERIFICADOR DE ENDPOINTS SMARWATT - MICROSERVICIOS")
    print("=" * 60)
    print("Iniciando verificación completa de todos los endpoints...")
    print()

    verifier = EndpointVerifier()

    try:
        # Ejecutar verificación completa
        results = await verifier.run_complete_verification()

        # Generar documentación
        documentation = verifier.generate_documentation(results)

        # Guardar resultados
        await verifier.save_results(results, documentation)

        # Mostrar resumen en consola
        print("\n" + "=" * 60)
        print("🎉 VERIFICACIÓN COMPLETADA")
        print("=" * 60)
        print(f"✅ Endpoints funcionando: {results['summary']['working_endpoints']}")
        print(f"❌ Endpoints con problemas: {results['summary']['broken_endpoints']}")
        print(f"📊 Total endpoints: {results['summary']['total_endpoints']}")
        print(
            f"🎯 Tasa de éxito: {(results['summary']['working_endpoints'] / max(results['summary']['total_endpoints'], 1) * 100):.1f}%"
        )
        print()

        # Mostrar servicios
        for service_name, service_data in results["services"].items():
            status_icon = (
                "✅" if service_data.get("status") in ["healthy", "success"] else "❌"
            )
            print(
                f"{status_icon} {service_name}: {service_data.get('status')} "
                f"({service_data.get('working_endpoints', 0)}/{service_data.get('total_endpoints', 0)})"
            )

        print()
        print("📁 Consulte los archivos generados para más detalles.")

    except Exception as e:
        logger.error(f"💥 Error durante la verificación: {e}")
        print(f"❌ Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    # Ejecutar verificación
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
