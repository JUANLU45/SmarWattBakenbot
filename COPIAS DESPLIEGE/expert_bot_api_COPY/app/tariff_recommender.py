"""
EXPERT BOT API - TARIFF RECOMMENDER SERVICE
==========================================

Servicio empresarial para recomendación de tarifas con BigQuery integrado.
Este servicio debe estar en expert_bot_api_COPY para ser llamado desde energy_ia_api_COPY.

FUNCIONALIDADES:
- Análisis de tarifas con datos reales de BigQuery
- Cálculo de costos precisos
- Recomendaciones personalizadas
- Integración con Vertex AI

VERSIÓN: 1.0.0 - EMPRESARIAL
FECHA: 2025-07-30
"""

import logging
import numpy as np
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from flask import current_app
from google.cloud import bigquery
from utils.error_handlers import AppError

# Configurar logger
logger = logging.getLogger("expert_bot_api.tariff_recommender")


def now_spanish_iso() -> str:
    """Obtiene timestamp español ISO"""
    return datetime.now().isoformat()


def now_spanish() -> datetime:
    """Obtiene datetime español"""
    return datetime.now()


class EnterpriseTariffRecommenderService:
    """Servicio empresarial para recomendación de tarifas - El mejor del mercado"""

    def __init__(self):
        self.bq_client = bigquery.Client()
        self.project_id = current_app.config["GCP_PROJECT_ID"]
        self.dataset_id = current_app.config["BQ_DATASET_ID"]
        self.tariffs_table = current_app.config.get(
            "BQ_MARKET_TARIFFS_TABLE_ID", "market_electricity_tariffs"
        )

        logger.info("🏢 EnterpriseTariffRecommenderService inicializado")

    def get_market_electricity_tariffs(self) -> List[Dict]:
        """Obtiene todas las tarifas del mercado actualizadas"""
        try:
            query = f"""
            SELECT 
                provider_name,
                tariff_name,
                tariff_type,
                tariff_id,
                fixed_monthly_fee,
                kwh_price_flat,
                kwh_price_peak,
                kwh_price_valley,
                power_price_per_kw_per_month,
                is_pvpc,
                is_active,
                update_timestamp
            FROM `{self.project_id}.{self.dataset_id}.{self.tariffs_table}`
            WHERE is_active = TRUE
            ORDER BY update_timestamp DESC
            LIMIT 50
            """

            query_job = self.bq_client.query(query)
            results = query_job.result()

            tariffs = []
            for row in results:
                tariff = dict(row)
                tariff["update_timestamp"] = (
                    tariff["update_timestamp"].isoformat()
                    if tariff["update_timestamp"]
                    else None
                )
                tariffs.append(tariff)

            logger.info(f"✅ Obtenidas {len(tariffs)} tarifas del mercado")
            return tariffs

        except Exception as e:
            logger.error(f"❌ Error obteniendo tarifas del mercado: {str(e)}")
            # Intentar obtener tarifas desde fuentes alternativas
            return self._get_emergency_fallback_tariffs()

    def _get_emergency_fallback_tariffs(self) -> List[Dict]:
        """Obtiene tarifas desde fuentes alternativas cuando falla la API principal"""
        try:
            # Intentar obtener desde BigQuery (datos históricos actualizados)
            query = """
                SELECT DISTINCT
                    provider_name,
                    tariff_name,
                    tariff_type,
                    tariff_id,
                    fixed_monthly_fee,
                    kwh_price_flat,
                    kwh_price_peak,
                    kwh_price_valley,
                    power_price_per_kw_per_month,
                    is_pvpc,
                    is_active,
                    update_timestamp
                FROM `{}.{}.market_tariffs`
                WHERE is_active = true
                  AND DATE(update_timestamp) >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
                ORDER BY provider_name, tariff_name
                LIMIT 10
            """.format(
                current_app.config["GCP_PROJECT_ID"],
                current_app.config["BQ_DATASET_ID"],
            )

            job_config = bigquery.QueryJobConfig()
            query_job = self.bq_client.query(query, job_config=job_config)
            results = list(query_job.result())

            if results:
                tariffs = []
                for row in results:
                    tariff = {
                        "provider_name": row.provider_name,
                        "tariff_name": row.tariff_name,
                        "tariff_type": row.tariff_type,
                        "tariff_id": row.tariff_id,
                        "fixed_monthly_fee": float(row.fixed_monthly_fee),
                        "kwh_price_flat": (
                            float(row.kwh_price_flat) if row.kwh_price_flat else None
                        ),
                        "kwh_price_peak": (
                            float(row.kwh_price_peak) if row.kwh_price_peak else None
                        ),
                        "kwh_price_valley": (
                            float(row.kwh_price_valley)
                            if row.kwh_price_valley
                            else None
                        ),
                        "power_price_per_kw_per_month": float(
                            row.power_price_per_kw_per_month
                        ),
                        "is_pvpc": bool(row.is_pvpc),
                        "is_active": bool(row.is_active),
                        "update_timestamp": (
                            row.update_timestamp.isoformat()
                            if row.update_timestamp
                            else None
                        ),
                    }
                    tariffs.append(tariff)

                logger.info(
                    f"✅ Obtenidas {len(tariffs)} tarifas desde BigQuery como fallback"
                )
                return tariffs

        except Exception as e:
            logger.error(f"❌ Error obteniendo tarifas desde BigQuery: {str(e)}")

        try:
            # Fallback final: obtener desde API de la CNMC (pública)
            response = requests.get(
                "https://www.cnmc.es/sites/default/files/comparador_ofertas.json",
                timeout=10,
            )

            if response.status_code == 200:
                cnmc_data = response.json()
                tariffs = []

                # Procesar datos reales de la CNMC
                for item in cnmc_data.get("data", [])[:10]:  # Limitar a 10
                    tariff = {
                        "provider_name": item.get("comercializadora", ""),
                        "tariff_name": item.get("nombre_tarifa", ""),
                        "tariff_type": item.get("tipo_tarifa", "2.0TD"),
                        "tariff_id": f"{item.get('comercializadora', '').lower()}_{item.get('nombre_tarifa', '').lower()}".replace(
                            " ", "_"
                        ),
                        "fixed_monthly_fee": float(item.get("termino_fijo_mensual", 0)),
                        "kwh_price_peak": (
                            float(item.get("precio_kwh_punta", 0))
                            if item.get("precio_kwh_punta")
                            else None
                        ),
                        "kwh_price_valley": (
                            float(item.get("precio_kwh_valle", 0))
                            if item.get("precio_kwh_valle")
                            else None
                        ),
                        "kwh_price_flat": (
                            float(item.get("precio_kwh_plano", 0))
                            if item.get("precio_kwh_plano")
                            else None
                        ),
                        "power_price_per_kw_per_month": float(
                            item.get("termino_potencia", 35.0)
                        ),
                        "is_pvpc": bool(item.get("es_pvpc", False)),
                        "is_active": True,
                        "update_timestamp": datetime.now().isoformat(),
                    }
                    tariffs.append(tariff)

                if tariffs:
                    logger.info(
                        f"✅ Obtenidas {len(tariffs)} tarifas desde API CNMC como fallback"
                    )
                    return tariffs

        except Exception as e:
            logger.error(f"❌ Error obteniendo tarifas desde CNMC: {str(e)}")

        # Si todo falla, devolver error explicativo
        logger.error("❌ No se pudieron obtener tarifas desde ninguna fuente")
        return []

    def calculate_annual_cost(
        self,
        tariff: Dict,
        consumption_kwh: float,
        contracted_power_kw: float,
        peak_percent: float = 35.0,
    ) -> Dict:
        """Calcula el costo anual exacto para una tarifa específica"""
        try:
            # Calcular consumo anual
            annual_kwh = consumption_kwh * 12
            peak_kwh = annual_kwh * (peak_percent / 100)
            valley_kwh = annual_kwh * (1 - peak_percent / 100)

            # Calcular término de potencia anual
            power_cost_annual = (
                tariff.get("power_price_per_kw_per_month", 38.0) * contracted_power_kw
            ) * 12

            # Calcular término de energía
            if tariff.get("kwh_price_peak") and tariff.get("kwh_price_valley"):
                # Tarifa con discriminación horaria
                energy_cost_annual = peak_kwh * tariff.get(
                    "kwh_price_peak", 0.15
                ) + valley_kwh * tariff.get("kwh_price_valley", 0.08)
            else:
                # Tarifa plana
                energy_cost_annual = annual_kwh * tariff.get("kwh_price_flat", 0.12)

            # Término fijo mensual
            fixed_cost_annual = tariff.get("fixed_monthly_fee", 15.0) * 12

            # Costo total anual
            total_annual_cost = (
                power_cost_annual + energy_cost_annual + fixed_cost_annual
            )

            # Agregar impuestos (21% IVA + 5.11% impuesto eléctrico)
            taxes_annual = total_annual_cost * 0.2611
            total_with_taxes = total_annual_cost + taxes_annual

            return {
                "annual_cost": round(total_with_taxes, 2),
                "monthly_cost": round(total_with_taxes / 12, 2),
                "power_cost": round(power_cost_annual, 2),
                "energy_cost": round(energy_cost_annual, 2),
                "fixed_cost": round(fixed_cost_annual, 2),
                "taxes": round(taxes_annual, 2),
                "peak_kwh_annual": round(peak_kwh, 2),
                "valley_kwh_annual": round(valley_kwh, 2),
            }

        except Exception as e:
            logger.error(f"❌ Error calculando costo anual: {str(e)}")
            return {"annual_cost": 0, "monthly_cost": 0, "error": str(e)}

    def get_personalized_recommendations(
        self,
        consumption_kwh: float,
        contracted_power_kw: float,
        user_location: str = "ES",
        current_monthly_cost: float = 0,
    ) -> Dict:
        """Obtiene recomendaciones personalizadas"""
        try:
            # 1. Obtener todas las tarifas del mercado
            all_tariffs = self.get_market_electricity_tariffs()

            if not all_tariffs:
                logger.warning("No se encontraron tarifas disponibles")
                return {"recommendations": []}

            # 2. Calcular costo para cada tarifa
            recommendations = []

            for tariff in all_tariffs:
                cost_analysis = self.calculate_annual_cost(
                    tariff, consumption_kwh, contracted_power_kw
                )

                if cost_analysis.get("error"):
                    continue

                # Calcular ahorro vs tarifa actual
                if current_monthly_cost > 0:
                    current_annual_cost = current_monthly_cost * 12
                    potential_savings = (
                        current_annual_cost - cost_analysis["annual_cost"]
                    )
                    savings_percentage = (potential_savings / current_annual_cost) * 100
                else:
                    potential_savings = 0
                    savings_percentage = 0

                recommendation = {
                    "provider_name": tariff["provider_name"],
                    "tariff_name": tariff["tariff_name"],
                    "tariff_id": tariff["tariff_id"],
                    "cost_analysis": cost_analysis,
                    "potential_savings": round(potential_savings, 2),
                    "savings_percentage": round(savings_percentage, 2),
                    "is_better_than_current": potential_savings > 0,
                    "tariff_type": tariff.get("tariff_type", "2.0TD"),
                    "has_time_discrimination": bool(tariff.get("kwh_price_peak")),
                }

                recommendations.append(recommendation)

            # 3. Ordenar por ahorro potencial
            recommendations.sort(key=lambda x: x["potential_savings"], reverse=True)

            # 4. Limitar a top 5
            top_recommendations = recommendations[:5]

            logger.info(f"✅ Generadas {len(top_recommendations)} recomendaciones")

            return {
                "recommendations": top_recommendations,
                "analysis_summary": {
                    "total_tariffs_analyzed": len(all_tariffs),
                    "user_consumption": consumption_kwh,
                    "user_power": contracted_power_kw,
                    "current_monthly_cost": current_monthly_cost,
                    "best_potential_savings": (
                        top_recommendations[0]["potential_savings"]
                        if top_recommendations
                        else 0
                    ),
                },
                "generated_at": now_spanish_iso(),
            }

        except Exception as e:
            logger.error(f"❌ Error generando recomendaciones: {str(e)}")
            return {
                "recommendations": [],
                "error": str(e),
                "generated_at": now_spanish_iso(),
            }
