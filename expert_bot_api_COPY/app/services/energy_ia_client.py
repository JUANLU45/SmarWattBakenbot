# expert_bot_api_COPY/app/services/energy_ia_client.py
# 🏢 CLIENTE API ROBUSTO PARA COMUNICACIÓN EMPRESARIAL

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging
import time
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime, timezone
import json
import hashlib
from flask import current_app

from smarwatt_auth.exceptions import AppError


@dataclass
class ApiResponse:
    """🏢 Respuesta de API empresarial"""

    success: bool
    data: Any
    status_code: int
    response_time: float
    request_id: str
    endpoint: str
    retry_count: int = 0
    error_details: Optional[str] = None


class EnergyIAApiClient:
    """
    🏢 CLIENTE API ROBUSTO EMPRESARIAL

    Características:
    - Reintentos automáticos con backoff exponencial
    - Timeouts configurables
    - Logging detallado de requests
    - Métricas de rendimiento
    - Manejo de errores empresarial
    - Cache de respuestas
    """

    def __init__(self, base_url: str, timeout: int = 15):
        """
        Inicializar cliente API robusto

        Args:
            base_url: URL base del servicio Energy IA API
            timeout: Timeout en segundos (default: 15)
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.logger = logging.getLogger("energy_ia_client")

        # Configurar sesión con reintentos
        self.session = requests.Session()

        # Estrategia de reintentos empresarial
        retry_strategy = Retry(
            total=3,  # 3 reintentos máximo
            status_forcelist=[429, 500, 502, 503, 504],  # Códigos que activan retry
            allowed_methods=["HEAD", "GET", "POST", "PUT", "DELETE"],
            backoff_factor=1,  # Backoff exponencial: 1s, 2s, 4s
            raise_on_redirect=False,
            raise_on_status=False,
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        # Configurar headers por defecto
        self.session.headers.update(
            {
                "Content-Type": "application/json",
                "User-Agent": "SmarWatt-ExpertBot/1.0",
                "X-Client-Version": "2025.1.0",
            }
        )

        # Métricas empresariales
        self.metrics = {
            "requests_total": 0,
            "requests_successful": 0,
            "requests_failed": 0,
            "retry_total": 0,
            "avg_response_time": 0.0,
            "last_request_time": None,
        }

        # Cache simple
        self.cache = {}
        self.cache_ttl = 300  # 5 minutos

    def get_user_profile(self, user_token: str) -> Dict[str, Any]:
        """
        Obtener perfil de usuario de Energy IA API

        Args:
            user_token: Token de autenticación del usuario

        Returns:
            Dict con datos del perfil del usuario

        Raises:
            AppError: Si hay error en la comunicación o respuesta
        """
        try:
            headers = {"Authorization": f"Bearer {user_token}"}

            response = self._make_request(
                method="GET",
                endpoint="/api/v1/energy/users/profile",
                headers=headers,
                cache_key=f"user_profile_{hashlib.sha256(user_token.encode()).hexdigest()[:16]}",
            )

            if response.success:
                return response.data
            else:
                raise AppError(
                    f"Error obteniendo perfil de usuario: {response.error_details}",
                    response.status_code,
                )

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error crítico comunicando con Energy IA API: {e}")
            raise AppError(f"El servicio de energía no está disponible: {e}", 503)
        except Exception as e:
            self.logger.error(f"Error inesperado en get_user_profile: {e}")
            raise AppError(f"Error interno obteniendo perfil: {str(e)}", 500)

    def get_tariff_recommendation(
        self, user_profile: Dict[str, Any], user_token: str
    ) -> Dict[str, Any]:
        """
        Obtener recomendación de tarifa

        Args:
            user_profile: Perfil del usuario
            user_token: Token de autenticación

        Returns:
            Dict con recomendación de tarifa
        """
        try:
            headers = {"Authorization": f"Bearer {user_token}"}
            payload = {"user_profile": user_profile}

            response = self._make_request(
                method="POST",
                endpoint="/api/v1/energy/tariff/recommend",
                headers=headers,
                json_data=payload,
                cache_key=f"tariff_rec_{hashlib.sha256(json.dumps(user_profile, sort_keys=True).encode()).hexdigest()[:16]}",
            )

            if response.success:
                return response.data
            else:
                raise AppError(
                    f"Error obteniendo recomendación: {response.error_details}",
                    response.status_code,
                )

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error crítico comunicando con Energy IA API: {e}")
            raise AppError(f"El servicio de energía no está disponible: {e}", 503)
        except Exception as e:
            self.logger.error(f"Error inesperado en get_tariff_recommendation: {e}")
            raise AppError(f"Error interno obteniendo recomendación: {str(e)}", 500)

    def process_chat_message(
        self,
        user_profile: Dict[str, Any],
        message: str,
        conversation_id: str,
        user_token: str,
    ) -> Dict[str, Any]:
        """
        Procesar mensaje de chat

        Args:
            user_profile: Perfil del usuario
            message: Mensaje del usuario
            conversation_id: ID de la conversación
            user_token: Token de autenticación

        Returns:
            Dict con respuesta del chatbot
        """
        try:
            headers = {"Authorization": f"Bearer {user_token}"}
            payload = {
                "user_profile": user_profile,
                "message": message,
                "conversation_id": conversation_id,
            }

            response = self._make_request(
                method="POST",
                endpoint="/api/v1/chat/message",
                headers=headers,
                json_data=payload,
                cache_key=None,  # No cachear mensajes de chat
            )

            if response.success:
                return response.data
            else:
                raise AppError(
                    f"Error procesando mensaje: {response.error_details}",
                    response.status_code,
                )

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error crítico comunicando con Energy IA API: {e}")
            raise AppError(f"El servicio de energía no está disponible: {e}", 503)
        except Exception as e:
            self.logger.error(f"Error inesperado en process_chat_message: {e}")
            raise AppError(f"Error interno procesando mensaje: {str(e)}", 500)

    def _make_request(
        self,
        method: str,
        endpoint: str,
        headers: Optional[Dict] = None,
        json_data: Optional[Dict] = None,
        params: Optional[Dict] = None,
        cache_key: Optional[str] = None,
    ) -> ApiResponse:
        """
        Realizar request HTTP robusto

        Args:
            method: Método HTTP (GET, POST, etc.)
            endpoint: Endpoint de la API
            headers: Headers adicionales
            json_data: Datos JSON para enviar
            params: Parámetros de query
            cache_key: Clave para cache (si se quiere cachear)

        Returns:
            ApiResponse con resultado
        """
        start_time = time.time()
        request_id = self._generate_request_id()
        url = f"{self.base_url}{endpoint}"

        # Verificar cache
        if cache_key and method.upper() == "GET":
            cached_response = self._get_cached_response(cache_key)
            if cached_response:
                self.logger.info(f"Cache hit para {endpoint}")
                return cached_response

        # Actualizar métricas
        self.metrics["requests_total"] += 1
        self.metrics["last_request_time"] = datetime.now(timezone.utc)

        # Preparar headers
        request_headers = self.session.headers.copy()
        if headers:
            request_headers.update(headers)
        request_headers["X-Request-ID"] = request_id

        retry_count = 0

        try:
            self.logger.info(f"[{request_id}] {method} {url}")

            # Realizar request
            response = self.session.request(
                method=method,
                url=url,
                headers=request_headers,
                json=json_data,
                params=params,
                timeout=self.timeout,
            )

            # Calcular tiempo de respuesta
            response_time = time.time() - start_time

            # Obtener información de reintentos
            if hasattr(response, "history"):
                retry_count = len(response.history)
                if retry_count > 0:
                    self.metrics["retry_total"] += retry_count

            # Crear respuesta
            api_response = ApiResponse(
                success=response.ok,
                data=response.json() if response.content else {},
                status_code=response.status_code,
                response_time=response_time,
                request_id=request_id,
                endpoint=endpoint,
                retry_count=retry_count,
                error_details=None if response.ok else response.text,
            )

            # Actualizar métricas
            self._update_metrics(api_response)

            # Logging
            self._log_response(api_response)

            # Cachear respuesta exitosa
            if cache_key and api_response.success and method.upper() == "GET":
                self._cache_response(cache_key, api_response)

            return api_response

        except requests.exceptions.Timeout:
            self.logger.error(f"[{request_id}] Timeout en {endpoint}")
            raise AppError(f"Timeout comunicando con servicio de energía", 504)
        except requests.exceptions.ConnectionError:
            self.logger.error(f"[{request_id}] Error de conexión en {endpoint}")
            raise AppError(f"Error de conexión con servicio de energía", 503)
        except requests.exceptions.RequestException as e:
            self.logger.error(f"[{request_id}] Error de request en {endpoint}: {e}")
            raise AppError(f"Error de comunicación: {str(e)}", 500)

    def _generate_request_id(self) -> str:
        """Generar ID único para request"""
        return f"req_{int(time.time() * 1000)}_{hashlib.sha256(str(time.time()).encode()).hexdigest()[:8]}"

    def _update_metrics(self, response: ApiResponse):
        """Actualizar métricas de rendimiento"""
        if response.success:
            self.metrics["requests_successful"] += 1
        else:
            self.metrics["requests_failed"] += 1

        # Calcular tiempo promedio de respuesta
        total_requests = self.metrics["requests_total"]
        current_avg = self.metrics["avg_response_time"]

        self.metrics["avg_response_time"] = (
            current_avg * (total_requests - 1) + response.response_time
        ) / total_requests

    def _log_response(self, response: ApiResponse):
        """Logging detallado de respuesta"""
        log_data = {
            "request_id": response.request_id,
            "endpoint": response.endpoint,
            "status_code": response.status_code,
            "response_time": f"{response.response_time:.3f}s",
            "retry_count": response.retry_count,
            "success": response.success,
        }

        if response.success:
            self.logger.info(f"API Response: {log_data}")
        else:
            log_data["error"] = response.error_details
            self.logger.error(f"API Error: {log_data}")

    def _get_cached_response(self, cache_key: str) -> Optional[ApiResponse]:
        """Obtener respuesta del cache"""
        if cache_key in self.cache:
            cached_data, cached_at = self.cache[cache_key]

            # Verificar TTL
            if time.time() - cached_at < self.cache_ttl:
                return cached_data

            # Limpiar cache expirado
            del self.cache[cache_key]

        return None

    def _cache_response(self, cache_key: str, response: ApiResponse):
        """Cachear respuesta"""
        # Crear copia para cache
        cached_response = ApiResponse(
            success=response.success,
            data=response.data,
            status_code=response.status_code,
            response_time=response.response_time,
            request_id=response.request_id,
            endpoint=response.endpoint,
            retry_count=response.retry_count,
            error_details=response.error_details,
        )

        self.cache[cache_key] = (cached_response, time.time())

        # Limitar tamaño del cache
        if len(self.cache) > 100:
            # Eliminar la entrada más antigua
            oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k][1])
            del self.cache[oldest_key]

    def get_metrics(self) -> Dict[str, Any]:
        """
        Obtener métricas de rendimiento

        Returns:
            Dict con métricas del cliente
        """
        return {
            **self.metrics,
            "success_rate": (
                self.metrics["requests_successful"]
                / max(1, self.metrics["requests_total"])
            )
            * 100,
            "cache_size": len(self.cache),
            "base_url": self.base_url,
            "timeout": self.timeout,
        }

    def clear_cache(self):
        """Limpiar cache"""
        self.cache.clear()
        self.logger.info("Cache limpiado")

    def health_check(self) -> Dict[str, Any]:
        """
        Verificar salud del servicio

        Returns:
            Dict con estado de salud
        """
        try:
            response = self._make_request(
                method="GET", endpoint="/health", cache_key=None
            )

            return {
                "status": "healthy" if response.success else "unhealthy",
                "response_time": response.response_time,
                "status_code": response.status_code,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
