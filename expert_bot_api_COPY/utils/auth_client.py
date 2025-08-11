# expert_bot_api_COPY/utils/auth_client.py
# 🔐 CLIENTE DE AUTENTICACIÓN PARA COMUNICACIÓN SEGURA SERVICIO-A-SERVICIO

import logging
import google.auth.transport.requests
import google.oauth2.id_token
from utils.error_handlers import AppError

logger = logging.getLogger(__name__)

def get_service_to_service_token(audience_url: str) -> str:
    """
    Genera un token de ID de Google para autenticar llamadas a otros servicios de Cloud Run.
    Esta es la práctica recomendada para una comunicación interna segura.
    
    Args:
        audience_url: La URL del servicio de Cloud Run que se va a invocar.
        
    Returns:
        Un token de ID de Google como una cadena.
        
    Raises:
        AppError: Si no se puede generar el token.
    """
    try:
        auth_req = google.auth.transport.requests.Request()
        token = google.oauth2.id_token.fetch_id_token(auth_req, audience_url)
        
        if not token:
            logger.critical("No se pudo obtener el token de ID de Google para la comunicación entre servicios.")
            raise AppError("No se pudo generar el token de autenticación interna.", 500)
            
        logger.info(f"Token de servicio a servicio generado exitosamente para la audiencia: {audience_url}")
        return token

    except Exception as e:
        logger.critical(f"Error crítico al generar el token de servicio a servicio: {str(e)}", exc_info=True)
        raise AppError(f"Error crítico de autenticación interna: {str(e)}", 500)
