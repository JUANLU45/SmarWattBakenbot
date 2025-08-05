"""
🏢 ENDPOINT DE PRUEBA PARA SISTEMA DE ENLACES EMPRESARIAL
Permite probar el sistema de enlaces inteligentes desde cualquier microservicio
"""

from flask import Blueprint, request, jsonify
from app.services.enterprise_links_service import get_enterprise_link_service
import logging

# Crear blueprint para endpoints de enlaces
links_bp = Blueprint("enterprise_links", __name__)
logger = logging.getLogger(__name__)


@links_bp.route("/links/test", methods=["POST"])
def test_links_system():
    """
    🔗 Endpoint de prueba para sistema de enlaces inteligentes

    Body:
    {
        "response_text": "Tu mensaje de prueba aquí"
    }

    Returns:
    {
        "original_response": "texto original",
        "enhanced_response": "texto con enlaces",
        "links_added": true/false,
        "service_status": {...}
    }
    """
    try:
        data = request.get_json()

        if not data or "response_text" not in data:
            return (
                jsonify(
                    {"error": "Campo 'response_text' requerido", "status": "error"}
                ),
                400,
            )

        response_text = data["response_text"]

        if not response_text or len(response_text.strip()) < 3:
            return (
                jsonify(
                    {
                        "error": "response_text debe tener al menos 3 caracteres",
                        "status": "error",
                    }
                ),
                400,
            )

        # Obtener servicio de enlaces
        links_service = get_enterprise_link_service()

        # Procesar texto
        enhanced_response = links_service.analyze_and_enhance_response(response_text)

        # Obtener estado del servicio
        service_status = links_service.get_enterprise_status()

        return (
            jsonify(
                {
                    "original_response": response_text,
                    "enhanced_response": enhanced_response,
                    "links_added": enhanced_response != response_text,
                    "character_diff": len(enhanced_response) - len(response_text),
                    "service_status": service_status,
                    "status": "success",
                }
            ),
            200,
        )

    except Exception as e:
        logger.error(f"❌ Error en test de enlaces: {str(e)}")
        return jsonify({"error": f"Error interno: {str(e)}", "status": "error"}), 500


@links_bp.route("/links/status", methods=["GET"])
def get_links_status():
    """
    📊 Obtener estado del servicio de enlaces empresarial

    Returns:
    {
        "service_status": {...},
        "available_links": [...],
        "version": "..."
    }
    """
    try:
        links_service = get_enterprise_link_service()
        service_status = links_service.get_enterprise_status()

        return jsonify(service_status), 200

    except Exception as e:
        logger.error(f"❌ Error obteniendo status de enlaces: {str(e)}")
        return jsonify({"error": f"Error interno: {str(e)}", "status": "error"}), 500


@links_bp.route("/links/direct/<link_type>", methods=["GET"])
def get_direct_link(link_type):
    """
    🔗 Obtener enlace directo por tipo

    Args:
        link_type: blog, dashboard, calculator, weather, contact, terms, privacy

    Returns:
    {
        "link_type": "...",
        "url": "...",
        "status": "success"
    }
    """
    try:
        links_service = get_enterprise_link_service()
        url = links_service.get_direct_link(link_type)

        if url:
            return (
                jsonify({"link_type": link_type, "url": url, "status": "success"}),
                200,
            )
        else:
            return (
                jsonify(
                    {
                        "error": f"Tipo de enlace '{link_type}' no encontrado",
                        "available_types": [
                            "blog",
                            "dashboard",
                            "calculator",
                            "weather",
                            "contact",
                            "terms",
                            "privacy",
                        ],
                        "status": "error",
                    }
                ),
                404,
            )

    except Exception as e:
        logger.error(f"❌ Error obteniendo enlace directo: {str(e)}")
        return jsonify({"error": f"Error interno: {str(e)}", "status": "error"}), 500


logger.info("✅ Blueprint de enlaces empresariales cargado correctamente")
