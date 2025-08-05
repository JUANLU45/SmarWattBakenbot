"""
🏢 ENTERPRISE LINKS SERVICE
Servicio empresarial para gestión inteligente de enlaces de Smarwatt
Detecta automáticamente contexto en respuestas y añade enlaces relevantes
"""

import re
import logging
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class SmarwattLink:
    """Modelo de datos para enlaces de Smarwatt"""

    url: str
    title: str
    keywords: List[str]
    context_phrases: List[str]
    priority: int  # 1-10, mayor prioridad = más relevante


class EnterpriseLinkService:
    """
    🏢 Servicio empresarial para gestión inteligente de enlaces

    Funcionalidades:
    - Detección automática de contexto en respuestas
    - Inserción inteligente de enlaces relevantes
    - Análisis semántico de contenido
    - Priorización de enlaces según relevancia
    """

    def __init__(self):
        """Inicializa el servicio con configuración empresarial"""
        self.smarwatt_links = self._initialize_enterprise_links()
        logger.info("🏢 Enterprise Link Service inicializado correctamente")

    def _initialize_enterprise_links(self) -> Dict[str, SmarwattLink]:
        """Inicializa enlaces empresariales con detección inteligente"""
        return {
            "blog": SmarwattLink(
                url="https://smarwatt.com/blog",
                title="Blog de Smarwatt",
                keywords=[
                    "blog",
                    "artículo",
                    "noticia",
                    "información",
                    "consejo",
                    "guía",
                    "actualidad",
                    "tendencia",
                    "aprende",
                    "descubre",
                ],
                context_phrases=[
                    "puedes leer más",
                    "más información",
                    "artículos relacionados",
                    "en nuestro blog",
                    "contenido adicional",
                    "guías detalladas",
                    "consejos útiles",
                    "últimas noticias",
                ],
                priority=8,
            ),
            "dashboard": SmarwattLink(
                url="https://smarwatt.com/dashboard",
                title="Dashboard de Smarwatt",
                keywords=[
                    "dashboard",
                    "panel",
                    "control",
                    "gestión",
                    "monitoreo",
                    "seguimiento",
                    "estadísticas",
                    "métricas",
                    "análisis",
                ],
                context_phrases=[
                    "en tu dashboard",
                    "panel de control",
                    "área personal",
                    "gestionar tu cuenta",
                    "ver estadísticas",
                    "monitorear consumo",
                ],
                priority=9,
            ),
            "calculator": SmarwattLink(
                url="https://smarwatt.com/calculator",
                title="Calculadora de Smarwatt",
                keywords=[
                    "calculadora",
                    "calcular",
                    "estimación",
                    "ahorro",
                    "coste",
                    "precio",
                    "tarifa",
                    "factura",
                    "consumo",
                    "gasto",
                ],
                context_phrases=[
                    "calcula tu ahorro",
                    "estima tu consumo",
                    "calculadora de tarifas",
                    "herramienta de cálculo",
                    "simula tu factura",
                    "estima costes",
                ],
                priority=10,
            ),
            "weather": SmarwattLink(
                url="https://smarwatt.com/weather",
                title="Información Meteorológica - Smarwatt",
                keywords=[
                    "tiempo",
                    "clima",
                    "meteorología",
                    "temperatura",
                    "lluvia",
                    "viento",
                    "solar",
                    "radiación",
                    "pronóstico",
                    "climático",
                ],
                context_phrases=[
                    "condiciones meteorológicas",
                    "información del tiempo",
                    "pronóstico del clima",
                    "datos meteorológicos",
                ],
                priority=7,
            ),
            "contact": SmarwattLink(
                url="https://smarwatt.com/contact",
                title="Contacto - Smarwatt",
                keywords=[
                    "contacto",
                    "contactar",
                    "ayuda",
                    "soporte",
                    "consulta",
                    "pregunta",
                    "asistencia",
                    "comunicar",
                    "escribir",
                    "llamar",
                ],
                context_phrases=[
                    "ponte en contacto",
                    "necesitas ayuda",
                    "más información",
                    "atención al cliente",
                    "servicio técnico",
                    "consulta personalizada",
                    "hablar con nosotros",
                    "resolver dudas",
                ],
                priority=9,
            ),
            "terms": SmarwattLink(
                url="https://smarwatt.com/terms",
                title="Términos y Condiciones - Smarwatt",
                keywords=[
                    "términos",
                    "condiciones",
                    "legal",
                    "contrato",
                    "acuerdo",
                    "política",
                    "uso",
                    "servicio",
                    "normativa",
                ],
                context_phrases=[
                    "términos y condiciones",
                    "política de uso",
                    "acuerdo de servicio",
                    "normativa legal",
                    "condiciones del servicio",
                ],
                priority=5,
            ),
            "privacy": SmarwattLink(
                url="https://smarwatt.com/privacy",
                title="Política de Privacidad - Smarwatt",
                keywords=[
                    "privacidad",
                    "datos",
                    "protección",
                    "gdpr",
                    "información",
                    "personal",
                    "tratamiento",
                    "cookies",
                    "confidencial",
                ],
                context_phrases=[
                    "política de privacidad",
                    "protección de datos",
                    "tratamiento de información",
                    "gestión de datos personales",
                    "privacidad y seguridad",
                ],
                priority=6,
            ),
        }

    def analyze_and_enhance_response(self, response_text: str) -> str:
        """
        Analiza respuesta y sugiere enlaces solo cuando es contextualmente natural

        Args:
            response_text: Texto de respuesta del chatbot

        Returns:
            str: Respuesta con enlaces naturales solo si es muy relevante
        """
        try:
            if not response_text or len(response_text.strip()) < 10:
                return response_text

            # Solo añadir enlaces en casos MUY específicos y naturales
            enhanced_response = self._add_natural_links_if_relevant(response_text)

            return enhanced_response

        except Exception as e:
            logger.error(f"❌ Error analizando respuesta para enlaces: {str(e)}")
            return response_text

    def _add_natural_links_if_relevant(self, response_text: str) -> str:
        """Integra enlaces de forma natural DENTRO del contexto de la conversación"""
        try:
            text_lower = response_text.lower()

            # Si ya hay enlaces, no procesar más
            if "smarwatt.com" in response_text:
                return response_text

            enhanced_response = response_text

            # BLOG: Integración natural cuando se menciona blog o información
            if any(
                phrase in text_lower
                for phrase in ["blog", "más información", "artículos", "puedes leer"]
            ):
                # Reemplazar menciones del blog con enlace integrado
                if (
                    "blog" in text_lower
                    and "smarwatt.com/blog" not in enhanced_response
                ):
                    enhanced_response = enhanced_response.replace(
                        "blog",
                        '<a href="https://smarwatt.com/blog" target="_blank">blog</a>',
                    ).replace(
                        "Blog",
                        '<a href="https://smarwatt.com/blog" target="_blank">Blog</a>',
                    )
                elif (
                    "más información" in enhanced_response
                    and "smarwatt.com/blog" not in enhanced_response
                ):
                    enhanced_response = enhanced_response.replace(
                        "más información",
                        'más información en <a href="https://smarwatt.com/blog" target="_blank">nuestro blog</a>',
                    )
                elif (
                    "artículos" in enhanced_response
                    and "smarwatt.com/blog" not in enhanced_response
                ):
                    enhanced_response = enhanced_response.replace(
                        "artículos",
                        '<a href="https://smarwatt.com/blog" target="_blank">artículos</a>',
                    )

            # CONTACTO: Solo cuando se menciona específicamente
            if any(
                word in text_lower
                for word in ["contacto", "contactar", "ayuda", "soporte"]
            ):
                if (
                    "contacto" in enhanced_response
                    and "smarwatt.com/contact" not in enhanced_response
                ):
                    enhanced_response = enhanced_response.replace(
                        "contacto",
                        '<a href="https://smarwatt.com/contact" target="_blank">contacto</a>',
                    ).replace(
                        "Contacto",
                        '<a href="https://smarwatt.com/contact" target="_blank">Contacto</a>',
                    )
                elif (
                    "contactar" in enhanced_response
                    and "smarwatt.com/contact" not in enhanced_response
                ):
                    enhanced_response = enhanced_response.replace(
                        "contactar",
                        '<a href="https://smarwatt.com/contact" target="_blank">contactar</a>',
                    )
                elif (
                    "ayuda" in enhanced_response
                    and "smarwatt.com/contact" not in enhanced_response
                ):
                    enhanced_response = enhanced_response.replace(
                        "ayuda",
                        '<a href="https://smarwatt.com/contact" target="_blank">ayuda</a>',
                    )

            # CALCULADORA: Solo cuando se menciona cálculos
            if any(
                word in text_lower
                for word in ["calcular", "calculadora", "simular", "herramienta"]
            ):
                if (
                    "calculadora" in enhanced_response
                    and "smarwatt.com/calculator" not in enhanced_response
                ):
                    enhanced_response = enhanced_response.replace(
                        "calculadora",
                        '<a href="https://smarwatt.com/calculator" target="_blank">calculadora</a>',
                    ).replace(
                        "Calculadora",
                        '<a href="https://smarwatt.com/calculator" target="_blank">Calculadora</a>',
                    )
                elif (
                    "calcular" in enhanced_response
                    and "smarwatt.com/calculator" not in enhanced_response
                ):
                    enhanced_response = enhanced_response.replace(
                        "calcular",
                        '<a href="https://smarwatt.com/calculator" target="_blank">calcular</a>',
                    )

            # DASHBOARD: Solo cuando se menciona cuenta/datos
            if any(
                word in text_lower
                for word in ["dashboard", "panel", "cuenta", "datos", "perfil"]
            ):
                if (
                    "dashboard" in enhanced_response
                    and "smarwatt.com/dashboard" not in enhanced_response
                ):
                    enhanced_response = enhanced_response.replace(
                        "dashboard",
                        '<a href="https://smarwatt.com/dashboard" target="_blank">dashboard</a>',
                    ).replace(
                        "Dashboard",
                        '<a href="https://smarwatt.com/dashboard" target="_blank">Dashboard</a>',
                    )
                elif (
                    "mi cuenta" in enhanced_response
                    and "smarwatt.com/dashboard" not in enhanced_response
                ):
                    enhanced_response = enhanced_response.replace(
                        "mi cuenta",
                        '<a href="https://smarwatt.com/dashboard" target="_blank">mi cuenta</a>',
                    )

            # ✨ LIMPIEZA FINAL DE ASTERISCOS PARA RESPUESTA NATURAL
            # Eliminar asteriscos de markdown/formateo que molestan
            enhanced_response = enhanced_response.replace("**", "").replace("*", "")

            return enhanced_response

        except Exception as e:
            logger.error(f"❌ Error integrando enlaces naturales: {str(e)}")
            return response_text

    def _detect_relevant_links(self, text: str) -> List[SmarwattLink]:
        """FUNCIÓN DESHABILITADA - No detectar enlaces automáticamente"""
        return []

    def _calculate_relevance_score(self, text: str, link: SmarwattLink) -> int:
        """FUNCIÓN DESHABILITADA - No calcular relevancia automática"""
        return 0

    def _add_contextual_links(self, response: str, links: List[SmarwattLink]) -> str:
        """FUNCIÓN DESHABILITADA - No añadir enlaces robotizados"""
        return response

    def _format_link_suggestions(self, links: List[SmarwattLink]) -> str:
        """FUNCIÓN DESHABILITADA - No formatear enlaces con asteriscos"""
        return ""

    def get_direct_link(self, link_type: str) -> Optional[str]:
        """Obtiene enlace directo por tipo específico"""
        try:
            if link_type in self.smarwatt_links:
                return self.smarwatt_links[link_type].url
            return None

        except Exception as e:
            logger.error(f"❌ Error obteniendo enlace directo: {str(e)}")
            return None

    def get_enterprise_status(self) -> Dict[str, Any]:
        """Retorna estado empresarial del servicio"""
        try:
            return {
                "service_name": "EnterpriseLinkService",
                "status": "active",
                "links_configured": len(self.smarwatt_links),
                "available_links": list(self.smarwatt_links.keys()),
                "version": "2025_enterprise",
            }

        except Exception as e:
            logger.error(f"❌ Error obteniendo status: {str(e)}")
            return {"status": "error", "error": str(e)}


# 🏢 INSTANCIA SINGLETON EMPRESARIAL
_enterprise_link_service_instance = None


def get_enterprise_link_service() -> EnterpriseLinkService:
    """Factory function para obtener instancia singleton del servicio"""
    global _enterprise_link_service_instance

    if _enterprise_link_service_instance is None:
        _enterprise_link_service_instance = EnterpriseLinkService()
        logger.info("🏢 EnterpriseLinkService singleton inicializado")

    return _enterprise_link_service_instance


logger.info("✅ Módulo EnterpriseLinkService cargado correctamente")
