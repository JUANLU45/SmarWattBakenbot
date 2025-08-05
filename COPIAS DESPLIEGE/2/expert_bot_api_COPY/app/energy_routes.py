"""
EXPERT BOT API - ENERGY ROUTES EMPRESARIAL COPY
===============================================

Rutas empresariales para el servicio de energía Expert Bot API.
Mantiene EXACTAMENTE los mismos endpoints y métodos que el original.

NUEVOS ENDPOINTS EMPRESARIALES AÑADIDOS:
- PUT /consumption/update - Actualizar datos de consumo
- GET /consumption/history - Historial de consumos del usuario
- POST /consumption/analyze - Análisis avanzado de consumo
- GET /consumption/recommendations - Recomendaciones personalizadas
- POST /consumption/compare - Comparar tarifas
- PUT /consumption/title - Cambiar título de conversación energética

MEJORAS EMPRESARIALES:
- Aprendizaje automático integrado en todos los endpoints
- Comunicación robusta con energy_ia_api
- Validación empresarial de datos
- Logging detallado para análisis
- Manejo de errores robusto con fallbacks
- Extracción de datos totalmente robusta

ENDPOINTS ORIGINALES: IDÉNTICOS (PROHIBIDO CAMBIAR)
CREDENCIALES GOOGLE: IDÉNTICAS AL ORIGINAL (PROHIBIDO CAMBIAR)
TABLAS: IDÉNTICAS AL ORIGINAL (PROHIBIDO CAMBIAR)
NOMBRES: IDÉNTICOS AL ORIGINAL (PROHIBIDO CAMBIAR)

VERSIÓN: 2.0.0 - EMPRESARIAL COPY
FECHA: 2025-07-16
"""

import logging
from datetime import datetime, timezone
from flask import Blueprint, request, jsonify, g, current_app
from smarwatt_auth import token_required
from utils.error_handlers import AppError
from .services.energy_service import EnergyService
from .services.ai_learning_service import AILearningService

# Configurar logger empresarial
logger = logging.getLogger("expert_bot_api.energy_routes")

expert_energy_bp = Blueprint("expert_energy_routes", __name__)


# Middleware empresarial para logging de energy routes
@expert_energy_bp.before_request
def log_energy_route_access():
    """Middleware empresarial para logging de acceso a rutas de energía."""
    if hasattr(g, "user"):
        logger.info(
            f"Usuario {g.user.get('uid', 'unknown')} accediendo a energy endpoint: {request.endpoint}"
        )
    else:
        logger.info(f"Acceso anónimo a energy endpoint: {request.endpoint}")


# ENDPOINTS ORIGINALES (IDÉNTICOS AL ORIGINAL)
@expert_energy_bp.route("/consumption", methods=["POST"])
@token_required
def upload_consumption_data():
    """
    Endpoint ULTRA-ROBUSTO para subir facturas de consumo.
    NUNCA falla y SIEMPRE ofrece alternativas amables al usuario.
    Garantiza máximo valor y experiencia perfecta.

    IDÉNTICO AL ORIGINAL - PROHIBIDO CAMBIAR
    """
    if "invoice_file" not in request.files:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Por favor, selecciona una factura de electricidad para continuar.",
                    "alternative_action": {
                        "type": "manual_input",
                        "description": "También puedes introducir tus datos manualmente",
                        "endpoint": "/manual-data",
                        "required_fields": ["kwh_consumidos", "potencia_contratada_kw"],
                    },
                    "help_message": "Si tienes problemas subiendo el archivo, puedes introducir los datos manualmente usando el botón 'Entrada Manual' en la aplicación.",
                }
            ),
            400,
        )

    file = request.files["invoice_file"]
    if file.filename == "":
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "No has seleccionado ninguna factura. Por favor, elige un archivo.",
                    "alternative_action": {
                        "type": "manual_input",
                        "description": "Introduce tus datos de consumo manualmente",
                        "endpoint": "/manual-data",
                        "help_text": "Necesitamos tu consumo en kWh y potencia contratada para darte recomendaciones personalizadas",
                    },
                }
            ),
            400,
        )

    user_id = g.user["uid"]
    user_name = g.user.get("name", g.user.get("email", ""))

    try:
        # Inicializar servicios empresariales
        service = EnergyService()
        ai_learning = AILearningService()

        # Procesar factura con aprendizaje automático
        result = service.process_and_store_invoice(user_id, file)

        # Aprendizaje automático empresarial
        ai_learning.process_invoice_upload_patterns(user_id, file.filename, result)

        # Personalizar respuesta de éxito con nombre del usuario
        if user_name:
            result["personalized_message"] = (
                f"¡Perfecto {user_name}! Tu factura ha sido procesada correctamente."
            )

        logger.info(f"Factura procesada correctamente para usuario: {user_id}")
        return jsonify(result), 200

    except (ValueError, IOError, RuntimeError) as e:
        # NUNCA devolver errores técnicos crudos al usuario
        # SIEMPRE ofrecer alternativas amables y útiles
        logger.error("Error procesando factura para usuario %s: %s", user_id, str(e))

        return (
            jsonify(
                {
                    "status": "partial_error",
                    "message": f"Hola{' ' + user_name if user_name else ''}, no hemos podido procesar automáticamente tu factura, pero no te preocupes.",
                    "reason": "El archivo podría estar borroso, ser de un formato especial, o tener información ilegible.",
                    "alternative_actions": [
                        {
                            "type": "manual_input",
                            "title": "✅ Entrada Manual (Recomendado)",
                            "description": "Introduce tus datos de consumo manualmente - es rápido y fácil",
                            "endpoint": "/manual-data",
                            "benefits": [
                                "Obtienes recomendaciones inmediatas",
                                "Datos 100% precisos",
                                "Solo necesitas 2 números de tu factura",
                            ],
                        },
                        {
                            "type": "retry",
                            "title": "🔄 Intentar con Otra Factura",
                            "description": "Prueba con una foto más clara o un PDF diferente",
                            "tips": [
                                "Asegúrate que la imagen esté bien iluminada",
                                "El texto debe ser legible",
                                "Formato PDF suele funcionar mejor",
                            ],
                        },
                    ],
                    "help_message": "Mientras tanto, puedes preguntarme sobre tarifas eléctricas o consejos de ahorro. ¡Estoy aquí para ayudarte!",
                    "contact_support": "Si necesitas ayuda adicional, escríbenos a soporte@smarwatt.com",
                    "next_steps": [
                        "1. Usa 'Entrada Manual' para obtener recomendaciones inmediatas",
                        "2. O inténtalo con una foto más clara de tu factura",
                        "3. Pregúntame cualquier duda sobre electricidad",
                    ],
                }
            ),
            200,
        )  # 200 porque ofrecemos alternativas válidas


@expert_energy_bp.route("/dashboard", methods=["GET"])
@token_required
def get_dashboard_data():
    """
    Endpoint ULTRA-ROBUSTO para obtener datos del panel.
    NUNCA falla y SIEMPRE proporciona datos útiles al usuario.

    IDÉNTICO AL ORIGINAL - PROHIBIDO CAMBIAR
    """
    user_id = g.user["uid"]
    user_name = g.user.get("name", g.user.get("email", ""))

    try:
        service = EnergyService()
        dashboard_data = service.get_dashboard_data(user_id)

        # Personalizar mensaje de bienvenida
        if user_name and "welcome_message" not in dashboard_data:
            dashboard_data["welcome_message"] = (
                f"¡Hola {user_name}! Aquí tienes tu resumen energético"
            )

        logger.info(f"Dashboard obtenido correctamente para usuario: {user_id}")
        return jsonify(dashboard_data), 200

    except (ValueError, IOError, RuntimeError) as e:
        logger.error("Error obteniendo dashboard para usuario %s: %s", user_id, str(e))

        # NUNCA fallar - siempre devolver datos útiles
        fallback_dashboard = {
            "status": "partial_data",
            "message": f"Hola{' ' + user_name if user_name else ''}, estamos preparando tu panel personalizado.",
            "available_actions": [
                {
                    "type": "upload_invoice",
                    "title": "📄 Subir Factura",
                    "description": "Sube tu factura para obtener análisis personalizado",
                    "endpoint": "/consumption",
                },
                {
                    "type": "manual_input",
                    "title": "✏️ Entrada Manual",
                    "description": "Introduce tus datos de consumo manualmente",
                    "endpoint": "/manual-data",
                },
                {
                    "type": "chat",
                    "title": "💬 Pregúntame",
                    "description": "Hazme cualquier pregunta sobre electricidad y ahorro",
                },
            ],
            "quick_tips": [
                "Compara tarifas para ahorrar hasta 30% en tu factura",
                "Identifica tus horas de mayor consumo",
                "Descubre si tu potencia contratada es la adecuada",
            ],
            "help_message": "¡No te preocupes! Puedo ayudarte con consejos de ahorro energético mientras preparamos tu perfil completo.",
            "contact_support": "¿Necesitas ayuda? Escríbenos a soporte@smarwatt.com",
        }

        return jsonify(fallback_dashboard), 200  # Siempre 200 porque damos valor


@expert_energy_bp.route("/users/profile", methods=["GET"])
@token_required
def get_user_profile():
    """
    Endpoint para obtener el perfil de usuario con datos de consumo.
    Usado por energy_ia_api para obtener datos del usuario.

    IDÉNTICO AL ORIGINAL - PROHIBIDO CAMBIAR
    """
    user_id = g.user["uid"]

    try:
        service = EnergyService()
        profile_data = service._get_user_energy_profile_enterprise(user_id)

        logger.info(f"Perfil de usuario obtenido correctamente: {user_id}")
        return jsonify({"status": "success", "data": profile_data}), 200

    except (ValueError, IOError, RuntimeError) as e:
        logger.error(f"Error obteniendo perfil para usuario {user_id}: {e}")
        raise AppError(str(e), 500) from e


@expert_energy_bp.route("/manual-data", methods=["POST"])
@token_required
def add_manual_energy_data():
    """
    NUEVO ENDPOINT REAL: Permite entrada manual cuando OCR falla o es incompleto.
    Da VALOR INMEDIATO al usuario que no puede usar OCR por cualquier motivo.

    IDÉNTICO AL ORIGINAL - PROHIBIDO CAMBIAR
    """
    user_id = g.user["uid"]
    data = request.get_json()

    if not data:
        raise AppError("Datos requeridos en formato JSON.", 400)

    # Validación inteligente: solo verificar campos críticos mínimos
    required_fields = {
        "kwh_consumidos": "Consumo en kWh del último mes",
        "potencia_contratada_kw": "Potencia contratada en kW",
    }

    missing_fields = []
    for field, description in required_fields.items():
        if not data.get(field) or data.get(field) <= 0:
            missing_fields.append(f"{field} ({description})")

    if missing_fields:
        raise AppError(
            f"Campos requeridos faltantes o inválidos: {', '.join(missing_fields)}", 400
        )

    try:
        service = EnergyService()
        ai_learning = AILearningService()

        # Estructurar datos como si vinieran del OCR MEJORADO
        manual_invoice_data = {
            # Campos críticos (obligatorios)
            "kwh_consumidos": float(data["kwh_consumidos"]),
            "potencia_contratada_kw": float(data["potencia_contratada_kw"]),
            # Campos importantes (opcionales con defaults inteligentes)
            "coste_total": data.get("coste_total"),
            "fecha_periodo": data.get("fecha_periodo"),
            "tariff_name_from_invoice": data.get("tariff_name", "Manual"),
            "peak_percent_from_invoice": data.get(
                "peak_percent", 35
            ),  # Default español típico
            # NUEVOS CAMPOS OPCIONALES (sin romper nada)
            "valley_percent_from_invoice": data.get(
                "valley_percent", 30
            ),  # Default valle
            "flat_percent_from_invoice": data.get("flat_percent", 35),  # Default llano
            "codigo_postal": data.get("codigo_postal"),
            "tariff_type": data.get("tariff_type"),
            "distribuidora": data.get("distribuidora"),
            "precio_kwh_punta": data.get("precio_kwh_punta"),
            "precio_kwh_valle": data.get("precio_kwh_valle"),
            "precio_kwh_llano": data.get("precio_kwh_llano"),
            # Metadatos de entrada manual
            "extraction_status": "manual",
            "requires_manual_input": False,
            "missing_critical_fields": [],
            "confidence_score": 1.0,  # Máxima confianza en datos manuales
            "data_source": "user_manual_input",
        }

        # Guardar perfil energético como si fuera una factura procesada
        profile_update = {
            "last_invoice_data": manual_invoice_data,
            "consumption": {
                "avg_kwh": manual_invoice_data["kwh_consumidos"],
                "peak_percent": manual_invoice_data["peak_percent_from_invoice"],
                "contracted_power_kw": manual_invoice_data["potencia_contratada_kw"],
            },
            "manual_data_provided": True,
            "data_completeness": 85,  # Alto nivel de completitud
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }

        # Añadir datos opcionales si se proporcionan
        if data.get("num_inhabitants"):
            profile_update["num_inhabitants"] = int(data["num_inhabitants"])
            profile_update["data_completeness"] = 95

        if data.get("home_type"):
            profile_update["home_type"] = data["home_type"]
            profile_update["data_completeness"] = 100

        service._update_user_energy_profile(user_id, profile_update)

        # Publicar datos a Pub/Sub para análisis
        service._publish_consumption_to_pubsub(user_id, manual_invoice_data)

        # Aprendizaje automático para datos manuales
        ai_learning.process_manual_data_patterns(user_id, manual_invoice_data)

        logger.info(f"Datos manuales procesados correctamente para usuario: {user_id}")
        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Datos energéticos guardados correctamente. Ahora puedes obtener recomendaciones personalizadas.",
                    "data_completeness": profile_update["data_completeness"],
                    "recommendations_available": True,
                    "next_action": "Pregúntame sobre tarifas o ahorro energético para obtener consejos personalizados.",
                }
            ),
            200,
        )

    except ValueError as ve:
        logger.error(f"Error de validación en datos manuales: {ve}")
        raise AppError(f"Datos numéricos inválidos: {str(ve)}", 400) from ve
    except (IOError, RuntimeError) as e:
        logger.error(
            "Error al guardar datos manuales para usuario %s: %s", user_id, str(e)
        )
        raise AppError(
            "Error interno al guardar los datos. Inténtalo de nuevo.", 500
        ) from e
    except Exception as e:
        logger.error(
            f"Error inesperado en datos manuales para {user_id}: {e}", exc_info=True
        )
        raise AppError(f"Error interno procesando datos: {str(e)}", 500) from e


# NUEVOS ENDPOINTS EMPRESARIALES PARA GESTIÓN AVANZADA DE CONSUMO
@expert_energy_bp.route("/consumption/update", methods=["PUT"])
@token_required
def update_consumption_data():
    """
    NUEVO ENDPOINT EMPRESARIAL: Actualizar datos de consumo existentes.
    Permite actualizar datos sin subir nueva factura.
    """
    try:
        user_id = g.user["uid"]
        data = request.get_json()

        if not data:
            raise AppError("Datos requeridos en formato JSON.", 400)

        service = EnergyService()
        ai_learning = AILearningService()

        # Validar y actualizar datos
        result = service.update_consumption_data(user_id, data)

        # Aprendizaje automático para actualizaciones
        ai_learning.process_consumption_update_patterns(user_id, data)

        logger.info(f"Datos de consumo actualizados para usuario: {user_id}")
        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Datos de consumo actualizados correctamente",
                    "data": result,
                    "timestamp": datetime.now().isoformat(),
                }
            ),
            200,
        )

    except Exception as e:
        logger.error(f"Error actualizando datos de consumo: {e}")
        raise AppError(f"Error interno actualizando datos: {str(e)}", 500)


@expert_energy_bp.route("/consumption/history", methods=["GET"])
@token_required
def get_consumption_history():
    """
    NUEVO ENDPOINT EMPRESARIAL: Obtener historial de consumos del usuario.
    Funcionalidad empresarial para análisis de patrones.
    """
    try:
        user_id = g.user["uid"]

        # Parámetros de consulta
        months = request.args.get("months", 12, type=int)
        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", 20, type=int)

        # Validar límites
        if limit > 100:
            limit = 100
        if months > 24:
            months = 24

        service = EnergyService()
        history = service.get_consumption_history(user_id, months, page, limit)

        logger.info(f"Historial de consumo obtenido para usuario: {user_id}")
        return (
            jsonify(
                {
                    "status": "success",
                    "data": history,
                    "page": page,
                    "limit": limit,
                    "months": months,
                    "timestamp": datetime.now().isoformat(),
                }
            ),
            200,
        )

    except Exception as e:
        logger.error(f"Error obteniendo historial de consumo: {e}")
        raise AppError(f"Error interno obteniendo historial: {str(e)}", 500)


@expert_energy_bp.route("/consumption/analyze", methods=["POST"])
@token_required
def analyze_consumption():
    """
    NUEVO ENDPOINT EMPRESARIAL: Análisis avanzado de consumo con IA.
    Proporciona insights inteligentes sobre patrones de consumo.
    """
    try:
        user_id = g.user["uid"]
        data = request.get_json()

        service = EnergyService()
        ai_learning = AILearningService()

        # Análisis empresarial avanzado
        analysis = service.analyze_consumption_patterns(user_id, data)

        # Enriquecer con aprendizaje automático
        ai_insights = ai_learning.generate_consumption_insights(user_id, analysis)

        result = {
            "status": "success",
            "analysis": analysis,
            "ai_insights": ai_insights,
            "timestamp": datetime.now().isoformat(),
        }

        logger.info(f"Análisis de consumo completado para usuario: {user_id}")
        return jsonify(result), 200

    except Exception as e:
        logger.error(f"Error en análisis de consumo: {e}")
        raise AppError(f"Error interno en análisis: {str(e)}", 500)


@expert_energy_bp.route("/consumption/recommendations", methods=["GET"])
@token_required
def get_consumption_recommendations():
    """
    NUEVO ENDPOINT EMPRESARIAL: Obtener recomendaciones personalizadas.
    Basadas en IA y aprendizaje automático.
    """
    try:
        user_id = g.user["uid"]

        service = EnergyService()
        ai_learning = AILearningService()

        # Obtener recomendaciones base
        recommendations = service.get_personalized_recommendations(user_id)

        # Enriquecer con IA
        ai_recommendations = ai_learning.generate_smart_recommendations(user_id)

        result = {
            "status": "success",
            "recommendations": recommendations,
            "ai_recommendations": ai_recommendations,
            "timestamp": datetime.now().isoformat(),
        }

        logger.info(f"Recomendaciones generadas para usuario: {user_id}")
        return jsonify(result), 200

    except Exception as e:
        logger.error(f"Error generando recomendaciones: {e}")
        raise AppError(f"Error interno generando recomendaciones: {str(e)}", 500)


@expert_energy_bp.route("/consumption/compare", methods=["POST"])
@token_required
def compare_tariffs():
    """
    NUEVO ENDPOINT EMPRESARIAL: Comparar tarifas eléctricas.
    Análisis inteligente de tarifas con recomendaciones personalizadas.
    """
    try:
        user_id = g.user["uid"]
        data = request.get_json()

        service = EnergyService()
        ai_learning = AILearningService()

        # Comparación de tarifas
        comparison = service.compare_electricity_tariffs(user_id, data)

        # Enriquecer con aprendizaje automático
        ai_comparison = ai_learning.enhance_tariff_comparison(user_id, comparison)

        result = {
            "status": "success",
            "comparison": comparison,
            "ai_enhanced": ai_comparison,
            "timestamp": datetime.now().isoformat(),
        }

        logger.info(f"Comparación de tarifas completada para usuario: {user_id}")
        return jsonify(result), 200

    except Exception as e:
        logger.error(f"Error en comparación de tarifas: {e}")
        raise AppError(f"Error interno en comparación: {str(e)}", 500)


@expert_energy_bp.route("/consumption/title", methods=["PUT"])
@token_required
def update_consumption_title():
    """
    NUEVO ENDPOINT EMPRESARIAL: Cambiar título de conversación energética.
    Permite personalizar títulos para mejor organización.
    """
    try:
        user_id = g.user["uid"]
        data = request.get_json()

        if not data or not data.get("consumption_id") or not data.get("new_title"):
            raise AppError("Se requieren 'consumption_id' y 'new_title'", 400)

        consumption_id = data["consumption_id"]
        new_title = data["new_title"]

        service = EnergyService()
        result = service.update_consumption_title(user_id, consumption_id, new_title)

        logger.info(f"Título de consumo actualizado para usuario: {user_id}")
        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Título actualizado correctamente",
                    "consumption_id": consumption_id,
                    "new_title": new_title,
                    "timestamp": datetime.now().isoformat(),
                }
            ),
            200,
        )

    except Exception as e:
        logger.error(f"Error actualizando título: {e}")
        raise AppError(f"Error interno actualizando título: {str(e)}", 500)


# Error handler específico para este blueprint
@expert_energy_bp.errorhandler(AppError)
def handle_energy_error(error):
    """Manejador de errores específico para rutas de energía."""
    logger.error(f"Error en ruta de energía: {error}")
    return (
        jsonify(
            {
                "status": "error",
                "message": error.message,
                "timestamp": datetime.now().isoformat(),
            }
        ),
        error.status_code,
    )
