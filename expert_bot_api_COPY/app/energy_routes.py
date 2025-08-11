"""
EXPERT BOT API - ENERGY ROUTES EMPRESARIAL COPY
===============================================

Rutas empresariales para el servicio de energía Expert Bot API.
"""
import logging
from flask import Blueprint, request, jsonify, g
from smarwatt_auth import token_required
from utils.error_handlers import AppError
from .services.energy_service import EnergyService
from .services.data_sync_service import DataSyncService
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger("expert_bot_api.energy_routes")
expert_energy_bp = Blueprint("expert_energy_routes", __name__)
executor = ThreadPoolExecutor(max_workers=2)

@expert_energy_bp.before_request
@token_required
def before_energy_request():
    """Middleware a nivel de blueprint para asegurar la autenticación."""
    pass

@expert_energy_bp.route("/consumption", methods=["POST"])
def upload_consumption_data():
    """Endpoint para subir facturas de consumo con sincronización y respuesta UX mejorada."""
    user_id = g.user["uid"]
    if "invoice_file" not in request.files or not request.files["invoice_file"].filename:
        raise AppError("No se ha proporcionado un archivo de factura.", 400)

    file = request.files["invoice_file"]
    
    try:
        data_sync_service = DataSyncService()
        executor.submit(data_sync_service.sync_user_profile_to_bigquery, user_id)
    except Exception as sync_e:
        logger.error(f"Error al iniciar la tarea de sincronización para {user_id}: {sync_e}")

    service = EnergyService()
    service.process_and_store_invoice(user_id, file)
    
    # Respuesta de éxito clara y consistente según el plan de mejora.
    return jsonify({
        "status": "success",
        "message": "Factura recibida. Te notificaremos cuando el análisis esté completo."
    }), 200

@expert_energy_bp.route("/manual-data", methods=["POST"])
def add_manual_energy_data():
    """Endpoint para entrada manual de datos con sincronización y respuesta UX mejorada."""
    user_id = g.user["uid"]
    data = request.get_json()
    if not data or not data.get("kwh_consumidos") or not data.get("potencia_contratada_kw"):
        raise AppError("Faltan campos requeridos: 'kwh_consumidos' y 'potencia_contratada_kw'.", 400)
    
    try:
        data_sync_service = DataSyncService()
        executor.submit(data_sync_service.sync_user_profile_to_bigquery, user_id)
    except Exception as sync_e:
        logger.error(f"Error al iniciar la tarea de sincronización para {user_id}: {sync_e}")

    service = EnergyService()
    service.process_manual_data(user_id, data)
    
    # Respuesta de éxito clara y consistente según el plan de mejora.
    return jsonify({
        "status": "success",
        "message": "Datos guardados correctamente. Ya puedes obtener tus recomendaciones."
    }), 200

@expert_energy_bp.route("/dashboard", methods=["GET"])
def get_dashboard_data():
    user_id = g.user["uid"]
    service = EnergyService()
    dashboard_data = service.get_dashboard_data(user_id)
    return jsonify(dashboard_data), 200

@expert_energy_bp.route("/users/profile", methods=["GET"])
def get_user_profile():
    user_id = g.user["uid"]
    service = EnergyService()
    profile_data = service.get_user_energy_profile_enterprise(user_id)
    return jsonify({"status": "success", "data": profile_data}), 200
