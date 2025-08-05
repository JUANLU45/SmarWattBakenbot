# energy_ia_api_COPY/utils/__init__.py
# 🏢 UTILIDADES EMPRESARIALES NIVEL 2025 - ENERGY IA API COPY

"""
Utilidades empresariales para energy_ia_api_COPY
Incluye autenticación, manejo de errores y herramientas de nivel empresarial
"""

import logging
from datetime import datetime
from .timezone_utils import now_spanish_iso

# Configuración de logging empresarial
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# Configuración empresarial
ENTERPRISE_CONFIG = {
    "version": "2025.1.0",
    "service_name": "energy_ia_api_copy_utils",
    "initialized_at": now_spanish_iso(),
    "enterprise_mode": True,
}

# Exportar utilidades principales desde la librería centralizada
from smarwatt_auth import (
    token_required,
    admin_required,
    EnterpriseAuth,
    UserContext,
    TokenInfo,
    AppError,
    AuthenticationError,
    AuthorizationError,
    RateLimitError,
)

from .error_handlers import (
    AppError,
    register_error_handlers,
    ErrorContext,
    EnterpriseErrorHandler,
    ErrorClassifier,
    ErrorReporter,
)

# Lista de exportaciones
__all__ = [
    # Autenticación
    "token_required",
    "admin_required",
    "EnterpriseAuth",
    "UserContext",
    "TokenInfo",
    "AppError",
    "AuthenticationError",
    "AuthorizationError",
    "RateLimitError",
    # Manejo de errores
    "register_error_handlers",
    "ErrorContext",
    "EnterpriseErrorHandler",
    "ErrorClassifier",
    "ErrorReporter",
    # Configuración
    "ENTERPRISE_CONFIG",
]

# Versión del módulo
__version__ = "2025.1.0"

logger.info(
    f"✅ Utilidades empresariales energy_ia_api_copy inicializadas v{__version__}"
)
