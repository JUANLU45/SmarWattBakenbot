# energy_ia_api_COPY/app/services/generative_chat_service.py
# 🏢 SERVICIO DE CHAT GENERATIVO EMPRESARIAL - REFINADO Y OPTIMIZADO

import logging
import json
import re
from typing import Dict, Any, Optional
from flask import current_app
import google.generativeai as genai
from utils.error_handlers import AppError
from app.services.enterprise_links_service import get_enterprise_link_service

logger = logging.getLogger(__name__)

class EnterpriseGenerativeChatService:
    """
    Gestiona conversaciones con el modelo Gemini, aplicando personalización avanzada,
    análisis de sentimiento y un sistema de enlaces inteligente.
    """

    def __init__(self) -> None:
        self.links_service = get_enterprise_link_service()
        self._initialize_gemini_model()
        logger.info("✅ EnterpriseGenerativeChatService inicializado con IA refinada.")

    def _initialize_gemini_model(self) -> None:
        """Inicializa el modelo Gemini con configuración e instrucciones de sistema mejoradas."""
        try:
            gemini_api_key = current_app.config.get("GEMINI_API_KEY")
            if not gemini_api_key:
                raise AppError("Clave API de Gemini no configurada.", 500)

            genai.configure(api_key=gemini_api_key)
            self.system_instruction = self._build_enterprise_system_instruction()
            self.model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config={"temperature": 0.3, "max_output_tokens": 800},
                # Safety settings simplificados para claridad
            )
        except Exception as e:
            logger.error(f"❌ Error inicializando Gemini: {str(e)}")
            raise AppError(f"Error inicializando servicio de chat: {str(e)}", 500)

    def _build_enterprise_system_instruction(self) -> str:
        """Construye las instrucciones de sistema, ahora incluyendo la capacidad de usar enlaces."""
        return (
            "Eres WattBot, un especialista en energía de SmarWatt. Tu tono es natural, experto y cercano.\n"
            "Tus capacidades clave son:\n"
            "1.  **Análisis Personalizado:** Usas los datos de la factura y perfil del usuario (consumo, tarifa, coste) para dar respuestas y cálculos precisos.\n"
            "2.  **Contexto Sutil:** No abrumas al usuario con sus datos. En un saludo, sé casual. En una consulta técnica, usa todos los detalles que tienes.\n"
            "3.  **Sistema de Enlaces:** Tienes acceso a una base de datos de enlaces útiles. Si el usuario pide 'ayuda', 'más información' o 'artículos', puedes buscar y proporcionar estos enlaces para enriquecer tu respuesta.\n"
            "4.  **No Redundancia:** Nunca pides información que ya se te ha proporcionado en el contexto, especialmente el código postal para recomendaciones.\n"
            "Tu objetivo es ser el asistente energético más útil y natural del mundo."
        )

    def send_message(self, chat_session: Any, user_message: str, user_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Procesa un mensaje de usuario, enriquece el contexto y genera una respuesta inteligente."""
        try:
            enhanced_prompt = self._build_enhanced_prompt(user_message, user_context)
            
            # La instrucción del sistema ahora se pasa directamente en la llamada a Gemini.
            full_prompt = [
                {'role': 'user', 'parts': [self.system_instruction, enhanced_prompt]}
            ]

            response = chat_session.send_message(full_prompt)
            
            # El historial se gestiona fuera, aquí solo procesamos un turno.
            
            final_response = self._add_links_if_user_requests(user_message, response.text)
            final_natural_response = self._make_response_natural(final_response)

            return {
                "response_text": final_natural_response,
                # El historial se devuelve vacío para que el cliente lo gestione.
                "chat_history": [], 
            }
        except Exception as e:
            logger.error(f"❌ Error procesando mensaje en generative_chat_service: {str(e)}", exc_info=True)
            return {"response_text": "Lo siento, estoy teniendo dificultades técnicas. Por favor, inténtalo de nuevo más tarde.", "chat_history": []}

    def _build_enhanced_prompt(self, user_message: str, user_context: Optional[Dict[str, Any]]) -> str:
        """Construye el prompt final para Gemini, añadiendo contexto e instrucciones sutiles."""
        context_parts = ["=== CONTEXTO DEL USUARIO ==="]

        if user_context:
            context_parts.append(self._build_user_context_prompt(user_context))
            data_completeness = self._calculate_data_completeness(user_context)

            # Instrucción sutil para usuarios con pocos datos
            if data_completeness < 50 and self._is_personal_analysis_request(user_message):
                context_parts.append("\n=== INSTRUCCIÓN ADICIONAL ===")
                context_parts.append(
                    "SUGERENCIA: Responde a la pregunta actual. Adicionalmente, menciona de forma sutil y amable que si el usuario proporcionara más detalles (como una factura de luz o datos manuales), podrías ofrecerle un análisis y recomendaciones mucho más precisos y personalizados."
                )
        else:
             context_parts.append("Usuario sin datos de consumo registrados.")
             if self._is_personal_analysis_request(user_message):
                context_parts.append("\n=== INSTRUCCIÓN ADICIONAL ===")
                context_parts.append(
                    "SUGERENCIA: El usuario está pidiendo un análisis personal pero no tenemos datos. Explícale amablemente qué tipo de información necesitarías (subir una factura o introducir datos manualmente) para poder ayudarle con recomendaciones a medida."
                )


        context_parts.append(f"\n=== PREGUNTA DEL USUARIO ===\n{user_message}")
        return "\n".join(context_parts)

    def _build_user_context_prompt(self, user_context: Dict[str, Any]) -> str:
        """Formatea el contexto del usuario para el prompt."""
        parts = []
        if user_context.get("user_name"):
            parts.append(f"Nombre: {user_context['user_name']}")
        
        invoice = user_context.get("last_invoice")
        if invoice and invoice.get("kwh_consumidos"):
            parts.append(f"Último consumo mensual: {invoice['kwh_consumidos']} kWh")
            parts.append(f"Coste de la última factura: {invoice.get('coste_total', 'N/A')}€")
            if invoice.get("comercializadora"):
                parts.append(f"Comercializadora: {invoice['comercializadora']}")
        
        return " | ".join(parts) if parts else "Sin datos de consumo disponibles."

    def _calculate_data_completeness(self, user_context: Optional[Dict[str, Any]]) -> float:
        """Calcula un score de completitud de datos (0-100)."""
        if not user_context: return 0
        score = 0
        if user_context.get("user_name"): score += 20
        if user_context.get("last_invoice", {}).get("kwh_consumidos"): score += 50
        if user_context.get("last_invoice", {}).get("comercializadora"): score += 30
        return min(100, score)

    def _is_personal_analysis_request(self, user_message: str) -> bool:
        """Determina si el usuario está pidiendo un análisis personal."""
        keywords = ["mi factura", "mi consumo", "cuánto gasto", "qué ahorro", "recomiéndame"]
        return any(keyword in user_message.lower() for keyword in keywords)

    def _add_links_if_user_requests(self, user_message: str, response_text: str) -> str:
        """Añade enlaces del sistema de enlaces si el usuario los pide."""
        help_keywords = ["ayuda", "más información", "artículo", "enlace", "calculadora"]
        if any(keyword in user_message.lower() for keyword in help_keywords):
            return self.links_service.analyze_and_enhance_response(response_text, user_message)
        return response_text

    def _make_response_natural(self, response_text: str) -> str:
        """Limpia la respuesta de Gemini para que sea más natural."""
        # Elimina asteriscos y espacios extra
        return re.sub(r'\s+', ' ', response_text.replace("*", "")).strip()

# Factory para mantener una única instancia del servicio
_enterprise_chat_service_instance = None

def get_enterprise_chat_service():
    global _enterprise_chat_service_instance
    if _enterprise_chat_service_instance is None:
        _enterprise_chat_service_instance = EnterpriseGenerativeChatService()
    return _enterprise_chat_service_instance
