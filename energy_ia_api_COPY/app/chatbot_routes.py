# energy_ia_api_COPY/app/chatbot_routes.py
# 🏢 CHATBOT EMPRESARIAL UNIFICADO NIVEL 2025 - COMUNICACIÓN ROBUSTA

import os
import logging
import json
import time
import jwt
from datetime import datetime
from utils.timezone_utils import now_spanish_iso, now_spanish
from typing import Dict, List, Optional, Any
from flask import Blueprint, request, jsonify, g, current_app
import requests
from google.cloud import bigquery

from smarwatt_auth import token_required
from utils.error_handlers import AppError
from app.services.generative_chat_service import get_enterprise_chat_service

# Configuración de logging empresarial
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Blueprint empresarial
chatbot_bp = Blueprint("chatbot_routes", __name__)


class EnterpriseChatbotService:
    """Servicio empresarial para comunicación robusta entre chatbots"""

    def __init__(self):
        self.chat_service = get_enterprise_chat_service()
        self.bq_client = bigquery.Client()
        self.project_id = current_app.config["GCP_PROJECT_ID"]
        self.dataset_id = current_app.config["BQ_DATASET_ID"]
        self.conversations_table = current_app.config["BQ_CONVERSATIONS_TABLE_ID"]
        self.ai_sentiment_table = current_app.config["BQ_AI_SENTIMENT_TABLE_ID"]
        self.expert_bot_url = current_app.config.get("EXPERT_BOT_API_URL")
        if not self.expert_bot_url:
            logger.error("❌ EXPERT_BOT_API_URL no configurada en producción")
            raise ValueError("EXPERT_BOT_API_URL debe estar configurada")

        logger.info("🏢 EnterpriseChatbotService inicializado")

    def get_user_context_robust(
        self, user_token: str, timeout: int = 5
    ) -> Dict[str, Any]:
        """Obtiene contexto del usuario de forma robusta con fallbacks"""
        try:
            headers = {"Authorization": f"Bearer {user_token}"}

            # Intentar obtener contexto completo
            response = requests.get(
                f"{self.expert_bot_url}/api/v1/energy/users/profile",
                headers=headers,
                timeout=timeout,
            )

            if response.status_code == 200:
                profile_data = response.json().get("data", {})
                return self._process_user_context(profile_data)

            # Si falla, intentar endpoint básico
            elif response.status_code == 404:
                logger.warning("Perfil no encontrado, intentando datos básicos")
                return self._get_basic_user_context(user_token)

            else:
                logger.warning(f"Error obteniendo perfil: {response.status_code}")
                return self._get_empty_context()

        except requests.exceptions.Timeout:
            logger.warning("Timeout obteniendo contexto - usando fallback")
            return self._get_cached_context(user_token)

        except requests.exceptions.ConnectionError:
            logger.warning("Error de conexión con expert-bot-api - modo offline")
            return self._get_empty_context()

        except Exception as e:
            logger.error(f"Error inesperado obteniendo contexto: {str(e)}")
            return self._get_empty_context()

    def _process_user_context(self, profile_data: Dict) -> Dict[str, Any]:
        """Procesa el contexto del usuario para el chatbot"""
        # USAR CAMPOS DEL ESQUEMA REAL BigQuery user_profiles_enriched

        # Nombre del usuario: usar displayName y email de los campos adicionales de Firestore
        user_name = profile_data.get("displayName", "") or profile_data.get("email", "")

        # ✅ EXTRAER DATOS DE FACTURA DETALLADOS (CORRECCIÓN CRÍTICA)
        last_invoice_data = profile_data.get("last_invoice_data", {})

        # 🌦️ INTEGRAR DATOS METEOROLÓGICOS PARA CONTEXTO INTELIGENTE
        weather_context = self._get_weather_context_safe(profile_data)

        # Contexto completo usando SOLO campos del esquema BigQuery + last_invoice_data
        context = {
            "uid": profile_data.get("user_id", ""),
            "user_name": user_name,
            "has_complete_data": bool(
                profile_data.get("consumption_kwh")
                or profile_data.get("monthly_consumption_kwh")
                or last_invoice_data.get("kwh_consumidos")
            ),
            "consumption_data": {
                "monthly_kwh": profile_data.get("monthly_consumption_kwh", 0)
                or profile_data.get("consumption_kwh", 0)
                or last_invoice_data.get("kwh_consumidos", 0),
                "avg_kwh_last_year": profile_data.get("avg_kwh_last_year", 0),
                "contracted_power_kw": profile_data.get("contracted_power_kw", 0)
                or last_invoice_data.get("potencia_contratada_kw", 0),
                "peak_percent_avg": profile_data.get("peak_percent_avg", 0),
            },
            "household_info": {
                "num_inhabitants": profile_data.get("num_inhabitants", 0),
                "home_type": profile_data.get("home_type", ""),
                "heating_type": profile_data.get("heating_type", ""),
                "has_ac": profile_data.get("has_ac", False),
                "has_pool": profile_data.get("has_pool", False),
                "is_teleworker": profile_data.get("is_teleworker", False),
                "post_code_prefix": profile_data.get("post_code_prefix", ""),
                "has_solar_panels": profile_data.get("has_solar_panels", False),
            },
            # ✅ DATOS CRÍTICOS DE FACTURA (NUEVA FUNCIONALIDAD)
            "last_invoice": {
                "comercializadora": last_invoice_data.get("comercializadora", ""),
                "coste_total": last_invoice_data.get("coste_total", 0),
                "tariff_name_from_invoice": last_invoice_data.get(
                    "tariff_name_from_invoice", ""
                ),
                "tariff_type": last_invoice_data.get("tariff_type", ""),
                "kwh_consumidos": last_invoice_data.get("kwh_consumidos", 0),
                "kwh_punta": last_invoice_data.get("kwh_punta", 0),
                "kwh_valle": last_invoice_data.get("kwh_valle", 0),
                "kwh_llano": last_invoice_data.get("kwh_llano", 0),
                "precio_kwh_punta": last_invoice_data.get("precio_kwh_punta", 0),
                "termino_energia": last_invoice_data.get("termino_energia", 0),
                "termino_potencia": last_invoice_data.get("termino_potencia", 0),
                "distribuidora": last_invoice_data.get("distribuidora", ""),
                "periodo_facturacion_dias": last_invoice_data.get(
                    "periodo_facturacion_dias", 0
                ),
                "potencia_maxima_demandada": last_invoice_data.get(
                    "potencia_maxima_demandada", 0
                ),
                "fecha_emision": last_invoice_data.get("fecha_emision", ""),
                "has_detailed_invoice": bool(
                    last_invoice_data.get("coste_total", 0) > 0
                ),
            },
            "weather_context": weather_context,  # 🌦️ CONTEXTO METEOROLÓGICO INTEGRADO
            "context_string": self._build_context_string(
                user_name, profile_data, weather_context
            ),
            "data_completeness": self._calculate_data_completeness(profile_data),
            "available_sources": self._get_available_sources(profile_data),
        }

        return context

    def _build_context_string(
        self, user_name: str, profile_data: Dict, weather_context: Optional[Dict] = None
    ) -> str:
        """Construye el string de contexto para el chatbot usando campos del esquema BigQuery"""
        context_parts = []

        # Saludo personalizado OBLIGATORIO
        if user_name:
            context_parts.append(f"USUARIO: {user_name}")

        # 🌦️ CONTEXTO METEOROLÓGICO (NUEVO)
        if weather_context and weather_context.get("weather_enabled"):
            weather_string = weather_context.get("weather_context_string", "")
            if weather_string:
                context_parts.append(weather_string)

        # ✅ DATOS DE FACTURA DETALLADOS (CORRECCIÓN CRÍTICA)
        last_invoice_data = profile_data.get("last_invoice_data", {})
        if last_invoice_data and last_invoice_data.get("coste_total", 0) > 0:
            context_parts.append(
                f"""
FACTURA ACTUAL REAL DEL USUARIO:
- Comercializadora: {last_invoice_data.get('comercializadora', 'No especificada')}
- Coste total mensual: {last_invoice_data.get('coste_total', 0)}€
- Tarifa contratada: {last_invoice_data.get('tariff_name_from_invoice', 'No especificada')}
- Tipo de tarifa: {last_invoice_data.get('tariff_type', 'No especificado')}
- Consumo total: {last_invoice_data.get('kwh_consumidos', 0)} kWh/mes
- Consumo punta: {last_invoice_data.get('kwh_punta', 0)} kWh ({round((last_invoice_data.get('kwh_punta', 0) / max(last_invoice_data.get('kwh_consumidos', 1), 1)) * 100, 1)}%)
- Consumo valle: {last_invoice_data.get('kwh_valle', 0)} kWh ({round((last_invoice_data.get('kwh_valle', 0) / max(last_invoice_data.get('kwh_consumidos', 1), 1)) * 100, 1)}%)
- Consumo llano: {last_invoice_data.get('kwh_llano', 0)} kWh ({round((last_invoice_data.get('kwh_llano', 0) / max(last_invoice_data.get('kwh_consumidos', 1), 1)) * 100, 1)}%)
- Precio punta: {last_invoice_data.get('precio_kwh_punta', 0):.6f}€/kWh
- Término energía: {last_invoice_data.get('termino_energia', 0)}€
- Término potencia: {last_invoice_data.get('termino_potencia', 0)}€
- Potencia contratada: {last_invoice_data.get('potencia_contratada_kw', profile_data.get('contracted_power_kw', 0))} kW
- Potencia máxima demandada: {last_invoice_data.get('potencia_maxima_demandada', 0)} kW
- Distribuidora: {last_invoice_data.get('distribuidora', 'No especificada')}
- Período facturación: {last_invoice_data.get('periodo_facturacion_dias', 0)} días
- Fecha emisión: {last_invoice_data.get('fecha_emision', 'No especificada')}
"""
            )

        # Datos de consumo usando campos del esquema BigQuery (fallback si no hay factura)
        elif profile_data.get("consumption_kwh") or profile_data.get(
            "monthly_consumption_kwh"
        ):
            context_parts.append(
                f"""
DATOS BÁSICOS DEL PERFIL DEL USUARIO:
- Consumo mensual: {profile_data.get('monthly_consumption_kwh', profile_data.get('consumption_kwh', 'N/A'))} kWh
- Promedio anual: {profile_data.get('avg_kwh_last_year', 'N/A')} kWh
- Potencia contratada: {profile_data.get('contracted_power_kw', 'N/A')} kW
- Porcentaje punta promedio: {profile_data.get('peak_percent_avg', 'N/A')}%
"""
            )

        # Datos del hogar usando campos del esquema BigQuery
        household_info = []
        if profile_data.get("num_inhabitants"):
            household_info.append(f"Habitantes: {profile_data.get('num_inhabitants')}")
        if profile_data.get("home_type"):
            household_info.append(f"Tipo de vivienda: {profile_data.get('home_type')}")
        if profile_data.get("heating_type"):
            household_info.append(f"Calefacción: {profile_data.get('heating_type')}")
        if profile_data.get("has_ac"):
            household_info.append("Tiene aire acondicionado")
        if profile_data.get("has_pool"):
            household_info.append("Tiene piscina")
        if profile_data.get("is_teleworker"):
            household_info.append("Teletrabaja")
        if profile_data.get("has_solar_panels"):
            household_info.append("Tiene paneles solares")
        if profile_data.get("post_code_prefix"):
            household_info.append(
                f"Código postal: {profile_data.get('post_code_prefix')}"
            )

        if household_info:
            context_parts.append(f"INFORMACIÓN DEL HOGAR: {', '.join(household_info)}")

        # ✅ INSTRUCCIONES ESPECÍFICAS PARA PERSONALIZACIÓN PREMIUM CON DISTRIBUCIÓN HORARIA
        if context_parts:
            # Calcular distribución horaria si tenemos los datos
            total_kwh = last_invoice_data.get("kwh_consumidos", 0)
            kwh_punta = last_invoice_data.get("kwh_punta", 0)
            kwh_valle = last_invoice_data.get("kwh_valle", 0)
            kwh_llano = last_invoice_data.get("kwh_llano", 0)

            distribution_info = ""
            if total_kwh > 0 and (kwh_punta > 0 or kwh_valle > 0 or kwh_llano > 0):
                punta_percent = (
                    round((kwh_punta / total_kwh) * 100, 1) if kwh_punta > 0 else 0
                )
                valle_percent = (
                    round((kwh_valle / total_kwh) * 100, 1) if kwh_valle > 0 else 0
                )
                llano_percent = (
                    round((kwh_llano / total_kwh) * 100, 1) if kwh_llano > 0 else 0
                )

                distribution_info = f"""
DISTRIBUCIÓN HORARIA EXACTA DEL USUARIO:
- Consumo punta: {kwh_punta} kWh ({punta_percent}% del total)
- Consumo valle: {kwh_valle} kWh ({valle_percent}% del total)  
- Consumo llano: {kwh_llano} kWh ({llano_percent}% del total)
- Total mensual: {total_kwh} kWh
- Potencia contratada: {last_invoice_data.get('potencia_contratada_kw', profile_data.get('contracted_power_kw', 0))} kW
- Coste mensual actual: {last_invoice_data.get('coste_total', 0)}€
"""

            context_parts.append(
                f"""
{distribution_info}
INSTRUCCIONES CRÍTICAS PARA RESPUESTA PERSONALIZADA:
- SALUDA SIEMPRE al usuario por su nombre: {user_name}
- USA SIEMPRE los datos reales específicos de SU factura para dar consejos personalizados
- MENCIONA valores específicos: {last_invoice_data.get('coste_total', profile_data.get('monthly_consumption_kwh', 0))}€, {last_invoice_data.get('comercializadora', 'su comercializadora')}, {last_invoice_data.get('tariff_name_from_invoice', 'su tarifa actual')}
- USA la distribución horaria EXACTA para recomendar tarifas específicas
- CALCULA ahorros potenciales usando SUS cifras reales de punta/valle/llano
- NO PIDAS más datos que ya tienes disponibles
- PROPORCIONA recomendaciones específicas para su perfil de consumo
"""
            )

        return " ".join(context_parts)

        if household_info:
            context_parts.append(f"DATOS DEL HOGAR: {', '.join(household_info)}")

        # Instrucciones específicas
        if context_parts:
            context_parts.append(
                """
INSTRUCCIONES IMPORTANTES:
- Saluda al usuario por su nombre si lo tienes
- Usa SIEMPRE estos datos reales para dar consejos personalizados
- Menciona valores específicos de su factura cuando sea relevante
- Compara con valores promedio del mercado
- Ofrece recomendaciones específicas basadas en su perfil
"""
            )

        return "\n".join(context_parts)

    def _calculate_data_completeness(self, profile_data: Dict) -> float:
        """Calcula completitud de los datos usando SOLO campos del esquema BigQuery user_profiles_enriched (0-100)"""
        score = 0

        # ✅ DATOS DE FACTURA DETALLADOS (40% - PESO ALTO)
        last_invoice_data = profile_data.get("last_invoice_data", {})
        if last_invoice_data.get("coste_total", 0) > 0:
            score += 15  # Tiene coste total
        if last_invoice_data.get("comercializadora"):
            score += 5  # Tiene comercializadora
        if last_invoice_data.get("tariff_name_from_invoice"):
            score += 5  # Tiene tarifa
        if last_invoice_data.get("kwh_consumidos", 0) > 0:
            score += 5  # Tiene consumo detallado
        if (
            last_invoice_data.get("kwh_punta", 0) > 0
            or last_invoice_data.get("kwh_valle", 0) > 0
        ):
            score += 10  # Tiene desglose horario

        # Datos básicos del hogar (25%)
        if profile_data.get("num_inhabitants"):
            score += 8
        if profile_data.get("home_type"):
            score += 8
        if profile_data.get("heating_type"):
            score += 9

        # Datos de consumo críticos (50%)
        if profile_data.get("consumption_kwh") or profile_data.get(
            "monthly_consumption_kwh"
        ):
            score += 20
        if profile_data.get("contracted_power_kw"):
            score += 15
        if profile_data.get("avg_kwh_last_year"):
            score += 15

        # Datos adicionales del perfil (20%)
        if profile_data.get("peak_percent_avg"):
            score += 5
        if profile_data.get("post_code_prefix"):
            score += 5
        if profile_data.get("has_ac") is not None:  # Puede ser False
            score += 2
        if profile_data.get("has_pool") is not None:
            score += 2
        if profile_data.get("is_teleworker") is not None:
            score += 2
        if profile_data.get("has_solar_panels") is not None:
            score += 2
        if profile_data.get("last_update_timestamp"):
            score += 2

        return min(score, 100.0)

    def _get_available_sources(self, profile_data: Dict) -> List[str]:
        """Obtiene fuentes de datos disponibles usando campos del esquema BigQuery"""
        sources = []

        # Fuente de datos de consumo actual
        if profile_data.get("consumption_kwh") or profile_data.get(
            "monthly_consumption_kwh"
        ):
            sources.append("consumption_data")

        # Fuente de datos históricos
        if profile_data.get("avg_kwh_last_year"):
            sources.append("historical_data")

        # Fuente de perfil del hogar
        if profile_data.get("num_inhabitants") or profile_data.get("home_type"):
            sources.append("household_profile")

        # Fuente de datos de eficiencia
        if profile_data.get("peak_percent_avg"):
            sources.append("efficiency_data")

        # Fuente de localización
        if profile_data.get("post_code_prefix"):
            sources.append("location_data")

        # Fuente de equipamiento
        if any(
            [
                profile_data.get("has_ac"),
                profile_data.get("has_pool"),
                profile_data.get("has_solar_panels"),
                profile_data.get("heating_type"),
            ]
        ):
            sources.append("equipment_data")

        return sources

    def _get_basic_user_context(self, user_token: str) -> Dict[str, Any]:
        """Obtiene contexto básico como fallback"""
        try:
            headers = {"Authorization": f"Bearer {user_token}"}
            response = requests.get(
                f"{self.expert_bot_url}/api/v1/users/basic-info",
                headers=headers,
                timeout=3,
            )

            if response.status_code == 200:
                basic_data = response.json().get("data", {})
                # Usar displayName/email consistente con el esquema unificado
                user_name = basic_data.get("displayName", "") or basic_data.get(
                    "email", ""
                )
                return {
                    "uid": basic_data.get("user_id", ""),
                    "user_name": user_name,
                    "has_complete_data": False,
                    "context_string": (
                        f"El usuario se llama {user_name}." if user_name else ""
                    ),
                    "data_completeness": 10,
                    "available_sources": [],
                }
        except Exception:
            pass

        return self._get_empty_context()

    def _get_cached_context(self, user_token: str) -> Dict[str, Any]:
        """Obtiene contexto desde caché empresarial con fallback a base de datos"""
        try:
            user_id = self._extract_user_id_from_token(user_token)
            if not user_id:
                return self._get_empty_context()

            query = f"""
                SELECT 
                    user_name,
                    context_data,
                    data_completeness,
                    cached_at,
                    TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), cached_at, MINUTE) as age_minutes
                FROM `{self.project_id}.{self.dataset_id}.user_context_cache`
                WHERE user_id = @user_id
                AND TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), cached_at, MINUTE) < 60
                ORDER BY cached_at DESC
                LIMIT 1
            """

            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("user_id", "STRING", user_id),
                ]
            )

            query_job = self.bq_client.query(query, job_config=job_config)
            results = list(query_job.result())

            if results:
                row = results[0]
                context_data = json.loads(row.context_data) if row.context_data else {}

                return {
                    "uid": context_data.get("uid", ""),
                    "user_name": row.user_name or "",
                    "has_complete_data": context_data.get("has_complete_data", False),
                    "context_string": context_data.get("context_string", ""),
                    "data_completeness": row.data_completeness or 0,
                    "available_sources": context_data.get("available_sources", []),
                    "cache_age_minutes": row.age_minutes,
                    "from_cache": True,
                }

            return self._get_empty_context()

        except Exception as e:
            logger.warning(f"Error accediendo a caché de contexto: {str(e)}")
            return self._get_empty_context()

    def _extract_user_id_from_token(self, token: str) -> Optional[str]:
        """Extrae user_id del token de forma segura"""
        try:
            decoded = jwt.decode(token, options={"verify_signature": False})
            return decoded.get("user_id") or decoded.get("uid")
        except Exception:
            return None

    def _get_weather_context_safe(self, profile_data: Dict) -> Dict[str, Any]:
        """🌦️ Obtiene contexto meteorológico de forma segura sin romper nada"""
        try:
            # Importar el servicio de IA solo cuando se necesita
            from app.services.vertex_ai_service import VertexAIService

            # Obtener ubicación del usuario (fallback a Madrid)
            location = (
                profile_data.get("location", "")
                or profile_data.get("post_code_prefix", "") + ",ES"
                or "Madrid,ES"
            )

            # Obtener datos meteorológicos usando la implementación ya existente
            vertex_service = VertexAIService()
            weather_data = vertex_service._get_weather_data(location)

            # Construir contexto meteorológico para el chatbot
            weather_context = {
                "weather_data": weather_data,
                "weather_enabled": True,
                "weather_context_string": self._build_weather_context_string(
                    weather_data
                ),
                "location": location,
            }

            logger.info(f"✅ Contexto meteorológico obtenido para {location}")
            return weather_context

        except Exception as e:
            logger.warning(
                f"⚠️ Error obteniendo contexto meteorológico (continuando sin él): {e}"
            )
            # NUNCA romper el chatbot por problemas meteorológicos
            return {
                "weather_data": {},
                "weather_enabled": False,
                "weather_context_string": "",
                "location": "Madrid,ES",
            }

    def _build_weather_context_string(self, weather_data: Dict) -> str:
        """🌤️ Construye string de contexto meteorológico para el chatbot"""
        if not weather_data:
            return ""

        try:
            temp = weather_data.get("temperature", 20)
            humidity = weather_data.get("humidity", 60)
            condition = weather_data.get("weather_condition", "desconocida")
            location = weather_data.get("location", "Madrid,ES")

            # Traducir condiciones al español
            condition_translations = {
                "clear": "despejado",
                "clouds": "nublado",
                "rain": "lluvia",
                "snow": "nieve",
                "thunderstorm": "tormenta",
                "drizzle": "llovizna",
                "mist": "niebla",
                "fog": "niebla",
            }

            condition_es = condition_translations.get(condition.lower(), condition)

            return f"""
DATOS METEOROLÓGICOS ACTUALES ({location}):
- Temperatura: {temp}°C
- Humedad: {humidity}%
- Condiciones: {condition_es}
- Impacto energético: {'Alto consumo por calor' if temp > 25 else 'Alto consumo por frío' if temp < 10 else 'Consumo normal'}

CONSIDERA EL CLIMA EN TUS RECOMENDACIONES DE CONSUMO ENERGÉTICO.
"""
        except Exception as e:
            logger.warning(f"Error construyendo contexto meteorológico: {e}")
            return ""

    def _get_empty_context(self) -> Dict[str, Any]:
        """Contexto vacío para modo degradado"""
        return {
            "uid": "",
            "user_name": "",
            "has_complete_data": False,
            "context_string": "",
            "data_completeness": 0,
            "available_sources": [],
        }

    def send_message_with_context(
        self, user_message: str, chat_history: List, user_context: Dict
    ) -> Dict[str, Any]:
        """Envía mensaje con contexto completo"""
        try:
            # Preparar contexto enriquecido
            context_string = user_context.get("context_string", "")

            # Crear sesión de chat empresarial
            chat_session = self.chat_service.start_new_chat()

            # Enviar contexto como primer mensaje si existe
            if context_string:
                try:
                    chat_session.send_message(context_string)
                except Exception as context_error:
                    logger.warning(f"Error enviando contexto: {context_error}")

            # Procesar historial de chat si existe
            for history_msg in chat_history:
                try:
                    # 🔧 MANEJO ROBUSTO: Soporte tanto strings como dicts
                    if isinstance(history_msg, str):
                        # Formato simple: array de strings
                        text = history_msg.strip()
                        if text and "DATOS REALES" not in text and len(text) > 0:
                            chat_session.send_message(text)
                            logger.debug(
                                f"✓ Historial procesado (string): {text[:50]}..."
                            )

                    elif isinstance(history_msg, dict):
                        # Formato complejo: array de objetos con role/parts
                        if history_msg.get("role") == "user":
                            # Extraer texto del formato parts
                            parts = history_msg.get("parts", [])
                            if isinstance(parts, list) and len(parts) > 0:
                                text = (
                                    parts[0].get("text", "")
                                    if isinstance(parts[0], dict)
                                    else str(parts[0])
                                )
                            else:
                                text = history_msg.get(
                                    "content", ""
                                )  # Formato alternativo

                            if (
                                text
                                and "DATOS REALES" not in text
                                and len(text.strip()) > 0
                            ):
                                chat_session.send_message(text.strip())
                                logger.debug(
                                    f"✓ Historial procesado (dict): {text[:50]}..."
                                )

                    else:
                        logger.warning(
                            f"⚠️ Formato de historial no reconocido: {type(history_msg)}"
                        )

                except Exception as history_error:
                    logger.warning(f"Error procesando historial: {history_error}")

            # Enviar mensaje principal con el servicio de chat enterprise
            result = self.chat_service.send_message(
                chat_session=chat_session,
                user_message=user_message,
                user_context=user_context,
            )

            # Enriquecer respuesta con metadata
            result["context_info"] = {
                "user_name": user_context.get("user_name", ""),
                "data_completeness": user_context.get("data_completeness", 0),
                "has_complete_data": user_context.get("has_complete_data", False),
                "available_sources": user_context.get("available_sources", []),
                "context_used": bool(context_string),
            }

            return result

        except Exception as e:
            logger.error(f"Error enviando mensaje con contexto: {str(e)}")
            raise AppError(f"Error en servicio de chat: {str(e)}", 500)

    def log_conversation(self, user_id: str, conversation_data: Dict):
        """Registra conversación en BigQuery"""
        try:
            table_id = f"{self.project_id}.{self.dataset_id}.{self.conversations_table}"
            table = self.bq_client.get_table(table_id)

            # USAR SOLO CAMPOS EXACTOS DE conversations_log
            log_data = {
                "conversation_id": conversation_data.get("conversation_id", ""),
                "message_id": f"{conversation_data.get('conversation_id', '')}_{int(time.time())}",
                "user_id": user_id,
                "timestamp_utc": now_spanish(),
                "sender": "user",
                "message_text": conversation_data.get("user_message", ""),
                "intent_detected": conversation_data.get("intent_detected", ""),
                "bot_action": "response",
                "sentiment": conversation_data.get("sentiment", "neutral"),
                "deleted": False,
                "deleted_at": None,
                "response_text": conversation_data.get("bot_response", ""),
                "context_completeness": conversation_data.get(
                    "context_completeness", 0
                ),
                "response_time_ms": conversation_data.get("response_time_ms", 0),
            }

            self.bq_client.insert_rows_json(table, [log_data])
            logger.info(f"✅ Conversación registrada para usuario {user_id}")

        except Exception as e:
            logger.error(f"❌ Error registrando conversación: {str(e)}")

    def log_sentiment_analysis(self, user_id: str, conversation_data: Dict):
        """🧠 Registra análisis de sentiment en ai_sentiment_analysis con campos exactos"""
        try:
            table_id = f"{self.project_id}.{self.dataset_id}.{self.ai_sentiment_table}"
            table = self.bq_client.get_table(table_id)

            # Generar sentiment analysis básico desde conversation_data
            sentiment_info = conversation_data.get("sentiment_analysis", {})

            # USAR SOLO LOS CAMPOS EXACTOS DE ai_sentiment_analysis
            sentiment_data = {
                "interaction_id": f"{conversation_data.get('conversation_id', '')}_{int(time.time())}",
                "conversation_id": conversation_data.get("conversation_id", ""),
                "user_id": user_id,
                "message_text": conversation_data.get("user_message", ""),
                "sentiment_score": float(sentiment_info.get("score", 0.0)),
                "sentiment_label": self._get_sentiment_label(
                    sentiment_info.get("score", 0.0)
                ),
                "confidence": float(sentiment_info.get("confidence", 0.0)),
                "emotional_indicators": json.dumps(
                    {
                        "positive_indicators": sentiment_info.get(
                            "positive_indicators", 0
                        ),
                        "negative_indicators": sentiment_info.get(
                            "negative_indicators", 0
                        ),
                        "message_length": sentiment_info.get("message_length", 0),
                    }
                ),
                "analyzed_at": now_spanish(),
            }

            self.bq_client.insert_rows_json(table, [sentiment_data])
            logger.info(f"✅ Sentiment analysis registrado para usuario {user_id}")

        except Exception as e:
            logger.error(f"❌ Error registrando sentiment analysis: {str(e)}")

    def _get_sentiment_label(self, score: float) -> str:
        """Convierte score numérico a label de sentiment"""
        if score > 0.2:
            return "positive"
        elif score < -0.2:
            return "negative"
        else:
            return "neutral"

    def log_conversation_with_auto_schema(self, user_id: str, conversation_data: Dict):
        """Registra conversación con auto-creación de columnas faltantes"""
        try:
            table_id = f"{self.project_id}.{self.dataset_id}.{self.conversations_table}"

            # USAR SOLO CAMPOS EXACTOS DE conversations_log
            log_data = {
                "conversation_id": conversation_data.get("conversation_id", ""),
                "message_id": f"{conversation_data.get('conversation_id', '')}_{int(time.time())}",
                "user_id": user_id,
                "timestamp_utc": now_spanish(),
                "sender": "user",
                "message_text": conversation_data.get("user_message", ""),
                "intent_detected": conversation_data.get("intent_detected", ""),
                "bot_action": "response",
                "sentiment": conversation_data.get("sentiment", "neutral"),
                "deleted": False,
                "deleted_at": None,
                "response_text": conversation_data.get("bot_response", ""),
                "context_completeness": conversation_data.get(
                    "context_completeness", 0
                ),
                "response_time_ms": conversation_data.get("response_time_ms", 0),
            }

            job_config = bigquery.LoadJobConfig(
                source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
                schema_update_options=[
                    bigquery.SchemaUpdateOption.ALLOW_FIELD_ADDITION,
                    bigquery.SchemaUpdateOption.ALLOW_FIELD_RELAXATION,
                ],
                write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
                autodetect=True,
            )

            table_ref = self.bq_client.get_table(table_id)
            job = self.bq_client.load_table_from_json(
                [log_data], table_ref, job_config=job_config
            )

            job.result()
            logger.info(
                f"✅ Conversación registrada con auto-schema para usuario {user_id}"
            )

        except Exception as e:
            logger.warning(f"⚠️ Auto-schema falló, usando método estándar: {str(e)}")
            self.log_conversation(user_id, conversation_data)
            # 🧠 TAMBIÉN registrar sentiment analysis
            self.log_sentiment_analysis(user_id, conversation_data)

    def communicate_with_expert_bot(
        self, user_id: str, message: str, token: str
    ) -> Dict:
        """Comunicación directa con expert-bot-api"""
        try:
            headers = {"Authorization": f"Bearer {token}"}
            payload = {
                "message": message,
                "user_id": user_id,
                "source": "energy_ia_api",
            }

            response = requests.post(
                f"{self.expert_bot_url}/api/v1/chat/cross-service",
                json=payload,
                headers=headers,
                timeout=10,
            )

            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(
                    f"Error comunicándose con expert-bot: {response.status_code}"
                )
                return {"error": f"Expert bot unavailable: {response.status_code}"}

        except Exception as e:
            logger.error(f"Error en comunicación con expert-bot: {str(e)}")
            return {"error": f"Communication error: {str(e)}"}


# Instancia global del servicio
chat_service = None


def get_chat_service():
    """Obtiene instancia del servicio de chat"""
    global chat_service
    if chat_service is None:
        chat_service = EnterpriseChatbotService()
    return chat_service


# === ENDPOINTS EMPRESARIALES ===


@chatbot_bp.route("/message", methods=["POST"])
@token_required
def send_chat_message():
    """Endpoint principal para chat empresarial con contexto robusto"""
    start_time = time.time()

    try:
        # Validar datos de entrada
        json_data = request.get_json()
        if not json_data or "message" not in json_data:
            raise AppError("Petición inválida. Se requiere el campo 'message'.", 400)

        user_message = json_data["message"]
        chat_history = json_data.get("history", [])
        user_id = g.user.get("uid")

        logger.info(f"📥 Mensaje recibido de usuario {user_id}: {user_message[:50]}...")

        # Obtener servicio de chat con manejo de errores
        try:
            service = get_chat_service()
        except Exception as init_error:
            logger.error(f"Error inicializando servicio de chat: {init_error}")
            raise AppError(
                "Servicio de chat temporalmente no disponible", 503
            ) from init_error

        # Obtener contexto del usuario de forma robusta
        try:
            user_context = service.get_user_context_robust(g.token)
        except Exception as context_error:
            logger.warning(f"Error obteniendo contexto: {context_error}")
            # Usar contexto mínimo como fallback
            user_context = {
                "user_id": user_id,
                "user_name": g.user.get("displayName", "") or g.user.get("email", ""),
                "data_completeness": 0,
                "fallback_mode": True,
            }

        # Enviar mensaje con contexto
        result = service.send_message_with_context(
            user_message, chat_history, user_context
        )

        # Calcular tiempo de respuesta
        response_time = (time.time() - start_time) * 1000

        # Obtener análisis de sentiment del chat service
        try:
            chat_service = get_enterprise_chat_service()
            sentiment_analysis = chat_service._analyze_message_sentiment(user_message)
        except Exception:
            # Fallback básico si no hay análisis disponible
            sentiment_analysis = {
                "score": 0.0,
                "confidence": 0.0,
                "positive_indicators": 0,
                "negative_indicators": 0,
                "message_length": len(user_message),
            }

        # Registrar conversación
        conversation_data = {
            "conversation_id": json_data.get("conversation_id", ""),
            "user_message": user_message,
            "bot_response": result.get("response_text", ""),
            "context_completeness": user_context.get("data_completeness", 0),
            "response_time_ms": response_time,
            "sentiment_analysis": sentiment_analysis,
        }

        service.log_conversation(user_id, conversation_data)
        # 🧠 TAMBIÉN registrar sentiment analysis
        service.log_sentiment_analysis(user_id, conversation_data)

        # Enriquecer respuesta
        result["meta"] = {
            "response_time_ms": response_time,
            "service_version": "2025.1.0",
            "enterprise_mode": True,
            "timestamp": now_spanish_iso(),
        }

        logger.info(
            f"📤 Respuesta enviada a usuario {user_id} en {response_time:.0f}ms"
        )

        return jsonify(result), 200

    except AppError as e:
        logger.error(f"❌ Error en chat: {str(e)}")
        return (
            jsonify(
                {"status": "error", "message": str(e), "error_code": e.status_code}
            ),
            e.status_code,
        )

    except Exception as e:
        logger.error(f"❌ Error inesperado en chat: {str(e)}")
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Error interno del servidor",
                    "error_code": 500,
                }
            ),
            500,
        )


@chatbot_bp.route("/message/v2", methods=["POST"])
@token_required
def send_chat_message_v2():
    """Endpoint mejorado con contexto directo desde expert-bot"""
    start_time = time.time()

    try:
        json_data = request.get_json()
        if not json_data or "message" not in json_data:
            raise AppError("Petición inválida. Se requiere el campo 'message'.", 400)

        user_message = json_data["message"]
        chat_history = json_data.get("history", [])
        user_context = json_data.get("user_context", {})  # Contexto directo

        # Obtener servicio de chat
        service = get_chat_service()

        # Si no hay contexto directo, obtenerlo
        if not user_context:
            user_context = service.get_user_context_robust(g.token)

        # Enviar mensaje con contexto
        result = service.send_message_with_context(
            user_message, chat_history, user_context
        )

        # Metadata de respuesta
        response_time = (time.time() - start_time) * 1000
        result["meta"] = {
            "response_time_ms": response_time,
            "service_version": "2025.1.0",
            "endpoint_version": "v2",
            "timestamp": now_spanish_iso(),
        }

        return jsonify(result), 200

    except Exception as e:
        logger.error(f"❌ Error en chat v2: {str(e)}")
        return (
            jsonify(
                {"status": "error", "message": f"Error en servicio de chat: {str(e)}"}
            ),
            500,
        )


@chatbot_bp.route("/cross-service", methods=["POST"])
@token_required
def cross_service_communication():
    """Endpoint para comunicación directa entre servicios"""
    try:
        json_data = request.get_json()
        if not json_data or "message" not in json_data:
            raise AppError("Mensaje requerido para comunicación entre servicios", 400)

        user_id = g.user.get("uid")
        message = json_data["message"]
        source_service = json_data.get("source", "unknown")

        # Obtener servicio de chat
        service = get_chat_service()

        # Procesar mensaje según el servicio origen
        if source_service == "expert_bot_api":
            # Mensaje desde expert-bot-api
            user_context = service.get_user_context_robust(g.token)
            result = service.send_message_with_context(message, [], user_context)
        else:
            # Comunicación con expert-bot-api
            result = service.communicate_with_expert_bot(user_id, message, g.token)

        return (
            jsonify(
                {
                    "status": "success",
                    "data": result,
                    "source_service": source_service,
                    "timestamp": now_spanish_iso(),
                }
            ),
            200,
        )

    except Exception as e:
        logger.error(f"❌ Error en comunicación entre servicios: {str(e)}")
        return (
            jsonify({"status": "error", "message": f"Error en comunicación: {str(e)}"}),
            500,
        )


@chatbot_bp.route("/conversations", methods=["GET"])
@token_required
def get_user_conversations():
    """Endpoint para obtener conversaciones del usuario con robustez empresarial"""
    try:
        user_id = g.user.get("uid")
        if not user_id:
            raise AppError("Usuario no autenticado", 401)

        # Validar parámetros de paginación
        limit = request.args.get("limit", 50, type=int)
        page = request.args.get("page", 1, type=int)

        if limit <= 0 or limit > 100:
            raise AppError("Límite debe estar entre 1 y 100", 400)
        if page <= 0:
            raise AppError("Página debe ser mayor a 0", 400)

        # Validar configuración de BigQuery
        try:
            gcp_project_id = current_app.config["GCP_PROJECT_ID"]
            bq_dataset_id = current_app.config["BQ_DATASET_ID"]
            bq_table_id = current_app.config["BQ_CONVERSATIONS_TABLE_ID"]
        except KeyError as config_error:
            logger.error(f"Configuración BigQuery faltante: {config_error}")
            raise AppError(
                "Configuración de base de datos no disponible", 503
            ) from config_error

        # Inicializar cliente BigQuery con manejo robusto
        try:
            bq_client = bigquery.Client(project=gcp_project_id)
        except Exception as bq_error:
            logger.error(f"Error inicializando BigQuery: {bq_error}")
            raise AppError(
                "Servicio de base de datos temporalmente no disponible", 503
            ) from bq_error

        # Query empresarial con validación
        query = f"""
        SELECT 
            conversation_id,
            message_text,
            response_text,
            context_completeness,
            response_time_ms,
            timestamp_utc
        FROM `{gcp_project_id}.{bq_dataset_id}.conversations_log`
        WHERE user_id = @user_id 
          AND (deleted IS NULL OR deleted = false)
        ORDER BY timestamp_utc DESC
        LIMIT @limit
        """

        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("user_id", "STRING", user_id),
                bigquery.ScalarQueryParameter("limit", "INT64", limit),
            ]
        )

        try:
            query_job = bq_client.query(query, job_config=job_config)
            results = query_job.result()
        except Exception as query_error:
            logger.error(f"Error ejecutando query conversaciones: {query_error}")
            raise AppError("Error obteniendo conversaciones", 500) from query_error

        conversations = []
        for row in results:
            try:
                conversations.append(
                    {
                        "conversation_id": row.conversation_id,
                        "message_text": row.message_text or "",
                        "response_text": row.response_text or "",
                        "context_completeness": row.context_completeness or 0,
                        "response_time_ms": row.response_time_ms or 0,
                        "timestamp": (
                            row.timestamp_utc.isoformat() if row.timestamp_utc else None
                        ),
                    }
                )
            except Exception as row_error:
                logger.warning(f"Error procesando fila de conversación: {row_error}")
                continue

        return (
            jsonify(
                {
                    "status": "success",
                    "data": {
                        "conversations": conversations,
                        "total_count": len(conversations),
                    },
                    "timestamp": now_spanish_iso(),
                }
            ),
            200,
        )

    except AppError:
        raise
    except Exception as e:
        logger.error(f"Error inesperado obteniendo conversaciones: {e}", exc_info=True)
        raise AppError(f"Error interno obteniendo conversaciones: {str(e)}", 500) from e


@chatbot_bp.route("/conversations/<conversation_id>", methods=["DELETE"])
@token_required
def delete_conversation(conversation_id):
    """Endpoint para borrar conversación específica empresarial"""
    try:
        user_id = g.user.get("uid")
        if not user_id:
            raise AppError("Usuario no autenticado", 401)

        # Validar conversation_id
        if not conversation_id or len(conversation_id.strip()) == 0:
            raise AppError("ID de conversación requerido", 400)

        conversation_id = conversation_id.strip()

        # Validar configuración BigQuery
        try:
            gcp_project_id = current_app.config["GCP_PROJECT_ID"]
            bq_dataset_id = current_app.config["BQ_DATASET_ID"]
            bq_table_id = current_app.config["BQ_CONVERSATIONS_TABLE_ID"]
        except KeyError as config_error:
            logger.error(f"Configuración BigQuery faltante: {config_error}")
            raise AppError(
                "Configuración de base de datos no disponible", 503
            ) from config_error

        # Inicializar cliente BigQuery
        try:
            bq_client = bigquery.Client(project=gcp_project_id)
        except Exception as bq_error:
            logger.error(f"Error inicializando BigQuery: {bq_error}")
            raise AppError(
                "Servicio de base de datos temporalmente no disponible", 503
            ) from bq_error

        # Marcar conversación como eliminada en BigQuery
        delete_query = f"""
            UPDATE `{gcp_project_id}.{bq_dataset_id}.conversations_log`
            SET deleted = true, deleted_at = CURRENT_TIMESTAMP()
            WHERE conversation_id = @conversation_id AND user_id = @user_id AND (deleted IS NULL OR deleted = false)
        """

        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter(
                    "conversation_id", "STRING", conversation_id
                ),
                bigquery.ScalarQueryParameter("user_id", "STRING", user_id),
            ]
        )

        try:
            query_job = bq_client.query(delete_query, job_config=job_config)
            query_job.result()

            if query_job.num_dml_affected_rows == 0:
                raise AppError("Conversación no encontrada o ya eliminada", 404)
        except AppError:
            raise
        except Exception as delete_error:
            logger.error(f"Error ejecutando eliminación: {delete_error}")
            raise AppError("Error eliminando conversación", 500) from delete_error

        logger.info(
            f"✅ Conversación {conversation_id} marcada como eliminada para usuario {user_id}"
        )

        return (
            jsonify(
                {
                    "status": "success",
                    "message": f"Conversación {conversation_id} eliminada correctamente",
                    "conversation_id": conversation_id,
                    "deleted_at": now_spanish_iso(),
                    "affected_rows": query_job.num_dml_affected_rows,
                }
            ),
            200,
        )

    except AppError:
        raise
    except Exception as e:
        logger.error(f"Error inesperado eliminando conversación: {e}", exc_info=True)
        raise AppError(f"Error interno eliminando conversación: {str(e)}", 500) from e


@chatbot_bp.route("/health", methods=["GET"])
def chatbot_health_check():
    """Health check empresarial completo del chatbot"""
    try:
        health_status = {"status": "healthy", "issues": []}

        # Verificar servicio de chat
        try:
            service = get_chat_service()
            test_result = service.chat_service.get_enterprise_metrics()
            if test_result.get("service_status") != "active":
                health_status["issues"].append("chat_service_degraded")
        except Exception as e:
            health_status["issues"].append(f"chat_service_error: {str(e)}")

        # Verificar BigQuery
        try:
            bq_client = bigquery.Client()
            test_query = "SELECT 1 as test_value"
            query_job = bq_client.query(test_query)
            list(query_job.result())
        except Exception as e:
            health_status["issues"].append(f"bigquery_error: {str(e)}")

        # Verificar comunicación con expert-bot
        try:
            test_url = current_app.config.get("EXPERT_BOT_API_URL")
            if not test_url:
                health_status["issues"].append("expert_bot_url_not_configured")
            else:
                response = requests.get(f"{test_url}/health", timeout=5)
                if response.status_code != 200:
                    health_status["issues"].append("expert_bot_communication_error")
        except Exception as e:
            health_status["issues"].append(f"expert_bot_unreachable: {str(e)}")

        # Determinar estado final
        if health_status["issues"]:
            health_status["status"] = "degraded"
            status_code = 503
        else:
            status_code = 200
            health_status["issues"] = []

        return (
            jsonify(
                {
                    "status": health_status["status"],
                    "service": "energy_ia_api_copy_chatbot",
                    "version": "2025.1.0",
                    "components": {
                        "generative_chat_service": (
                            "operational"
                            if "chat_service" not in str(health_status["issues"])
                            else "degraded"
                        ),
                        "bigquery": (
                            "operational"
                            if "bigquery" not in str(health_status["issues"])
                            else "degraded"
                        ),
                        "expert_bot_communication": (
                            "operational"
                            if "expert_bot" not in str(health_status["issues"])
                            else "degraded"
                        ),
                    },
                    "issues": health_status["issues"],
                    "timestamp": now_spanish_iso(),
                }
            ),
            status_code,
        )

    except Exception as e:
        logger.error(f"❌ Error crítico en health check: {str(e)}")
        return (
            jsonify(
                {
                    "status": "unhealthy",
                    "error": str(e),
                    "timestamp": now_spanish_iso(),
                }
            ),
            500,
        )
