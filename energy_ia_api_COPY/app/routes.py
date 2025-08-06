# energy_ia_api_COPY/app/routes.py
# 🏢 RECOMENDADOR DE TARIFAS EXTRA EMPRESARIAL NIVEL 2025

import os
import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from flask import Blueprint, jsonify, g, current_app, request, Response
import requests
from utils.timezone_utils import now_spanish_iso, now_spanish
from google.cloud import bigquery
from google.cloud import aiplatform
import pandas as pd
import numpy as np

from smarwatt_auth import token_required, admin_required
from utils.error_handlers import AppError
from app.services.vertex_ai_service import VertexAIService

# Configuración de logging empresarial
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_duplicate_tariff_robust(
    bq_client, table_id, supplier_name, tariff_name, tariff_type
):
    """
    🔒 VALIDACIÓN ANTIDUPLICADOS ULTRA ROBUSTA - EMPRESARIAL
    ========================================================

    Sistema que NUNCA falla, NUNCA para el backend, SIEMPRE es compatible.
    Si hay errores de conexión o BigQuery falla → Permite continuar con advertencia.
    Solo bloquea si hay duplicado CONFIRMADO.

    GARANTÍAS:
    - NUNCA rompe el backend
    - NUNCA para por errores de red
    - Compatible con datos parciales
    - Manejo graceful de todos los errores
    """
    try:
        # Normalizar datos de entrada (robusto contra None o espacios)
        supplier_clean = str(supplier_name or "").strip().upper()
        tariff_clean = str(tariff_name or "").strip().upper()
        type_clean = str(tariff_type or "").strip().upper()

        # Si faltan datos críticos → Permitir continuar (robusto)
        if not supplier_clean or not tariff_clean or not type_clean:
            logger.warning(
                f"⚠️ Datos incompletos para validación duplicados - CONTINUANDO"
            )
            return False  # No es duplicado, continuar

        # Query robusta con timeout y parámetros seguros
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
            # Timeout robusto - si tarda más, continuar
            job_timeout=10.0,  # 10 segundos máximo
        )

        # Ejecutar con manejo robusto de errores
        query_job = bq_client.query(query, job_config=job_config)
        results = list(query_job.result(timeout=15))  # 15s total timeout

        is_duplicate = results[0].count > 0 if results else False

        if is_duplicate:
            logger.warning(f"🔄 DUPLICADO DETECTADO: {supplier_clean} - {tariff_clean}")
        else:
            logger.debug(f"✅ Validación OK: {supplier_clean} - {tariff_clean}")

        return is_duplicate

    except Exception as e:
        # ERROR CRÍTICO: NUNCA parar el backend por validación duplicados
        error_msg = str(e)
        logger.error(f"❌ Error validación duplicados (CONTINUANDO): {error_msg}")

        # Si es error de red/timeout → Continuar sin bloquear
        if any(
            keyword in error_msg.lower()
            for keyword in ["timeout", "deadline", "connection", "network"]
        ):
            logger.warning(f"🌐 Error de red en validación - PERMITIENDO continuar")
            return False

        # Si es error de tabla no existe → Continuar (primera vez)
        if "not found" in error_msg.lower() or "does not exist" in error_msg.lower():
            logger.info(f"📋 Tabla nueva detectada - PERMITIENDO continuar")
            return False

        # Cualquier otro error → Continuar con advertencia (ROBUSTO)
        logger.warning(
            f"⚠️ Error desconocido en validación duplicados - CONTINUANDO por robustez"
        )
        return False  # Nunca parar el sistema


# Blueprint empresarial
energy_bp = Blueprint("energy_routes", __name__)


class EnterpriseTariffRecommenderService:
    """Servicio empresarial para recomendación de tarifas - El mejor del mercado"""

    def __init__(self):
        self.bq_client = bigquery.Client()
        self.project_id = current_app.config["GCP_PROJECT_ID"]
        self.dataset_id = current_app.config["BQ_DATASET_ID"]
        self.tariffs_table = current_app.config["BQ_MARKET_TARIFFS_TABLE_ID"]
        self.vertex_service = VertexAIService()

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
            FROM `{self.project_id}.{self.dataset_id}.market_electricity_tariffs`
            WHERE is_active = TRUE
            ORDER BY update_timestamp DESC
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
            raise AppError(f"Error accediendo a datos de tarifas: {str(e)}", 500)

    def calculate_annual_cost(self, tariff: Dict, consumption_profile: Dict) -> Dict:
        """Calcula el costo anual exacto para una tarifa específica"""
        try:
            # Extraer datos del perfil
            avg_kwh = consumption_profile.get("avg_kwh", 0)
            contracted_power_kw = consumption_profile.get("contracted_power_kw", 0)
            peak_percent = consumption_profile.get("peak_percent", 50) / 100

            # Calcular consumo anual
            annual_kwh = avg_kwh * 12
            peak_kwh = annual_kwh * peak_percent
            valley_kwh = annual_kwh * (1 - peak_percent)

            # Calcular término fijo anual
            fixed_term_annual = (
                (tariff.get("fixed_term_price") or 0) * contracted_power_kw
            ) * 12

            # Calcular término variable
            if tariff.get("discriminated_hourly", False):
                # Tarifa con discriminación horaria
                peak_cost = peak_kwh * (tariff.get("peak_price") or 0)
                valley_cost = valley_kwh * (tariff.get("valley_price") or 0)
                variable_term_annual = peak_cost + valley_cost
            else:
                # Tarifa sin discriminación horaria
                variable_term_annual = annual_kwh * (
                    tariff.get("variable_term_price") or 0
                )

            # Aplicar descuentos promocionales - Asegurar que total_cost nunca sea None
            total_cost = (fixed_term_annual or 0) + (variable_term_annual or 0)

            if tariff.get("promotion_discount_percentage", 0) > 0:
                promotion_months = tariff.get("promotion_duration_months", 12)
                # Protección contra división por None
                monthly_cost = (total_cost or 0) / 12
                discounted_months_cost = (
                    monthly_cost
                    * (1 - tariff.get("promotion_discount_percentage", 0) / 100)
                ) * promotion_months
                regular_months_cost = monthly_cost * (12 - promotion_months)
                total_cost = discounted_months_cost + regular_months_cost

            # Calcular ahorro vs tarifa actual (si existe)
            current_annual_cost = consumption_profile.get("current_annual_cost", 0)
            annual_savings = max(0, current_annual_cost - total_cost)
            savings_percentage = (
                (annual_savings / current_annual_cost * 100)
                if current_annual_cost > 0
                else 0
            )

            return {
                "annual_cost": round(total_cost or 0, 2),
                "monthly_cost": round((total_cost or 0) / 12, 2),
                "fixed_term_annual": round(fixed_term_annual or 0, 2),
                "variable_term_annual": round(variable_term_annual or 0, 2),
                "annual_savings": round(annual_savings, 2),
                "savings_percentage": round(savings_percentage, 2),
                "peak_kwh_annual": round(peak_kwh, 2),
                "valley_kwh_annual": round(valley_kwh, 2),
            }

        except Exception as e:
            logger.error(f"❌ Error calculando costo anual: {str(e)}")
            return {"annual_cost": 0, "monthly_cost": 0, "error": str(e)}

    def get_advanced_recommendation(self, consumption_profile: Dict) -> Dict:
        """Obtiene recomendación avanzada - mejor que cualquier página web"""
        try:
            # 1. Obtener todas las tarifas del mercado
            all_tariffs = self.get_market_electricity_tariffs()

            if not all_tariffs:
                raise AppError(
                    "No se encontraron tarifas disponibles en el mercado", 404
                )

            # 2. Calcular costo para cada tarifa
            tariff_analysis = []

            for tariff in all_tariffs:
                cost_analysis = self.calculate_annual_cost(tariff, consumption_profile)

                # Crear análisis completo
                analysis = {
                    "tariff_info": tariff,
                    "cost_analysis": cost_analysis,
                    "suitability_score": self._calculate_suitability_score(
                        tariff, consumption_profile
                    ),
                    "pros": self._get_tariff_pros(tariff, consumption_profile),
                    "cons": self._get_tariff_cons(tariff, consumption_profile),
                    "recommendation_reason": self._get_recommendation_reason(
                        tariff, consumption_profile, cost_analysis
                    ),
                }

                tariff_analysis.append(analysis)

            # 3. Ordenar por mejor opción (costo + conveniencia)
            sorted_tariffs = sorted(
                tariff_analysis,
                key=lambda x: (
                    x["cost_analysis"]["annual_cost"] * 0.7  # 70% peso en costo
                    + (100 - x["suitability_score"]) * 0.3  # 30% peso en conveniencia
                ),
            )

            # 4. Crear recomendación final
            best_tariff = sorted_tariffs[0]

            # 5. Usar ML para refinamiento adicional
            ml_prediction = self.vertex_service.get_tariff_recommendation(
                consumption_profile
            )

            recommendation = {
                "user_profile": consumption_profile,
                "best_recommendation": {
                    "tariff": best_tariff["tariff_info"],
                    "cost_analysis": best_tariff["cost_analysis"],
                    "suitability_score": best_tariff["suitability_score"],
                    "pros": best_tariff["pros"],
                    "cons": best_tariff["cons"],
                    "recommendation_reason": best_tariff["recommendation_reason"],
                },
                "top_3_alternatives": sorted_tariffs[1:4],
                "market_analysis": {
                    "total_tariffs_analyzed": len(all_tariffs),
                    "average_market_price": round(
                        np.mean(
                            [t["cost_analysis"]["annual_cost"] for t in tariff_analysis]
                        ),
                        2,
                    ),
                    "cheapest_option": min(
                        tariff_analysis, key=lambda x: x["cost_analysis"]["annual_cost"]
                    ),
                    "most_popular": max(
                        tariff_analysis,
                        key=lambda x: x["tariff_info"].get("customer_rating", 0),
                    ),
                },
                "ml_insights": ml_prediction,
                "generated_at": now_spanish_iso(),
                "expires_at": (now_spanish() + timedelta(hours=24)).isoformat(),
            }

            # 6. Registrar recomendación en BigQuery
            self._log_recommendation(consumption_profile["user_id"], recommendation)

            logger.info(
                f"✅ Recomendación generada para usuario {consumption_profile['user_id']}"
            )
            return recommendation

        except Exception as e:
            logger.error(f"❌ Error generando recomendación avanzada: {str(e)}")
            raise AppError(f"Error en motor de recomendaciones: {str(e)}", 500)

    def _calculate_suitability_score(self, tariff: Dict, profile: Dict) -> float:
        """Calcula puntuación de conveniencia (0-100)"""
        score = 50  # Base

        # Bonus por discriminación horaria si el usuario tiene patrón adecuado
        if (
            tariff.get("discriminated_hourly", False)
            and profile.get("peak_percent", 50) < 40
        ):
            score += 15

        # Bonus por energía verde
        if tariff.get("green_energy_percentage", 0) > 50:
            score += 10

        # Penalización por permanencia larga
        permanence = tariff.get("contract_permanence_months", 0)
        if permanence > 12:
            score -= 5
        elif permanence == 0:
            score += 5

        # Bonus por rating alto
        rating = tariff.get("customer_rating", 0)
        if rating > 4:
            score += 10
        elif rating < 3:
            score -= 10

        # Bonus por promociones
        if tariff.get("promotion_discount_percentage", 0) > 0:
            score += 8

        return min(100, max(0, score))

    def _get_tariff_pros(self, tariff: Dict, profile: Dict) -> List[str]:
        """Obtiene ventajas de la tarifa"""
        pros = []

        if tariff.get("green_energy_percentage", 0) > 50:
            pros.append(f"🌱 {tariff.get('green_energy_percentage', 0)}% energía verde")

        if tariff.get("contract_permanence_months", 0) == 0:
            pros.append("🔓 Sin permanencia")

        if tariff.get("customer_rating", 0) > 4:
            pros.append(
                f"⭐ Excelente valoración ({tariff.get('customer_rating', 0)}/5)"
            )

        if tariff.get("promotion_discount_percentage", 0) > 0:
            pros.append(
                f"💸 {tariff.get('promotion_discount_percentage', 0)}% descuento por {tariff.get('promotion_duration_months', 0)} meses"
            )

        if tariff.get("discriminated_hourly", False):
            pros.append("⏰ Tarifa con discriminación horaria")

        if tariff.get("additional_services"):
            pros.append(
                f"➕ Servicios adicionales: {tariff.get('additional_services', '')}"
            )

        return pros

    def _get_tariff_cons(self, tariff: Dict, profile: Dict) -> List[str]:
        """Obtiene desventajas de la tarifa"""
        cons = []

        permanence = tariff.get("contract_permanence_months", 0)
        if permanence > 12:
            cons.append(f"🔒 Permanencia de {permanence} meses")

        if tariff.get("cancellation_fee", 0) > 0:
            cons.append(
                f"💰 Penalización por cancelación: {tariff.get('cancellation_fee', 0)}€"
            )

        if tariff.get("customer_rating", 0) < 3:
            cons.append(f"⚠️ Valoración baja ({tariff.get('customer_rating', 0)}/5)")

        if tariff.get("indexing_type") == "variable":
            cons.append("📈 Precio variable (puede subir)")

        if (
            tariff.get("discriminated_hourly", False)
            and profile.get("peak_percent", 50) > 60
        ):
            cons.append("⚠️ Tarifa horaria no ventajosa para tu perfil")

        return cons

    def _get_recommendation_reason(
        self, tariff: Dict, profile: Dict, cost_analysis: Dict
    ) -> str:
        """Genera razón personalizada de la recomendación"""
        savings = cost_analysis.get("annual_savings", 0)

        if savings > 100:
            return f"Te ahorrarías {savings:.0f}€ al año ({cost_analysis.get('savings_percentage', 0):.1f}%) con esta tarifa."
        elif tariff.get("green_energy_percentage", 0) > 50:
            return f"Tarifa ecológica con {tariff.get('green_energy_percentage', 0)}% energía verde y precio competitivo."
        elif tariff.get("customer_rating", 0) > 4:
            return f"Excelente valoración de clientes ({tariff.get('customer_rating', 0)}/5) con precio justo."
        else:
            return (
                "Tarifa con la mejor relación calidad-precio para tu perfil de consumo."
            )

    def _log_recommendation(self, user_id: str, recommendation: Dict):
        """Registra la recomendación en BigQuery"""
        try:
            table_id = f"{self.project_id}.{self.dataset_id}.{current_app.config['BQ_RECOMMENDATION_LOG_TABLE_ID']}"
            table = self.bq_client.get_table(table_id)

            # Generar ID único para la recomendación
            recommendation_id = f"rec_{user_id}_{int(now_spanish().timestamp())}"
            current_timestamp = now_spanish()

            log_data = {
                "recommendation_id": recommendation_id,
                "user_id": user_id,
                "timestamp_utc": current_timestamp,
                "input_avg_kwh": recommendation.get("user_profile", {}).get(
                    "avg_kwh", 0
                ),
                "input_peak_percent": recommendation.get("user_profile", {}).get(
                    "peak_percent", 0
                ),
                "input_contracted_power_kw": recommendation.get("user_profile", {}).get(
                    "contracted_power_kw", 0
                ),
                "input_num_inhabitants": recommendation.get("user_profile", {}).get(
                    "num_inhabitants", 0
                ),
                "input_home_type": recommendation.get("user_profile", {}).get(
                    "home_type", ""
                ),
                "recommended_provider": recommendation["best_recommendation"]["tariff"][
                    "provider_name"
                ],
                "recommended_tariff_name": recommendation["best_recommendation"][
                    "tariff"
                ]["tariff_name"],
                "estimated_annual_saving": recommendation["best_recommendation"][
                    "cost_analysis"
                ].get("annual_savings", 0),
                "estimated_annual_cost": recommendation["best_recommendation"][
                    "cost_analysis"
                ]["annual_cost"],
                "reference_tariff_name": recommendation.get("current_tariff", {}).get(
                    "tariff_name", ""
                ),
                "reference_annual_cost": recommendation.get("current_tariff", {}).get(
                    "annual_cost", 0
                ),
                "consumption_kwh": recommendation.get("user_profile", {}).get(
                    "total_consumption_kwh", 0
                ),
                "timestamp": current_timestamp,
                "record_date": current_timestamp.date(),
                "total_savings": recommendation["best_recommendation"][
                    "cost_analysis"
                ].get("annual_savings", 0),
                "annual_cost": recommendation["best_recommendation"]["cost_analysis"][
                    "annual_cost"
                ],
            }

            self.bq_client.insert_rows_json(table, [log_data])
            logger.info(
                f"✅ Recomendación registrada en BigQuery para usuario {user_id}"
            )

        except Exception as e:
            logger.error(f"❌ Error registrando recomendación: {str(e)}")


# Instancia global del servicio
recommender_service = None


def get_recommender_service():
    """Obtiene instancia del servicio de recomendaciones"""
    global recommender_service
    if recommender_service is None:
        recommender_service = EnterpriseTariffRecommenderService()
    return recommender_service


# === ENDPOINTS EMPRESARIALES ===


@energy_bp.route("/tariffs/recommendations", methods=["GET"])
@token_required
def get_tariff_recommendations_route():
    """Endpoint principal - Recomendación de tarifas EXTRA empresarial"""
    try:
        user_id = g.user.get("uid")
        logger.info(f"🔍 Iniciando recomendación de tarifas para usuario {user_id}")

        # 1. Obtener perfil de consumo del usuario via HTTP call a expert_bot_api
        try:
            expert_bot_url = current_app.config.get("EXPERT_BOT_API_URL")
            if not expert_bot_url:
                logger.error("❌ EXPERT_BOT_API_URL no configurada en producción")
                return (
                    jsonify(
                        {"error": "Configuración de servicio Expert Bot no disponible"}
                    ),
                    500,
                )
            headers = {"Authorization": f"Bearer {g.token}"}

            response = requests.get(
                f"{expert_bot_url}/api/v1/energy/users/profile",
                headers=headers,
                timeout=15,
            )

            if response.status_code != 200:
                raise AppError(
                    f"Error obteniendo perfil de usuario: {response.status_code}",
                    response.status_code,
                )

            profile_response = response.json()
            consumption_data = profile_response.get("data")

            # Validar que tenemos datos mínimos
            if not consumption_data or not consumption_data.get("last_invoice_data"):
                raise AppError(
                    "No se encontró perfil de consumo detallado para el usuario. Por favor, sube una factura.",
                    404,
                )

            # Preparar datos para el motor de recomendaciones
            consumption_profile = {
                "user_id": user_id,
                "avg_kwh": consumption_data["last_invoice_data"].get(
                    "kwh_consumidos", 0
                ),
                "peak_percent": consumption_data["last_invoice_data"].get(
                    "peak_percent_from_invoice", 50
                ),
                "contracted_power_kw": consumption_data["last_invoice_data"].get(
                    "potencia_contratada_kw", 0
                ),
                "num_inhabitants": consumption_data.get("num_inhabitants", 2),
                "home_type": consumption_data.get("home_type", "apartment"),
                "current_annual_cost": consumption_data["last_invoice_data"].get(
                    "importe_total", 0
                )
                * 12,
                "current_supplier": consumption_data["last_invoice_data"].get(
                    "supplier_name", "Unknown"
                ),
                "usage_pattern": consumption_data.get("usage_pattern", "normal"),
            }

            # Validar datos críticos
            if not all(
                [
                    consumption_profile["avg_kwh"],
                    consumption_profile["contracted_power_kw"],
                ]
            ):
                raise AppError(
                    "Datos de consumo incompletos para generar recomendación", 400
                )

        except AppError as e:
            raise e
        except Exception as e:
            logger.error(f"❌ Error obteniendo perfil: {str(e)}")
            raise AppError(f"Error al obtener perfil de usuario: {str(e)}", 500)

        # 2. Obtener recomendación avanzada
        try:
            service = get_recommender_service()
            recommendation = service.get_advanced_recommendation(consumption_profile)

            logger.info(
                f"✅ Recomendación generada exitosamente para usuario {user_id}"
            )

            return (
                jsonify(
                    {
                        "status": "success",
                        "message": "Recomendación de tarifas generada exitosamente",
                        "data": recommendation,
                        "meta": {
                            "generated_at": now_spanish_iso(),
                            "service_version": "2025.1.0",
                            "enterprise_mode": True,
                        },
                    }
                ),
                200,
            )

        except Exception as e:
            logger.error(f"❌ Error en motor de recomendaciones: {str(e)}")
            raise AppError(f"Error generando recomendación: {str(e)}", 500)

    except AppError as e:
        logger.error(f"❌ Error en endpoint de recomendaciones: {str(e)}")
        return (
            jsonify(
                {"status": "error", "message": str(e), "error_code": e.status_code}
            ),
            e.status_code,
        )

    except Exception as e:
        logger.error(f"❌ Error inesperado: {str(e)}")
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Error interno del servidor",
                    "error_code": 500,
                }
            ),
            500,
        )


@energy_bp.route("/tariffs/market-data", methods=["GET"])
@token_required
def get_market_data():
    """Endpoint para obtener datos del mercado de tarifas"""
    try:
        service = get_recommender_service()
        tariffs = service.get_market_electricity_tariffs()

        # Estadísticas del mercado
        stats = {
            "total_tariffs": len(tariffs),
            "providers": len(set(t["provider_name"] for t in tariffs)),
            "with_peak_valley": len(
                [
                    t
                    for t in tariffs
                    if t.get("kwh_price_peak") and t.get("kwh_price_valley")
                ]
            ),
            "pvpc_tariffs": len([t for t in tariffs if t.get("is_pvpc", False)]),
            "active_tariffs": len([t for t in tariffs if t.get("is_active", False)]),
            "last_updated": max(
                t.get("update_timestamp", "")
                for t in tariffs
                if t.get("update_timestamp")
            ),
        }

        return (
            jsonify(
                {
                    "status": "success",
                    "data": {"tariffs": tariffs, "market_statistics": stats},
                }
            ),
            200,
        )

    except Exception as e:
        logger.error(f"❌ Error obteniendo datos del mercado: {str(e)}")
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"Error obteniendo datos del mercado: {str(e)}",
                }
            ),
            500,
        )


@energy_bp.route("/admin/tariffs/add", methods=["POST", "OPTIONS"])
@admin_required
def add_tariff_data():
    """Endpoint ADMIN para agregar datos de tarifas directamente"""
    # Manejar petición OPTIONS para CORS
    if request.method == "OPTIONS":
        response = Response()
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response, 200

    try:
        data = request.get_json()

        if not data:
            raise AppError("Datos de tarifa requeridos", 400)

        # Validar campos requeridos
        required_fields = [
            "supplier_name",
            "tariff_name",
            "tariff_type",
            "fixed_term_price",
            "variable_term_price",
        ]
        for field in required_fields:
            if field not in data:
                raise AppError(f"Campo requerido faltante: {field}", 400)

        # Preparar datos para inserción con CAMPOS EXACTOS de BigQuery
        tariff_data = {
            "provider_name": data.get("provider_name", data.get("supplier_name", "")),
            "tariff_name": data["tariff_name"],
            "tariff_type": data["tariff_type"],
            "tariff_id": data.get(
                "tariff_id",
                f"{data.get('provider_name', data.get('supplier_name', ''))}-{data['tariff_name']}-{int(now_spanish().timestamp())}",
            ),
            "fixed_monthly_fee": float(
                data.get("fixed_monthly_fee", data.get("fixed_term_price", 0))
            ),
            "kwh_price_flat": float(
                data.get("kwh_price_flat", data.get("variable_term_price", 0))
            ),
            "kwh_price_peak": float(
                data.get("kwh_price_peak", data.get("peak_price", 0))
            ),
            "kwh_price_valley": float(
                data.get("kwh_price_valley", data.get("valley_price", 0))
            ),
            "power_price_per_kw_per_month": float(
                data.get("power_price_per_kw_per_month", 0)
            ),
            "is_pvpc": data.get(
                "is_pvpc", data.get("tariff_type", "").lower() == "pvpc"
            ),
            "is_active": data.get("is_active", True),
            "update_timestamp": now_spanish(),
            "is_active": True,
            "created_by_admin": g.user.get("uid"),
            "data_source": "admin_panel",
        }

        # Insertar en BigQuery (misma tabla que el script)
        bq_client = bigquery.Client()
        project_id = current_app.config["GCP_PROJECT_ID"]
        dataset_id = current_app.config["BQ_DATASET_ID"]
        table_id = f"{project_id}.{dataset_id}.{current_app.config['BQ_MARKET_TARIFFS_TABLE_ID']}"

        # 🔒 VALIDACIÓN ANTIDUPLICADOS ROBUSTA (NO PARA EL SISTEMA JAMÁS)
        try:
            is_duplicate = check_duplicate_tariff_robust(
                bq_client,
                table_id,
                data.get("provider_name", data.get("supplier_name")),
                data.get("tariff_name"),
                data.get("tariff_type"),
            )

            if is_duplicate:
                # Duplicado confirmado → Retornar error 409 pero NO parar sistema
                logger.info(
                    f"🔄 Duplicado prevenido: {data.get('provider_name', data.get('supplier_name'))} - {data.get('tariff_name')}"
                )
                return (
                    jsonify(
                        {
                            "status": "duplicate_prevented",
                            "message": f"Tarifa ya existe: {data.get('provider_name', data.get('supplier_name'))} - {data.get('tariff_name')}",
                            "duplicate_data": {
                                "provider_name": data.get(
                                    "provider_name", data.get("supplier_name")
                                ),
                                "tariff_name": data.get("tariff_name"),
                                "tariff_type": data.get("tariff_type"),
                            },
                        }
                    ),
                    409,  # HTTP 409 Conflict
                )
        except Exception as validation_error:
            # Error en validación → CONTINUAR sin parar (MÁXIMA ROBUSTEZ)
            logger.error(
                f"❌ Fallo validación duplicados - CONTINUANDO: {str(validation_error)}"
            )

        table = bq_client.get_table(table_id)
        errors = bq_client.insert_rows_json(table, [tariff_data])

        if errors:
            raise AppError(f"Error insertando datos: {errors}", 500)

        logger.info(
            f"✅ Tarifa añadida por admin {g.user.get('uid')}: {data.get('provider_name', data.get('supplier_name'))} - {data['tariff_name']}"
        )

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Tarifa añadida exitosamente",
                    "data": {
                        "provider_name": data.get(
                            "provider_name", data.get("supplier_name")
                        ),
                        "tariff_name": data["tariff_name"],
                        "inserted_at": now_spanish_iso(),
                    },
                }
            ),
            201,
        )

    except AppError as e:
        return jsonify({"status": "error", "message": str(e)}), e.status_code

    except Exception as e:
        logger.error(f"❌ Error añadiendo tarifa: {str(e)}")
        return jsonify({"status": "error", "message": f"Error interno: {str(e)}"}), 500


@energy_bp.route("/admin/tariffs/batch-add", methods=["POST", "OPTIONS"])
@admin_required
def batch_add_tariffs():
    """Endpoint ADMIN para agregar múltiples tarifas en lote"""
    # Manejar petición OPTIONS para CORS
    if request.method == "OPTIONS":
        response = Response()
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response, 200

    try:
        data = request.get_json()

        if not data or "tariffs" not in data:
            raise AppError("Lista de tarifas requerida", 400)

        tariffs = data["tariffs"]
        if not isinstance(tariffs, list) or len(tariffs) == 0:
            raise AppError("Lista de tarifas debe contener al menos una tarifa", 400)

        # Procesar cada tarifa
        processed_tariffs = []
        errors = []

        for i, tariff in enumerate(tariffs):
            try:
                # Validar campos básicos
                if not all(
                    field in tariff
                    for field in ["supplier_name", "tariff_name", "tariff_type"]
                ) and not all(
                    field in tariff
                    for field in ["provider_name", "tariff_name", "tariff_type"]
                ):
                    errors.append(f"Tarifa {i+1}: Campos requeridos faltantes")
                    continue

                # Preparar datos con CAMPOS EXACTOS de BigQuery
                tariff_data = {
                    "provider_name": tariff.get(
                        "provider_name", tariff.get("supplier_name", "")
                    ),
                    "tariff_name": tariff["tariff_name"],
                    "tariff_type": tariff["tariff_type"],
                    "tariff_id": tariff.get(
                        "tariff_id",
                        f"{tariff.get('provider_name', tariff.get('supplier_name', ''))}-{tariff['tariff_name']}-{int(now_spanish().timestamp())}",
                    ),
                    "fixed_monthly_fee": float(
                        tariff.get(
                            "fixed_monthly_fee", tariff.get("fixed_term_price", 0)
                        )
                    ),
                    "kwh_price_flat": float(
                        tariff.get(
                            "kwh_price_flat", tariff.get("variable_term_price", 0)
                        )
                    ),
                    "kwh_price_peak": float(
                        tariff.get("kwh_price_peak", tariff.get("peak_price", 0))
                    ),
                    "kwh_price_valley": float(
                        tariff.get("kwh_price_valley", tariff.get("valley_price", 0))
                    ),
                    "power_price_per_kw_per_month": float(
                        tariff.get("power_price_per_kw_per_month", 0)
                    ),
                    "is_pvpc": tariff.get(
                        "is_pvpc", tariff.get("tariff_type", "").lower() == "pvpc"
                    ),
                    "update_timestamp": now_spanish(),
                    "is_active": True,
                }

                processed_tariffs.append(tariff_data)

            except Exception as e:
                errors.append(f"Tarifa {i+1}: {str(e)}")

        # Insertar en BigQuery si hay tarifas válidas
        if processed_tariffs:
            bq_client = bigquery.Client()
            project_id = current_app.config["GCP_PROJECT_ID"]
            dataset_id = current_app.config["BQ_DATASET_ID"]
            table_id = f"{project_id}.{dataset_id}.{current_app.config['BQ_MARKET_TARIFFS_TABLE_ID']}"

            # 🔒 VALIDACIÓN ANTIDUPLICADOS BATCH ROBUSTA
            validated_tariffs = []
            duplicate_count = 0
            validation_errors = 0

            for tariff in processed_tariffs:
                try:
                    is_duplicate = check_duplicate_tariff_robust(
                        bq_client,
                        table_id,
                        tariff.get("provider_name"),
                        tariff.get("tariff_name"),
                        tariff.get("tariff_type"),
                    )

                    if is_duplicate:
                        duplicate_count += 1
                        errors.append(
                            f"Duplicado: {tariff.get('provider_name')} - {tariff.get('tariff_name')}"
                        )
                    else:
                        validated_tariffs.append(tariff)

                except Exception as val_error:
                    # Error validación → CONTINUAR con la tarifa (ROBUSTO)
                    validation_errors += 1
                    logger.warning(
                        f"⚠️ Error validando tarifa (CONTINUANDO): {str(val_error)}"
                    )
                    validated_tariffs.append(tariff)  # Incluir por robustez

            # Insertar solo tarifas validadas (o todas si falla validación)
            final_tariffs = (
                validated_tariffs if validated_tariffs else processed_tariffs
            )

            table = bq_client.get_table(table_id)
            insert_errors = bq_client.insert_rows_json(table, final_tariffs)

            if insert_errors:
                errors.extend([f"Error BigQuery: {error}" for error in insert_errors])

            # Log estadísticas robustas
            logger.info(
                f"📊 Batch estadísticas - Procesadas: {len(final_tariffs)}, Duplicados: {duplicate_count}, Errores validación: {validation_errors}"
            )
        else:
            duplicate_count = 0

        logger.info(
            f"✅ Batch insert completado por admin {g.user.get('uid')}: {len(final_tariffs if 'final_tariffs' in locals() else processed_tariffs)} tarifas procesadas"
        )

        return (
            jsonify(
                {
                    "status": "success",
                    "message": f"Proceso completado: {len(final_tariffs if 'final_tariffs' in locals() else processed_tariffs)} tarifas insertadas",
                    "statistics": {
                        "total_processed": len(processed_tariffs),
                        "successfully_inserted": len(
                            final_tariffs
                            if "final_tariffs" in locals()
                            else processed_tariffs
                        ),
                        "duplicates_prevented": (
                            duplicate_count if "duplicate_count" in locals() else 0
                        ),
                        "validation_errors_handled": (
                            validation_errors if "validation_errors" in locals() else 0
                        ),
                    },
                    "data": {
                        "processed_count": len(processed_tariffs),
                        "error_count": len(errors),
                        "errors": errors if errors else None,
                    },
                }
            ),
            200,
        )

    except Exception as e:
        logger.error(f"❌ Error en batch insert: {str(e)}")
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"Error en procesamiento batch: {str(e)}",
                }
            ),
            500,
        )


@energy_bp.route("/tariffs/compare", methods=["POST", "OPTIONS"])
@token_required
def compare_tariffs():
    """Endpoint para comparar tarifas específicas"""
    # Manejar petición OPTIONS para CORS
    if request.method == "OPTIONS":
        response = Response()
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response, 200

    try:
        data = request.get_json()

        if not data or "tariff_ids" not in data:
            raise AppError("IDs de tarifas requeridos", 400)

        tariff_ids = data["tariff_ids"]
        if not isinstance(tariff_ids, list) or len(tariff_ids) < 2:
            raise AppError("Se requieren al menos 2 tarifas para comparar", 400)

        # Obtener perfil del usuario
        user_id = g.user.get("uid")

        # Obtener tarifas específicas
        service = get_recommender_service()
        all_tariffs = service.get_market_electricity_tariffs()

        # Filtrar tarifas solicitadas
        selected_tariffs = []
        for tariff in all_tariffs:
            if f"{tariff['provider_name']}-{tariff['tariff_name']}" in tariff_ids:
                selected_tariffs.append(tariff)

        if len(selected_tariffs) < 2:
            raise AppError("No se encontraron suficientes tarifas para comparar", 404)

        # Obtener perfil de consumo (simulado para comparación)
        consumption_profile = {
            "user_id": user_id,
            "avg_kwh": data.get("avg_kwh", 300),
            "peak_percent": data.get("peak_percent", 50),
            "contracted_power_kw": data.get("contracted_power_kw", 4.6),
            "current_annual_cost": data.get("current_annual_cost", 1200),
        }

        # Comparar tarifas
        comparison = []
        for tariff in selected_tariffs:
            cost_analysis = service.calculate_annual_cost(tariff, consumption_profile)
            comparison.append(
                {
                    "tariff": tariff,
                    "cost_analysis": cost_analysis,
                    "suitability_score": service._calculate_suitability_score(
                        tariff, consumption_profile
                    ),
                    "pros": service._get_tariff_pros(tariff, consumption_profile),
                    "cons": service._get_tariff_cons(tariff, consumption_profile),
                }
            )

        # Ordenar por mejor opción
        comparison.sort(key=lambda x: x["cost_analysis"]["annual_cost"])

        return (
            jsonify(
                {
                    "status": "success",
                    "data": {
                        "comparison": comparison,
                        "best_option": comparison[0],
                        "consumption_profile": consumption_profile,
                        "compared_at": now_spanish_iso(),
                    },
                }
            ),
            200,
        )

    except AppError as e:
        return jsonify({"status": "error", "message": str(e)}), e.status_code

    except Exception as e:
        logger.error(f"❌ Error en comparación: {str(e)}")
        return (
            jsonify(
                {"status": "error", "message": f"Error comparando tarifas: {str(e)}"}
            ),
            500,
        )
