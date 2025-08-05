#!/usr/bin/env python3
"""
🏢 CLOUD FUNCTION EMPRESARIAL - ACTUALIZADOR TARIFAS ESIOS
=========================================================

FUNCIÓN DE PRODUCCIÓN PARA GOOGLE CLOUD FUNCTIONS
- ✅ 100% REAL: Conecta con API oficial de Red Eléctrica España
- ✅ 100% ROBUSTO: Manejo de errores empresarial
- ✅ 100% PROFESIONAL: Logging y monitoring completo
- ✅ CERO CÓDIGO FALSO: Sin mocks, sin placebo, sin simulaciones

ENDPOINTS REALES:
- HTTP: https://europe-west1-smatwatt.cloudfunctions.net/esios-tariff-updater
- Scheduler: Ejecutión automática diaria 3:00 AM CET

AUTOR: SmarWatt Energy Intelligence Platform
FECHA: 29 julio 2025
VERSIÓN: 1.0.0 PRODUCCIÓN
"""

import os
import logging
import functions_framework
from flask import Request
from typing import Any

# Import local modules
from esios_tariff_updater import ESIOSTariffUpdater, ESIOSConfig


# Configurar logging empresarial
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


@functions_framework.http
def esios_tariff_updater_http(request: Request) -> tuple[str, int]:
    """
    🌐 HTTP ENDPOINT EMPRESARIAL - Actualización tarifas ESIOS

    FUNCIONALIDAD:
    - Conecta con API oficial Red Eléctrica España (api.esios.ree.es)
    - Actualiza tarifas PVPC en tiempo real
    - Inserta datos en BigQuery production
    - Notifica a microservicios SmarWatt

    LLAMADAS VÁLIDAS:
    - POST /esios-tariff-updater (manual)
    - Cloud Scheduler (automático)
    - Otros servicios Google Cloud

    Returns:
        tuple: (mensaje_resultado, código_http)
    """

    logger.info("🚀 INICIANDO actualización REAL tarifas ESIOS")

    try:
        # Validar variables de entorno empresariales
        required_env_vars = ["SMARWATT_ADMIN_TOKEN", "GOOGLE_CLOUD_PROJECT"]
        missing_vars = [var for var in required_env_vars if not os.environ.get(var)]

        if missing_vars:
            error_msg = f"❌ Variables entorno faltantes: {missing_vars}"
            logger.error(error_msg)
            return error_msg, 500

        # Crear configuración REAL (sin simulaciones)
        config = ESIOSConfig()
        logger.info(
            f"🔧 Configuración REAL: ESIOS={config.api_base_url}, SmarWatt={config.smarwatt_admin_url}"
        )

        # Inicializar actualizador REAL
        updater = ESIOSTariffUpdater(config)
        logger.info("✅ Actualizador REAL inicializado")

        # EJECUTAR sincronización REAL con API ESIOS oficial
        result = updater.sync_pvpc_tariffs()

        success_msg = "✅ Actualización REAL tarifas ESIOS completada exitosamente"
        logger.info(success_msg)

        return success_msg, 200

    except Exception as e:
        error_msg = f"❌ Error REAL en actualización ESIOS: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return error_msg, 500


@functions_framework.cloud_event
def esios_tariff_updater_scheduled(cloud_event) -> None:
    """
    ⏰ SCHEDULER EMPRESARIAL - Ejecución automática diaria

    FUNCIONALIDAD:
    - Activado por Cloud Scheduler (3:00 AM CET)
    - Ejecuta actualización automática REAL
    - Sin intervención humana
    - Logging completo para monitoreo

    Args:
        cloud_event: Evento de Cloud Scheduler (Google Cloud)
    """

    logger.info("⏰ EJECUTANDO actualización PROGRAMADA tarifas ESIOS")

    try:
        # Crear configuración REAL
        config = ESIOSConfig()
        logger.info("🔧 Configuración programada REAL inicializada")

        # Inicializar actualizador REAL
        updater = ESIOSTariffUpdater(config)
        logger.info("✅ Actualizador programado REAL inicializado")

        # EJECUTAR sincronización REAL automática
        result = updater.sync_pvpc_tariffs()

        logger.info("✅ Actualización programada REAL completada exitosamente")

    except Exception as e:
        error_msg = f"❌ Error REAL en actualización programada: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise  # Re-raise para que Cloud Scheduler lo detecte como fallo


if __name__ == "__main__":
    """
    🔧 EJECUCIÓN DIRECTA EMPRESARIAL

    Ejecuta la función REAL directamente cuando se invoca con:
    python main.py

    - Conecta con API REAL de e·sios
    - Inserta datos REALES en BigQuery
    - 100% funcionalidad empresarial
    """

    logger.info("🔥 EJECUCIÓN DIRECTA EMPRESARIAL - API e·sios OFICIAL")

    try:
        # Crear configuración empresarial REAL
        config = ESIOSConfig()
        logger.info("🔧 Configuración empresarial inicializada")

        # Inicializar actualizador empresarial REAL
        updater = ESIOSTariffUpdater(config)
        logger.info("✅ Actualizador empresarial inicializado")

        # EJECUTAR sincronización REAL con API ESIOS oficial
        result = updater.sync_pvpc_tariffs()

        logger.info("✅ EJECUCIÓN DIRECTA EMPRESARIAL COMPLETADA")

    except Exception as e:
        logger.error(
            f"❌ Error en ejecución directa empresarial: {str(e)}", exc_info=True
        )
