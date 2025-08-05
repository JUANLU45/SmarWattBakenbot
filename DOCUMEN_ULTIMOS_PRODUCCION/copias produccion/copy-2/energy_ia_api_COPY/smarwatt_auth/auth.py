# smarwatt_auth/auth.py
# 🏢 AUTENTICACIÓN EMPRESARIAL SMARWATT - CÓDIGO PRINCIPAL

from functools import wraps
from flask import request, g, current_app
from firebase_admin import auth
import logging
import time
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
import jwt  # type: ignore
import hashlib
from collections import defaultdict
import threading

from .exceptions import (
    AppError,
    AuthenticationError,
    AuthorizationError,
    RateLimitError,
)

try:
    from google.oauth2 import id_token as google_id_token  # type: ignore
    from google.auth.transport import requests as google_requests  # type: ignore
except ImportError:
    google_id_token = None
    google_requests = None


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

        return str(auth_header.split(" ")[1])

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
        self.token_cache: Dict[str, Any] = {}
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

        except Exception as e:
            logging.error("Error validando token: %s", e)
            raise AuthenticationError("Token inválido", 401) from e

    def _validate_token_types(self, token: str) -> TokenInfo:
        """Validar diferentes tipos de tokens"""

        # Intentar Firebase primero
        try:
            decoded_token = auth.verify_id_token(token)
            user_record = auth.get_user(decoded_token["uid"])

            return TokenInfo(
                token=token,
                token_type="firebase",
                expires_at=datetime.fromtimestamp(decoded_token["exp"], timezone.utc),
                issued_at=datetime.fromtimestamp(decoded_token["iat"], timezone.utc),
                issuer=decoded_token["iss"],
                audience=decoded_token["aud"],
                claims={
                    "uid": user_record.uid,
                    "email": user_record.email,
                    "displayName": user_record.display_name,
                    "plan": (
                        user_record.custom_claims.get("plan", "free")
                        if user_record.custom_claims
                        else "free"
                    ),
                    "custom_claims": user_record.custom_claims or {},
                },
            )

        except (
            auth.InvalidIdTokenError,
            auth.ExpiredIdTokenError,
            auth.RevokedIdTokenError,
            KeyError,
            ValueError,
        ):
            pass

        # Intentar Google Service Account
        try:
            if google_id_token and google_requests:
                idinfo = google_id_token.verify_oauth2_token(
                    token, google_requests.Request()
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

        except ValueError:
            pass
        except AttributeError:
            pass
        except KeyError:
            pass

        # Intentar JWT personalizado
        try:
            return self._validate_custom_jwt(token)
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, AuthenticationError):
            pass

        raise AuthenticationError("Tipo de token no soportado", 401)

    def _validate_custom_jwt(self, token: str) -> TokenInfo:
        """Validar JWT personalizado"""
        try:
            secret = current_app.config.get("JWT_SECRET_KEY")
            if not secret:
                raise AuthenticationError("JWT secret no configurado", 500)

            payload = jwt.decode(token, secret, algorithms=["HS256"])

            return TokenInfo(
                token=token,
                token_type="custom_jwt",
                expires_at=datetime.fromtimestamp(payload["exp"], timezone.utc),
                issued_at=datetime.fromtimestamp(payload["iat"], timezone.utc),
                issuer=payload.get("iss", "smarwatt"),
                audience=payload.get("aud", "smarwatt-api"),
                claims=payload,
            )

        except jwt.ExpiredSignatureError as exc:
            raise AuthenticationError("Token expirado", 401) from exc
        except jwt.InvalidTokenError as exc:
            raise AuthenticationError("Token JWT inválido", 401) from exc

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
        self.service_tokens: Dict[str, Any] = {}
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

            return str(token)

        except Exception as e:
            logging.error("Error generando token de servicio: %s", e)
            raise AuthenticationError("Error generando token de servicio", 500) from e

    def verify_service_token(self, token: str) -> Dict[str, Any]:
        """Verificar token de servicio"""
        try:
            secret = current_app.config.get("SERVICE_SECRET_KEY")
            if not secret:
                raise AuthenticationError("Service secret no configurado", 500)

            payload = jwt.decode(token, secret, algorithms=["HS256"])

            # Verificar servicio
            service_id = payload.get("service_id")
            if not service_id:
                raise AuthenticationError("Token de servicio inválido", 401)

            if not isinstance(payload, dict):
                raise AuthenticationError("Token de servicio inválido", 401)
            return payload

        except jwt.ExpiredSignatureError as exc:
            raise AuthenticationError("Token de servicio expirado", 401) from exc
        except jwt.InvalidTokenError as exc:
            raise AuthenticationError("Token de servicio inválido", 401) from exc


class RateLimiter:
    """🏢 Limitador de velocidad empresarial"""

    def __init__(self) -> None:
        self.requests: Dict[str, List[float]] = defaultdict(list)
        self.lock = threading.Lock()
        self._current_user_context = None  # Inicializar el atributo aquí

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
            self._set_user_context_if_available()

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

    def _set_user_context_if_available(self) -> None:
        """🏢 Establecer contexto de usuario si está disponible"""
        try:
            # Intentar obtener contexto del usuario desde Flask g
            if hasattr(g, "user_context") and g.user_context:
                self._current_user_context = g.user_context
            else:
                # Limpiar contexto si no está disponible
                self._current_user_context = None

        except (AttributeError, KeyError, TypeError):
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
        return str(req.remote_addr) if req.remote_addr else "unknown"

    def _get_client_limits(self, client_id: str) -> Dict[str, int]:
        """🏢 Obtener límites empresariales del cliente"""
        try:
            # 🔍 Identificar tipo de usuario basado en el token
            user_type = self._identify_user_type(client_id)

            # 🏢 Límites empresariales por tipo de usuario
            if user_type == "registered_user":
                return {
                    "requests_per_minute": 150,  # Usuario registrado
                    "requests_per_hour": 2000,
                    "requests_per_day": 15000,
                }
            elif user_type == "enterprise_user":
                return {
                    "requests_per_minute": 300,  # Usuario empresarial
                    "requests_per_hour": 5000,
                    "requests_per_day": 50000,
                }
            else:
                # Usuario no registrado - límites más restrictivos
                return {
                    "requests_per_minute": 30,
                    "requests_per_hour": 200,
                    "requests_per_day": 1000,
                }

        except (AttributeError, KeyError, TypeError) as e:
            logging.error(
                "Error determinando límites para cliente %s: %s", client_id, e
            )
            # Fallback a límites por defecto
            return self.default_limits

    def _identify_user_type(self, client_id: str) -> str:
        """🏢 Identificar tipo de usuario empresarial"""
        try:
            # Si no tenemos información del token, es usuario no registrado
            if not hasattr(self, "_current_user_context"):
                return "anonymous_user"

            # Obtener contexto del usuario actual si está disponible
            user_context = getattr(self, "_current_user_context", None)

            if user_context:
                # Usuario registrado con rol empresarial
                if user_context.role in ["admin", "enterprise"]:
                    return "enterprise_user"
                # Usuario registrado estándar
                elif user_context.role == "user":
                    return "registered_user"

            # Si el client_id parece ser un hash de token, es usuario registrado
            if len(client_id) == 16 and client_id.isalnum():
                return "registered_user"

            # Por defecto, usuario no registrado
            return "anonymous_user"

        except (AttributeError, KeyError, TypeError) as e:
            logging.error("Error identificando tipo de usuario: %s", e)
            return "anonymous_user"

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
        self.sessions: Dict[str, Any] = {}
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

        # Verificar expiración
        if self._is_session_expired(session):
            del self.sessions[session_id]
            return None

        user_ctx = session["user_context"]
        if isinstance(user_ctx, UserContext):
            return user_ctx
        return None

    def _is_session_expired(self, session: Dict[str, Any]) -> bool:
        """Verificar si la sesión expiró"""
        last_activity = session["last_activity"]
        expiry_time = last_activity + timedelta(seconds=self.session_ttl)

        return bool(datetime.now(timezone.utc) > expiry_time)


# Instancias globales
_enterprise_auth = EnterpriseAuth()
_token_validator = TokenValidator()
_service_authenticator = ServiceAuthenticator()


def token_required(f: Any) -> Any:
    """🏢 Decorador empresarial para proteger rutas"""

    @wraps(f)
    def decorated_function(*args: Any, **kwargs: Any) -> Any:
        # 🌐 EXCLUIR peticiones OPTIONS de autenticación (CORS preflight)
        if request.method == "OPTIONS":
            return f(*args, **kwargs)

        try:
            # Autenticar request
            user_context = _enterprise_auth.authenticate_request(request)

            # Extraer y guardar token en contexto global
            auth_header = request.headers.get("Authorization", "")
            if auth_header.startswith("Bearer "):
                g.token = auth_header.split(" ")[1]
            else:
                g.token = None

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

        except AuthenticationError as e:
            raise e
        except Exception as e:
            logging.error("Error en decorador token_required: %s", e)
            raise AuthenticationError("Error de autenticación", 401) from e

    return decorated_function


def admin_required(f: Any) -> Any:
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

    return decorated_function
