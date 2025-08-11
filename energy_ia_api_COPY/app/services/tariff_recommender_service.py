# energy_ia_api_COPY/app/services/tariff_recommender_service.py
# 🏢 SERVICIO DE RECOMENDACIÓN DE TARIFAS EMPRESARIAL - LÓGICA DE NEGOCIO AISLADA

import logging
from datetime import datetime
from typing import Dict, List, Any
from flask import current_app
from google.cloud import bigquery
from google.api_core import exceptions as google_exceptions
import numpy as np

from utils.error_handlers import AppError
from app.services.vertex_ai_service import VertexAIService
from utils.timezone_utils import now_spanish_iso, now_spanish

# Configuración de logging para el servicio
logger = logging.getLogger(__name__)


def check_duplicate_tariff_robust(
    bq_client, table_id, supplier_name, tariff_name, tariff_type
):
    """
    🔒 VALIDACIÓN ANTIDUPLICADOS ULTRA ROBUSTA - EMPRESARIAL
    """
    try:
        supplier_clean = str(supplier_name or "").strip().upper()
        tariff_clean = str(tariff_name or "").strip().upper()
        type_clean = str(tariff_type or "").strip().upper()

        if not supplier_clean or not tariff_clean or not type_clean:
            logger.warning("⚠️ Datos incompletos para validación duplicados - CONTINUANDO")
            return False

        query = f"""
        SELECT COUNT(*) as count
        FROM `{table_id}`
        WHERE UPPER(TRIM(COALESCE(provider_name, ''))) = @supplier
          AND UPPER(TRIM(COALESCE(tariff_name, ''))) = @tariff_name  
          AND UPPER(TRIM(COALESCE(tariff_type, ''))) = @tariff_type
        LIMIT 1
        """

        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("supplier", "STRING", supplier_clean),
                bigquery.ScalarQueryParameter("tariff_name", "STRING", tariff_clean),
                bigquery.ScalarQueryParameter("tariff_type", "STRING", type_clean),
            ],
            job_timeout=10.0,
        )

        query_job = bq_client.query(query, job_config=job_config)
        results = list(query_job.result(timeout=15))
        is_duplicate = results[0].count > 0 if results else False

        if is_duplicate:
            logger.warning(f"🔄 DUPLICADO DETECTADO: {supplier_clean} - {tariff_clean}")
        else:
            logger.debug(f"✅ Validación OK: {supplier_clean} - {tariff_clean}")

        return is_duplicate
    except Exception as e:
        error_msg = str(e)
        logger.error(f"❌ Error validación duplicados (CONTINUANDO): {error_msg}")
        if any(keyword in error_msg.lower() for keyword in ["timeout", "deadline", "connection", "network"]):
            logger.warning("🌐 Error de red en validación - PERMITIENDO continuar")
        elif "not found" in error_msg.lower() or "does not exist" in error_msg.lower():
            logger.info("📋 Tabla nueva detectada - PERMITIENDO continuar")
        else:
            logger.warning("⚠️ Error desconocido en validación duplicados - CONTINUANDO por robustez")
        return False


class EnterpriseTariffRecommenderService:
    """Servicio empresarial para recomendación de tarifas - El mejor del mercado"""

    def __init__(self):
        self.bq_client = bigquery.Client()
        self.project_id = current_app.config["GCP_PROJECT_ID"]
        self.dataset_id = current_app.config["BQ_DATASET_ID"]
        # TODO: VERIFICAR MILIMÉTRICAMENTE el nombre de esta tabla con el esquema real.
        self.tariffs_table = f"{self.project_id}.{self.dataset_id}.market_electricity_tariffs"
        # TODO: VERIFICAR MILIMÉTRICAMENTE el nombre de esta tabla con el esquema real.
        self.recommendation_log_table = f"{self.project_id}.{self.dataset_id}.recommendation_log"
        self.vertex_service = VertexAIService()
        logger.info("🏢 EnterpriseTariffRecommenderService inicializado")

    def get_market_electricity_tariffs(self) -> List[Dict]:
        """Obtiene todas las tarifas del mercado actualizadas"""
        # TODO: VERIFICAR MILIMÉTRICAMENTE cada uno de estos campos con el esquema real.
        query = f"""
        SELECT 
            provider_name, tariff_name, tariff_type, tariff_id, fixed_monthly_fee,
            kwh_price_flat, kwh_price_peak, kwh_price_valley, power_price_per_kw_per_month,
            is_pvpc, is_active, update_timestamp
        FROM `{self.tariffs_table}`
        WHERE is_active = TRUE
        ORDER BY update_timestamp DESC
        """
        try:
            query_job = self.bq_client.query(query)
            results = query_job.result()
            tariffs = [dict(row) for row in results]
            for tariff in tariffs:
                if 'update_timestamp' in tariff and tariff['update_timestamp']:
                    tariff['update_timestamp'] = tariff['update_timestamp'].isoformat()
            logger.info(f"✅ Obtenidas {len(tariffs)} tarifas del mercado")
            return tariffs
        except google_exceptions.GoogleAPICallError as e:
            logger.error(f"❌ Error de API de BigQuery obteniendo tarifas: {str(e)}")
            raise AppError(f"Error de comunicación con la base de datos de tarifas: {str(e)}", 503)
        except Exception as e:
            logger.error(f"❌ Error inesperado obteniendo tarifas del mercado: {str(e)}")
            raise AppError(f"Error interno accediendo a datos de tarifas: {str(e)}", 500)

    def calculate_annual_cost(self, tariff: Dict, consumption_profile: Dict) -> Dict:
        """Calcula el costo anual exacto para una tarifa específica"""
        try:
            avg_kwh = float(consumption_profile.get("avg_kwh", 0) or 0)
            contracted_power_kw = float(consumption_profile.get("contracted_power_kw", 0) or 0)
            peak_percent = (float(consumption_profile.get("peak_percent", 50) or 50)) / 100

            annual_kwh = avg_kwh * 12
            peak_kwh = annual_kwh * peak_percent
            valley_kwh = annual_kwh * (1 - peak_percent)

            power_cost = (float(tariff.get("power_price_per_kw_per_month", 0) or 0) * contracted_power_kw) * 12
            fixed_fee = float(tariff.get("fixed_monthly_fee", 0) or 0) * 12
            fixed_term_annual = power_cost + fixed_fee

            if tariff.get("kwh_price_peak") and tariff.get("kwh_price_valley"):
                variable_term_annual = (peak_kwh * float(tariff["kwh_price_peak"])) + (valley_kwh * float(tariff["kwh_price_valley"]))
            else:
                variable_term_annual = annual_kwh * float(tariff.get("kwh_price_flat", 0) or 0)

            total_cost = fixed_term_annual + variable_term_annual

            current_annual_cost = float(consumption_profile.get("current_annual_cost", 0) or 0)
            annual_savings = max(0, current_annual_cost - total_cost)
            savings_percentage = (annual_savings / current_annual_cost * 100) if current_annual_cost > 0 else 0

            return {
                "annual_cost": round(total_cost, 2),
                "monthly_cost": round(total_cost / 12, 2),
                "annual_savings": round(annual_savings, 2),
                "savings_percentage": round(savings_percentage, 2),
            }
        except (ValueError, TypeError) as e:
            logger.error(f"❌ Error de tipo de dato calculando costo anual: {str(e)}")
            return {"annual_cost": 0, "monthly_cost": 0, "error": "Invalid data format during cost calculation."}
        except Exception as e:
            logger.error(f"❌ Error inesperado calculando costo anual: {str(e)}")
            return {"annual_cost": 0, "monthly_cost": 0, "error": str(e)}

    def get_advanced_recommendation(self, consumption_profile: Dict) -> Dict:
        """Obtiene recomendación avanzada y la registra de forma robusta."""
        try:
            all_tariffs = self.get_market_electricity_tariffs()
            if not all_tariffs:
                raise AppError("Actualmente no hay tarifas disponibles en el mercado para comparar.", 404)

            tariff_analysis = []
            for tariff in all_tariffs:
                cost_analysis = self.calculate_annual_cost(tariff, consumption_profile)
                if "error" in cost_analysis:
                    logger.warning(f"Saltando tarifa {tariff.get('tariff_name')} debido a un error de cálculo.")
                    continue
                
                analysis = {
                    "tariff_info": tariff,
                    "cost_analysis": cost_analysis,
                }
                tariff_analysis.append(analysis)

            if not tariff_analysis:
                raise AppError("No se pudieron calcular los costos para las tarifas disponibles.", 500)

            sorted_tariffs = sorted(tariff_analysis, key=lambda x: x["cost_analysis"]["annual_cost"])
            best_tariff = sorted_tariffs[0]
            
            recommendation = {
                "best_recommendation": best_tariff,
                "top_3_alternatives": sorted_tariffs[1:4],
                "generated_at": now_spanish_iso(),
            }

            self._log_recommendation(consumption_profile["user_id"], recommendation, consumption_profile)
            logger.info(f"✅ Recomendación generada y registrada para usuario {consumption_profile['user_id']}")
            return recommendation
        except AppError as e:
            logger.error(f"❌ Error de aplicación generando recomendación: {str(e)}")
            raise e
        except Exception as e:
            logger.error(f"❌ Error inesperado generando recomendación avanzada: {str(e)}")
            raise AppError(f"Error interno en el motor de recomendaciones: {str(e)}", 500)

    def _log_recommendation(self, user_id: str, recommendation: Dict, consumption_profile: Dict):
        """
        Registra la recomendación en BigQuery de forma robusta y a prueba de fallos.
        """
        try:
            best_rec = recommendation.get("best_recommendation", {})
            tariff_info = best_rec.get("tariff_info", {})
            cost_analysis = best_rec.get("cost_analysis", {})

            # Validación de datos críticos antes de la inserción
            required_keys = ["provider_name", "tariff_name"]
            if not all(key in tariff_info for key in required_keys):
                logger.error("❌ Datos de tarifa insuficientes para registrar la recomendación.")
                return 
            
            # TODO: VERIFICAR MILIMÉTRICAMENTE cada uno de estos campos con el esquema real.
            log_data = {
                "recommendation_id": f"rec_{user_id}_{int(datetime.now().timestamp())}",
                "user_id": user_id,
                "timestamp_utc": now_spanish_iso(),
                "input_avg_kwh": consumption_profile.get("avg_kwh"),
                "input_peak_percent": consumption_profile.get("peak_percent"),
                "input_contracted_power_kw": consumption_profile.get("contracted_power_kw"),
                "recommended_provider": tariff_info.get("provider_name"),
                "recommended_tariff_name": tariff_info.get("tariff_name"),
                "estimated_annual_saving": cost_analysis.get("annual_savings"),
                "estimated_annual_cost": cost_analysis.get("annual_cost"),
            }

            errors = self.bq_client.insert_rows_json(self.recommendation_log_table, [log_data])
            if not errors:
                logger.info(f"✅ Recomendación registrada en BigQuery para usuario {user_id}")
            else:
                # Este log es crítico para producción. Muestra exactamente qué falló.
                logger.error(f"❌ Fallo en la inserción a BigQuery para {user_id}: {errors}")
        
        except KeyError as e:
            # Este error previene fallos si la estructura de 'recommendation' cambia.
            logger.error(f"❌ Error de clave (KeyError) al preparar el log de recomendación: {str(e)}")
        except google_exceptions.GoogleAPICallError as e:
            logger.error(f"❌ Error de API de BigQuery registrando recomendación: {str(e)}")
        except Exception as e:
            # Captura cualquier otro error para que el proceso principal no falle.
            logger.error(f"❌ Error inesperado registrando recomendación: {str(e)}")

    # Las funciones add_tariff y batch_add_tariffs permanecen como placeholders
    # hasta que se definan completamente sus requisitos y esquemas.
    def add_tariff(self, tariff_data: Dict, admin_id: str) -> Dict[str, Any]:
        """Añade una nueva tarifa a la base de datos."""
        logger.info(f"Función 'add_tariff' llamada por admin {admin_id}. Implementación pendiente.")
        return {"status": "pending_implementation"}

    def batch_add_tariffs(self, tariffs: List[Dict], admin_id: str) -> Dict[str, Any]:
        """Añade múltiples tarifas en lote."""
        logger.info(f"Función 'batch_add_tariffs' llamada por admin {admin_id}. Implementación pendiente.")
        return {"status": "pending_implementation", "tariffs_received": len(tariffs)}
