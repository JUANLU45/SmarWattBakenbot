# expert_bot_api_COPY/utils/__init__.py

"""
🏢 UTILIDADES EMPRESARIALES NIVEL 2025
Módulo de utilidades empresariales para SmarWatt Expert Bot API
"""

from .error_handlers import (
    AppError,
    ValidationError,
    ServiceUnavailableError,
    DataError,
    EnterpriseErrorHandler,
    ErrorClassifier,
    ErrorReporter,
    register_error_handlers,
    log_error_enterprise,
    create_error_response,
    sanitize_error_data,
)

__version__ = "2025.1.0"
__author__ = "SmarWatt Enterprise Team"
__description__ = "Utilidades empresariales para Expert Bot API"

# Configuración empresarial
ENTERPRISE_CONFIG = {
    "version": "2025.1.0",
    "mode": "enterprise",
    "logging_level": "INFO",
    "error_reporting": True,
    "metrics_enabled": True,
    "security_enhanced": True,
}

# Exportar configuración
__all__ = [
    # Autenticación centralizada
    "token_required",
    "admin_required",
    "EnterpriseAuth",
    "UserContext",
    "TokenInfo",
    "AuthenticationError",
    "AuthorizationError",
    "RateLimitError",
    # Manejo de errores
    "AppError",
    "ValidationError",
    "ServiceUnavailableError",
    "DataError",
    "EnterpriseErrorHandler",
    "ErrorClassifier",
    "ErrorReporter",
    "register_error_handlers",
    "log_error_enterprise",
    "create_error_response",
    "sanitize_error_data",
    # Configuración
    "ENTERPRISE_CONFIG",
]
