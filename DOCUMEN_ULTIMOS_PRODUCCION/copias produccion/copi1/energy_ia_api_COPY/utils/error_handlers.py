# energy_ia_api_COPY/utils/error_handlers.py
# 🏢 MANEJO DE ERRORES EMPRESARIAL NIVEL 2025 - ENERGY IA API COPY

import os
import logging
import json
import traceback
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from flask import Flask, request, jsonify, g
from werkzeug.exceptions import HTTPException
import requests
from .timezone_utils import now_spanish_iso

# Configuración de logging empresarial
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AppError(Exception):
    """Excepción personalizada empresarial para errores de aplicación"""

    def __init__(
        self, message: str, status_code: int = 500, details: Optional[Dict] = None
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        self.timestamp = now_spanish_iso()
        self.error_id = self._generate_error_id()

        # Log del error
        logger.error(f"AppError[{self.error_id}]: {message} (Status: {status_code})")

    def _generate_error_id(self) -> str:
        """Genera ID único para el error"""
        import uuid

        return str(uuid.uuid4())[:8]

    def to_dict(self) -> Dict[str, Any]:
        """Convierte error a diccionario"""
        return {
            "error_id": self.error_id,
            "message": self.message,
            "status_code": self.status_code,
            "details": self.details,
            "timestamp": self.timestamp,
            "service": "energy_ia_api_copy",
        }


class ErrorContext:
    """Contexto empresarial para manejo de errores"""

    def __init__(self):
        self.error_count = 0
        self.error_history = []
        self.user_context = {}
        self.request_context = {}

    def add_error(self, error: AppError):
        """Añade error al contexto"""
        self.error_count += 1
        self.error_history.append(
            {
                "error_id": error.error_id,
                "message": error.message,
                "status_code": error.status_code,
                "timestamp": error.timestamp,
            }
        )

        # Mantener solo los últimos 10 errores
        if len(self.error_history) > 10:
            self.error_history = self.error_history[-10:]

    def set_user_context(self, user_data: Dict):
        """Establece contexto del usuario"""
        self.user_context = {
            "user_id": user_data.get("uid", ""),
            "email": user_data.get("email", ""),
            "auth_method": user_data.get("auth_method", ""),
            "subscription_status": user_data.get("subscription_status", ""),
        }

    def set_request_context(self, request_data: Dict):
        """Establece contexto de la petición"""
        self.request_context = {
            "method": request_data.get("method", ""),
            "endpoint": request_data.get("endpoint", ""),
            "user_agent": request_data.get("user_agent", ""),
            "ip_address": request_data.get("ip_address", ""),
            "timestamp": now_spanish_iso(),
        }

    def get_full_context(self) -> Dict[str, Any]:
        """Obtiene contexto completo"""
        return {
            "error_count": self.error_count,
            "error_history": self.error_history,
            "user_context": self.user_context,
            "request_context": self.request_context,
        }


class EnterpriseErrorHandler:
    """Manejador de errores empresarial"""

    def __init__(self):
        self.error_classifier = ErrorClassifier()
        self.error_reporter = ErrorReporter()
        self.error_context = ErrorContext()

        logger.info("🏢 EnterpriseErrorHandler inicializado")

    def handle_app_error(self, error: AppError) -> Dict[str, Any]:
        """Maneja errores de aplicación"""
        try:
            # Añadir al contexto
            self.error_context.add_error(error)

            # Clasificar error
            error_category = self.error_classifier.classify_error(error)

            # Obtener contexto del usuario si está disponible
            user_data = g.get("user", {})
            if user_data:
                self.error_context.set_user_context(user_data)

            # Contexto de la petición
            if request:
                self.error_context.set_request_context(
                    {
                        "method": request.method,
                        "endpoint": request.endpoint,
                        "user_agent": request.headers.get("User-Agent", ""),
                        "ip_address": request.remote_addr,
                    }
                )

            # Reportar error si es crítico
            if error.status_code >= 500:
                self.error_reporter.report_critical_error(error, self.error_context)

            # Preparar respuesta
            response = {
                "status": "error",
                "error_id": error.error_id,
                "message": self._sanitize_error_message(
                    error.message, error.status_code
                ),
                "error_code": error.status_code,
                "category": error_category,
                "timestamp": error.timestamp,
                "service": "energy_ia_api_copy",
            }

            # Añadir detalles para desarrolladores en modo debug
            if os.environ.get("FLASK_ENV") == "development":
                response["details"] = error.details
                response["context"] = self.error_context.get_full_context()

            return response

        except Exception as e:
            logger.error(f"❌ Error en manejador de errores: {str(e)}")
            return {
                "status": "error",
                "message": "Error interno del servidor",
                "error_code": 500,
                "timestamp": now_spanish_iso(),
            }

    def handle_http_error(self, error: HTTPException) -> Dict[str, Any]:
        """Maneja errores HTTP estándar"""
        app_error = AppError(
            message=error.description or "Error HTTP",
            status_code=error.code,
            details={"original_error": str(error)},
        )

        return self.handle_app_error(app_error)

    def handle_unexpected_error(self, error: Exception) -> Dict[str, Any]:
        """Maneja errores inesperados"""
        # Crear AppError desde excepción
        app_error = AppError(
            message="Error interno del servidor",
            status_code=500,
            details={
                "original_error": str(error),
                "error_type": type(error).__name__,
                "traceback": traceback.format_exc(),
            },
        )

        # Reportar error crítico
        self.error_reporter.report_critical_error(app_error, self.error_context)

        return self.handle_app_error(app_error)

    def _sanitize_error_message(self, message: str, status_code: int) -> str:
        """Sanitiza mensajes de error para el usuario"""
        # No mostrar detalles internos en producción
        if os.environ.get("FLASK_ENV") == "production" and status_code >= 500:
            return "Error interno del servidor. Por favor, inténtalo más tarde."

        # Filtrar información sensible
        sensitive_keywords = ["password", "token", "secret", "key", "credential"]
        for keyword in sensitive_keywords:
            if keyword.lower() in message.lower():
                return "Error de autenticación. Verifica tus credenciales."

        return message


class ErrorClassifier:
    """Clasificador de errores empresarial"""

    def __init__(self):
        self.error_patterns = {
            "authentication": [
                "token",
                "auth",
                "login",
                "credential",
                "permission",
                "unauthorized",
            ],
            "validation": ["required", "invalid", "format", "missing", "validation"],
            "database": ["connection", "query", "bigquery", "firestore", "database"],
            "external_service": ["api", "service", "request", "timeout", "connection"],
            "ml_model": ["model", "prediction", "vertex", "ai", "gemini"],
            "business_logic": [
                "tariff",
                "recommendation",
                "consumption",
                "calculation",
            ],
        }

    def classify_error(self, error: AppError) -> str:
        """Clasifica el error según patrones"""
        message_lower = error.message.lower()

        # Clasificar por código de estado
        if error.status_code == 401:
            return "authentication"
        elif error.status_code == 403:
            return "authorization"
        elif error.status_code == 404:
            return "not_found"
        elif error.status_code == 429:
            return "rate_limit"
        elif error.status_code >= 500:
            return "server_error"

        # Clasificar por patrones de mensaje
        for category, keywords in self.error_patterns.items():
            if any(keyword in message_lower for keyword in keywords):
                return category

        return "unknown"

    def get_error_severity(self, error: AppError) -> str:
        """Determina la severidad del error"""
        if error.status_code >= 500:
            return "critical"
        elif error.status_code >= 400:
            return "warning"
        else:
            return "info"

    def should_retry(self, error: AppError) -> bool:
        """Determina si el error debería ser reintentado"""
        retry_codes = [429, 502, 503, 504]
        return error.status_code in retry_codes

    def get_user_action(self, error: AppError) -> str:
        """Sugiere acción para el usuario"""
        if error.status_code == 401:
            return "Por favor, inicia sesión nuevamente"
        elif error.status_code == 403:
            return "No tienes permisos para realizar esta acción"
        elif error.status_code == 404:
            return "El recurso solicitado no existe"
        elif error.status_code == 429:
            return "Demasiadas peticiones. Espera un momento e intenta de nuevo"
        elif error.status_code >= 500:
            return "Error del servidor. Intenta más tarde o contacta soporte"
        else:
            return "Verifica los datos enviados e intenta de nuevo"


class ErrorReporter:
    """Reportador de errores empresarial"""

    def __init__(self):
        self.slack_webhook = os.environ.get("SLACK_ERROR_WEBHOOK", "")
        self.email_endpoint = os.environ.get("ERROR_EMAIL_ENDPOINT", "")
        self.monitoring_endpoint = os.environ.get("MONITORING_ENDPOINT", "")

    def report_critical_error(self, error: AppError, context: ErrorContext):
        """Reporta errores críticos a sistemas externos"""
        try:
            error_report = {
                "service": "energy_ia_api_copy",
                "error_id": error.error_id,
                "message": error.message,
                "status_code": error.status_code,
                "timestamp": error.timestamp,
                "details": error.details,
                "context": context.get_full_context(),
                "environment": os.environ.get("FLASK_ENV", "unknown"),
            }

            # Enviar a Slack
            if self.slack_webhook:
                self._send_to_slack(error_report)

            # Enviar por email
            if self.email_endpoint:
                self._send_email_alert(error_report)

            # Enviar a sistema de monitoreo
            if self.monitoring_endpoint:
                self._send_to_monitoring(error_report)

            logger.info(f"📧 Error crítico reportado: {error.error_id}")

        except Exception as e:
            logger.error(f"❌ Error reportando error crítico: {str(e)}")

    def _send_to_slack(self, error_report: Dict):
        """Envía error a Slack"""
        try:
            message = {
                "text": f"🚨 ERROR CRÍTICO en {error_report['service']}",
                "attachments": [
                    {
                        "color": "danger",
                        "fields": [
                            {
                                "title": "Error ID",
                                "value": error_report["error_id"],
                                "short": True,
                            },
                            {
                                "title": "Mensaje",
                                "value": error_report["message"],
                                "short": False,
                            },
                            {
                                "title": "Código de Estado",
                                "value": str(error_report["status_code"]),
                                "short": True,
                            },
                            {
                                "title": "Timestamp",
                                "value": error_report["timestamp"],
                                "short": True,
                            },
                        ],
                    }
                ],
            }

            response = requests.post(self.slack_webhook, json=message, timeout=5)
            if response.status_code == 200:
                logger.info("✅ Error enviado a Slack")
            else:
                logger.warning(f"⚠️ Error enviando a Slack: {response.status_code}")

        except Exception as e:
            logger.error(f"❌ Error enviando a Slack: {str(e)}")

    def _send_email_alert(self, error_report: Dict):
        """Envía alerta por email"""
        try:
            email_data = {
                "subject": f"ERROR CRÍTICO - {error_report['service']} - {error_report['error_id']}",
                "message": f"""
Error crítico detectado en {error_report['service']}:

Error ID: {error_report['error_id']}
Mensaje: {error_report['message']}
Código de Estado: {error_report['status_code']}
Timestamp: {error_report['timestamp']}
Entorno: {error_report['environment']}

Contexto: {json.dumps(error_report['context'], indent=2)}

Detalles: {json.dumps(error_report['details'], indent=2)}
                """,
                "recipients": ["admin@smarwatt.com", "tech@smarwatt.com"],
            }

            response = requests.post(self.email_endpoint, json=email_data, timeout=10)
            if response.status_code == 200:
                logger.info("✅ Alerta enviada por email")
            else:
                logger.warning(f"⚠️ Error enviando email: {response.status_code}")

        except Exception as e:
            logger.error(f"❌ Error enviando email: {str(e)}")

    def _send_to_monitoring(self, error_report: Dict):
        """Envía error a sistema de monitoreo"""
        try:
            monitoring_data = {
                "service": error_report["service"],
                "error_id": error_report["error_id"],
                "error_type": "critical",
                "message": error_report["message"],
                "status_code": error_report["status_code"],
                "timestamp": error_report["timestamp"],
                "metadata": error_report["context"],
            }

            response = requests.post(
                self.monitoring_endpoint, json=monitoring_data, timeout=5
            )
            if response.status_code == 200:
                logger.info("✅ Error enviado a sistema de monitoreo")
            else:
                logger.warning(f"⚠️ Error enviando a monitoreo: {response.status_code}")

        except Exception as e:
            logger.error(f"❌ Error enviando a monitoreo: {str(e)}")


# Instancias globales
error_handler = EnterpriseErrorHandler()
error_classifier = ErrorClassifier()
error_reporter = ErrorReporter()


def register_error_handlers(app: Flask):
    """Registra manejadores de errores en la aplicación Flask"""

    @app.errorhandler(AppError)
    def handle_app_error(error: AppError):
        """Maneja errores de aplicación personalizados"""
        response_data = error_handler.handle_app_error(error)
        return jsonify(response_data), error.status_code

    @app.errorhandler(HTTPException)
    def handle_http_error(error: HTTPException):
        """Maneja errores HTTP estándar"""
        response_data = error_handler.handle_http_error(error)
        return jsonify(response_data), error.code

    @app.errorhandler(Exception)
    def handle_unexpected_error(error: Exception):
        """Maneja errores inesperados"""
        response_data = error_handler.handle_unexpected_error(error)
        return jsonify(response_data), 500

    @app.errorhandler(404)
    def handle_not_found(error):
        """Maneja errores 404"""
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Endpoint no encontrado",
                    "error_code": 404,
                    "service": "energy_ia_api_copy",
                    "timestamp": now_spanish_iso(),
                }
            ),
            404,
        )

    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        """Maneja errores 405"""
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Método no permitido",
                    "error_code": 405,
                    "service": "energy_ia_api_copy",
                    "timestamp": now_spanish_iso(),
                }
            ),
            405,
        )

    @app.errorhandler(429)
    def handle_rate_limit(error):
        """Maneja errores de rate limiting"""
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Demasiadas peticiones. Intenta más tarde.",
                    "error_code": 429,
                    "service": "energy_ia_api_copy",
                    "timestamp": now_spanish_iso(),
                }
            ),
            429,
        )

    # Middleware para errores no capturados
    @app.before_request
    def before_request():
        """Middleware ejecutado antes de cada petición"""
        try:
            # Inicializar contexto de error
            error_handler.error_context = ErrorContext()

            # Validar headers básicos
            if (
                request.content_length and request.content_length > 16 * 1024 * 1024
            ):  # 16MB
                raise AppError("Petición demasiado grande", 413)

        except Exception as e:
            logger.error(f"❌ Error en before_request: {str(e)}")

    logger.info("✅ Manejadores de errores empresariales registrados")


# === FUNCIONES DE UTILIDAD ===


def create_validation_error(field: str, value: Any, expected: str) -> AppError:
    """Crea error de validación estandarizado"""
    return AppError(
        message=f"Campo '{field}' inválido",
        status_code=400,
        details={
            "field": field,
            "value": str(value),
            "expected": expected,
            "validation_error": True,
        },
    )


def create_not_found_error(resource: str, identifier: str) -> AppError:
    """Crea error de recurso no encontrado"""
    return AppError(
        message=f"{resource} no encontrado",
        status_code=404,
        details={
            "resource": resource,
            "identifier": identifier,
            "not_found_error": True,
        },
    )


def create_external_service_error(service: str, error_msg: str) -> AppError:
    """Crea error de servicio externo"""
    return AppError(
        message=f"Error en servicio externo: {service}",
        status_code=503,
        details={
            "service": service,
            "original_error": error_msg,
            "external_service_error": True,
        },
    )


def get_error_stats() -> Dict[str, Any]:
    """Obtiene estadísticas de errores"""
    # Calcular categorías de errores reales
    error_categories = {}
    if (
        hasattr(error_handler.error_context, "error_history")
        and error_handler.error_context.error_history
    ):
        for error_info in error_handler.error_context.error_history:
            category = error_info.get("error_type", "unknown")
            error_categories[category] = error_categories.get(category, 0) + 1

    return {
        "total_errors": error_handler.error_context.error_count,
        "recent_errors": len(error_handler.error_context.error_history),
        "error_categories": error_categories,
        "timestamp": now_spanish_iso(),
    }


logger.info("✅ Manejo de errores empresarial energy_ia_api_copy inicializado")
