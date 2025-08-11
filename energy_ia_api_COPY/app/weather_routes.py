# energy_ia_api_COPY/app/weather_routes.py
# 🌦️ RUTAS PARA CONSEJOS ENERGÉTICOS BASADOS EN EL CLIMA

import logging
from flask import Blueprint, jsonify, request
from utils.error_handlers import AppError
from smarwatt_auth import token_required
from .services.weather_service import WeatherService

logger = logging.getLogger(__name__)
weather_bp = Blueprint("weather_routes", __name__)

@weather_bp.route("/api/v1/energy/contextual-advice", methods=["GET"])
@token_required
def get_contextual_advice_route():
    """
    Proporciona consejos energéticos personalizados basados en el clima actual
    y el perfil de consumo del usuario.
    """
    try:
        user_id = request.args.get("user_id")
        if not user_id:
            raise AppError("El parámetro 'user_id' es requerido.", 400)

        weather_service = WeatherService()
        advice = weather_service.get_weather_based_advice(user_id)

        return jsonify({
            "status": "success",
            "user_id": user_id,
            "advice": advice
        }), 200

    except AppError as e:
        logger.error(f"❌ Error de aplicación al obtener consejo contextual: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), e.status_code
    except Exception as e:
        logger.error(f"❌ Error inesperado al obtener consejo contextual: {str(e)}")
        return jsonify({"status": "error", "message": "Error interno del servidor."}), 500
