# src/autonomous_runner.py
# Orquestador principal del simulador de entrenamiento autónomo

import sys
import os
import time
import logging
from typing import List, Dict, Any
from datetime import datetime, timedelta
import signal

# Añadir el directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar configuración y módulos
from config.simulation_config import (
    AUTONOMOUS_MODE,
    EXECUTION_INTERVAL_HOURS,
    NUM_USERS_PER_RUN,
    EXPERT_BOT_API_URL,
    ENERGY_IA_API_URL,
    AUTH_TOKEN,
    validate_configuration,
    estimate_daily_cost,
    LOG_LEVEL,
    LOG_FILE,
)

from src.api_client import create_api_client
from src.interaction_simulator import create_interaction_simulator
from data.es_data_generators import generate_synthetic_user_id

# Configurar logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(LOG_FILE, encoding="utf-8"), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)


class AutonomousTrainingRunner:
    """
    Orquestador principal del sistema de entrenamiento autónomo.
    Controla la ejecución, costes y métricas del simulador.
    """

    def __init__(self):
        """Inicializa el runner autónomo."""
        self.is_running = False
        self.total_executions = 0
        self.total_users_simulated = 0
        self.total_errors = 0
        self.start_time = datetime.now()
        self.api_client = None
        self.simulator = None

        # Configurar manejo de señales para parada elegante
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

        logger.info("🚀 AutonomousTrainingRunner inicializado")

    def _signal_handler(self, signum, frame):
        """Maneja señales de interrupción para parada elegante."""
        logger.info("⚠️ Señal de interrupción recibida. Deteniendo simulador...")
        self.is_running = False

    def initialize_services(self) -> bool:
        """
        Inicializa los servicios necesarios para la simulación.

        Returns:
            True si la inicialización fue exitosa
        """
        try:
            logger.info("🔧 Inicializando servicios...")

            # Validar configuración
            validate_configuration()
            logger.info("✅ Configuración validada")

            # Crear cliente API
            self.api_client = create_api_client(
                EXPERT_BOT_API_URL, ENERGY_IA_API_URL, AUTH_TOKEN
            )

            # Verificar conectividad
            health_status = self.api_client.health_check()
            if not all(health_status.values()):
                logger.error(
                    "❌ Algunos servicios no están disponibles: %s", health_status
                )
                return False

            logger.info("✅ Servicios disponibles: %s", health_status)

            # Crear simulador
            self.simulator = create_interaction_simulator(self.api_client)
            logger.info("✅ Simulador de interacciones inicializado")

            # Mostrar estimación de costes
            cost_info = estimate_daily_cost()
            logger.info(
                "💰 Estimación de costes diarios: $%.2f USD",
                cost_info["estimated_cost_usd"],
            )
            logger.info(
                "📊 Usuarios diarios estimados: %d", int(cost_info["daily_users"])
            )
            logger.info(
                "📞 Llamadas API diarias estimadas: %d",
                int(cost_info["daily_api_calls"]),
            )

            return True

        except Exception as e:
            logger.error("❌ Error inicializando servicios: %s", e)
            return False

    def run_single_simulation(self) -> Dict[str, Any]:
        """
        Ejecuta una única simulación completa.

        Returns:
            Resultado de la simulación
        """
        execution_start = datetime.now()
        logger.info(
            "🎯 Iniciando ejecución #%d - %d usuarios",
            self.total_executions + 1,
            NUM_USERS_PER_RUN,
        )

        try:
            # Generar IDs de usuarios sintéticos
            user_ids = [generate_synthetic_user_id() for _ in range(NUM_USERS_PER_RUN)]
            logger.info("👥 Generados %d usuarios sintéticos", len(user_ids))

            # Ejecutar simulación
            session_results = self.simulator.simulate_batch_users(user_ids)

            # Calcular métricas de la ejecución
            successful_sessions = sum(
                1 for result in session_results if result["success"]
            )
            failed_sessions = len(session_results) - successful_sessions

            # Actualizar estadísticas globales
            self.total_executions += 1
            self.total_users_simulated += len(user_ids)
            self.total_errors += failed_sessions

            # Obtener estadísticas del simulador
            sim_stats = self.simulator.get_simulation_statistics()

            execution_time = (datetime.now() - execution_start).total_seconds()

            execution_result = {
                "execution_number": self.total_executions,
                "start_time": execution_start,
                "end_time": datetime.now(),
                "duration_seconds": execution_time,
                "users_requested": NUM_USERS_PER_RUN,
                "users_processed": len(user_ids),
                "successful_sessions": successful_sessions,
                "failed_sessions": failed_sessions,
                "success_rate": successful_sessions / len(user_ids) if user_ids else 0,
                "simulator_stats": sim_stats,
                "session_results": session_results,
            }

            # Log de resultados
            logger.info(
                "✅ Ejecución #%d completada en %.1f segundos",
                self.total_executions,
                execution_time,
            )
            logger.info(
                "📊 Resultado: %d/%d sesiones exitosas (%.1f%%)",
                successful_sessions,
                len(user_ids),
                (successful_sessions / len(user_ids) * 100) if user_ids else 0,
            )
            logger.info("💬 Mensajes enviados: %d", sim_stats["messages_sent"])
            logger.info(
                "💰 Recomendaciones solicitadas: %d",
                sim_stats["recommendations_requested"],
            )
            logger.info("📄 Facturas subidas: %d", sim_stats["invoices_uploaded"])

            return execution_result

        except Exception as e:
            logger.error("❌ Error en ejecución #%d: %s", self.total_executions + 1, e)
            self.total_errors += 1

            return {
                "execution_number": self.total_executions + 1,
                "start_time": execution_start,
                "end_time": datetime.now(),
                "error": str(e),
                "success": False,
            }

    def run_autonomous_mode(self):
        """Ejecuta el simulador en modo autónomo continuo."""
        logger.info(
            "🔄 Iniciando modo autónomo - Intervalo: %d horas", EXECUTION_INTERVAL_HOURS
        )

        self.is_running = True

        while self.is_running:
            try:
                # Ejecutar simulación
                result = self.run_single_simulation()

                if not self.is_running:
                    break

                # Calcular tiempo hasta próxima ejecución
                next_execution = datetime.now() + timedelta(
                    hours=EXECUTION_INTERVAL_HOURS
                )
                logger.info(
                    "💤 Próxima ejecución programada para: %s",
                    next_execution.strftime("%Y-%m-%d %H:%M:%S"),
                )

                # Dormir hasta la próxima ejecución (con verificación periódica)
                sleep_seconds = EXECUTION_INTERVAL_HOURS * 3600
                sleep_interval = 60  # Verificar cada minuto si debe parar

                while sleep_seconds > 0 and self.is_running:
                    time.sleep(min(sleep_interval, sleep_seconds))
                    sleep_seconds -= sleep_interval

                    # Log periódico de estado
                    if sleep_seconds % 3600 == 0 and sleep_seconds > 0:  # Cada hora
                        hours_remaining = sleep_seconds / 3600
                        logger.info(
                            "⏰ %.0f horas hasta próxima ejecución", hours_remaining
                        )

            except KeyboardInterrupt:
                logger.info("⚠️ Interrupción manual recibida")
                break
            except Exception as e:
                logger.error("❌ Error en modo autónomo: %s", e)
                logger.info("🔄 Reintentando en 10 minutos...")
                time.sleep(600)  # Esperar 10 minutos antes de reintentar

        logger.info("🛑 Modo autónomo detenido")

    def run_manual_mode(self):
        """Ejecuta una única simulación en modo manual."""
        logger.info("🎯 Ejecutando modo manual - Una sola ejecución")

        result = self.run_single_simulation()

        if result.get("success", True):
            logger.info("✅ Simulación manual completada exitosamente")
        else:
            logger.error(
                "❌ Simulación manual falló: %s",
                result.get("error", "Error desconocido"),
            )

        return result

    def get_global_statistics(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas globales del runner.

        Returns:
            Diccionario con métricas globales
        """
        current_time = datetime.now()
        uptime = (current_time - self.start_time).total_seconds()

        return {
            "start_time": self.start_time,
            "current_time": current_time,
            "uptime_seconds": uptime,
            "uptime_hours": uptime / 3600,
            "total_executions": self.total_executions,
            "total_users_simulated": self.total_users_simulated,
            "total_errors": self.total_errors,
            "executions_per_hour": (
                self.total_executions / (uptime / 3600) if uptime > 0 else 0
            ),
            "users_per_hour": (
                self.total_users_simulated / (uptime / 3600) if uptime > 0 else 0
            ),
            "error_rate": (
                self.total_errors / self.total_users_simulated
                if self.total_users_simulated > 0
                else 0
            ),
            "is_running": self.is_running,
            "mode": "autonomous" if AUTONOMOUS_MODE else "manual",
        }

    def cleanup(self):
        """Limpia recursos al finalizar."""
        try:
            if self.api_client:
                self.api_client.close()
                logger.info("✅ Cliente API cerrado")

            # Log de estadísticas finales
            stats = self.get_global_statistics()
            logger.info("📊 Estadísticas finales:")
            logger.info("  - Tiempo activo: %.1f horas", stats["uptime_hours"])
            logger.info("  - Ejecuciones totales: %d", stats["total_executions"])
            logger.info("  - Usuarios simulados: %d", stats["total_users_simulated"])
            logger.info("  - Tasa de error: %.2f%%", stats["error_rate"] * 100)

        except Exception as e:
            logger.error("❌ Error en cleanup: %s", e)


def main():
    """Función principal del simulador."""
    logger.info("🚀 Iniciando Simulador de Entrenamiento IA SmarWatt")
    logger.info("📅 Fecha: %s", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    logger.info("⚙️ Modo: %s", "Autónomo" if AUTONOMOUS_MODE else "Manual")

    # Crear runner
    runner = AutonomousTrainingRunner()

    try:
        # Inicializar servicios
        if not runner.initialize_services():
            logger.error("❌ Error inicializando servicios. Abortando.")
            return 1

        # Ejecutar según modo configurado
        if AUTONOMOUS_MODE:
            runner.run_autonomous_mode()
        else:
            runner.run_manual_mode()

    except KeyboardInterrupt:
        logger.info("⚠️ Interrupción manual del usuario")
    except Exception as e:
        logger.error("❌ Error fatal: %s", e)
        return 1
    finally:
        # Cleanup
        runner.cleanup()
        logger.info("👋 Simulador finalizado")

    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
