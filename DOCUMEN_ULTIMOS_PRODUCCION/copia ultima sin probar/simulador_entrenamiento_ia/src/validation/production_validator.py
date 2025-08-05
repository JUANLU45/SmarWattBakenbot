# src/validation/production_validator.py
# Validador exhaustivo contra producción REAL

import os
import sys
import logging
import requests
from typing import Dict, List, Tuple, Optional
import json
from datetime import datetime

# Agregar el directorio padre al path para imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from config.simulation_config import *


class ProductionValidator:
    """
    Validador que verifica que TODOS los endpoints, tablas y configuraciones
    coincidan EXACTAMENTE con el código de producción en Google Cloud Run.

    🔒 TOLERANCIA CERO A DISCREPANCIAS 🔒
    """

    def __init__(self):
        self.logger = self._setup_logger()
        self.validation_errors = []
        self.validation_warnings = []

    def _setup_logger(self) -> logging.Logger:
        """Configura el logger para validación."""
        logger = logging.getLogger("ProductionValidator")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def validate_all(self) -> bool:
        """
        Ejecuta TODAS las validaciones contra producción.

        Returns:
            bool: True si TODO está correcto, False si hay algún error.
        """
        self.logger.info("🔥 INICIANDO VALIDACIÓN EXHAUSTIVA CONTRA PRODUCCIÓN 🔥")
        self.logger.info("=" * 70)

        validations = [
            ("URLs de Microservicios", self._validate_microservice_urls),
            ("Endpoints Específicos", self._validate_specific_endpoints),
            ("Tablas BigQuery", self._validate_bigquery_tables),
            ("Token Firebase", self._validate_firebase_token),
            ("Configuración GCP", self._validate_gcp_config),
            ("Límites de Costes", self._validate_cost_limits),
            ("Coherencia de Datos", self._validate_data_consistency),
        ]

        all_valid = True

        for validation_name, validation_func in validations:
            self.logger.info(f"🔍 Validando: {validation_name}")
            try:
                is_valid = validation_func()
                if is_valid:
                    self.logger.info(f"✅ {validation_name}: CORRECTO")
                else:
                    self.logger.error(f"❌ {validation_name}: FALLÓ")
                    all_valid = False
            except Exception as e:
                self.logger.error(f"💥 {validation_name}: ERROR - {str(e)}")
                self.validation_errors.append(f"{validation_name}: {str(e)}")
                all_valid = False

            self.logger.info("-" * 50)

        # Resumen final
        self._print_validation_summary(all_valid)
        return all_valid

    def _validate_microservice_urls(self) -> bool:
        """Valida que las URLs de los microservicios sean exactamente las de producción."""

        # URLs EXACTAS de producción según comamdos_desplige_variables_reales.md
        expected_urls = {
            "EXPERT_BOT_API_URL": "https://expert-bot-api-1010012211318.europe-west1.run.app",
            "ENERGY_IA_API_URL": "https://energy-ia-api-1010012211318.europe-west1.run.app",
        }

        is_valid = True

        for var_name, expected_url in expected_urls.items():
            actual_url = globals().get(var_name)

            if actual_url != expected_url:
                self.validation_errors.append(
                    f"{var_name}: Esperado '{expected_url}', actual '{actual_url}'"
                )
                is_valid = False
            else:
                self.logger.info(f"✅ {var_name}: {actual_url}")

        return is_valid

    def _validate_specific_endpoints(self) -> bool:
        """Valida endpoints específicos contra el archivo endopoin.md."""

        # Endpoints críticos que DEBEN existir según endopoin.md
        critical_endpoints = {
            ENERGY_IA_API_URL: [
                "/api/v1/chatbot/message/v2",  # Chat V2
                "/api/v1/energy/tariffs/recommendations",  # Recomendaciones
                "/api/v1/chatbot/health",  # Health check
                "/api/v1/links/status",  # Links status
            ],
            EXPERT_BOT_API_URL: [
                "/api/v1/energy/consumption",  # Consumo (OCR)
                "/api/v1/energy/manual-data",  # Datos manuales
                "/api/v1/energy/users/profile",  # Perfil usuario
                "/api/v1/chatbot/session/start",  # Inicio sesión
            ],
        }

        is_valid = True

        for base_url, endpoints in critical_endpoints.items():
            self.logger.info(f"Validando endpoints en: {base_url}")

            for endpoint in endpoints:
                full_url = f"{base_url}{endpoint}"

                try:
                    # Hacer una petición HEAD para verificar que el endpoint existe
                    response = requests.head(full_url, timeout=10)

                    if response.status_code == 404:
                        self.validation_errors.append(
                            f"Endpoint NO ENCONTRADO: {full_url}"
                        )
                        is_valid = False
                    else:
                        self.logger.info(f"✅ Endpoint existe: {endpoint}")

                except requests.exceptions.RequestException as e:
                    self.validation_warnings.append(
                        f"No se pudo verificar endpoint {full_url}: {str(e)}"
                    )

        return is_valid

    def _validate_bigquery_tables(self) -> bool:
        """Valida que todas las tablas BigQuery coincidan con producción."""

        # Tablas EXACTAS según comamdos_desplige_variables_reales.md
        expected_tables = {
            "BQ_CONVERSATIONS_TABLE_ID": "conversations_log",
            "BQ_CONSUMPTION_LOG_TABLE_ID": "consumption_log",
            "BQ_USER_PROFILES_TABLE_ID": "user_profiles_enriched",
            "BQ_MARKET_TARIFFS_TABLE_ID": "market_electricity_tariffs",
            "BQ_RECOMMENDATION_LOG_TABLE_ID": "recommendation_log",
            "BQ_UPLOADED_DOCS_TABLE_ID": "uploaded_documents_log",
            "BQ_FEEDBACK_TABLE_ID": "feedback_log",
            "BQ_AI_SENTIMENT_TABLE_ID": "ai_sentiment_analysis",
            "BQ_AI_PATTERNS_TABLE_ID": "ai_user_patterns",
            "BQ_AI_OPTIMIZATION_TABLE_ID": "ai_prompt_optimization",
            "BQ_AI_PREDICTIONS_TABLE_ID": "ai_predictions",
            "BQ_AI_BUSINESS_METRICS_TABLE_ID": "ai_business_metrics",
            "BQ_ASYNC_TASKS_TABLE_ID": "async_tasks",
            "BQ_WORKER_METRICS_TABLE_ID": "worker_metrics",
        }

        is_valid = True

        for var_name, expected_table in expected_tables.items():
            actual_table = globals().get(var_name)

            if actual_table != expected_table:
                self.validation_errors.append(
                    f"{var_name}: Esperado '{expected_table}', actual '{actual_table}'"
                )
                is_valid = False
            else:
                self.logger.info(f"✅ {var_name}: {actual_table}")

        return is_valid

    def _validate_firebase_token(self) -> bool:
        """Valida que el token Firebase sea válido y real."""

        if not AUTH_TOKEN:
            self.validation_errors.append("AUTH_TOKEN no está configurado")
            return False

        if len(AUTH_TOKEN) < 100:
            self.validation_errors.append(
                "AUTH_TOKEN parece demasiado corto para ser válido"
            )
            return False

        # Verificar que no sea un token de ejemplo o placeholder
        invalid_tokens = ["PLACEHOLDER", "EXAMPLE", "TEST", "FAKE", "DEMO"]

        for invalid in invalid_tokens:
            if invalid.upper() in AUTH_TOKEN.upper():
                self.validation_errors.append(
                    f"AUTH_TOKEN contiene texto placeholder: {invalid}"
                )
                return False

        self.logger.info("✅ AUTH_TOKEN tiene formato válido")
        return True

    def _validate_gcp_config(self) -> bool:
        """Valida configuración de Google Cloud."""

        expected_config = {
            "GCP_PROJECT_ID": "smatwatt",
            "BQ_DATASET_ID": "smartwatt_data",
        }

        is_valid = True

        for var_name, expected_value in expected_config.items():
            actual_value = globals().get(var_name)

            if actual_value != expected_value:
                self.validation_errors.append(
                    f"{var_name}: Esperado '{expected_value}', actual '{actual_value}'"
                )
                is_valid = False
            else:
                self.logger.info(f"✅ {var_name}: {actual_value}")

        return is_valid

    def _validate_cost_limits(self) -> bool:
        """Valida que los límites de coste estén dentro del presupuesto de €5/mes."""

        monthly_cost = estimate_monthly_cost()

        if not monthly_cost["within_budget"]:
            self.validation_errors.append(
                f"Configuración excede presupuesto: €{monthly_cost['total_monthly_cost_eur']} > €5.00"
            )
            return False

        if monthly_cost["budget_usage_percentage"] > 90:
            self.validation_warnings.append(
                f"Uso del presupuesto alto: {monthly_cost['budget_usage_percentage']}%"
            )

        self.logger.info(
            f"✅ Coste mensual estimado: €{monthly_cost['total_monthly_cost_eur']} "
            f"({monthly_cost['budget_usage_percentage']}% del presupuesto)"
        )

        return True

    def _validate_data_consistency(self) -> bool:
        """Valida consistencia interna de configuración."""

        # Verificar que EXECUTION_INTERVAL_HOURS sea coherente con presupuesto
        if EXECUTION_INTERVAL_HOURS < 24:
            self.validation_warnings.append(
                f"Intervalo de ejecución muy frecuente: {EXECUTION_INTERVAL_HOURS}h (puede exceder presupuesto)"
            )

        # Verificar que NUM_USERS_PER_RUN * API_CALLS_PER_USER sea razonable
        calls_per_run = NUM_USERS_PER_RUN * API_CALLS_PER_USER
        if calls_per_run > 1000:
            self.validation_warnings.append(
                f"Llamadas por ejecución altas: {calls_per_run} (riesgo de coste)"
            )

        self.logger.info(f"✅ Llamadas por ejecución: {calls_per_run}")
        self.logger.info(f"✅ Intervalo de ejecución: {EXECUTION_INTERVAL_HOURS}h")

        return True

    def _print_validation_summary(self, all_valid: bool):
        """Imprime resumen final de validación."""

        self.logger.info("=" * 70)
        self.logger.info("🎯 RESUMEN DE VALIDACIÓN CONTRA PRODUCCIÓN")
        self.logger.info("=" * 70)

        if all_valid:
            self.logger.info("🎉 ¡TODAS LAS VALIDACIONES PASARON!")
            self.logger.info("✅ Configuración 100% compatible con producción")
            self.logger.info("✅ Listo para ejecutar simulador de entrenamiento")
        else:
            self.logger.error("❌ VALIDACIÓN FALLÓ - HAY ERRORES CRÍTICOS")
            self.logger.error("🚫 NO ejecutar simulador hasta corregir errores")

        if self.validation_errors:
            self.logger.error(f"\n🔥 ERRORES CRÍTICOS ({len(self.validation_errors)}):")
            for i, error in enumerate(self.validation_errors, 1):
                self.logger.error(f"   {i}. {error}")

        if self.validation_warnings:
            self.logger.warning(f"\n⚠️  ADVERTENCIAS ({len(self.validation_warnings)}):")
            for i, warning in enumerate(self.validation_warnings, 1):
                self.logger.warning(f"   {i}. {warning}")

        # Estimación final de costes
        monthly_cost = estimate_monthly_cost()
        self.logger.info(f"\n💰 ESTIMACIÓN FINAL DE COSTES:")
        self.logger.info(
            f"   • Coste mensual: €{monthly_cost['total_monthly_cost_eur']}"
        )
        self.logger.info(
            f"   • Uso presupuesto: {monthly_cost['budget_usage_percentage']}%"
        )
        self.logger.info(f"   • Llamadas/mes: {monthly_cost['monthly_api_calls']}")

        self.logger.info("=" * 70)


def main():
    """Función principal para ejecutar validación."""
    validator = ProductionValidator()

    try:
        is_valid = validator.validate_all()

        if is_valid:
            print("\n🚀 VALIDACIÓN EXITOSA - Simulador listo para ejecutar")
            return 0
        else:
            print("\n🛑 VALIDACIÓN FALLÓ - Corregir errores antes de continuar")
            return 1

    except Exception as e:
        print(f"\n💥 ERROR CRÍTICO EN VALIDACIÓN: {str(e)}")
        return 1


if __name__ == "__main__":
    exit(main())
