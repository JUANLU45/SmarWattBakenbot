# expert_bot_api_COPY/utils/error_handlers.py

from flask import jsonify, request, current_app
import logging
import traceback
import time
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime, timezone
from .timezone_utils import now_spanish
from enum import Enum
import uuid
import json
import sys
import os


class ErrorLevel(Enum):
    """🏢 Niveles de error empresarial"""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class ErrorCategory(Enum):
    """🏢 Categorías de error empresarial"""

    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    VALIDATION = "validation"
    BUSINESS_LOGIC = "business_logic"
    EXTERNAL_SERVICE = "external_service"
    DATABASE = "database"
    NETWORK = "network"
    SYSTEM = "system"
    UNKNOWN = "unknown"


@dataclass
class ErrorContext:
    """🏢 Contexto de error empresarial"""

    error_id: str
    timestamp: datetime
    level: ErrorLevel
    category: ErrorCategory
    message: str
    details: Optional[str] = None
    stack_trace: Optional[str] = None
    user_id: Optional[str] = None
    request_id: Optional[str] = None
    endpoint: Optional[str] = None
    method: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    additional_data: Optional[Dict[str, Any]] = None


class AppError(Exception):
    """🏢 Clase de error personalizada empresarial"""

    def __init__(
        self,
        message: str,
        status_code: int = 400,
        error_code: Optional[str] = None,
        details: Optional[str] = None,
        level: ErrorLevel = ErrorLevel.MEDIUM,
        category: ErrorCategory = ErrorCategory.UNKNOWN,
        additional_data: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code or f"ERR_{status_code}"
        self.details = details
        self.level = level
        self.category = category
        self.additional_data = additional_data or {}
        self.error_id = str(uuid.uuid4())
        self.timestamp = now_spanish()


class ValidationError(AppError):
    """🏢 Error de validación empresarial"""

    def __init__(
        self,
        message: str,
        field: Optional[str] = None,
        validation_errors: Optional[List[Dict[str, str]]] = None,
        **kwargs,
    ):
        super().__init__(
            message=message,
            status_code=400,
            error_code="VALIDATION_ERROR",
            level=ErrorLevel.LOW,
            category=ErrorCategory.VALIDATION,
            **kwargs,
        )
        self.field = field
        self.validation_errors = validation_errors or []


class AuthenticationError(AppError):
    """🏢 Error de autenticación empresarial"""

    def __init__(self, message: str, **kwargs):
        super().__init__(
            message=message,
            status_code=401,
            error_code="AUTHENTICATION_ERROR",
            level=ErrorLevel.HIGH,
            category=ErrorCategory.AUTHENTICATION,
            **kwargs,
        )


class AuthorizationError(AppError):
    """🏢 Error de autorización empresarial"""

    def __init__(
        self, message: str, required_permission: Optional[str] = None, **kwargs
    ):
        super().__init__(
            message=message,
            status_code=403,
            error_code="AUTHORIZATION_ERROR",
            level=ErrorLevel.HIGH,
            category=ErrorCategory.AUTHORIZATION,
            **kwargs,
        )
        self.required_permission = required_permission


class RateLimitError(AppError):
    """🏢 Error de límite de velocidad empresarial"""

    def __init__(self, message: str, retry_after: Optional[int] = None, **kwargs):
        super().__init__(
            message=message,
            status_code=429,
            error_code="RATE_LIMIT_ERROR",
            level=ErrorLevel.MEDIUM,
            category=ErrorCategory.SYSTEM,
            **kwargs,
        )
        self.retry_after = retry_after


class ServiceUnavailableError(AppError):
    """🏢 Error de servicio no disponible empresarial"""

    def __init__(self, message: str, service_name: Optional[str] = None, **kwargs):
        super().__init__(
            message=message,
            status_code=503,
            error_code="SERVICE_UNAVAILABLE",
            level=ErrorLevel.CRITICAL,
            category=ErrorCategory.EXTERNAL_SERVICE,
            **kwargs,
        )
        self.service_name = service_name


class DataError(AppError):
    """🏢 Error de datos empresarial"""

    def __init__(self, message: str, data_source: Optional[str] = None, **kwargs):
        super().__init__(
            message=message,
            status_code=422,
            error_code="DATA_ERROR",
            level=ErrorLevel.MEDIUM,
            category=ErrorCategory.DATABASE,
            **kwargs,
        )
        self.data_source = data_source


class EnterpriseErrorHandler:
    """🏢 Manejador de errores empresarial"""

    def __init__(self):
        self.error_reporter = ErrorReporter()
        self.error_classifier = ErrorClassifier()

    def handle_error(self, error: Exception, request=None) -> Dict[str, Any]:
        """Manejar error empresarial"""

        # Clasificar error
        error_context = self.error_classifier.classify_error(error, request)

        # Reportar error
        self.error_reporter.report_error(error_context)

        # Crear respuesta
        response = self._create_error_response(error_context)

        return response

    def _create_error_response(self, error_context: ErrorContext) -> Dict[str, Any]:
        """Crear respuesta de error"""

        # Respuesta básica
        response = {
            "error": {
                "error_id": error_context.error_id,
                "message": error_context.message,
                "timestamp": error_context.timestamp.isoformat(),
                "level": error_context.level.value,
                "category": error_context.category.value,
            }
        }

        # Agregar detalles si no es producción
        if not self._is_production():
            if error_context.details:
                response["error"]["details"] = error_context.details

            if error_context.stack_trace:
                response["error"]["stack_trace"] = error_context.stack_trace

            if error_context.additional_data:
                response["error"]["additional_data"] = error_context.additional_data

        # Agregar información de contexto
        if error_context.request_id:
            response["error"]["request_id"] = error_context.request_id

        return response

    def _is_production(self) -> bool:
        """Verificar si estamos en producción"""
        return current_app.config.get("ENV") == "production"


class ErrorClassifier:
    """🏢 Clasificador de errores empresarial"""

    def classify_error(self, error: Exception, request=None) -> ErrorContext:
        """Clasificar error"""

        # Obtener información del request
        request_info = self._extract_request_info(request)

        # Clasificar según tipo de error
        if isinstance(error, AppError):
            return self._classify_app_error(error, request_info)
        else:
            return self._classify_generic_error(error, request_info)

    def _extract_request_info(self, request) -> Dict[str, Any]:
        """Extraer información del request"""
        if not request:
            return {}

        info = {
            "endpoint": request.endpoint,
            "method": request.method,
            "ip_address": request.remote_addr,
            "user_agent": request.headers.get("User-Agent"),
            "request_id": getattr(request, "request_id", None),
        }

        # Extraer user_id si existe
        try:
            from flask import g

            if hasattr(g, "user") and g.user:
                info["user_id"] = g.user.get("uid")
        except:
            pass

        return info

    def _classify_app_error(
        self, error: AppError, request_info: Dict[str, Any]
    ) -> ErrorContext:
        """Clasificar AppError"""

        return ErrorContext(
            error_id=error.error_id,
            timestamp=error.timestamp,
            level=error.level,
            category=error.category,
            message=error.message,
            details=error.details,
            stack_trace=self._get_stack_trace(error),
            user_id=request_info.get("user_id"),
            request_id=request_info.get("request_id"),
            endpoint=request_info.get("endpoint"),
            method=request_info.get("method"),
            ip_address=request_info.get("ip_address"),
            user_agent=request_info.get("user_agent"),
            additional_data=error.additional_data,
        )

    def _classify_generic_error(
        self, error: Exception, request_info: Dict[str, Any]
    ) -> ErrorContext:
        """Clasificar error genérico"""

        # Determinar categoría por tipo de error
        category = self._determine_category(error)
        level = self._determine_level(error)

        return ErrorContext(
            error_id=str(uuid.uuid4()),
            timestamp=datetime.now(timezone.utc),
            level=level,
            category=category,
            message=str(error),
            details=f"Tipo de error: {type(error).__name__}",
            stack_trace=self._get_stack_trace(error),
            user_id=request_info.get("user_id"),
            request_id=request_info.get("request_id"),
            endpoint=request_info.get("endpoint"),
            method=request_info.get("method"),
            ip_address=request_info.get("ip_address"),
            user_agent=request_info.get("user_agent"),
            additional_data={"error_type": type(error).__name__},
        )

    def _determine_category(self, error: Exception) -> ErrorCategory:
        """Determinar categoría del error"""

        error_type = type(error).__name__

        if any(
            keyword in error_type.lower()
            for keyword in ["auth", "permission", "forbidden"]
        ):
            return ErrorCategory.AUTHENTICATION
        elif any(
            keyword in error_type.lower() for keyword in ["validation", "value", "type"]
        ):
            return ErrorCategory.VALIDATION
        elif any(
            keyword in error_type.lower()
            for keyword in ["database", "sql", "connection"]
        ):
            return ErrorCategory.DATABASE
        elif any(
            keyword in error_type.lower()
            for keyword in ["network", "timeout", "connection"]
        ):
            return ErrorCategory.NETWORK
        elif any(
            keyword in error_type.lower() for keyword in ["system", "os", "memory"]
        ):
            return ErrorCategory.SYSTEM
        else:
            return ErrorCategory.UNKNOWN

    def _determine_level(self, error: Exception) -> ErrorLevel:
        """Determinar nivel del error"""

        error_type = type(error).__name__

        if any(
            keyword in error_type.lower() for keyword in ["critical", "fatal", "system"]
        ):
            return ErrorLevel.CRITICAL
        elif any(
            keyword in error_type.lower()
            for keyword in ["auth", "permission", "security"]
        ):
            return ErrorLevel.HIGH
        elif any(
            keyword in error_type.lower() for keyword in ["validation", "value", "type"]
        ):
            return ErrorLevel.LOW
        else:
            return ErrorLevel.MEDIUM

    def _get_stack_trace(self, error: Exception) -> str:
        """Obtener stack trace"""
        return traceback.format_exc()


class ErrorReporter:
    """🏢 Reportador de errores empresarial"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def report_error(self, error_context: ErrorContext):
        """Reportar error"""

        # Log local
        self._log_error(error_context)

        # Reportar a sistemas externos
        self._report_to_external_systems(error_context)

        # Alertas críticas
        if error_context.level == ErrorLevel.CRITICAL:
            self._send_critical_alert(error_context)

    def _log_error(self, error_context: ErrorContext):
        """Log del error"""

        log_data = {
            "error_id": error_context.error_id,
            "timestamp": error_context.timestamp.isoformat(),
            "level": error_context.level.value,
            "category": error_context.category.value,
            "message": error_context.message,
            "user_id": error_context.user_id,
            "endpoint": error_context.endpoint,
            "method": error_context.method,
            "ip_address": error_context.ip_address,
        }

        # Determinar nivel de log
        if error_context.level == ErrorLevel.CRITICAL:
            self.logger.critical(json.dumps(log_data))
        elif error_context.level == ErrorLevel.HIGH:
            self.logger.error(json.dumps(log_data))
        elif error_context.level == ErrorLevel.MEDIUM:
            self.logger.warning(json.dumps(log_data))
        else:
            self.logger.info(json.dumps(log_data))

    def _report_to_external_systems(self, error_context: ErrorContext):
        """Reportar a sistemas externos"""

        # TODO: Implementar integración con sistemas de monitoreo
        # Como Sentry, DataDog, etc.
        pass

    def _send_critical_alert(self, error_context: ErrorContext):
        """Enviar alerta crítica"""

        # TODO: Implementar alertas (email, Slack, etc.)
        self.logger.critical(f"ALERTA CRÍTICA: {error_context.message}")


# Instancias globales
_error_handler = EnterpriseErrorHandler()


def register_error_handlers(app):
    """🏢 Registrar manejadores de errores empresariales"""

    @app.errorhandler(AppError)
    def handle_app_error(error: AppError):
        """Manejar AppError"""
        response_data = _error_handler.handle_error(error, request)
        return jsonify(response_data), error.status_code

    @app.errorhandler(ValidationError)
    def handle_validation_error(error: ValidationError):
        """Manejar ValidationError"""
        response_data = _error_handler.handle_error(error, request)

        # Agregar errores de validación específicos
        if error.validation_errors:
            response_data["error"]["validation_errors"] = error.validation_errors

        if error.field:
            response_data["error"]["field"] = error.field

        return jsonify(response_data), error.status_code

    @app.errorhandler(AuthenticationError)
    def handle_authentication_error(error: AuthenticationError):
        """Manejar AuthenticationError"""
        response_data = _error_handler.handle_error(error, request)
        return jsonify(response_data), error.status_code

    @app.errorhandler(AuthorizationError)
    def handle_authorization_error(error: AuthorizationError):
        """Manejar AuthorizationError"""
        response_data = _error_handler.handle_error(error, request)

        if error.required_permission:
            response_data["error"]["required_permission"] = error.required_permission

        return jsonify(response_data), error.status_code

    @app.errorhandler(RateLimitError)
    def handle_rate_limit_error(error: RateLimitError):
        """Manejar RateLimitError"""
        response_data = _error_handler.handle_error(error, request)

        response = jsonify(response_data)

        if error.retry_after:
            response.headers["Retry-After"] = str(error.retry_after)

        return response, error.status_code

    @app.errorhandler(ServiceUnavailableError)
    def handle_service_unavailable_error(error: ServiceUnavailableError):
        """Manejar ServiceUnavailableError"""
        response_data = _error_handler.handle_error(error, request)

        if error.service_name:
            response_data["error"]["service_name"] = error.service_name

        return jsonify(response_data), error.status_code

    @app.errorhandler(DataError)
    def handle_data_error(error: DataError):
        """Manejar DataError"""
        response_data = _error_handler.handle_error(error, request)

        if error.data_source:
            response_data["error"]["data_source"] = error.data_source

        return jsonify(response_data), error.status_code

    @app.errorhandler(404)
    def handle_not_found_error(error):
        """Manejar 404"""
        app_error = AppError(
            message="Recurso no encontrado",
            status_code=404,
            error_code="NOT_FOUND",
            level=ErrorLevel.LOW,
            category=ErrorCategory.SYSTEM,
        )

        response_data = _error_handler.handle_error(app_error, request)
        return jsonify(response_data), 404

    @app.errorhandler(405)
    def handle_method_not_allowed_error(error):
        """Manejar 405"""
        app_error = AppError(
            message="Método no permitido",
            status_code=405,
            error_code="METHOD_NOT_ALLOWED",
            level=ErrorLevel.LOW,
            category=ErrorCategory.SYSTEM,
        )

        response_data = _error_handler.handle_error(app_error, request)
        return jsonify(response_data), 405

    @app.errorhandler(500)
    def handle_internal_server_error(error):
        """Manejar 500"""
        app_error = AppError(
            message="Ha ocurrido un error interno en el servidor",
            status_code=500,
            error_code="INTERNAL_SERVER_ERROR",
            level=ErrorLevel.CRITICAL,
            category=ErrorCategory.SYSTEM,
            details=str(error),
        )

        response_data = _error_handler.handle_error(app_error, request)
        return jsonify(response_data), 500

    @app.errorhandler(Exception)
    def handle_generic_error(error):
        """Manejar errores genéricos"""
        response_data = _error_handler.handle_error(error, request)
        return jsonify(response_data), 500


# Funciones de utilidad
def log_error_enterprise(error: Exception, request=None):
    """Registrar error empresarial"""
    _error_handler.handle_error(error, request)


def create_error_response(
    message: str,
    status_code: int = 400,
    error_code: Optional[str] = None,
    details: Optional[str] = None,
) -> Dict[str, Any]:
    """Crear respuesta de error"""

    app_error = AppError(
        message=message, status_code=status_code, error_code=error_code, details=details
    )

    return _error_handler.handle_error(app_error)


def sanitize_error_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Sanitizar datos de error para producción"""

    # Lista de campos sensibles
    sensitive_fields = [
        "password",
        "token",
        "secret",
        "key",
        "api_key",
        "auth_token",
        "access_token",
        "refresh_token",
        "private_key",
        "certificate",
        "credentials",
    ]

    sanitized = {}

    for key, value in data.items():
        if any(sensitive in key.lower() for sensitive in sensitive_fields):
            sanitized[key] = "[SANITIZED]"
        elif isinstance(value, dict):
            sanitized[key] = sanitize_error_data(value)
        elif isinstance(value, list):
            sanitized[key] = [
                sanitize_error_data(item) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            sanitized[key] = value

    return sanitized
