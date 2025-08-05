# src/api_client.py
# Cliente HTTP robusto para comunicación con microservicios en producción

import requests
import time
import logging
import json
from typing import Dict, Any, Optional
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from datetime import datetime

# Configurar logging
logger = logging.getLogger(__name__)


class ProductionAPIClient:
    """
    Cliente API robusto para comunicación con microservicios desplegados en Google Cloud Run.
    Incluye reintentos automáticos, timeouts configurables y manejo de errores empresarial.
    """

    def __init__(
        self,
        expert_bot_url: str,
        energy_ia_url: str,
        auth_token: str,
        timeout: int = 30,
    ):
        """
        Inicializa el cliente API con configuración para producción.

        Args:
            expert_bot_url: URL del Expert Bot API en Google Cloud Run
            energy_ia_url: URL del Energy IA API en Google Cloud Run
            auth_token: Token Firebase válido para autenticación
            timeout: Timeout en segundos para las peticiones
        """
        self.expert_bot_url = expert_bot_url.rstrip("/")
        self.energy_ia_url = energy_ia_url.rstrip("/")
        self.timeout = timeout

        # Headers de autenticación
        self.headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json",
            "User-Agent": "SmarWatt-Training-Simulator/1.0",
            "Accept": "application/json",
        }

        # Configurar sesión HTTP con reintentos
        self.session = requests.Session()

        # Estrategia de reintentos con backoff exponencial
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT"],
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        logger.info(
            f"Cliente API inicializado para URLs: {expert_bot_url}, {energy_ia_url}"
        )

    def _make_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """
        Realiza una petición HTTP con manejo robusto de errores.

        Args:
            method: Método HTTP (GET, POST, etc.)
            url: URL completa del endpoint
            **kwargs: Argumentos adicionales para requests

        Returns:
            Response object

        Raises:
            requests.RequestException: En caso de error en la petición
        """
        try:
            kwargs.setdefault("headers", {}).update(self.headers)
            kwargs.setdefault("timeout", self.timeout)

            start_time = time.time()
            response = self.session.request(method, url, **kwargs)
            response_time = (time.time() - start_time) * 1000

            logger.info(
                f"{method} {url} - {response.status_code} ({response_time:.0f}ms)"
            )

            response.raise_for_status()
            return response

        except requests.exceptions.Timeout:
            logger.error(f"Timeout en petición {method} {url}")
            raise
        except requests.exceptions.ConnectionError:
            logger.error(f"Error de conexión {method} {url}")
            raise
        except requests.exceptions.HTTPError as e:
            logger.error(f"Error HTTP {method} {url}: {e}")
            raise
        except Exception as e:
            logger.error(f"Error inesperado {method} {url}: {e}")
            raise

    def post_manual_data(
        self, user_id: str, profile_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Simula la subida de datos manuales al Expert Bot API.
        Endpoint: POST /api/v1/energy/manual-data

        Args:
            user_id: ID del usuario sintético
            profile_data: Datos del perfil generados por es_data_generators

        Returns:
            Respuesta del API
        """
        endpoint = f"{self.expert_bot_url}/api/v1/energy/manual-data"

        # Preparar payload según lo que espera el endpoint real
        payload = {
            "kwh_consumidos": profile_data["kwh_consumidos"],
            "potencia_contratada_kw": profile_data["potencia_contratada_kw"],
            "coste_total": profile_data.get("coste_total"),
            "tariff_name_from_invoice": profile_data.get("tariff_name_from_invoice"),
            "comercializadora": profile_data.get("comercializadora"),
            "home_type": profile_data.get("home_type"),
            "num_inhabitants": profile_data.get("num_inhabitants"),
            "post_code_prefix": profile_data.get("post_code_prefix"),
            "fecha_emision": profile_data.get("fecha_emision"),
            "simulation_user_id": user_id,  # Identificar que es usuario simulado
        }

        try:
            response = self._make_request("POST", endpoint, json=payload)
            result = response.json()

            logger.info(f"✅ Datos manuales enviados para usuario {user_id}")
            return result

        except Exception as e:
            logger.error(f"❌ Error enviando datos manuales para {user_id}: {e}")
            return {"error": str(e), "status": "failed"}

    def post_chat_message(
        self, user_id: str, user_context: Dict[str, Any], message_text: str
    ) -> Dict[str, Any]:
        """
        Simula una interacción de chat usando el endpoint v2 optimizado.
        Endpoint: POST /api/v1/chatbot/message/v2

        Args:
            user_id: ID del usuario sintético
            user_context: Contexto del usuario con su perfil
            message_text: Mensaje a enviar

        Returns:
            Respuesta del chatbot
        """
        endpoint = f"{self.energy_ia_url}/api/v1/chatbot/message/v2"

        # Preparar payload según lo que espera el endpoint v2
        payload = {
            "message": message_text,
            "user_context": user_context,
            "history": [],  # Historial vacío para nuevas conversaciones
            "simulation_metadata": {
                "is_simulation": True,
                "simulation_user_id": user_id,
                "timestamp": datetime.now().isoformat(),
            },
        }

        try:
            response = self._make_request("POST", endpoint, json=payload)
            result = response.json()

            logger.info(
                f"💬 Mensaje enviado para usuario {user_id}: {message_text[:50]}..."
            )
            return result

        except Exception as e:
            logger.error(f"❌ Error enviando mensaje para {user_id}: {e}")
            return {"error": str(e), "status": "failed"}

    def get_tariff_recommendations(self, user_id: str) -> Dict[str, Any]:
        """
        Simula una petición de recomendación de tarifas.
        Endpoint: GET /api/v1/energy/tariffs/recommendations

        Args:
            user_id: ID del usuario sintético

        Returns:
            Recomendaciones de tarifas
        """
        endpoint = f"{self.energy_ia_url}/api/v1/energy/tariffs/recommendations"

        # Añadir parámetros de simulación
        params = {"simulation_user": user_id, "source": "training_simulator"}

        try:
            response = self._make_request("GET", endpoint, params=params)
            result = response.json()

            logger.info(f"💰 Recomendaciones obtenidas para usuario {user_id}")
            return result

        except Exception as e:
            logger.error(f"❌ Error obteniendo recomendaciones para {user_id}: {e}")
            return {"error": str(e), "status": "failed"}

    def post_consumption_data(
        self, user_id: str, profile_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Simula la subida de datos de consumo (como si fuera OCR de factura).
        Endpoint: POST /api/v1/energy/consumption

        Args:
            user_id: ID del usuario sintético
            profile_data: Datos del perfil para simular factura

        Returns:
            Respuesta del procesamiento de consumo
        """
        endpoint = f"{self.expert_bot_url}/api/v1/energy/consumption"

        # Simular datos de factura procesados por OCR
        payload = {
            "consumption_data": {
                "kwh_consumidos": profile_data["kwh_consumidos"],
                "potencia_contratada_kw": profile_data["potencia_contratada_kw"],
                "coste_total": profile_data.get("coste_total"),
                "periodo_facturacion": "mensual",
                "fecha_emision": profile_data.get("fecha_emision"),
                "comercializadora": profile_data.get("comercializadora"),
            },
            "source": "simulation_ocr",
            "simulation_user_id": user_id,
        }

        try:
            response = self._make_request("POST", endpoint, json=payload)
            result = response.json()

            logger.info(f"📄 Datos de consumo procesados para usuario {user_id}")
            return result

        except Exception as e:
            logger.error(f"❌ Error procesando consumo para {user_id}: {e}")
            return {"error": str(e), "status": "failed"}

    def health_check(self) -> Dict[str, bool]:
        """
        Verifica el estado de salud de ambos microservicios.

        Returns:
            Estado de ambos servicios
        """
        health_status = {}

        # Verificar Expert Bot API
        try:
            response = self._make_request("GET", f"{self.expert_bot_url}/health")
            health_status["expert_bot_api"] = response.status_code == 200
        except Exception:
            health_status["expert_bot_api"] = False

        # Verificar Energy IA API
        try:
            response = self._make_request("GET", f"{self.energy_ia_url}/health")
            health_status["energy_ia_api"] = response.status_code == 200
        except Exception:
            health_status["energy_ia_api"] = False

        logger.info(f"Health check: {health_status}")
        return health_status

    def close(self):
        """Cierra la sesión HTTP."""
        self.session.close()
        logger.info("Cliente API cerrado correctamente")


# Función de conveniencia para crear cliente
def create_api_client(
    expert_bot_url: str, energy_ia_url: str, auth_token: str
) -> ProductionAPIClient:
    """
    Crea una instancia del cliente API con la configuración proporcionada.

    Args:
        expert_bot_url: URL del Expert Bot API
        energy_ia_url: URL del Energy IA API
        auth_token: Token de autenticación

    Returns:
        Instancia configurada del cliente API
    """
    return ProductionAPIClient(expert_bot_url, energy_ia_url, auth_token)
