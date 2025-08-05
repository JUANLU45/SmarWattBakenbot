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
                title="El Ladrón de tu Factura - Calculadora de Consumo Eléctrico",
                keywords=[
                    "calculadora",
                    "calcular",
                    "consumo",
                    "eléctrico",
                    "electrodomésticos",
                    "aparatos",
                    "ladrón",
                    "factura",
                    "coste",
                    "gasto",
                    "ahorro",
                    "kwh",
                    "potencia",
                    "watts",
                ],
                context_phrases=[
                    "calcula el consumo",
                    "qué aparato consume más",
                    "coste de electrodomésticos",
                    "el ladrón de tu factura",
                    "calculadora de consumo",
                    "gasto de aparatos",
                    "cuánto consume mi nevera",
                    "aparatos que más gastan",
                ],
                priority=10,
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

    def analyze_and_enhance_response(
        self,
        response_text: str,
        user_message: str = "",
        weather_data: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Analiza respuesta y añade enlaces SOLO cuando el usuario los pide específicamente
        o en contextos MUY específicos

        Args:
            response_text: Texto de respuesta del chatbot
            user_message: Mensaje original del usuario
            weather_data: Datos meteorológicos reales de OpenWeatherMap (opcional)

        Returns:
            str: Respuesta con enlaces HTML con iconos solo si es explícitamente solicitado
        """
        try:
            if not response_text or len(response_text.strip()) < 10:
                return response_text

            # Solo añadir enlaces cuando el usuario los pida EXPLÍCITAMENTE
            enhanced_response = self._add_contextual_links_if_requested(
                response_text, user_message, weather_data
            )

            return enhanced_response

        except Exception as e:
            logger.error(f"❌ Error analizando respuesta para enlaces: {str(e)}")
            return response_text

    def _add_contextual_links_if_requested(
        self,
        response_text: str,
        user_message: str,
        weather_data: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Añade enlaces ÚNICAMENTE cuando:
        1. El usuario pide explícitamente un enlace
        2. En contextos muy específicos como recomendar artículos sobre placas solares
        """
        try:
            user_lower = user_message.lower()
            response_lower = response_text.lower()

            # Si ya hay enlaces, no procesar más
            if "smarwatt.com" in response_text:
                return response_text

            enhanced_response = response_text

            # 1. ENLACES EXPLÍCITOS - Usuario pide directamente
            if any(
                phrase in user_lower
                for phrase in [
                    "enlace al blog",
                    "enlace del blog",
                    "link del blog",
                    "página del blog",
                    "enlace de contacto",
                    "enlace del contacto",
                    "página de contacto",
                    "enlace a la calculadora",
                    "enlace del calculadora",
                    "página calculadora",
                ]
            ):
                enhanced_response = self._add_requested_link(
                    enhanced_response, user_lower
                )

            # 2. CONTEXTOS ESPECÍFICOS - Solo para recomendaciones específicas
            elif any(
                phrase in response_lower
                for phrase in [
                    "te recomiendo leer",
                    "puedes consultar nuestro artículo",
                    "tenemos información detallada",
                    "encontrarás más detalles",
                ]
            ) and any(
                topic in user_lower
                for topic in [
                    "placas solares",
                    "paneles solares",
                    "energía solar",
                    "instalación solar",
                ]
            ):
                # Solo para artículos sobre energía solar
                enhanced_response = self._add_blog_recommendation(enhanced_response)

            # 3. CONTEXTOS ESPECÍFICOS - Calculadora de consumo eléctrico
            elif any(
                phrase in user_lower
                for phrase in [
                    "cuánto consume",
                    "cuánto gasta",
                    "consumo de",
                    "gasto de",
                    "aparato que más consume",
                    "electrodoméstico que más gasta",
                    "calcular consumo",
                    "calcular gasto",
                ]
            ) and any(
                response_phrase in response_lower
                for response_phrase in [
                    "puedes usar nuestra calculadora",
                    "te recomiendo usar la calculadora",
                    "con nuestra herramienta",
                    "para un cálculo exacto",
                ]
            ):
                # Solo para consultas sobre consumo de aparatos
                enhanced_response = self._add_consumption_calculator_recommendation(
                    enhanced_response
                )

            # 4. CONTEXTOS ESPECÍFICOS - Información meteorológica y clima
            elif (
                any(
                    phrase in user_lower
                    for phrase in [
                        "tiempo",
                        "clima",
                        "temperatura",
                        "lluvia",
                        "calor",
                        "frío",
                        "meteorología",
                        "pronóstico",
                    ]
                )
                and weather_data
            ):
                # Detectar ubicación específica en mensaje del usuario
                user_location = self._detect_location_in_message(user_message)
                if user_location:
                    # Actualizar datos meteorológicos con ubicación detectada
                    enhanced_weather_data = weather_data.copy()
                    enhanced_weather_data["location"] = user_location
                    enhanced_response = self._add_weather_context_enhancement(
                        enhanced_response, enhanced_weather_data
                    )
                else:
                    # Solo cuando hay datos meteorológicos reales disponibles
                    enhanced_response = self._add_weather_context_enhancement(
                        enhanced_response, weather_data
                    )

            return enhanced_response

        except Exception as e:
            logger.error(f"❌ Error añadiendo enlaces contextuales: {str(e)}")
            return response_text

    def _add_requested_link(self, response_text: str, user_request: str) -> str:
        """Añade el enlace específico que el usuario pidió con icono y 'pinche aquí'"""
        try:
            if "blog" in user_request:
                link_html = """<br><br><a href="https://smarwatt.com/blog" target="_blank" style="color: #2563eb; text-decoration: none; font-weight: bold;">
📝 Blog de Smarwatt - <span style="text-decoration: underline;">pinche aquí</span>
</a>"""
                return response_text + link_html

            elif "contact" in user_request or "contacto" in user_request:
                link_html = """<br><br><a href="https://smarwatt.com/contact" target="_blank" style="color: #2563eb; text-decoration: none; font-weight: bold;">
📞 Contacto - <span style="text-decoration: underline;">pinche aquí</span>
</a>"""
                return response_text + link_html

            elif "calculadora" in user_request or "calculator" in user_request:
                link_html = """<br><br><a href="https://smarwatt.com/calculator" target="_blank" style="color: #2563eb; text-decoration: none; font-weight: bold;">
🧮 El Ladrón de tu Factura - <span style="text-decoration: underline;">pinche aquí</span>
</a>"""
                return response_text + link_html

            return response_text

        except Exception as e:
            logger.error(f"❌ Error añadiendo enlace solicitado: {str(e)}")
            return response_text

    def _add_blog_recommendation(self, response_text: str) -> str:
        """Añade enlace al blog solo cuando se recomienda un artículo específico"""
        try:
            link_html = """<br><br><a href="https://smarwatt.com/blog" target="_blank" style="color: #2563eb; text-decoration: none; font-weight: bold;">
📝 Ver artículo completo - <span style="text-decoration: underline;">pinche aquí</span>
</a>"""
            return response_text + link_html

        except Exception as e:
            logger.error(f"❌ Error añadiendo recomendación de blog: {str(e)}")
            return response_text

    def _add_consumption_calculator_recommendation(self, response_text: str) -> str:
        """Añade enlace a la calculadora de consumo solo cuando se habla de consumo de aparatos"""
        try:
            link_html = """<br><br><a href="https://smarwatt.com/calculator" target="_blank" style="color: #2563eb; text-decoration: none; font-weight: bold;">
🧮 Usar El Ladrón de tu Factura - <span style="text-decoration: underline;">pinche aquí</span>
</a>"""
            return response_text + link_html

        except Exception as e:
            logger.error(f"❌ Error añadiendo recomendación de calculadora: {str(e)}")
            return response_text

    def _add_weather_context_enhancement(
        self, response_text: str, weather_data: Dict[str, Any]
    ) -> str:
        """
        Añade información meteorológica real contextualizada para energía
        Usa datos reales de OpenWeatherMap API disponibles en el sistema
        """
        try:
            if not weather_data:
                return response_text

            # Extraer datos meteorológicos verificados del sistema
            temp = weather_data.get("temp", weather_data.get("temperature"))
            humidity = weather_data.get("humidity")
            description = weather_data.get(
                "description", weather_data.get("weather_description")
            )
            location = weather_data.get("location", "Madrid,ES")

            # Obtener información geográfica específica
            city_info = self._extract_geographic_context(location)

            # Construir información meteorológica contextualizada para energía
            weather_info = []

            if temp is not None:
                # Contextualizar temperatura para consumo energético con ubicación específica
                temp_celsius = float(temp)
                if temp_celsius < 15:
                    impact = f"con el frío {city_info['adjective']}, calefacción puede aumentar el consumo 40-60%"
                elif temp_celsius > 25:
                    impact = f"con el calor {city_info['adjective']}, aire acondicionado puede aumentar el consumo 30-50%"
                else:
                    impact = f"temperatura ideal en {city_info['name']} para ahorro energético"

                weather_info.append(
                    f"🌡️ **{city_info['name']}: {temp_celsius:.1f}°C** - {impact}"
                )

            if humidity is not None:
                # Contextualizar humedad para consumo energético con ubicación específica
                humidity_percent = float(humidity)
                if humidity_percent > 70:
                    humidity_impact = f"la alta humedad {city_info['adjective']} puede requerir deshumidificador"
                elif humidity_percent < 30:
                    humidity_impact = f"la baja humedad {city_info['adjective']} puede requerir humidificador"
                else:
                    humidity_impact = f"humedad óptima en {city_info['name']}"

                weather_info.append(
                    f"💧 **{city_info['name']}: {humidity_percent}%** - {humidity_impact}"
                )

            if description:
                # Contextualizar condiciones climáticas para energía con ubicación específica
                desc_lower = str(description).lower()
                if any(word in desc_lower for word in ["lluvia", "nublado", "oscuro"]):
                    lighting_impact = f"con el cielo {city_info['adjective']}, mayor uso de iluminación recomendado"
                elif any(word in desc_lower for word in ["sol", "despejado", "claro"]):
                    lighting_impact = f"aprovecha el sol de {city_info['name']} para ahorrar en iluminación"
                else:
                    lighting_impact = f"condiciones normales en {city_info['name']}"

                weather_info.append(
                    f"☀️ **{city_info['name']}: {description}** - {lighting_impact}"
                )

            if weather_info:
                weather_enhancement = f"""<br><br>🌤️ **Información meteorológica para optimizar tu consumo energético:**<br>
{chr(10).join(weather_info)}"""
                return response_text + weather_enhancement

            return response_text

        except Exception as e:
            logger.error(f"❌ Error añadiendo contexto meteorológico: {str(e)}")
            return response_text

    def _extract_geographic_context(self, location: str) -> Dict[str, str]:
        """
        Extrae contexto geográfico real desde ubicación o código postal
        Maneja ciudades, pueblos y códigos postales españoles reales
        """
        try:
            if not location:
                return {"name": "Madrid", "adjective": "madrileño", "region": "Madrid"}

            location_clean = location.upper().replace(",ES", "").strip()

            # Mapeo REAL de códigos postales españoles por rangos (datos oficiales)
            postal_ranges = {
                # Madrid (28xxx)
                range(28000, 28999): {
                    "name": "Madrid",
                    "adjective": "madrileño",
                    "region": "Madrid",
                },
                # Barcelona (08xxx)
                range(8000, 8999): {
                    "name": "Barcelona",
                    "adjective": "barcelonés",
                    "region": "Cataluña",
                },
                # Valencia (46xxx)
                range(46000, 46999): {
                    "name": "Valencia",
                    "adjective": "valenciano",
                    "region": "Valencia",
                },
                # Sevilla (41xxx)
                range(41000, 41999): {
                    "name": "Sevilla",
                    "adjective": "sevillano",
                    "region": "Andalucía",
                },
                # Zaragoza (50xxx)
                range(50000, 50999): {
                    "name": "Zaragoza",
                    "adjective": "zaragozano",
                    "region": "Aragón",
                },
                # Málaga (29xxx)
                range(29000, 29999): {
                    "name": "Málaga",
                    "adjective": "malagueño",
                    "region": "Andalucía",
                },
                # Murcia (30xxx)
                range(30000, 30999): {
                    "name": "Murcia",
                    "adjective": "murciano",
                    "region": "Murcia",
                },
                # Palma (07xxx)
                range(7000, 7999): {
                    "name": "Palma",
                    "adjective": "palmesano",
                    "region": "Baleares",
                },
                # Las Palmas (35xxx)
                range(35000, 35999): {
                    "name": "Las Palmas",
                    "adjective": "palmense",
                    "region": "Canarias",
                },
                # Bilbao (48xxx)
                range(48000, 48999): {
                    "name": "Bilbao",
                    "adjective": "bilbaíno",
                    "region": "País Vasco",
                },
                # Alicante (03xxx)
                range(3000, 3999): {
                    "name": "Alicante",
                    "adjective": "alicantino",
                    "region": "Valencia",
                },
                # Córdoba (14xxx)
                range(14000, 14999): {
                    "name": "Córdoba",
                    "adjective": "cordobés",
                    "region": "Andalucía",
                },
                # Valladolid (47xxx)
                range(47000, 47999): {
                    "name": "Valladolid",
                    "adjective": "vallisoletano",
                    "region": "Castilla y León",
                },
                # Vigo (36xxx)
                range(36000, 36999): {
                    "name": "Vigo",
                    "adjective": "vigués",
                    "region": "Galicia",
                },
                # Gijón (33xxx)
                range(33000, 33999): {
                    "name": "Gijón",
                    "adjective": "gijonés",
                    "region": "Asturias",
                },
                # Granada (18xxx)
                range(18000, 18999): {
                    "name": "Granada",
                    "adjective": "granadino",
                    "region": "Andalucía",
                },
                # Vitoria (01xxx)
                range(1000, 1999): {
                    "name": "Vitoria",
                    "adjective": "vitoriano",
                    "region": "País Vasco",
                },
                # A Coruña (15xxx)
                range(15000, 15999): {
                    "name": "A Coruña",
                    "adjective": "coruñés",
                    "region": "Galicia",
                },
                # Elche (03xxx - específico)
                range(3200, 3299): {
                    "name": "Elche",
                    "adjective": "ilicitano",
                    "region": "Valencia",
                },
                # Oviedo (33xxx - específico)
                range(33000, 33099): {
                    "name": "Oviedo",
                    "adjective": "ovetense",
                    "region": "Asturias",
                },
                # Santa Cruz (38xxx)
                range(38000, 38999): {
                    "name": "Santa Cruz de Tenerife",
                    "adjective": "chicharrero",
                    "region": "Canarias",
                },
                # Pamplona (31xxx)
                range(31000, 31999): {
                    "name": "Pamplona",
                    "adjective": "pamplonés",
                    "region": "Navarra",
                },
                # Almería (04xxx)
                range(4000, 4999): {
                    "name": "Almería",
                    "adjective": "almeriense",
                    "region": "Andalucía",
                },
                # San Sebastián (20xxx)
                range(20000, 20999): {
                    "name": "San Sebastián",
                    "adjective": "donostiarra",
                    "region": "País Vasco",
                },
                # Santander (39xxx)
                range(39000, 39999): {
                    "name": "Santander",
                    "adjective": "santanderino",
                    "region": "Cantabria",
                },
                # León (24xxx)
                range(24000, 24999): {
                    "name": "León",
                    "adjective": "leonés",
                    "region": "Castilla y León",
                },
                # Burgos (09xxx)
                range(9000, 9999): {
                    "name": "Burgos",
                    "adjective": "burgalés",
                    "region": "Castilla y León",
                },
                # Salamanca (37xxx)
                range(37000, 37999): {
                    "name": "Salamanca",
                    "adjective": "salmantino",
                    "region": "Castilla y León",
                },
                # Cáceres (10xxx)
                range(10000, 10999): {
                    "name": "Cáceres",
                    "adjective": "cacereño",
                    "region": "Extremadura",
                },
                # Badajoz (06xxx)
                range(6000, 6999): {
                    "name": "Badajoz",
                    "adjective": "pacense",
                    "region": "Extremadura",
                },
                # Toledo (45xxx)
                range(45000, 45999): {
                    "name": "Toledo",
                    "adjective": "toledano",
                    "region": "Castilla-La Mancha",
                },
                # Ciudad Real (13xxx)
                range(13000, 13999): {
                    "name": "Ciudad Real",
                    "adjective": "ciudadrealeño",
                    "region": "Castilla-La Mancha",
                },
                # Albacete (02xxx)
                range(2000, 2999): {
                    "name": "Albacete",
                    "adjective": "albaceteño",
                    "region": "Castilla-La Mancha",
                },
                # Cuenca (16xxx)
                range(16000, 16999): {
                    "name": "Cuenca",
                    "adjective": "conquense",
                    "region": "Castilla-La Mancha",
                },
                # Guadalajara (19xxx)
                range(19000, 19999): {
                    "name": "Guadalajara",
                    "adjective": "guadalajareño",
                    "region": "Castilla-La Mancha",
                },
                # Ávila (05xxx)
                range(5000, 5999): {
                    "name": "Ávila",
                    "adjective": "abulense",
                    "region": "Castilla y León",
                },
                # Segovia (40xxx)
                range(40000, 40999): {
                    "name": "Segovia",
                    "adjective": "segoviano",
                    "region": "Castilla y León",
                },
                # Soria (42xxx)
                range(42000, 42999): {
                    "name": "Soria",
                    "adjective": "soriano",
                    "region": "Castilla y León",
                },
                # Palencia (34xxx)
                range(34000, 34999): {
                    "name": "Palencia",
                    "adjective": "palentino",
                    "region": "Castilla y León",
                },
                # Zamora (49xxx)
                range(49000, 49999): {
                    "name": "Zamora",
                    "adjective": "zamorano",
                    "region": "Castilla y León",
                },
                # Huelva (21xxx)
                range(21000, 21999): {
                    "name": "Huelva",
                    "adjective": "onubense",
                    "region": "Andalucía",
                },
                # Cádiz (11xxx)
                range(11000, 11999): {
                    "name": "Cádiz",
                    "adjective": "gaditano",
                    "region": "Andalucía",
                },
                # Jaén (23xxx)
                range(23000, 23999): {
                    "name": "Jaén",
                    "adjective": "jiennense",
                    "region": "Andalucía",
                },
                # Logroño (26xxx)
                range(26000, 26999): {
                    "name": "Logroño",
                    "adjective": "logroñés",
                    "region": "La Rioja",
                },
                # Huesca (22xxx)
                range(22000, 22999): {
                    "name": "Huesca",
                    "adjective": "oscense",
                    "region": "Aragón",
                },
                # Teruel (44xxx)
                range(44000, 44999): {
                    "name": "Teruel",
                    "adjective": "turolense",
                    "region": "Aragón",
                },
                # Castellón (12xxx)
                range(12000, 12999): {
                    "name": "Castellón",
                    "adjective": "castellonense",
                    "region": "Valencia",
                },
                # Tarragona (43xxx)
                range(43000, 43999): {
                    "name": "Tarragona",
                    "adjective": "tarraconense",
                    "region": "Cataluña",
                },
                # Lleida (25xxx)
                range(25000, 25999): {
                    "name": "Lleida",
                    "adjective": "leridano",
                    "region": "Cataluña",
                },
                # Girona (17xxx)
                range(17000, 17999): {
                    "name": "Girona",
                    "adjective": "gerundense",
                    "region": "Cataluña",
                },
                # Lugo (27xxx)
                range(27000, 27999): {
                    "name": "Lugo",
                    "adjective": "lucense",
                    "region": "Galicia",
                },
                # Ourense (32xxx)
                range(32000, 32999): {
                    "name": "Ourense",
                    "adjective": "ourensano",
                    "region": "Galicia",
                },
                # Pontevedra (36xxx - específico para ciudad)
                range(36200, 36299): {
                    "name": "Pontevedra",
                    "adjective": "pontevedrés",
                    "region": "Galicia",
                },
                # Ceuta (51xxx) - Ciudad Autónoma
                range(51000, 51999): {
                    "name": "Ceuta",
                    "adjective": "ceutí",
                    "region": "Ceuta",
                },
                # Melilla (52xxx) - Ciudad Autónoma
                range(52000, 52999): {
                    "name": "Melilla",
                    "adjective": "melillense",
                    "region": "Melilla",
                },
            }

            # Detectar si es código postal numérico
            if location_clean.isdigit() and len(location_clean) == 5:
                postal_code = int(location_clean)
                for code_range, city_info in postal_ranges.items():
                    if postal_code in code_range:
                        return city_info

                # Si no encuentra rango específico, usar primer dígito para provincia
                first_digit = int(location_clean[0])
                province_mapping = {
                    1: {"name": "Álava", "adjective": "alavés", "region": "País Vasco"},
                    2: {
                        "name": "Albacete",
                        "adjective": "albaceteño",
                        "region": "Castilla-La Mancha",
                    },
                    3: {
                        "name": "Alicante",
                        "adjective": "alicantino",
                        "region": "Valencia",
                    },
                    4: {
                        "name": "Almería",
                        "adjective": "almeriense",
                        "region": "Andalucía",
                    },
                    5: {
                        "name": "Ávila",
                        "adjective": "abulense",
                        "region": "Castilla y León",
                    },
                }
                return province_mapping.get(
                    first_digit,
                    {"name": "Madrid", "adjective": "madrileño", "region": "Madrid"},
                )

            # Mapeo directo de nombres de ciudades
            city_names = {
                "MADRID": {
                    "name": "Madrid",
                    "adjective": "madrileño",
                    "region": "Madrid",
                },
                "BARCELONA": {
                    "name": "Barcelona",
                    "adjective": "barcelonés",
                    "region": "Cataluña",
                },
                "VALENCIA": {
                    "name": "Valencia",
                    "adjective": "valenciano",
                    "region": "Valencia",
                },
                "SEVILLA": {
                    "name": "Sevilla",
                    "adjective": "sevillano",
                    "region": "Andalucía",
                },
                "ZARAGOZA": {
                    "name": "Zaragoza",
                    "adjective": "zaragozano",
                    "region": "Aragón",
                },
                "MÁLAGA": {
                    "name": "Málaga",
                    "adjective": "malagueño",
                    "region": "Andalucía",
                },
                "MALAGA": {
                    "name": "Málaga",
                    "adjective": "malagueño",
                    "region": "Andalucía",
                },
                "MURCIA": {
                    "name": "Murcia",
                    "adjective": "murciano",
                    "region": "Murcia",
                },
                "PALMA": {
                    "name": "Palma",
                    "adjective": "palmesano",
                    "region": "Baleares",
                },
                "LAS PALMAS": {
                    "name": "Las Palmas",
                    "adjective": "palmense",
                    "region": "Canarias",
                },
                "BILBAO": {
                    "name": "Bilbao",
                    "adjective": "bilbaíno",
                    "region": "País Vasco",
                },
                "ALICANTE": {
                    "name": "Alicante",
                    "adjective": "alicantino",
                    "region": "Valencia",
                },
                "CÓRDOBA": {
                    "name": "Córdoba",
                    "adjective": "cordobés",
                    "region": "Andalucía",
                },
                "CORDOBA": {
                    "name": "Córdoba",
                    "adjective": "cordobés",
                    "region": "Andalucía",
                },
                "VALLADOLID": {
                    "name": "Valladolid",
                    "adjective": "vallisoletano",
                    "region": "Castilla y León",
                },
                "VIGO": {"name": "Vigo", "adjective": "vigués", "region": "Galicia"},
                "GIJÓN": {
                    "name": "Gijón",
                    "adjective": "gijonés",
                    "region": "Asturias",
                },
                "GIJON": {
                    "name": "Gijón",
                    "adjective": "gijonés",
                    "region": "Asturias",
                },
                "GRANADA": {
                    "name": "Granada",
                    "adjective": "granadino",
                    "region": "Andalucía",
                },
                "VITORIA": {
                    "name": "Vitoria",
                    "adjective": "vitoriano",
                    "region": "País Vasco",
                },
                "A CORUÑA": {
                    "name": "A Coruña",
                    "adjective": "coruñés",
                    "region": "Galicia",
                },
                "LA CORUÑA": {
                    "name": "A Coruña",
                    "adjective": "coruñés",
                    "region": "Galicia",
                },
                "ELCHE": {
                    "name": "Elche",
                    "adjective": "ilicitano",
                    "region": "Valencia",
                },
                "OVIEDO": {
                    "name": "Oviedo",
                    "adjective": "ovetense",
                    "region": "Asturias",
                },
                "PAMPLONA": {
                    "name": "Pamplona",
                    "adjective": "pamplonés",
                    "region": "Navarra",
                },
                "SAN SEBASTIÁN": {
                    "name": "San Sebastián",
                    "adjective": "donostiarra",
                    "region": "País Vasco",
                },
                "SAN SEBASTIAN": {
                    "name": "San Sebastián",
                    "adjective": "donostiarra",
                    "region": "País Vasco",
                },
                "SANTANDER": {
                    "name": "Santander",
                    "adjective": "santanderino",
                    "region": "Cantabria",
                },
                "LEÓN": {
                    "name": "León",
                    "adjective": "leonés",
                    "region": "Castilla y León",
                },
                "LEON": {
                    "name": "León",
                    "adjective": "leonés",
                    "region": "Castilla y León",
                },
                "BURGOS": {
                    "name": "Burgos",
                    "adjective": "burgalés",
                    "region": "Castilla y León",
                },
                "SALAMANCA": {
                    "name": "Salamanca",
                    "adjective": "salmantino",
                    "region": "Castilla y León",
                },
                "CÁCERES": {
                    "name": "Cáceres",
                    "adjective": "cacereño",
                    "region": "Extremadura",
                },
                "CACERES": {
                    "name": "Cáceres",
                    "adjective": "cacereño",
                    "region": "Extremadura",
                },
                "BADAJOZ": {
                    "name": "Badajoz",
                    "adjective": "pacense",
                    "region": "Extremadura",
                },
                "TOLEDO": {
                    "name": "Toledo",
                    "adjective": "toledano",
                    "region": "Castilla-La Mancha",
                },
                "CIUDAD REAL": {
                    "name": "Ciudad Real",
                    "adjective": "ciudadrealeño",
                    "region": "Castilla-La Mancha",
                },
                "ALBACETE": {
                    "name": "Albacete",
                    "adjective": "albaceteño",
                    "region": "Castilla-La Mancha",
                },
                "CUENCA": {
                    "name": "Cuenca",
                    "adjective": "conquense",
                    "region": "Castilla-La Mancha",
                },
                "GUADALAJARA": {
                    "name": "Guadalajara",
                    "adjective": "guadalajareño",
                    "region": "Castilla-La Mancha",
                },
                "ÁVILA": {
                    "name": "Ávila",
                    "adjective": "abulense",
                    "region": "Castilla y León",
                },
                "AVILA": {
                    "name": "Ávila",
                    "adjective": "abulense",
                    "region": "Castilla y León",
                },
                "SEGOVIA": {
                    "name": "Segovia",
                    "adjective": "segoviano",
                    "region": "Castilla y León",
                },
                "SORIA": {
                    "name": "Soria",
                    "adjective": "soriano",
                    "region": "Castilla y León",
                },
                "PALENCIA": {
                    "name": "Palencia",
                    "adjective": "palentino",
                    "region": "Castilla y León",
                },
                "ZAMORA": {
                    "name": "Zamora",
                    "adjective": "zamorano",
                    "region": "Castilla y León",
                },
                "HUELVA": {
                    "name": "Huelva",
                    "adjective": "onubense",
                    "region": "Andalucía",
                },
                "CÁDIZ": {
                    "name": "Cádiz",
                    "adjective": "gaditano",
                    "region": "Andalucía",
                },
                "CADIZ": {
                    "name": "Cádiz",
                    "adjective": "gaditano",
                    "region": "Andalucía",
                },
                "JAÉN": {
                    "name": "Jaén",
                    "adjective": "jiennense",
                    "region": "Andalucía",
                },
                "JAEN": {
                    "name": "Jaén",
                    "adjective": "jiennense",
                    "region": "Andalucía",
                },
                "LOGROÑO": {
                    "name": "Logroño",
                    "adjective": "logroñés",
                    "region": "La Rioja",
                },
                "LOGRONO": {
                    "name": "Logroño",
                    "adjective": "logroñés",
                    "region": "La Rioja",
                },
                "HUESCA": {
                    "name": "Huesca",
                    "adjective": "oscense",
                    "region": "Aragón",
                },
                "TERUEL": {
                    "name": "Teruel",
                    "adjective": "turolense",
                    "region": "Aragón",
                },
                "CASTELLÓN": {
                    "name": "Castellón",
                    "adjective": "castellonense",
                    "region": "Valencia",
                },
                "CASTELLON": {
                    "name": "Castellón",
                    "adjective": "castellonense",
                    "region": "Valencia",
                },
                "TARRAGONA": {
                    "name": "Tarragona",
                    "adjective": "tarraconense",
                    "region": "Cataluña",
                },
                "LLEIDA": {
                    "name": "Lleida",
                    "adjective": "leridano",
                    "region": "Cataluña",
                },
                "GIRONA": {
                    "name": "Girona",
                    "adjective": "gerundense",
                    "region": "Cataluña",
                },
                "LUGO": {
                    "name": "Lugo",
                    "adjective": "lucense",
                    "region": "Galicia",
                },
                "OURENSE": {
                    "name": "Ourense",
                    "adjective": "ourensano",
                    "region": "Galicia",
                },
                "PONTEVEDRA": {
                    "name": "Pontevedra",
                    "adjective": "pontevedrés",
                    "region": "Galicia",
                },
                "CEUTA": {
                    "name": "Ceuta",
                    "adjective": "ceutí",
                    "region": "Ceuta",
                },
                "MELILLA": {
                    "name": "Melilla",
                    "adjective": "melillense",
                    "region": "Melilla",
                },
            }

            # Buscar coincidencia directa
            if location_clean in city_names:
                return city_names[location_clean]

            # Buscar coincidencia parcial
            for city_key, city_info in city_names.items():
                if city_key in location_clean or location_clean in city_key:
                    return city_info

            # Fallback: extraer primera palabra como ciudad
            first_word = location_clean.split()[0] if location_clean else "MADRID"
            return {
                "name": first_word.title(),
                "adjective": "local",
                "region": "España",
            }

        except Exception as e:
            logger.error(f"❌ Error extrayendo contexto geográfico: {str(e)}")
            return {"name": "Madrid", "adjective": "madrileño", "region": "Madrid"}

    def _detect_location_in_message(self, user_message: str) -> Optional[str]:
        """
        Detecta ubicación específica mencionada en mensaje del usuario
        Reconoce ciudades, códigos postales y referencias geográficas naturales
        """
        try:
            if not user_message:
                return None

            message_upper = user_message.upper()

            # Patrones de ubicación en lenguaje natural
            location_patterns = [
                # Ciudades principales con diferentes formas
                ("MADRID", "Madrid,ES"),
                ("BARCELONA", "Barcelona,ES"),
                ("VALENCIA", "Valencia,ES"),
                ("SEVILLA", "Sevilla,ES"),
                ("ZARAGOZA", "Zaragoza,ES"),
                ("MÁLAGA", "Málaga,ES"),
                ("MALAGA", "Málaga,ES"),
                ("MURCIA", "Murcia,ES"),
                ("PALMA", "Palma,ES"),
                ("LAS PALMAS", "Las Palmas,ES"),
                ("BILBAO", "Bilbao,ES"),
                ("ALICANTE", "Alicante,ES"),
                ("CÓRDOBA", "Córdoba,ES"),
                ("CORDOBA", "Córdoba,ES"),
                ("VALLADOLID", "Valladolid,ES"),
                ("VIGO", "Vigo,ES"),
                ("GIJÓN", "Gijón,ES"),
                ("GIJON", "Gijón,ES"),
                ("GRANADA", "Granada,ES"),
                ("VITORIA", "Vitoria,ES"),
                ("A CORUÑA", "A Coruña,ES"),
                ("LA CORUÑA", "A Coruña,ES"),
                ("ELCHE", "Elche,ES"),
                ("OVIEDO", "Oviedo,ES"),
                ("PAMPLONA", "Pamplona,ES"),
                ("SAN SEBASTIÁN", "San Sebastián,ES"),
                ("SAN SEBASTIAN", "San Sebastián,ES"),
                ("ALMERÍA", "Almería,ES"),
                ("ALMERIA", "Almería,ES"),
                ("SANTANDER", "Santander,ES"),
                ("TOLEDO", "Toledo,ES"),
                ("BADAJOZ", "Badajoz,ES"),
                ("SALAMANCA", "Salamanca,ES"),
                ("HUELVA", "Huelva,ES"),
                ("LLEIDA", "Lleida,ES"),
                ("TARRAGONA", "Tarragona,ES"),
                ("CÁDIZ", "Cádiz,ES"),
                ("CADIZ", "Cádiz,ES"),
                ("JAÉN", "Jaén,ES"),
                ("JAEN", "Jaén,ES"),
                ("OURENSE", "Ourense,ES"),
                ("PONTEVEDRA", "Pontevedra,ES"),
                ("LUGO", "Lugo,ES"),
                ("LEÓN", "León,ES"),
                ("LEON", "León,ES"),
                ("PALENCIA", "Palencia,ES"),
                ("BURGOS", "Burgos,ES"),
                ("SORIA", "Soria,ES"),
                ("SEGOVIA", "Segovia,ES"),
                ("ÁVILA", "Ávila,ES"),
                ("AVILA", "Ávila,ES"),
                ("GUADALAJARA", "Guadalajara,ES"),
                ("CUENCA", "Cuenca,ES"),
                ("ALBACETE", "Albacete,ES"),
                ("CIUDAD REAL", "Ciudad Real,ES"),
                ("CÁCERES", "Cáceres,ES"),
                ("MÉRIDA", "Mérida,ES"),
                ("LOGROÑO", "Logroño,ES"),
                ("LOGROÑO", "Logroño,ES"),
                ("HUESCA", "Huesca,ES"),
                ("TERUEL", "Teruel,ES"),
                ("CASTELLÓN", "Castellón,ES"),
                ("CASTELLON", "Castellón,ES"),
                ("SANTANDER", "Santander,ES"),
                ("LEÓN", "León,ES"),
                ("LEON", "León,ES"),
                ("BURGOS", "Burgos,ES"),
                ("SALAMANCA", "Salamanca,ES"),
                ("CÁCERES", "Cáceres,ES"),
                ("CACERES", "Cáceres,ES"),
                ("BADAJOZ", "Badajoz,ES"),
                ("TOLEDO", "Toledo,ES"),
                ("CIUDAD REAL", "Ciudad Real,ES"),
                ("ALBACETE", "Albacete,ES"),
                ("CUENCA", "Cuenca,ES"),
                ("GUADALAJARA", "Guadalajara,ES"),
                ("ÁVILA", "Ávila,ES"),
                ("AVILA", "Ávila,ES"),
                ("SEGOVIA", "Segovia,ES"),
                ("SORIA", "Soria,ES"),
                ("PALENCIA", "Palencia,ES"),
                ("ZAMORA", "Zamora,ES"),
                ("HUELVA", "Huelva,ES"),
                ("CÁDIZ", "Cádiz,ES"),
                ("CADIZ", "Cádiz,ES"),
                ("JAÉN", "Jaén,ES"),
                ("JAEN", "Jaén,ES"),
                ("LOGROÑO", "Logroño,ES"),
                ("LOGRONO", "Logroño,ES"),
                ("HUESCA", "Huesca,ES"),
                ("TERUEL", "Teruel,ES"),
                ("TARRAGONA", "Tarragona,ES"),
                ("LLEIDA", "Lleida,ES"),
                ("GIRONA", "Girona,ES"),
                ("LUGO", "Lugo,ES"),
                ("OURENSE", "Ourense,ES"),
                ("PONTEVEDRA", "Pontevedra,ES"),
                ("CEUTA", "Ceuta,ES"),
                ("MELILLA", "Melilla,ES"),
            ]

            # Buscar ciudades mencionadas directamente
            for city_pattern, location_code in location_patterns:
                if city_pattern in message_upper:
                    return location_code

            # Detectar códigos postales mencionados (5 dígitos)
            postal_matches = re.findall(r"\b(\d{5})\b", user_message)
            if postal_matches:
                # Usar el primer código postal encontrado
                return str(postal_matches[0])

            # Detectar frases contextuales con ubicación
            contextual_patterns = [
                (r"EN ([A-ZÁÉÍÓÚÑ\s]+)", r"\1,ES"),
                (r"DE ([A-ZÁÉÍÓÚÑ\s]+)", r"\1,ES"),
                (r"DESDE ([A-ZÁÉÍÓÚÑ\s]+)", r"\1,ES"),
                (r"AQUÍ EN ([A-ZÁÉÍÓÚÑ\s]+)", r"\1,ES"),
                (r"SOY DE ([A-ZÁÉÍÓÚÑ\s]+)", r"\1,ES"),
                (r"VIVO EN ([A-ZÁÉÍÓÚÑ\s]+)", r"\1,ES"),
                (r"ESTOY EN ([A-ZÁÉÍÓÚÑ\s]+)", r"\1,ES"),
            ]

            for pattern, replacement in contextual_patterns:
                match = re.search(pattern, message_upper)
                if match:
                    location_mentioned = match.group(1).strip()
                    # Verificar si la ubicación mencionada es una ciudad conocida
                    for city_pattern, location_code in location_patterns:
                        if city_pattern in location_mentioned:
                            return location_code
                    # Si no es ciudad conocida, usar tal como está
                    return f"{location_mentioned.title()},ES"

            return None

        except Exception as e:
            logger.error(f"❌ Error detectando ubicación en mensaje: {str(e)}")
            return None

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
