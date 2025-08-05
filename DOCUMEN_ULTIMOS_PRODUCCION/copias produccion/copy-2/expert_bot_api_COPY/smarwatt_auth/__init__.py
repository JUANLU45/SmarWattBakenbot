# smarwatt_auth/__init__.py
from .exceptions import (
    AppError,
    AuthenticationError,
    AuthorizationError,
    RateLimitError,
)

# Exportar todos los componentes
__all__ = [
    "token_required",
    "admin_required",
    "EnterpriseAuth",
    "UserContext",
    "TokenInfo",
    "AppError",
    "AuthenticationError",
    "AuthorizationError",
    "RateLimitError",
]

"""
SmarWatt Authentication Library
===============================

Librería empresarial centralizada para autenticación en microservicios SmarWatt.

Características:
- Autenticación Firebase avanzada
- Rate limiting empresarial
- Gestión de sesiones robusta
- Validación de tokens multinivel
- Logging empresarial completo

Uso:
    from smarwatt_auth import token_required, admin_required
    from smarwatt_auth import EnterpriseAuth
"""

from .auth import (
    token_required,
    admin_required,
    EnterpriseAuth,
    UserContext,
    TokenInfo,
)

from .exceptions import (
    AppError,
    AuthenticationError,
    AuthorizationError,
    RateLimitError,
)

# Exportar todas las clases y funciones
__all__ = [
    "token_required",
    "admin_required",
    "EnterpriseAuth",
    "UserContext",
    "TokenInfo",
    "AppError",
    "AuthenticationError",
    "AuthorizationError",
    "RateLimitError",
]

__version__ = "1.0.0"
__author__ = "SmarWatt Enterprise Team"
__email__ = "dev@smarwatt.com"
