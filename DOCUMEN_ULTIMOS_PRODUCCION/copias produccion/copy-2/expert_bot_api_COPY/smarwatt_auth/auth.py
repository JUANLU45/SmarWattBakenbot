# smarwatt_auth/auth.py
# 🏢 AUTENTICACIÓN EMPRESARIAL SMARWATT - CÓDIGO PRINCIPAL

from functools import wraps
from flask import request, g, current_app
import logging
import time
import threading
import os
from typing import Dict, Any, Optional, List, Callable, TypeVar, cast, Tuple
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
import hashlib
from collections import defaultdict
import time
import logging
from typing import Dict, Any, Optional, List
from flask import request, g

from google.cloud import firestore
from google.api_core import exceptions as google_exceptions
from utils.error_handlers import AppError
from .exceptions import AuthenticationError, AuthorizationError, RateLimitError

# 🏢 CONFIGURACIÓN EMPRESARIAL PARA PRODUCCIÓN
# Imports empresariales con manejo de errores robusto
try:
    import firebase_admin
    from firebase_admin import auth, credentials

    FIREBASE_AVAILABLE = True

    # 🎯 INICIALIZACIÓN AUTOMÁTICA PARA PRODUCCIÓN
    if not firebase_admin._apps:
        try:
            # En Cloud Run: usa automáticamente las credenciales de la service account
            # Los secretos están montados en directorios separados por --set-secrets
            if os.path.exists("/credentials/firebase-adminsdk-key"):
                # Producción: usar secreto montado
                cred = credentials.Certificate("/credentials/firebase-adminsdk-key")
                firebase_admin.initialize_app(cred)
                logging.info(
                    "🏢 Firebase inicializado con credenciales de Secret Manager"
                )
            else:
                # Fallback: usar Default Application Credentials
                firebase_admin.initialize_app()
                logging.info(
                    "🏢 Firebase inicializado con Default Application Credentials"
                )
        except Exception as e:
            logging.error(f"Error inicializando Firebase: {e}")
            FIREBASE_AVAILABLE = False

except ImportError:
    FIREBASE_AVAILABLE = False
    logging.warning("Firebase Admin SDK no disponible - modo degrado activado")


@dataclass
class UserProfile:
    """🏢 Perfil de usuario empresarial"""

    uid: str
    email: str
    display_name: str
    subscription_plan: str
    subscription_status: str
    role: str
    created_at: str
    updated_at: str
    preferences: Dict[str, Any]


class FirebaseAuthService:
    """🏢 Servicio de autenticación Firebase empresarial"""

    def __init__(self) -> None:
        self.firestore_client = firestore.Client()
        self.users_collection = self.firestore_client.collection("users")
        self.energy_profiles_collection = self.firestore_client.collection(
            "user_energy_profiles"
        )

    def verify_firebase_token(self, token: str) -> Optional[UserProfile]:
        """🔐 Verificar token Firebase y obtener perfil empresarial"""
        try:
            # Verificar token Firebase
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token["uid"]

            # Obtener perfil completo del usuario
            user_doc = self.users_collection.document(uid).get()
            if not user_doc.exists:
                return None

            user_data = user_doc.to_dict()

            return UserProfile(
                uid=uid,
                email=user_data.get("email", ""),
                display_name=user_data.get("displayName", ""),
                subscription_plan=user_data.get("subscription", {}).get("plan", "free"),
                subscription_status=user_data.get("subscription", {}).get(
                    "status", "inactive"
                ),
                role=user_data.get("role", "user"),
                created_at=user_data.get("createdAt", ""),
                updated_at=user_data.get("updatedAt", ""),
                preferences=user_data.get("preferences", {}),
            )

        except Exception as e:
            logging.error(f"Error verificando token Firebase: {e}")
            return None


def admin_required(f):
    """🔐 Decorador de autorización administrativa"""

    def decorated(*args, **kwargs):
        if not hasattr(g, "user_profile") or g.user_profile.role != "admin":
            raise AuthorizationError("Acceso administrativo requerido", 403)
        return f(*args, **kwargs)

    return decorated


def premium_required(f):
    """🔐 Decorador de autorización premium"""

    def decorated(*args, **kwargs):
        if not hasattr(g, "user_profile"):
            raise AuthorizationError("Autenticación requerida", 401)

        if g.user_profile.subscription_plan not in ["pro", "enterprise"]:
            raise AuthorizationError("Suscripción premium requerida", 403)

        return f(*args, **kwargs)

    return decorated
    logging.warning("🔴 Firebase Admin no disponible - autenticación limitada")


try:
    import jwt

    JWT_AVAILABLE = True
except ImportError:
    JWT_AVAILABLE = False
    logging.warning("🔴 JWT no disponible - autenticación limitada")

try:
    from google.oauth2 import id_token as google_id_token
    from google.auth.transport import requests as google_requests

    GOOGLE_AUTH_AVAILABLE = True
except ImportError:
    GOOGLE_AUTH_AVAILABLE = False
    logging.warning("🔴 Google Auth no disponible - autenticación limitada")

from .exceptions import (
    AuthenticationError,
    AuthorizationError,
    RateLimitError,
)


@dataclass
class UserContext:
    """🏢 Contexto de usuario empresarial"""

    uid: str
    email: str
    display_name: str
    subscription_status: str
    custom_claims: Optional[Dict[str, Any]] = None
    role: str = "user"
    permissions: Optional[List[str]] = None
    last_active: Optional[datetime] = None
    session_id: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    auth_method: Optional[str] = None
    security_level: str = "standard"


@dataclass
class TokenInfo:
    """🏢 Información de token empresarial"""

    token: str
    token_type: str
    expires_at: datetime
    issued_at: datetime
    issuer: str
    audience: str
    scopes: Optional[List[str]] = None
    claims: Optional[Dict[str, Any]] = None


class EnterpriseAuth:
    """🏢 Sistema de autenticación empresarial"""

    def __init__(self) -> None:
        self.rate_limiter = RateLimiter()
        self.session_manager = SessionManager()
        self.token_validator = TokenValidator()
        self.service_authenticator = ServiceAuthenticator()

    def authenticate_request(self, req: Any) -> UserContext:
        """Autenticar request empresarial"""
        try:
            # Verificar rate limiting
            self.rate_limiter.check_rate_limit(req)

            # Extraer token
            token = self._extract_token(req)

            # Validar token
            token_info = self.token_validator.validate_token(token)

            # Crear contexto de usuario
            user_context = self._create_user_context(token_info, req)

            # Registrar actividad
            self.session_manager.update_session(user_context)

            return user_context

        except (AuthenticationError, AuthorizationError, RateLimitError):
            raise
        except Exception as e:
            logging.error("Error en autenticación empresarial: %s", e)
            raise AuthenticationError("Error de autenticación", 401) from e

    def _extract_token(self, req: Any) -> str:
        """Extraer token del request"""
        auth_header = req.headers.get("Authorization")

        if not auth_header:
            raise AuthenticationError("Falta el token de autorización", 401)

        if not auth_header.startswith("Bearer "):
            raise AuthenticationError("Formato de token inválido", 401)

        token_parts = auth_header.split(" ")
        if len(token_parts) != 2:
            raise AuthenticationError("Formato de token inválido", 401)

        return str(token_parts[1])

    def _create_user_context(self, token_info: TokenInfo, req: Any) -> UserContext:
        """Crear contexto de usuario"""
        claims = token_info.claims or {}

        return UserContext(
            uid=claims.get("uid", ""),
            email=claims.get("email", ""),
            display_name=claims.get("displayName", claims.get("email", "")),
            subscription_status=claims.get("plan", "free"),
            custom_claims=claims.get("custom_claims", {}),
            role=claims.get("role", "user"),
            permissions=claims.get("permissions", []),
            last_active=datetime.now(timezone.utc),
            session_id=claims.get("session_id"),
            ip_address=req.remote_addr,
            user_agent=req.headers.get("User-Agent"),
            auth_method=token_info.token_type,
            security_level=claims.get("security_level", "standard"),
        )


class TokenValidator:
    """🏢 Validador de tokens empresarial"""

    def __init__(self) -> None:
        self.token_cache: Dict[str, Tuple[TokenInfo, float]] = {}
        self.cache_ttl = 300  # 5 minutos

    def validate_token(self, token: str) -> TokenInfo:
        """Validar token con cache"""
        try:
            # Verificar cache
            cached_info = self._get_cached_token(token)
            if cached_info:
                return cached_info

            # Validar token
            token_info = self._validate_token_types(token)

            # Cachear resultado
            self._cache_token(token, token_info)

            return token_info

        except (AuthenticationError, AuthorizationError, RateLimitError):
            raise
        except Exception as e:
            logging.error("Error validando token: %s", e)
            raise AuthenticationError("Token inválido", 401) from e

    def _validate_token_types(self, token: str) -> TokenInfo:
        """Validar diferentes tipos de tokens"""

        # Intentar Firebase primero
        if FIREBASE_AVAILABLE:
            try:
                decoded_token = auth.verify_id_token(token)
                user_record = auth.get_user(decoded_token["uid"])

                return TokenInfo(
                    token=token,
                    token_type="firebase",
                    expires_at=datetime.fromtimestamp(
                        decoded_token["exp"], timezone.utc
                    ),
                    issued_at=datetime.fromtimestamp(
                        decoded_token["iat"], timezone.utc
                    ),
                    issuer=decoded_token["iss"],
                    audience=decoded_token["aud"],
                    claims={
                        "uid": user_record.uid,
                        "email": user_record.email or "",
                        "displayName": user_record.display_name or "",
                        "plan": (
                            user_record.custom_claims.get("plan", "free")
                            if user_record.custom_claims
                            else "free"
                        ),
                        "custom_claims": user_record.custom_claims or {},
                    },
                )

            except (ValueError, KeyError, TypeError) as e:
                logging.info("No es un token Firebase válido: %s", e)

        # Intentar Google Service Account
        if GOOGLE_AUTH_AVAILABLE:
            try:
                # Crear request con typing explícito
                google_request = google_requests.Request()  # type: ignore
                idinfo: Dict[str, Any] = google_id_token.verify_oauth2_token(  # type: ignore
                    token, google_request
                )

                return TokenInfo(
                    token=token,
                    token_type="google_service",
                    expires_at=datetime.fromtimestamp(idinfo["exp"], timezone.utc),
                    issued_at=datetime.fromtimestamp(idinfo["iat"], timezone.utc),
                    issuer=idinfo["iss"],
                    audience=idinfo["aud"],
                    claims={
                        "uid": idinfo.get("sub", ""),
                        "email": idinfo.get("email", ""),
                        "displayName": idinfo.get("email", ""),
                        "plan": "service",
                        "role": "service",
                    },
                )

            except (ValueError, KeyError, TypeError) as e:
                logging.info("No es un token Google válido: %s", e)

        # Intentar JWT personalizado
        if JWT_AVAILABLE:
            try:
                return self._validate_custom_jwt(token)
            except (ValueError, KeyError, TypeError) as e:
                logging.info("No es un JWT personalizado válido: %s", e)

        raise AuthenticationError("Tipo de token no soportado", 401)

    def _validate_custom_jwt(self, token: str) -> TokenInfo:
        """Validar JWT personalizado"""
        try:
            secret = os.getenv("JWT_SECRET", "dev-secret-key")
            if not secret:
                raise AuthenticationError("JWT secret no configurado", 500)

            payload = jwt.decode(
                token, secret, algorithms=["HS256"], options={"verify_exp": True}
            )

            return TokenInfo(
                token=token,
                token_type="custom_jwt",
                expires_at=datetime.fromtimestamp(payload["exp"], timezone.utc),
                issued_at=datetime.fromtimestamp(payload["iat"], timezone.utc),
                issuer=payload.get("iss", "smarwatt"),
                audience=payload.get("aud", "smarwatt-api"),
                claims=payload,
            )

        except jwt.ExpiredSignatureError as e:
            raise AuthenticationError("Token expirado", 401) from e
        except jwt.InvalidTokenError as e:
            raise AuthenticationError("Token JWT inválido", 401) from e
        except Exception as e:
            logging.error("Error validando JWT personalizado: %s", e)
            raise AuthenticationError("Error interno validando token", 500) from e

    def _get_cached_token(self, token: str) -> Optional[TokenInfo]:
        """Obtener token del cache"""
        token_hash = hashlib.sha256(token.encode()).hexdigest()

        if token_hash in self.token_cache:
            cached_info, cached_at = self.token_cache[token_hash]

            # Verificar TTL
            if time.time() - cached_at < self.cache_ttl:
                # Verificar expiración del token
                if cached_info.expires_at > datetime.now(timezone.utc):
                    return cached_info

            # Limpiar cache expirado
            del self.token_cache[token_hash]

        return None

    def _cache_token(self, token: str, token_info: TokenInfo) -> None:
        """Cachear token"""
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        self.token_cache[token_hash] = (token_info, time.time())


class ServiceAuthenticator:
    """🏢 Autenticador de servicios empresarial"""

    def __init__(self) -> None:
        self.service_tokens: Dict[str, Dict[str, Any]] = {}
        self.token_expiry = 3600  # 1 hora

    def generate_service_token(
        self, service_id: str, scopes: Optional[List[str]] = None
    ) -> str:
        """Generar token de servicio"""
        try:
            payload = {
                "service_id": service_id,
                "scopes": scopes or [],
                "iat": datetime.now(timezone.utc),
                "exp": datetime.now(timezone.utc)
                + timedelta(seconds=self.token_expiry),
                "iss": "smarwatt-enterprise",
                "aud": "smarwatt-api",
            }

            secret = current_app.config.get("SERVICE_SECRET_KEY")
            if not secret:
                raise AuthenticationError("Service secret no configurado", 500)

            token = jwt.encode(payload, secret, algorithm="HS256")

            # Registrar token
            self.service_tokens[service_id] = {
                "token": token,
                "created_at": datetime.now(timezone.utc),
                "scopes": scopes or [],
            }

            return token

        except Exception as e:
            logging.error("Error generando token de servicio: %s", e)
            raise AuthenticationError("Error generando token de servicio", 500) from e

    def verify_service_token(self, token: str) -> Dict[str, Any]:
        """Verificar token de servicio"""
        try:
            secret = current_app.config.get("SERVICE_SECRET_KEY")
            if not secret:
                raise AuthenticationError("Service secret no configurado", 500)

            decoded_payload: Dict[str, Any] = jwt.decode(
                token, secret, algorithms=["HS256"]
            )

            # Verificar servicio
            service_id = decoded_payload.get("service_id")
            if not service_id:
                raise AuthenticationError("Token de servicio inválido", 401)

            return decoded_payload

        except jwt.ExpiredSignatureError as e:
            raise AuthenticationError("Token de servicio expirado", 401) from e
        except jwt.InvalidTokenError as e:
            raise AuthenticationError("Token de servicio inválido", 401) from e


class RateLimiter:
    """🏢 Limitador de velocidad empresarial"""

    def __init__(self) -> None:
        self.requests: Dict[str, List[float]] = defaultdict(list)
        self.lock = threading.Lock()

        # Configuración por defecto
        self.default_limits = {
            "requests_per_minute": 100,
            "requests_per_hour": 1000,
            "requests_per_day": 10000,
        }

    def check_rate_limit(self, req: Any) -> None:
        """🏢 Verificar límite de velocidad empresarial"""
        with self.lock:
            # Identificar cliente
            client_id = self._get_client_id(req)

            # 🏢 Obtener contexto de usuario si está disponible
            self._set_user_context_if_available(req)

            # Obtener límites empresariales
            limits = self._get_client_limits(client_id)

            # Verificar límites
            current_time = time.time()

            # Limpiar requests antiguos
            self._cleanup_old_requests(client_id, current_time)

            # Verificar cada límite
            for period, limit in limits.items():
                if self._is_rate_limited(client_id, period, limit, current_time):
                    raise RateLimitError(f"Límite de {period} excedido", 429)

            # Registrar request
            self.requests[client_id].append(current_time)

    def _set_user_context_if_available(self, req: Any) -> None:
        """🏢 Establecer contexto de usuario si está disponible"""
        try:
            # Intentar obtener contexto del usuario desde Flask g
            from flask import g

            if hasattr(g, "user_context") and g.user_context:
                self._current_user_context = g.user_context
            else:
                # Limpiar contexto si no está disponible
                self._current_user_context = None

        except Exception:
            # Si no está disponible Flask g, continuar sin contexto
            self._current_user_context = None

    def _get_client_id(self, req: Any) -> str:
        """Obtener ID del cliente"""
        # Priorizar token de usuario
        auth_header = req.headers.get("Authorization")
        if auth_header:
            try:
                token = auth_header.split(" ")[1]
                return hashlib.sha256(token.encode()).hexdigest()[:16]
            except (IndexError, AttributeError):
                pass

        # Fallback a IP
        return getattr(req, "remote_addr", None) or "unknown"

    def _get_client_limits(self, _client_id: str) -> Dict[str, int]:
        """Obtener límites del cliente"""
        # Implementar límites por usuario/plan en el futuro
        return self.default_limits.copy()

    def _cleanup_old_requests(self, client_id: str, current_time: float) -> None:
        """Limpiar requests antiguos"""
        if client_id not in self.requests:
            return

        # Mantener solo últimas 24 horas
        cutoff_time = current_time - 86400  # 24 horas
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id] if req_time > cutoff_time
        ]

    def _is_rate_limited(
        self, client_id: str, period: str, limit: int, current_time: float
    ) -> bool:
        """Verificar si está limitado"""
        if client_id not in self.requests:
            return False

        # Calcular ventana de tiempo
        if period == "requests_per_minute":
            window = 60
        elif period == "requests_per_hour":
            window = 3600
        elif period == "requests_per_day":
            window = 86400
        else:
            return False

        # Contar requests en ventana
        window_start = current_time - window
        recent_requests = [
            req_time for req_time in self.requests[client_id] if req_time > window_start
        ]

        return len(recent_requests) >= limit


class SessionManager:
    """🏢 Gestor de sesiones empresarial"""

    def __init__(self) -> None:
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.session_ttl = 3600  # 1 hora

    def update_session(self, user_context: UserContext) -> None:
        """Actualizar sesión de usuario"""
        session_id = user_context.session_id or user_context.uid

        self.sessions[session_id] = {
            "user_context": user_context,
            "last_activity": datetime.now(timezone.utc),
            "ip_address": user_context.ip_address,
            "user_agent": user_context.user_agent,
        }

    def get_session(self, session_id: str) -> Optional[UserContext]:
        """Obtener sesión"""
        session = self.sessions.get(session_id)
        if not session:
            return None

        if session and not self._is_session_expired(session):
            user_ctx = session.get("user_context")
            if isinstance(user_ctx, UserContext):
                return user_ctx

        if session_id in self.sessions:
            del self.sessions[session_id]

        return None

    def _is_session_expired(self, session: Dict[str, Any]) -> bool:
        """Verificar si la sesión expiró"""
        last_activity = session.get("last_activity")
        if not isinstance(last_activity, datetime):
            return True

        expiry_time = last_activity + timedelta(seconds=self.session_ttl)
        return bool(datetime.now(timezone.utc) > expiry_time)


# Instancias globales
_enterprise_auth = EnterpriseAuth()
_token_validator = TokenValidator()
_service_authenticator = ServiceAuthenticator()

# TypeVar para decoradores tipados
F = TypeVar("F", bound=Callable[..., Any])


def token_required(f: F) -> F:
    """🏢 Decorador empresarial para proteger rutas"""

    @wraps(f)
    def decorated_function(*args: Any, **kwargs: Any) -> Any:
        # 🌐 EXCLUIR peticiones OPTIONS de autenticación (CORS preflight)
        if request.method == "OPTIONS":
            return f(*args, **kwargs)

        try:
            # Autenticar request
            user_context = _enterprise_auth.authenticate_request(request)

            # Establecer contexto global
            g.user = {
                "uid": user_context.uid,
                "email": user_context.email,
                "displayName": user_context.display_name,
                "subscription_status": user_context.subscription_status,
                "role": user_context.role,
                "permissions": user_context.permissions,
                "security_level": user_context.security_level,
            }
            g.user_context = user_context

            return f(*args, **kwargs)

        except AuthenticationError:
            raise
        except Exception as e:
            logging.error("Error en decorador token_required: %s", e)
            raise AuthenticationError("Error de autenticación", 401) from e

    return cast(F, decorated_function)


def admin_required(f: F) -> F:
    """🏢 Decorador para rutas de administrador"""

    @wraps(f)
    def decorated_function(*args: Any, **kwargs: Any) -> Any:
        # Primero aplicar token_required
        user_context = _enterprise_auth.authenticate_request(request)

        # Verificar si es admin
        if user_context.role != "admin":
            raise AuthorizationError("Acceso de administrador requerido", 403)

        # Establecer contexto
        g.user = {
            "uid": user_context.uid,
            "email": user_context.email,
            "displayName": user_context.display_name,
            "subscription_status": user_context.subscription_status,
            "role": user_context.role,
            "permissions": user_context.permissions,
            "security_level": user_context.security_level,
        }
        g.user_context = user_context

        return f(*args, **kwargs)

    return cast(F, decorated_function)
