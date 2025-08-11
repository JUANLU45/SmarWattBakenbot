# energy_ia_api_COPY/utils/security.py
# 🔐 MÓDULO DE SEGURIDAD PARA LA VALIDACIÓN DE TOKENS INTERNOS

import logging
from functools import wraps
from flask import request, current_app
from google.oauth2 import id_token
from google.auth.transport import requests

from .error_handlers import AppError

logger = logging.getLogger(__name__)

def internal_auth_required(func):
    """
    Decorador para proteger endpoints que solo deben ser llamados por otros
    servicios de Google Cloud, validando el token de ID firmado por Google.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            logger.warning("Intento de acceso interno sin cabecera de autenticación.")
            raise AppError("No autorizado: Falta token de autenticación.", 401)

        token = auth_header.split("Bearer ")[1]
        
        try:
            # La audiencia debe ser la URL del servicio que recibe la llamada.
            audience = current_app.config.get("SERVICE_URL") # Necesitarás configurar esto
            if not audience:
                 # Como fallback, intenta construir la URL desde la petición.
                 audience = request.url_root.rstrip('/')

            # id_token.verify_oauth2_token validará la firma, la expiración y la audiencia.
            id_token.verify_oauth2_token(token, requests.Request(), audience)
            
            logger.info(f"Acceso interno autenticado correctamente para el endpoint: {request.path}")
            return func(*args, **kwargs)

        except ValueError as e:
            logger.error(f"Error de validación de token interno: {str(e)}", exc_info=True)
            raise AppError("No autorizado: Token inválido.", 401)
        except Exception as e:
            logger.error(f"Error inesperado durante la autenticación interna: {str(e)}", exc_info=True)
            raise AppError("Error interno de autenticación.", 500)
            
    return wrapper
