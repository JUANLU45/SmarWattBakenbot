# energy_ia_api_COPY/app/routes.py
# 🏢 CAPA DE RUTAS - LÓGICA DE NEGOCIO EXTERNALIZADA

import logging
from flask import Blueprint, jsonify, g, current_app, request, Response
import requests
from smarwatt_auth import token_required, admin_required
from utils.error_handlers import AppError
from utils.timezone_utils import now_spanish_iso
from app.services.tariff_recommender_service import EnterpriseTariffRecommenderService, check_duplicate_tariff_robust
from google.cloud import bigquery

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Blueprint empresarial
energy_bp = Blueprint("energy_routes", __name__)

# Instancia global del servicio para reutilización
recommender_service = None

def get_recommender_service():
    """Obtiene una instancia singleton del servicio de recomendaciones."""
    global recommender_service
    if recommender_service is None:
        recommender_service = EnterpriseTariffRecommenderService()
    return recommender_service

# === ENDPOINTS EMPRESARIALES ===

@energy_bp.route("/tariffs/recommendations", methods=["GET"])
@token_required
def get_tariff_recommendations_route():
    """Endpoint principal - Recomendación de tarifas extra empresarial."""
    try:
        user_id = g.user.get("uid")
        logger.info(f"🔍 Iniciando recomendación de tarifas para usuario {user_id}")

        # 1. Obtener perfil de consumo del usuario via HTTP call a expert_bot_api
        expert_bot_url = current_app.config.get("EXPERT_BOT_API_URL")
        if not expert_bot_url:
            raise AppError("Configuración de servicio Expert Bot no disponible", 500)
        
        headers = {"Authorization": f"Bearer {g.token}"}
        profile_url = f"{expert_bot_url}/users/profile"
        
        response = requests.get(profile_url, headers=headers, timeout=15)
        response.raise_for_status()
        
        consumption_data = response.json().get("data")
        if not consumption_data or not consumption_data.get("last_invoice_data"):
            raise AppError("No se encontró perfil de consumo para el usuario.", 404)

        consumption_profile = {
            "user_id": user_id,
            "avg_kwh": consumption_data["last_invoice_data"].get("kwh_consumidos", 0),
            "peak_percent": consumption_data["last_invoice_data"].get("peak_percent_from_invoice", 50),
            "contracted_power_kw": consumption_data["last_invoice_data"].get("potencia_contratada_kw", 0),
            "current_annual_cost": consumption_data["last_invoice_data"].get("importe_total", 0) * 12,
        }

        if not all([consumption_profile["avg_kwh"], consumption_profile["contracted_power_kw"]]):
            raise AppError("Datos de consumo incompletos para generar recomendación", 400)

        # 2. Obtener recomendación avanzada desde el servicio
        service = get_recommender_service()
        recommendation = service.get_advanced_recommendation(consumption_profile)
        
        logger.info(f"✅ Recomendación generada exitosamente para usuario {user_id}")
        return jsonify({
            "status": "success",
            "message": "Recomendación de tarifas generada exitosamente",
            "data": recommendation,
        }), 200

    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Error obteniendo perfil de expert_bot_api: {str(e)}")
        raise AppError(f"Error de comunicación interna para obtener el perfil: {str(e)}", 503)
    except AppError as e:
        logger.error(f"❌ Error de aplicación en endpoint de recomendaciones: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), e.status_code
    except Exception as e:
        logger.error(f"❌ Error inesperado en recomendaciones: {str(e)}")
        return jsonify({"status": "error", "message": "Error interno del servidor"}), 500

@energy_bp.route("/tariffs/market-data", methods=["GET"])
@token_required
def get_market_data():
    """Endpoint para obtener datos del mercado de tarifas."""
    try:
        service = get_recommender_service()
        tariffs = service.get_market_electricity_tariffs()
        # Aquí se podría añadir lógica para estadísticas si se desea
        return jsonify({"status": "success", "data": {"tariffs": tariffs}}), 200
    except Exception as e:
        logger.error(f"❌ Error obteniendo datos del mercado: {str(e)}")
        return jsonify({"status": "error", "message": f"Error obteniendo datos del mercado: {str(e)}"}), 500

@energy_bp.route("/admin/tariffs/add", methods=["POST"])
@admin_required
def add_tariff_data():
    """Endpoint ADMIN para agregar datos de tarifas directamente."""
    try:
        data = request.get_json()
        if not data:
            raise AppError("Datos de tarifa requeridos", 400)

        # Delegar la lógica de añadir tarifa al servicio
        service = get_recommender_service()
        result = service.add_tariff(data, g.user.get("uid"))

        return jsonify({"status": "success", "message": "Tarifa añadida exitosamente", "data": result}), 201
    except AppError as e:
        return jsonify({"status": "error", "message": str(e)}), e.status_code
    except Exception as e:
        logger.error(f"❌ Error añadiendo tarifa: {str(e)}")
        return jsonify({"status": "error", "message": f"Error interno: {str(e)}"}), 500

@energy_bp.route("/admin/tariffs/batch-add", methods=["POST"])
@admin_required
def batch_add_tariffs():
    """Endpoint ADMIN para agregar múltiples tarifas en lote."""
    try:
        data = request.get_json()
        if not data or "tariffs" not in data:
            raise AppError("Lista de tarifas ('tariffs') requerida", 400)

        # Delegar la lógica de añadir tarifas en lote al servicio
        service = get_recommender_service()
        result = service.batch_add_tariffs(data["tariffs"], g.user.get("uid"))
        
        return jsonify({"status": "success", "message": "Proceso de lote completado.", "data": result}), 200
    except AppError as e:
        return jsonify({"status": "error", "message": str(e)}), e.status_code
    except Exception as e:
        logger.error(f"❌ Error en batch insert: {str(e)}")
        return jsonify({"status": "error", "message": f"Error en procesamiento batch: {str(e)}"}), 500

@energy_bp.route("/tariffs/compare", methods=["POST"])
@token_required
def compare_tariffs_route():
    """Endpoint para comparar tarifas específicas."""
    try:
        data = request.get_json()
        if not data or "tariff_ids" not in data:
            raise AppError("Se requiere una lista de 'tariff_ids'", 400)
        
        # Simulación de perfil de consumo para la comparación
        consumption_profile = {
            "user_id": g.user.get("uid"),
            "avg_kwh": data.get("avg_kwh", 300), # Default si no se provee
            "peak_percent": data.get("peak_percent", 50),
            "contracted_power_kw": data.get("contracted_power_kw", 4.6),
        }

        service = get_recommender_service()
        comparison = service.compare_tariffs(data["tariff_ids"], consumption_profile)
        
        return jsonify({"status": "success", "data": comparison}), 200
    except AppError as e:
        return jsonify({"status": "error", "message": str(e)}), e.status_code
    except Exception as e:
        logger.error(f"❌ Error en comparación de tarifas: {str(e)}")
        return jsonify({"status": "error", "message": f"Error comparando tarifas: {str(e)}"}), 500
