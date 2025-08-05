# src/interaction_simulator.py
# Motor de simulación de usuarios para entrenar los modelos de IA

import sys
import os
import time
import random
import logging
from typing import Dict, Any, List
from datetime import datetime

# Añadir el directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.api_client import ProductionAPIClient
from src.profile_generator import ProfileGenerator
from data.es_data_generators import generate_random_message
from config.simulation_config import (
    API_CALLS_PER_USER,
    INVOICE_UPLOAD_RATE,
    RECOMMENDATION_REQUEST_RATE,
)

logger = logging.getLogger(__name__)


class InteractionSimulator:
    """
    Motor de simulación de usuarios que replica comportamientos reales.
    Diseñado para entrenar los modelos de IA de forma realista y coste-eficiente.
    """

    def __init__(self, api_client: ProductionAPIClient):
        """
        Inicializa el simulador de interacciones.

        Args:
            api_client: Cliente configurado para comunicación con APIs
        """
        self.api_client = api_client
        self.profile_generator = ProfileGenerator()
        self.simulation_stats = {
            "users_created": 0,
            "messages_sent": 0,
            "recommendations_requested": 0,
            "invoices_uploaded": 0,
            "errors": 0,
            "start_time": datetime.now(),
        }

        logger.info("InteractionSimulator inicializado")

    def simulate_user_session(self, user_id: str) -> Dict[str, Any]:
        """
        Simula un ciclo de vida completo de un usuario ficticio.

        Args:
            user_id: ID del usuario sintético

        Returns:
            Resumen de la sesión simulada
        """
        session_results = {
            "user_id": user_id,
            "start_time": datetime.now(),
            "steps_completed": [],
            "errors": [],
            "success": True,
        }

        try:
            logger.info("Iniciando sesión de usuario %s", user_id)

            # 1. Crear perfil de usuario ficticio
            profile = self._create_user_profile(user_id, session_results)
            if not profile:
                session_results["success"] = False
                return session_results

            # 2. Simular entrada de datos manuales
            self._simulate_manual_data_entry(user_id, profile, session_results)

            # 3. Simular conversaciones de chat (entrenar IA conversacional)
            self._simulate_chat_interactions(user_id, profile, session_results)

            # 4. Simular subida de factura (si aplica)
            if random.random() < INVOICE_UPLOAD_RATE:
                self._simulate_invoice_upload(user_id, profile, session_results)

            # 5. Simular petición de recomendaciones (si aplica)
            if random.random() < RECOMMENDATION_REQUEST_RATE:
                self._simulate_recommendation_request(user_id, session_results)

            # Pausa realista entre acciones
            time.sleep(random.uniform(2, 5))

            session_results["end_time"] = datetime.now()
            session_results["duration_seconds"] = (
                session_results["end_time"] - session_results["start_time"]
            ).total_seconds()

            logger.info("✅ Sesión completada para usuario %s", user_id)

        except Exception as e:
            logger.error("❌ Error en sesión de usuario %s: %s", user_id, e)
            session_results["success"] = False
            session_results["errors"].append(f"Error general: {str(e)}")
            self.simulation_stats["errors"] += 1

        return session_results

    def _create_user_profile(
        self, user_id: str, session_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Crea y valida el perfil del usuario."""
        try:
            profile = self.profile_generator.generate_single_profile()
            profile["user_id"] = user_id  # Sobrescribir con el ID proporcionado

            session_results["steps_completed"].append("profile_created")
            logger.debug("Perfil creado para usuario %s", user_id)

            return profile

        except Exception as e:
            error_msg = f"Error creando perfil: {str(e)}"
            session_results["errors"].append(error_msg)
            logger.error("❌ %s", error_msg)
            return None

    def _simulate_manual_data_entry(
        self, user_id: str, profile: Dict[str, Any], session_results: Dict[str, Any]
    ):
        """Simula la entrada manual de datos energéticos."""
        try:
            result = self.api_client.post_manual_data(user_id, profile["profile_data"])

            if "error" not in result:
                session_results["steps_completed"].append("manual_data_sent")
                self.simulation_stats["users_created"] += 1
                logger.info("✅ Datos manuales enviados para usuario %s", user_id)
            else:
                session_results["errors"].append(
                    f"Error en datos manuales: {result['error']}"
                )
                self.simulation_stats["errors"] += 1

        except Exception as e:
            error_msg = f"Error enviando datos manuales: {str(e)}"
            session_results["errors"].append(error_msg)
            logger.error("❌ %s", error_msg)
            self.simulation_stats["errors"] += 1

    def _simulate_chat_interactions(
        self, user_id: str, profile: Dict[str, Any], session_results: Dict[str, Any]
    ):
        """Simula múltiples interacciones de chat para entrenar la IA."""
        messages_sent = 0

        for i in range(API_CALLS_PER_USER):
            try:
                # Generar mensaje realista
                message = generate_random_message()
                user_context = profile["user_context"]

                # Enviar mensaje
                result = self.api_client.post_chat_message(
                    user_id, user_context, message
                )

                if "error" not in result:
                    messages_sent += 1
                    self.simulation_stats["messages_sent"] += 1
                    logger.debug(
                        "💬 Mensaje %d/%d enviado para usuario %s",
                        i + 1,
                        API_CALLS_PER_USER,
                        user_id,
                    )
                else:
                    session_results["errors"].append(
                        f"Error en mensaje {i+1}: {result['error']}"
                    )
                    self.simulation_stats["errors"] += 1

                # Pausa realista entre mensajes
                time.sleep(random.uniform(5, 15))

            except Exception as e:
                error_msg = f"Error en mensaje {i+1}: {str(e)}"
                session_results["errors"].append(error_msg)
                logger.error("❌ %s", error_msg)
                self.simulation_stats["errors"] += 1

        session_results["steps_completed"].append(f"chat_messages_sent_{messages_sent}")
        logger.info(
            "💬 Enviados %d/%d mensajes para usuario %s",
            messages_sent,
            API_CALLS_PER_USER,
            user_id,
        )

    def _simulate_invoice_upload(
        self, user_id: str, profile: Dict[str, Any], session_results: Dict[str, Any]
    ):
        """Simula la subida de una factura para entrenamiento del OCR."""
        try:
            result = self.api_client.post_consumption_data(
                user_id, profile["profile_data"]
            )

            if "error" not in result:
                session_results["steps_completed"].append("invoice_uploaded")
                self.simulation_stats["invoices_uploaded"] += 1
                logger.info("📄 Factura simulada subida para usuario %s", user_id)
            else:
                session_results["errors"].append(
                    f"Error subiendo factura: {result['error']}"
                )
                self.simulation_stats["errors"] += 1

        except Exception as e:
            error_msg = f"Error subiendo factura: {str(e)}"
            session_results["errors"].append(error_msg)
            logger.error("❌ %s", error_msg)
            self.simulation_stats["errors"] += 1

    def _simulate_recommendation_request(
        self, user_id: str, session_results: Dict[str, Any]
    ):
        """Simula una petición de recomendaciones de tarifas."""
        try:
            result = self.api_client.get_tariff_recommendations(user_id)

            if "error" not in result:
                session_results["steps_completed"].append("recommendations_requested")
                self.simulation_stats["recommendations_requested"] += 1
                logger.info("💰 Recomendaciones obtenidas para usuario %s", user_id)
            else:
                session_results["errors"].append(
                    f"Error obteniendo recomendaciones: {result['error']}"
                )
                self.simulation_stats["errors"] += 1

        except Exception as e:
            error_msg = f"Error obteniendo recomendaciones: {str(e)}"
            session_results["errors"].append(error_msg)
            logger.error("❌ %s", error_msg)
            self.simulation_stats["errors"] += 1

    def simulate_batch_users(self, user_ids: List[str]) -> List[Dict[str, Any]]:
        """
        Simula un lote de usuarios de forma secuencial.

        Args:
            user_ids: Lista de IDs de usuarios a simular

        Returns:
            Lista de resultados de cada sesión
        """
        logger.info("🚀 Iniciando simulación de lote: %d usuarios", len(user_ids))

        batch_results = []
        successful_sessions = 0

        for i, user_id in enumerate(user_ids):
            try:
                session_result = self.simulate_user_session(user_id)
                batch_results.append(session_result)

                if session_result["success"]:
                    successful_sessions += 1

                # Log de progreso cada 10 usuarios
                if (i + 1) % 10 == 0:
                    logger.info(
                        "Progreso: %d/%d usuarios procesados", i + 1, len(user_ids)
                    )

                # Pausa entre usuarios para evitar saturar APIs
                time.sleep(random.uniform(1, 3))

            except Exception as e:
                logger.error("❌ Error procesando usuario %s: %s", user_id, e)
                self.simulation_stats["errors"] += 1
                continue

        logger.info(
            "✅ Lote completado: %d/%d sesiones exitosas",
            successful_sessions,
            len(user_ids),
        )
        return batch_results

    def get_simulation_statistics(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas detalladas de la simulación.

        Returns:
            Diccionario con métricas de rendimiento
        """
        current_time = datetime.now()
        duration = (current_time - self.simulation_stats["start_time"]).total_seconds()

        return {
            **self.simulation_stats,
            "current_time": current_time,
            "total_duration_seconds": duration,
            "users_per_minute": (
                self.simulation_stats["users_created"] / (duration / 60)
                if duration > 0
                else 0
            ),
            "messages_per_minute": (
                self.simulation_stats["messages_sent"] / (duration / 60)
                if duration > 0
                else 0
            ),
            "error_rate": self.simulation_stats["errors"]
            / max(self.simulation_stats["messages_sent"], 1),
            "success_rate": 1
            - (
                self.simulation_stats["errors"]
                / max(self.simulation_stats["messages_sent"], 1)
            ),
        }

    def reset_statistics(self):
        """Reinicia las estadísticas de simulación."""
        self.simulation_stats = {
            "users_created": 0,
            "messages_sent": 0,
            "recommendations_requested": 0,
            "invoices_uploaded": 0,
            "errors": 0,
            "start_time": datetime.now(),
        }
        logger.info("Estadísticas de simulación reiniciadas")


# Función de conveniencia
def create_interaction_simulator(
    api_client: ProductionAPIClient,
) -> InteractionSimulator:
    """Crea una instancia del simulador de interacciones."""
    return InteractionSimulator(api_client)


# Test del módulo
if __name__ == "__main__":
    # Configurar logging para test
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    print("🧪 Test del InteractionSimulator (sin ejecutar APIs reales)...")

    # Crear cliente mock para test
    class MockAPIClient:
        def post_manual_data(self, user_id, profile_data):
            return {"status": "success", "message": "Mock data posted"}

        def post_chat_message(self, user_id, user_context, message):
            return {"status": "success", "response": "Mock chat response"}

        def get_tariff_recommendations(self, user_id):
            return {"status": "success", "recommendations": ["Mock recommendation"]}

        def post_consumption_data(self, user_id, profile_data):
            return {"status": "success", "message": "Mock consumption data"}

    # Crear simulador con cliente mock
    mock_client = MockAPIClient()
    simulator = InteractionSimulator(mock_client)

    # Simular algunos usuarios
    test_user_ids = ["test_user_001", "test_user_002"]
    results = simulator.simulate_batch_users(test_user_ids)

    # Mostrar estadísticas
    stats = simulator.get_simulation_statistics()
    print(f"\n📊 Estadísticas del test:")
    print(f"  Usuarios creados: {stats['users_created']}")
    print(f"  Mensajes enviados: {stats['messages_sent']}")
    print(f"  Tasa de éxito: {stats['success_rate']:.2%}")

    print("\n✅ Test completado correctamente")
