# smarwatt_auth/auth.py
# 🏢 AUTENTICACIÓN EMPRESARIAL SMARWATT - CÓDIGO PRINCIPAL

from functools import wraps
from flask import request, g, current_app
import firebase_admin
from firebase_admin import auth
import logging
import time
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
import jwt
import hashlib
import hmac
import secrets
from collections import defaultdict
import threading

from .exceptions import (
    AppError,
    AuthenticationError,
    AuthorizationError,
    RateLimitError,
)
from google.oauth2 import id_token as google_id_token
from google.auth.transport import requests as google_requests


@dataclass
class UserContext:
    """🏢 Contexto de usuario empresarial"""

    uid: str
    email: str
    display_name: str
    subscription_status: str
    custom_claims: Dict[str, Any] = None
    role: str = "user"
    permissions: List[str] = None
    last_active: datetime = None
    session_id: str = None
    ip_address: str = None
    user_agent: str = None
    auth_method: str = None
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
    scopes: List[str] = None
    claims: Dict[str, Any] = None


class EnterpriseAuth:
    """🏢 Sistema de autenticación empresarial"""

    def __init__(self):
        self.rate_limiter = RateLimiter()
        self.session_manager = SessionManager()
        self.token_validator = TokenValidator()
        self.service_authenticator = ServiceAuthenticator()

    def authenticate_request(self, request) -> UserContext:
        """Autenticar request empresarial"""
        try:
            # Verificar rate limiting
            self.rate_limiter.check_rate_limit(request)

            # Extraer token
            token = self._extract_token(request)

            # Validar token
            token_info = self.token_validator.validate_token(token)

            # Crear contexto de usuario
            user_context = self._create_user_context(token_info, request)

            # Registrar actividad
            self.session_manager.update_session(user_context)

            return user_context

        except Exception as e:
            logging.error(f"Error en autenticación empresarial: {e}")
            raise AuthenticationError("Error de autenticación", 401)

    def _extract_token(self, request) -> str:
        """Extraer token del request"""
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            raise AuthenticationError("Falta el token de autorización", 401)

        if not auth_header.startswith("Bearer "):
            raise AuthenticationError("Formato de token inválido", 401)

        return auth_header.split(" ")[1]

    def _create_user_context(self, token_info: TokenInfo, request) -> UserContext:
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
            ip_address=request.remote_addr,
            user_agent=request.headers.get("User-Agent"),
            auth_method=token_info.token_type,
            security_level=claims.get("security_level", "standard"),
        )


class TokenValidator:
    """🏢 Validador de tokens empresarial"""

    def __init__(self):
        self.token_cache = {}
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
            logging.error(f"Error validando token: {e}")
            raise AuthenticationError("Token inválido", 401)

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

        except Exception:
            pass

        # Intentar Google Service Account
        try:
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

        except Exception:
            pass

        # Intentar JWT personalizado
        try:
            return self._validate_custom_jwt(token)
        except Exception:
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

        except jwt.ExpiredSignatureError:
            raise AuthenticationError("Token expirado", 401)
        except jwt.InvalidTokenError:
            raise AuthenticationError("Token JWT inválido", 401)

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

    def _cache_token(self, token: str, token_info: TokenInfo):
        """Cachear token"""
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        self.token_cache[token_hash] = (token_info, time.time())


class ServiceAuthenticator:
    """🏢 Autenticador de servicios empresarial"""

    def __init__(self):
        self.service_tokens = {}
        self.token_expiry = 3600  # 1 hora

    def generate_service_token(self, service_id: str, scopes: List[str] = None) -> str:
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
            logging.error(f"Error generando token de servicio: {e}")
            raise AuthenticationError("Error generando token de servicio", 500)

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

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthenticationError("Token de servicio expirado", 401)
        except jwt.InvalidTokenError:
            raise AuthenticationError("Token de servicio inválido", 401)


class RateLimiter:
    """🏢 Limitador de velocidad empresarial"""

    def __init__(self):
        self.requests = defaultdict(list)
        self.lock = threading.Lock()

        # Configuración por defecto
        self.default_limits = {
            "requests_per_minute": 100,
            "requests_per_hour": 1000,
            "requests_per_day": 10000,
        }

    def check_rate_limit(self, request):
        """Verificar límite de velocidad"""
        with self.lock:
            # Identificar cliente
            client_id = self._get_client_id(request)

            # Obtener límites
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

    def _get_client_id(self, request) -> str:
        """Obtener ID del cliente"""
        # Priorizar token de usuario
        auth_header = request.headers.get("Authorization")
        if auth_header:
            try:
                token = auth_header.split(" ")[1]
                return hashlib.sha256(token.encode()).hexdigest()[:16]
            except:
                pass

        # Fallback a IP
        return request.remote_addr or "unknown"

    def _get_client_limits(self, client_id: str) -> Dict[str, int]:
        """Obtener límites del cliente basado en su plan y tipo"""
        try:
            # Determinar tipo de usuario para aplicar límites apropiados
            user_type = self._determine_user_type(client_id)

            if user_type == "enterprise_user":
                return {
                    "requests_per_minute": 120,  # Límite alto para empresas
                    "requests_per_hour": 5000,
                    "requests_per_day": 50000,
                }
            elif user_type == "registered_user":
                return {
                    "requests_per_minute": 60,  # Límite medio para usuarios registrados
                    "requests_per_hour": 1000,
                    "requests_per_day": 10000,
                }
            else:  # anonymous_user
                return {
                    "requests_per_minute": 20,  # Límite bajo para usuarios anónimos
                    "requests_per_hour": 200,
                    "requests_per_day": 1000,
                }
        except Exception:
            # Fallback a límites por defecto si hay error
            return self.default_limits

    def _determine_user_type(self, client_id: str) -> str:
        """Determinar el tipo de usuario basado en el client_id"""
        try:
            # Si el client_id proviene de un token JWT válido (hash más largo)
            if len(client_id) >= 16 and client_id != "unknown":
                # Intentar determinar si es empresa o usuario registrado
                # Por simplicidad, asumimos que tokens largos = usuarios registrados
                # En producción, esto debería consultar la base de datos de usuarios

                # Heurística simple: si el client_id contiene patrones de empresa
                if any(
                    pattern in client_id.lower()
                    for pattern in ["enterprise", "company", "corp", "ltd"]
                ):
                    return "enterprise_user"
                else:
                    return "registered_user"
            else:
                # IP address o identificador simple = usuario anónimo
                return "anonymous_user"
        except Exception:
            # En caso de error, asumir usuario anónimo (más restrictivo)
            return "anonymous_user"

    def _cleanup_old_requests(self, client_id: str, current_time: float):
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

    def __init__(self):
        self.sessions = {}
        self.session_ttl = 3600  # 1 hora

    def update_session(self, user_context: UserContext):
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

        return session["user_context"]

    def _is_session_expired(self, session: Dict[str, Any]) -> bool:
        """Verificar si la sesión expiró"""
        last_activity = session["last_activity"]
        expiry_time = last_activity + timedelta(seconds=self.session_ttl)

        return datetime.now(timezone.utc) > expiry_time


# Instancias globales
_enterprise_auth = EnterpriseAuth()
_token_validator = TokenValidator()
_service_authenticator = ServiceAuthenticator()


def token_required(f):
    """🏢 Decorador empresarial para proteger rutas"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
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

        except AuthenticationError as e:
            raise e
        except Exception as e:
            logging.error(f"Error en decorador token_required: {e}")
            raise AuthenticationError("Error de autenticación", 401)

    return decorated_function


def admin_required(f):
    """🏢 Decorador para rutas de administrador"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
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
