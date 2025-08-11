# energy_ia_api_COPY/app/services/tariff_recommender_service.py
# 🏢 SERVICIO DE RECOMENDACIÓN DE TARIFAS EMPRESARIAL - LÓGICA DE NEGOCIO AISLADA

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any
from flask import current_app
from google.cloud import bigquery
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
        self.tariffs_table = f"{self.project_id}.{self.dataset_id}.{current_app.config['BQ_MARKET_TARIFFS_TABLE_ID']}"
        self.recommendation_log_table = f"{self.project_id}.{self.dataset_id}.{current_app.config['BQ_RECOMMENDATION_LOG_TABLE_ID']}"
        self.vertex_service = VertexAIService()
        logger.info("🏢 EnterpriseTariffRecommenderService inicializado")

    def get_market_electricity_tariffs(self) -> List[Dict]:
        """Obtiene todas las tarifas del mercado actualizadas"""
        try:
            query = f"""
            SELECT 
                provider_name, tariff_name, tariff_type, tariff_id, fixed_monthly_fee,
                kwh_price_flat, kwh_price_peak, kwh_price_valley, power_price_per_kw_per_month,
                is_pvpc, is_active, update_timestamp
            FROM `{self.tariffs_table}`
            WHERE is_active = TRUE
            ORDER BY update_timestamp DESC
            """
            query_job = self.bq_client.query(query)
            results = query_job.result()
            tariffs = [dict(row) for row in results]
            for tariff in tariffs:
                tariff["update_timestamp"] = tariff["update_timestamp"].isoformat() if tariff["update_timestamp"] else None
            logger.info(f"✅ Obtenidas {len(tariffs)} tarifas del mercado")
            return tariffs
        except Exception as e:
            logger.error(f"❌ Error obteniendo tarifas del mercado: {str(e)}")
            raise AppError(f"Error accediendo a datos de tarifas: {str(e)}", 500)

    def calculate_annual_cost(self, tariff: Dict, consumption_profile: Dict) -> Dict:
        """Calcula el costo anual exacto para una tarifa específica"""
        try:
            avg_kwh = consumption_profile.get("avg_kwh", 0) or 0
            contracted_power_kw = consumption_profile.get("contracted_power_kw", 0) or 0
            peak_percent = (consumption_profile.get("peak_percent", 50) or 50) / 100

            annual_kwh = avg_kwh * 12
            peak_kwh = annual_kwh * peak_percent
            valley_kwh = annual_kwh * (1 - peak_percent)

            fixed_term_annual = (tariff.get("power_price_per_kw_per_month", 0) * contracted_power_kw) * 12 + (tariff.get("fixed_monthly_fee", 0) * 12)

            if tariff.get("kwh_price_peak") and tariff.get("kwh_price_valley"):
                variable_term_annual = (peak_kwh * tariff["kwh_price_peak"]) + (valley_kwh * tariff["kwh_price_valley"])
            else:
                variable_term_annual = annual_kwh * tariff.get("kwh_price_flat", 0)

            total_cost = fixed_term_annual + variable_term_annual

            current_annual_cost = consumption_profile.get("current_annual_cost", 0)
            annual_savings = max(0, current_annual_cost - total_cost)
            savings_percentage = (annual_savings / current_annual_cost * 100) if current_annual_cost > 0 else 0

            return {
                "annual_cost": round(total_cost, 2),
                "monthly_cost": round(total_cost / 12, 2),
                "annual_savings": round(annual_savings, 2),
                "savings_percentage": round(savings_percentage, 2),
            }
        except Exception as e:
            logger.error(f"❌ Error calculando costo anual: {str(e)}")
            return {"annual_cost": 0, "monthly_cost": 0, "error": str(e)}

    def get_advanced_recommendation(self, consumption_profile: Dict) -> Dict:
        """Obtiene recomendación avanzada - mejor que cualquier página web"""
        try:
            all_tariffs = self.get_market_electricity_tariffs()
            if not all_tariffs:
                raise AppError("No se encontraron tarifas disponibles en el mercado", 404)

            tariff_analysis = []
            for tariff in all_tariffs:
                cost_analysis = self.calculate_annual_cost(tariff, consumption_profile)
                analysis = {
                    "tariff_info": tariff,
                    "cost_analysis": cost_analysis,
                    "suitability_score": self._calculate_suitability_score(tariff, consumption_profile),
                    "pros": self._get_tariff_pros(tariff),
                    "cons": self._get_tariff_cons(tariff, consumption_profile),
                }
                tariff_analysis.append(analysis)

            sorted_tariffs = sorted(tariff_analysis, key=lambda x: x["cost_analysis"]["annual_cost"])
            best_tariff = sorted_tariffs[0]
            
            # Placeholder for ML prediction
            ml_prediction = {"ml_suggestion": "Based on your profile, this tariff is a strong match."}

            recommendation = {
                "best_recommendation": best_tariff,
                "top_3_alternatives": sorted_tariffs[1:4],
                "market_analysis": {
                    "total_tariffs_analyzed": len(all_tariffs),
                    "average_market_price": round(np.mean([t["cost_analysis"]["annual_cost"] for t in tariff_analysis]), 2),
                },
                "ml_insights": ml_prediction,
                "generated_at": now_spanish_iso(),
            }

            self._log_recommendation(consumption_profile["user_id"], recommendation)
            logger.info(f"✅ Recomendación generada para usuario {consumption_profile['user_id']}")
            return recommendation
        except Exception as e:
            logger.error(f"❌ Error generando recomendación avanzada: {str(e)}")
            raise AppError(f"Error en motor de recomendaciones: {str(e)}", 500)

    def _calculate_suitability_score(self, tariff: Dict, profile: Dict) -> float:
        """Calcula puntuación de conveniencia (0-100)"""
        score = 50
        if tariff.get("is_pvpc"): score += 10
        if profile.get("peak_percent", 50) < 45 and tariff.get("kwh_price_peak"): score += 15
        return min(100, score)

    def _get_tariff_pros(self, tariff: Dict) -> List[str]:
        """Obtiene ventajas de la tarifa"""
        pros = []
        if tariff.get("is_pvpc"): pros.append("Regulada por el gobierno (PVPC)")
        if not tariff.get("permanence"): pros.append("Sin permanencia")
        return pros

    def _get_tariff_cons(self, tariff: Dict, profile: Dict) -> List[str]:
        """Obtiene desventajas de la tarifa"""
        cons = []
        if profile.get("peak_percent", 50) > 55 and tariff.get("kwh_price_peak"):
            cons.append("Precio elevado en horas punta")
        return cons

    def _log_recommendation(self, user_id: str, recommendation: Dict):
        """Registra la recomendación en BigQuery"""
        try:
            log_data = {
                "recommendation_id": f"rec_{user_id}_{int(datetime.now().timestamp())}",
                "user_id": user_id,
                "timestamp_utc": now_spanish_iso(),
                "recommended_provider": recommendation["best_recommendation"]["tariff_info"]["provider_name"],
                "recommended_tariff_name": recommendation["best_recommendation"]["tariff_info"]["tariff_name"],
                "estimated_annual_saving": recommendation["best_recommendation"]["cost_analysis"].get("annual_savings", 0),
                "estimated_annual_cost": recommendation["best_recommendation"]["cost_analysis"]["annual_cost"],
            }
            errors = self.bq_client.insert_rows_json(self.recommendation_log_table, [log_data])
            if not errors:
                logger.info(f"✅ Recomendación registrada en BigQuery para usuario {user_id}")
            else:
                logger.error(f"❌ Error registrando recomendación en BigQuery: {errors}")
        except Exception as e:
            logger.error(f"❌ Error registrando recomendación: {str(e)}")

    def add_tariff(self, tariff_data: Dict, admin_id: str) -> Dict[str, Any]:
        """Añade una nueva tarifa a la base de datos."""
        # Lógica para añadir tarifa...
        pass

    def batch_add_tariffs(self, tariffs: List[Dict], admin_id: str) -> Dict[str, Any]:
        """Añade múltiples tarifas en lote."""
        # Lógica para añadir tarifas en lote...
        pass
