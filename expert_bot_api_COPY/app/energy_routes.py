"""
EXPERT BOT API - ENERGY ROUTES EMPRESARIAL COPY
===============================================

Rutas empresariales para el servicio de energía Expert Bot API.
"""
import logging
from flask import Blueprint, request, jsonify, g, current_app
from smarwatt_auth import token_required
from utils.error_handlers import AppError
from .services.energy_service import EnergyService
from .services.ai_learning_service import AILearningService
from .services.data_sync_service import DataSyncService
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger("expert_bot_api.energy_routes")
expert_energy_bp = Blueprint("expert_energy_routes", __name__)
executor = ThreadPoolExecutor(max_workers=2)

@expert_energy_bp.before_request
def log_energy_route_access():
    if hasattr(g, "user"):
        logger.info(f"Usuario {g.user.get('uid', 'unknown')} accediendo a: {request.endpoint}")

@expert_energy_bp.route("/consumption", methods=["POST"])
@token_required
def upload_consumption_data():
    """Endpoint para subir facturas de consumo con sincronización de datos."""
    user_id = g.user["uid"]
    if "invoice_file" not in request.files or not request.files["invoice_file"].filename:
        raise AppError("No se ha proporcionado un archivo de factura.", 400)

    file = request.files["invoice_file"]
    
    try:
        # 🚀 SINCRONIZACIÓN ASÍNCRONA 🚀
        data_sync_service = DataSyncService()
        executor.submit(data_sync_service.sync_user_profile_to_bigquery, user_id)
        logger.info(f"Tarea de sincronización iniciada tras subida de factura para {user_id}.")
    except Exception as sync_e:
        logger.error(f"Error al iniciar la tarea de sincronización para {user_id}: {sync_e}")

    service = EnergyService()
    result = service.process_and_store_invoice(user_id, file)
    
    # Aquí puedes añadir la lógica de AILearningService si es necesario
    # ai_learning = AILearningService()
    # ai_learning.process_invoice_upload_patterns(user_id, file.filename, result)
    
    return jsonify(result), 200

@expert_energy_bp.route("/manual-data", methods=["POST"])
@token_required
def add_manual_energy_data():
    """Endpoint para entrada manual de datos con sincronización."""
    user_id = g.user["uid"]
    data = request.get_json()
    if not data or not data.get("kwh_consumidos") or not data.get("potencia_contratada_kw"):
        raise AppError("Faltan campos requeridos: 'kwh_consumidos' y 'potencia_contratada_kw'.", 400)
    
    try:
        # 🚀 SINCRONIZACIÓN ASÍNCRONA 🚀
        data_sync_service = DataSyncService()
        executor.submit(data_sync_service.sync_user_profile_to_bigquery, user_id)
        logger.info(f"Tarea de sincronización iniciada tras entrada manual para {user_id}.")
    except Exception as sync_e:
        logger.error(f"Error al iniciar la tarea de sincronización para {user_id}: {sync_e}")

    service = EnergyService()
    # Asumimos que existe un método para manejar los datos manuales
    result = service.process_manual_data(user_id, data)
    
    return jsonify(result), 200

# ... (El resto de los endpoints permanecen, pero la lógica de sincronización ya no es necesaria aquí)
# ... (dashboard, profile, etc.)
@expert_energy_bp.route("/dashboard", methods=["GET"])
@token_required
def get_dashboard_data():
    user_id = g.user["uid"]
    service = EnergyService()
    dashboard_data = service.get_dashboard_data(user_id)
    return jsonify(dashboard_data), 200

@expert_energy_bp.route("/users/profile", methods=["GET"])
@token_required
def get_user_profile():
    user_id = g.user["uid"]
    service = EnergyService()
    profile_data = service.get_user_energy_profile_enterprise(user_id)
    return jsonify({"status": "success", "data": profile_data}), 200
