# energy_ia_api_COPY/app/services/generative_chat_service.py
# 🏢 SERVICIO DE CHAT GENERATIVO EMPRESARIAL NIVEL 2025

# Standard library imports
import json
import logging
import os
import sys
import time
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional

# Third-party imports
import google.generativeai as genai  # type: ignore
from flask import current_app
from google.cloud import bigquery  # type: ignore
import requests

# Local imports
from smarwatt_auth import EnterpriseAuth
from utils.error_handlers import AppError
from utils.timezone_utils import now_spanish_iso
from app.services.enterprise_links_service import get_enterprise_link_service


# 🧠 INTEGRACIÓN DIRECTA AI LEARNING SERVICE
# Importación dinámica para evitar dependencias circulares
def _get_ai_learning_service():
    """Factory para AI Learning Service con importación dinámica segura"""
    try:
        import sys
        import os

        # Añadir path del expert_bot_api_COPY al sys.path temporalmente
        expert_bot_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../../expert_bot_api_COPY")
        )

        if expert_bot_path not in sys.path:
            sys.path.insert(0, expert_bot_path)

        from app.services.ai_learning_service import AILearningService

        return AILearningService()

    except ImportError as e:
        logging.warning(f"⚠️ AI Learning Service no disponible: {str(e)}")
        return None
    except Exception as e:
        logging.error(f"❌ Error importando AI Learning Service: {str(e)}")
        return None


class EnterpriseGenerativeChatService:
    """
    🏢 SERVICIO DE CHAT GENERATIVO EMPRESARIAL 2025
    Gestiona conversaciones con modelo de lenguaje grande (Gemini) con:
    - Aprendizaje automático totalmente integrado
    - Personalización empresarial máxima
    - Análisis de sentiment en tiempo real
    - Comunicación robusta con expert_bot_api
    - Logging empresarial completo
    """

    def __init__(self) -> None:
        self.enterprise_auth: EnterpriseAuth = EnterpriseAuth()
        self.bigquery_client: Optional[bigquery.Client] = None
        self.model: Optional[Any] = None
        self.project_id: Optional[str] = None
        self.bq_dataset_id: Optional[str] = None
        self.interaction_log_table: Optional[str] = None
        self.learning_table: Optional[str] = None

        # 🔗 SERVICIO DE ENLACES EMPRESARIAL
        self.links_service = get_enterprise_link_service()

        # 🧠 AI LEARNING SERVICE INTEGRACIÓN DIRECTA
        self.ai_learning_service = _get_ai_learning_service()
        if self.ai_learning_service:
            logging.info("✅ AI Learning Service integrado exitosamente")
        else:
            logging.warning(
                "⚠️ AI Learning Service no disponible - usando análisis básico"
            )

        self._initialize_gemini_model()
        self._initialize_bigquery_client()

        logging.info("🏢 EnterpriseGenerativeChatService inicializado con IA avanzada")

    def _initialize_gemini_model(self) -> None:
        """Inicializa el modelo Gemini con configuración empresarial"""
        try:
            gemini_api_key = current_app.config.get("GEMINI_API_KEY")
            if not gemini_api_key:
                raise AppError("Clave API de Gemini no configurada", 500)

            genai.configure(api_key=gemini_api_key)

            # 🧠 INSTRUCCIONES EMPRESARIALES AVANZADAS PARA GEMINI
            self.system_instruction = self._build_enterprise_system_instruction()

            # Inicializar modelo con configuración empresarial compatible
            self.model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    top_p=0.9,
                    top_k=40,
                    max_output_tokens=2048,
                ),
                safety_settings=[
                    {
                        "category": "HARM_CATEGORY_HARASSMENT",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
                    },
                    {
                        "category": "HARM_CATEGORY_HATE_SPEECH",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
                    },
                    {
                        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
                    },
                    {
                        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
                    },
                ],
            )

            logging.info("✅ Modelo Gemini empresarial inicializado")

        except Exception as e:
            logging.error(f"❌ Error inicializando Gemini: {str(e)}")
            raise AppError(f"Error inicializando servicio de chat: {str(e)}", 500)

    def _initialize_bigquery_client(self) -> None:
        """Inicializa cliente BigQuery para logging empresarial"""
        try:
            self.project_id = current_app.config.get("GCP_PROJECT_ID")
            self.bq_dataset_id = current_app.config.get("BQ_DATASET_ID")
            self.interaction_log_table = current_app.config.get(
                "BQ_CONVERSATIONS_TABLE_ID", "conversations_log"
            )
            self.learning_table = current_app.config.get(
                "BQ_LEARNING_TABLE_ID", "ai_learning_data"
            )

            if self.project_id:
                self.bigquery_client = bigquery.Client(project=self.project_id)
                logging.info("✅ Cliente BigQuery empresarial inicializado")
            else:
                logging.warning("⚠️ GCP_PROJECT_ID no configurado - logging limitado")

        except Exception as e:
            logging.error(f"❌ Error inicializando BigQuery: {str(e)}")
            # No es crítico, continúa sin logging a BigQuery

    def _build_enterprise_system_instruction(self) -> str:
        """Construye instrucciones del sistema empresariales"""
        return (
            "Eres WattBot, un especialista en energía de SmarWatt.\n\n"
            "PERSONALIDAD Y TONO OBLIGATORIO:\n"
            "- Conversación totalmente natural, como hablas con un amigo cercano\n"
            "- Cero jerga técnica, cero lenguaje robotizado\n"
            "- Respuestas directas sin rodeos\n"
            "- SIEMPRE saluda al usuario por su nombre cuando esté disponible\n"
            "- PROHIBIDO ABSOLUTAMENTE usar asteriscos (*), negritas (**texto**), viñetas con *, emojis corporativos o cualquier formato markdown\n"
            "- Escribe en párrafos normales, conversación fluida\n"
            "- Si necesitas hacer una lista, usa simplemente números (1., 2., 3.) o guiones (-) al inicio de línea, NUNCA asteriscos\n\n"
            "QUÉ HACES:\n"
            "- Ayudas a entender y reducir facturas de luz\n"
            "- Analizas consumos energéticos reales del usuario\n"
            "- Recomiendas tarifas y mejoras de eficiencia específicas\n"
            "- Respondes sobre energía renovable y sostenibilidad\n\n"
            "CÓMO TRABAJAS CON DATOS REALES:\n"
            "- OBLIGATORIO: Usa SIEMPRE los datos específicos del usuario (comercializadora, coste, kWh, tarifa)\n"
            "- Da consejos basados en SUS cifras reales de la factura, no genéricos\n"
            "- Menciona específicamente su comercializadora, su coste mensual, su tarifa actual\n"
            "- Calcula ahorros potenciales usando sus datos exactos\n"
            "- Si tienes información completa de su factura, NO pidas más datos\n\n"
            "PRIORIDAD MÁXIMA - PERSONALIZACIÓN PREMIUM:\n"
            "- Si tienes su nombre: SALÚDALO SIEMPRE\n"
            "- Si tienes su comercializadora: MENCIÓNALA específicamente\n"
            "- Si tienes su coste mensual: ÚSALO para cálculos reales\n"
            "- Si tienes su tarifa: EVALÚALA y RECOMIENDA alternativas específicas\n"
            "- Si tienes su consumo por franjas: ANALÍZALO y da consejos específicos\n\n"
            "EJEMPLOS DE RESPUESTAS PREMIUM:\n"
            "- 'Hola Tomates Juanlu, veo que con Naturgy estás pagando 171€/mes con la Tarifa Por Uso Luz. Eso está bastante caro para tu consumo de 801 kWh/mes.'\n"
            "- 'Con tu distribución de consumo actual, te recomiendo cambiar a una tarifa que te permita ahorrar en las horas valle.'\n"
            "- 'Basándome en tus datos reales, podrías ahorrar unos 25€/mes cambiando de tarifa.'\n\n"
            "FORMATO DE RESPUESTA OBLIGATORIO:\n"
            "- Párrafos normales de conversación\n"
            "- Si haces listas: usa números (1., 2., 3.) o guiones simples (-) NUNCA asteriscos\n"
            "- Texto plano, sin negritas, sin cursivas, sin asteriscos\n"
            "- Conversación fluida como si hablaras cara a cara\n\n"
            "NUNCA:\n"
            "- Pidas información que ya tienes disponible\n"
            "- Des respuestas genéricas si tienes datos específicos\n"
            "- Ignores el nombre del usuario\n"
            "- Olvides mencionar su comercializadora o tarifa actual\n"
            "- Uses asteriscos (*) o negritas (**) bajo ninguna circunstancia\n\n"
            "Eres un especialista premium que usa los datos reales del usuario para dar valor específico y personalizado con conversación 100% natural."
        )

    def start_new_chat(self) -> Any:
        """Inicia nueva sesión de chat empresarial"""
        try:
            if self.model is None:
                raise AppError(
                    "El modelo Gemini no está inicializado correctamente", 500
                )
            chat_session = self.model.start_chat(history=[])
            logging.info("💬 Nueva sesión de chat empresarial iniciada")
            return chat_session
        except Exception as e:
            logging.error(f"❌ Error iniciando chat: {str(e)}")
            raise AppError(f"Error iniciando sesión de chat: {str(e)}", 500)

    def send_message(
        self,
        chat_session: Any,
        user_message: str,
        user_context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        🧠 ENVÍO DE MENSAJE CON IA EMPRESARIAL AVANZADA
        Procesa mensaje con aprendizaje automático y personalización máxima
        """
        start_time = time.time()

        try:
            # 🧠 ANÁLISIS DE SENTIMENT EN TIEMPO REAL
            sentiment_analysis = self._analyze_message_sentiment(user_message)

            # 🧠 ENRIQUECIMIENTO CON CONTEXTO EMPRESARIAL
            enhanced_message = self._build_enhanced_message(
                user_message, user_context, sentiment_analysis
            )

            # 🔧 INCORPORAR INSTRUCCIONES DEL SISTEMA (COMPATIBLE CON VERSIÓN ACTUAL)
            enhanced_message = f"{self.system_instruction}\n\n{enhanced_message}"

            # 📊 COMUNICACIÓN CON EXPERT_BOT_API SI ES NECESARIO
            if self._should_consult_expert_bot(user_message, user_context):
                expert_response = self._consult_expert_bot(user_message, user_context)
                enhanced_message = self._integrate_expert_response(
                    enhanced_message, expert_response
                )

            # 🚀 ENVÍO A GEMINI CON STREAMING EMPRESARIAL PARA EVITAR OOM
            try:
                # STREAMING: Evita cargar respuesta completa en memoria
                response_stream = chat_session.send_message(
                    enhanced_message, stream=True
                )
                full_response = ""

                # Procesar stream por chunks pequeños
                for chunk in response_stream:
                    if chunk.text:
                        full_response += chunk.text

                # Crear objeto response compatible
                class StreamResponse:
                    def __init__(self, text):
                        self.text = text

                response = StreamResponse(full_response)
                logging.info(
                    f"✅ Streaming exitoso - Respuesta: {len(full_response)} chars"
                )

            except Exception as streaming_error:
                logging.warning(
                    f"⚠️ Streaming falló, usando método tradicional: {streaming_error}"
                )
                # FALLBACK: Si streaming falla, usar método original
                response = chat_session.send_message(enhanced_message)

            response_time = time.time() - start_time

            # 📈 ANÁLISIS DE RESPUESTA PARA APRENDIZAJE
            response_analysis = self._analyze_response_quality(
                user_message, response.text, user_context
            )

            # 🔗 ENLACES INTELIGENTES SOLO CUANDO EL USUARIO LOS SOLICITA ESPECÍFICAMENTE
            enhanced_response_with_links = self._add_links_if_user_requests(
                user_message, response.text
            )

            # 💾 LOGGING EMPRESARIAL COMPLETO
            interaction_data = self._log_enterprise_interaction(
                user_message,
                enhanced_response_with_links,  # 🔗 Usar respuesta con enlaces contextuales
                user_context,
                sentiment_analysis,
                response_analysis,
                response_time,
            )

            # 🧠 ACTUALIZACIÓN DE APRENDIZAJE AUTOMÁTICO CON AI LEARNING SERVICE
            if user_context is not None:
                self._update_learning_patterns(user_context, interaction_data)

                # 🔥 PROCESAMIENTO AVANZADO CON AI LEARNING SERVICE
                if self.ai_learning_service and user_context.get("uid"):
                    try:
                        learning_data = {
                            "user_id": user_context["uid"],
                            "conversation_id": interaction_data.get(
                                "interaction_id", "unknown"
                            ),
                            "user_message": user_message,
                            "bot_response": enhanced_response_with_links,
                            "sentiment_analysis": sentiment_analysis,
                            "response_time": response_time,
                            "timestamp": now_spanish_iso(),
                        }

                        enterprise_analysis = (
                            self.ai_learning_service.process_enterprise_interaction(
                                learning_data
                            )
                        )

                        # Añadir resultados empresariales a métricas
                        interaction_data["enterprise_learning"] = enterprise_analysis

                        logging.info(
                            "✅ Procesamiento empresarial AI Learning completado"
                        )

                    except Exception as e:
                        logging.warning(
                            f"⚠️ Error en procesamiento empresarial AI Learning: {str(e)}"
                        )
                        # Continuar sin fallar

            # 📊 SERIALIZACIÓN DE HISTORIAL
            serializable_history = self._serialize_chat_history(chat_session.history)

            return {
                "response_text": enhanced_response_with_links,  # 🔗 Respuesta con enlaces inteligentes
                "chat_history": serializable_history,
                "enterprise_metrics": {
                    "context_used": user_context is not None,
                    "ai_learning_applied": bool(
                        user_context and user_context.get("ai_learned_patterns")
                    ),
                    "sentiment_score": sentiment_analysis.get("score", 0.0),
                    "enterprise_sentiment_analysis": sentiment_analysis.get(
                        "enterprise_analysis", False
                    ),
                    "response_time": response_time,
                    "personalization_level": self._calculate_personalization_level(
                        user_context
                    ),
                    "expert_bot_consulted": self._should_consult_expert_bot(
                        user_message, user_context
                    ),
                    "quality_score": response_analysis.get("quality_score", 0.0),
                    "links_enhanced": enhanced_response_with_links
                    != response.text,  # 🔗 Flag de mejora
                    "ai_learning_service_active": self.ai_learning_service is not None,
                },
                "prompt_used": enhanced_message,
                "interaction_id": interaction_data.get("interaction_id"),
                "learning_updates": interaction_data.get("learning_updates", []),
            }

        except Exception as e:
            logging.error(f"❌ Error procesando mensaje: {str(e)}")
            return {
                "response_text": "Disculpa, he tenido un problema interno. Por favor, inténtalo de nuevo.",
                "chat_history": [],
                "enterprise_metrics": {"error": True, "error_message": str(e)},
            }

    def _analyze_message_sentiment(self, message: str) -> Dict[str, Any]:
        """Analiza sentiment del mensaje del usuario con AI Learning Service"""
        try:
            # 🧠 USAR AI LEARNING SERVICE SI ESTÁ DISPONIBLE
            if self.ai_learning_service:
                try:
                    # Generar IDs temporales para el análisis
                    temp_user_id = "temp_analysis_user"
                    temp_conversation_id = str(uuid.uuid4())

                    # Análisis empresarial avanzado
                    sentiment_analysis = (
                        self.ai_learning_service.analyze_sentiment_enterprise(
                            temp_user_id, temp_conversation_id, message
                        )
                    )

                    return {
                        "score": sentiment_analysis.sentiment_score,
                        "confidence": sentiment_analysis.confidence,
                        "sentiment_label": sentiment_analysis.sentiment_label,
                        "emotional_indicators": sentiment_analysis.emotional_indicators,
                        "personalization_hints": sentiment_analysis.personalization_hints,
                        "risk_factors": sentiment_analysis.risk_factors,
                        "engagement_level": sentiment_analysis.engagement_level,
                        "enterprise_analysis": True,
                        "timestamp": now_spanish_iso(),
                    }

                except Exception as e:
                    logging.warning(
                        f"⚠️ Error con AI Learning Service, usando análisis básico: {str(e)}"
                    )
                    # Continuar con análisis básico

            # 🔄 ANÁLISIS BÁSICO DE FALLBACK
            positive_keywords = [
                "gracias",
                "excelente",
                "perfecto",
                "genial",
                "bien",
                "bueno",
            ]
            negative_keywords = [
                "problema",
                "error",
                "mal",
                "malo",
                "frustrado",
                "difícil",
            ]

            message_lower = message.lower()
            positive_count = sum(
                1 for word in positive_keywords if word in message_lower
            )
            negative_count = sum(
                1 for word in negative_keywords if word in message_lower
            )

            # Cálculo de score básico
            score = 0.0
            if positive_count > negative_count:
                score = min(1.0, positive_count * 0.3)
            elif negative_count > positive_count:
                score = max(-1.0, negative_count * -0.3)

            return {
                "score": score,
                "confidence": abs(score),
                "positive_indicators": positive_count,
                "negative_indicators": negative_count,
                "message_length": len(message),
                "enterprise_analysis": False,
                "timestamp": now_spanish_iso(),
            }

        except Exception as e:
            logging.error(f"❌ Error analizando sentiment: {str(e)}")
            return {"score": 0.0, "confidence": 0.0, "error": str(e)}

    def _build_enhanced_message(
        self,
        user_message: str,
        user_context: Optional[Dict[str, Any]],
        sentiment_analysis: Dict[str, Any],
    ) -> str:
        """Construye mensaje enriquecido con contexto empresarial"""
        try:
            context_parts = ["=== 🏢 CONTEXTO EMPRESARIAL SMARWATT ==="]

            # 🧠 DATOS DEL USUARIO
            if user_context:
                context_parts.append(self._build_user_context_prompt(user_context))

            # 🧠 ANÁLISIS DE SENTIMENT CON AI LEARNING SERVICE
            if sentiment_analysis.get("score") != 0:
                context_parts.append(f"\n🧠 ANÁLISIS DE SENTIMENT:")
                context_parts.append(
                    f"- Score emocional: {sentiment_analysis['score']:.2f}"
                )
                context_parts.append(
                    f"- Confianza: {sentiment_analysis['confidence']:.2f}"
                )

                # 🔥 INFORMACIÓN AVANZADA SI ESTÁ DISPONIBLE
                if sentiment_analysis.get("enterprise_analysis"):
                    context_parts.append("- Análisis: AI Learning Service (Avanzado)")

                    if sentiment_analysis.get("engagement_level"):
                        context_parts.append(
                            f"- Nivel engagement: {sentiment_analysis['engagement_level']}"
                        )

                    if sentiment_analysis.get("risk_factors"):
                        risk_count = len(sentiment_analysis["risk_factors"])
                        if risk_count > 0:
                            context_parts.append(
                                f"⚠️ Factores de riesgo detectados: {risk_count}"
                            )

                    if sentiment_analysis.get("personalization_hints"):
                        hints_count = len(sentiment_analysis["personalization_hints"])
                        if hints_count > 0:
                            context_parts.append(
                                f"💡 Hints personalización: {hints_count}"
                            )
                else:
                    context_parts.append("- Análisis: Básico (fallback)")

                if sentiment_analysis["score"] < -0.2:
                    context_parts.append(
                        "⚠️ USUARIO CON SENTIMENT NEGATIVO - Usar tono empático y soluciones específicas"
                    )
                elif sentiment_analysis["score"] > 0.2:
                    context_parts.append(
                        "😊 USUARIO CON SENTIMENT POSITIVO - Mantener energía y ofrecer valor adicional"
                    )

            # 🧠 INSTRUCCIONES ESPECÍFICAS PREMIUM
            context_parts.append(
                "\n=== 🎯 INSTRUCCIONES CRÍTICAS PERSONALIZACIÓN PREMIUM ==="
            )
            context_parts.append(
                "1. SALUDA OBLIGATORIAMENTE por su nombre si está disponible"
            )
            context_parts.append(
                "2. MENCIONA específicamente su comercializadora, coste mensual y tarifa actual"
            )
            context_parts.append(
                "3. CALCULA ahorros usando SUS cifras exactas de factura"
            )
            context_parts.append(
                "4. PROPORCIONA recomendaciones específicas para SU perfil de consumo"
            )
            context_parts.append("5. NUNCA pidas datos que ya tienes disponibles")
            context_parts.append("6. ADAPTA el tono según el sentiment detectado")
            context_parts.append(
                "7. USA valores específicos: X€/mes, Y kWh, Z comercializadora"
            )

            context_parts.append(f"\n📝 PREGUNTA DEL USUARIO: {user_message}")

            return "\n".join(context_parts)

        except Exception as e:
            logging.error(f"❌ Error construyendo mensaje enriquecido: {str(e)}")
            return user_message

    def _build_user_context_prompt(self, user_context: Dict[str, Any]) -> str:
        """
        🏢 CONSTRUYE PROMPT EMPRESARIAL CON TODOS LOS DATOS DISPONIBLES

        Usa TODOS los datos disponibles para personalización máxima:
        - Datos personales y de factura completos
        - Datos de consumo por franjas horarias
        - Información de comercializadora y distribuidora
        - Datos del hogar y ubicación
        - Patrones de aprendizaje automático

        DISEÑO ROBUSTO: Funciona con datos completos, parciales o mínimos
        """
        context_parts = []

        # ✅ DATOS PERSONALES PRIORITARIOS
        if user_context.get("user_name"):
            context_parts.append(f"👤 USUARIO: {user_context['user_name']}")

        # ✅ DATOS DE FACTURA COMPLETOS (TODOS LOS 20+ CAMPOS)
        if user_context.get("last_invoice"):
            invoice = user_context["last_invoice"]
            context_parts.append("📋 DATOS COMPLETOS DE FACTURA:")

            # Datos críticos básicos
            if invoice.get("kwh_consumidos"):
                context_parts.append(
                    f"- Consumo total: {invoice['kwh_consumidos']} kWh/mes"
                )
            if invoice.get("coste_total"):
                context_parts.append(f"- Coste mensual: {invoice['coste_total']}€")

            # ✅ COMERCIALIZADORA Y TARIFA (ANTES IGNORADOS)
            if invoice.get("comercializadora"):
                context_parts.append(
                    f"- Comercializadora actual: {invoice['comercializadora']}"
                )
            if invoice.get("tariff_name_from_invoice"):
                context_parts.append(
                    f"- Tarifa contratada: {invoice['tariff_name_from_invoice']}"
                )
            if invoice.get("tariff_type"):
                context_parts.append(f"- Tipo de tarifa: {invoice['tariff_type']}")

            # ✅ CONSUMO POR FRANJAS HORARIAS (ANTES IGNORADOS)
            if (
                invoice.get("kwh_punta")
                or invoice.get("kwh_valle")
                or invoice.get("kwh_llano")
            ):
                context_parts.append("- Desglose horario:")
                if invoice.get("kwh_punta"):
                    context_parts.append(f"  · Punta: {invoice['kwh_punta']} kWh")
                if invoice.get("kwh_valle"):
                    context_parts.append(f"  · Valle: {invoice['kwh_valle']} kWh")
                if invoice.get("kwh_llano"):
                    context_parts.append(f"  · Llano: {invoice['kwh_llano']} kWh")

            # ✅ PRECIOS Y TÉRMINOS (ANTES IGNORADOS)
            if invoice.get("precio_kwh_punta"):
                context_parts.append(
                    f"- Precio punta: {invoice['precio_kwh_punta']:.4f}€/kWh"
                )
            if invoice.get("termino_energia"):
                context_parts.append(
                    f"- Término energía: {invoice['termino_energia']}€"
                )
            if invoice.get("termino_potencia"):
                context_parts.append(
                    f"- Término potencia: {invoice['termino_potencia']}€"
                )

            # ✅ POTENCIA Y DATOS TÉCNICOS (ANTES IGNORADOS)
            if invoice.get("potencia_contratada_kw"):
                context_parts.append(
                    f"- Potencia contratada: {invoice['potencia_contratada_kw']} kW"
                )
            if invoice.get("potencia_maxima_demandada"):
                context_parts.append(
                    f"- Potencia máxima demandada: {invoice['potencia_maxima_demandada']} kW"
                )

            # ✅ DISTRIBUIDORA Y UBICACIÓN (ANTES IGNORADOS)
            if invoice.get("distribuidora"):
                context_parts.append(f"- Distribuidora: {invoice['distribuidora']}")
            if invoice.get("codigo_postal"):
                context_parts.append(f"- Código postal: {invoice['codigo_postal']}")

            # ✅ DATOS TEMPORALES Y FACTURACIÓN (ANTES IGNORADOS)
            if invoice.get("periodo_facturacion_dias"):
                context_parts.append(
                    f"- Período facturación: {invoice['periodo_facturacion_dias']} días"
                )
            if invoice.get("fecha_emision"):
                context_parts.append(f"- Fecha emisión: {invoice['fecha_emision']}")

            # ✅ CALCULAR PORCENTAJES AUTOMÁTICAMENTE
            if invoice.get("peak_percent_from_invoice"):
                context_parts.append(
                    f"- Consumo en horas punta: {invoice['peak_percent_from_invoice']}%"
                )
            elif invoice.get("kwh_punta") and invoice.get("kwh_consumidos"):
                peak_percent = round(
                    (invoice["kwh_punta"] / invoice["kwh_consumidos"]) * 100, 1
                )
                context_parts.append(f"- Consumo en horas punta: {peak_percent}%")

        # ✅ DATOS DEL HOGAR Y PERFIL (ANTES IGNORADOS PARCIALMENTE)
        household_info = []
        if user_context.get("home_type"):
            household_info.append(f"Tipo: {user_context['home_type']}")
        if user_context.get("num_inhabitants"):
            household_info.append(f"Habitantes: {user_context['num_inhabitants']}")
        if user_context.get("heating_type"):
            household_info.append(f"Calefacción: {user_context['heating_type']}")
        if user_context.get("has_ac"):
            household_info.append("Aire acondicionado: Sí")
        if user_context.get("has_pool"):
            household_info.append("Piscina: Sí")
        if user_context.get("is_teleworker"):
            household_info.append("Teletrabajo: Sí")
        if user_context.get("has_solar_panels"):
            household_info.append("Paneles solares: Sí")
        if user_context.get("post_code_prefix"):
            household_info.append(f"CP: {user_context['post_code_prefix']}")

        if household_info:
            context_parts.append(f"🏠 PERFIL DEL HOGAR: {' | '.join(household_info)}")

        # ✅ APRENDIZAJE AUTOMÁTICO Y PATRONES (MANTENIDO Y MEJORADO)
        if user_context.get("ai_learned_patterns"):
            patterns = user_context["ai_learned_patterns"]
            context_parts.append("🧠 PATRONES APRENDIDOS:")

            if "communication_style" in patterns:
                style = patterns["communication_style"]["data"]
                context_parts.append(
                    f"- Estilo comunicación: {style.get('formality_level', 'normal')}"
                )
                if style.get("message_length_preference"):
                    context_parts.append(
                        f"- Prefiere respuestas: {style['message_length_preference']}"
                    )

            if "interest_topics" in patterns:
                topics = patterns["interest_topics"]["data"]
                top_topics = [k for k, v in topics.items() if v > 0]
                if top_topics:
                    context_parts.append(
                        f"- Temas de interés: {', '.join(top_topics[:3])}"
                    )

            if "satisfaction_history" in patterns:
                satisfaction_data = patterns["satisfaction_history"]["data"]
                if satisfaction_data:
                    avg_satisfaction = sum(
                        item.get("sentiment_score", 0)
                        for item in satisfaction_data[-3:]
                    ) / min(3, len(satisfaction_data))
                    if avg_satisfaction > 0.3:
                        context_parts.append("- Historial: Generalmente satisfecho")
                    elif avg_satisfaction < -0.3:
                        context_parts.append(
                            "- Historial: Ha tenido frustraciones previas"
                        )

        # ✅ RESUMEN DE COMPLETITUD DE DATOS
        data_completeness = self._calculate_data_completeness(user_context)
        if data_completeness >= 90:
            context_parts.append(
                "📊 DATOS: Perfil completo (90%+) - Máxima personalización disponible"
            )
        elif data_completeness >= 70:
            context_parts.append(
                "📊 DATOS: Perfil detallado (70%+) - Alta personalización"
            )
        elif data_completeness >= 50:
            context_parts.append(
                "📊 DATOS: Perfil básico (50%+) - Personalización media"
            )
        else:
            context_parts.append(
                "📊 DATOS: Perfil mínimo (<50%) - Personalización básica"
            )

        return "\n".join(context_parts)

    def _calculate_data_completeness(self, user_context: Dict[str, Any]) -> float:
        """Calcula el porcentaje de completitud de datos del usuario (0-100)"""
        score = 0
        total_possible = 100

        # Datos básicos (30 puntos)
        if user_context.get("user_name"):
            score += 10
        if user_context.get("last_invoice", {}).get("kwh_consumidos"):
            score += 10
        if user_context.get("last_invoice", {}).get("coste_total"):
            score += 10

        # Datos de factura avanzados (40 puntos)
        invoice = user_context.get("last_invoice", {})
        if invoice.get("comercializadora"):
            score += 8
        if invoice.get("kwh_punta") or invoice.get("kwh_valle"):
            score += 8
        if invoice.get("potencia_contratada_kw"):
            score += 8
        if invoice.get("distribuidora"):
            score += 8
        if invoice.get("tariff_name_from_invoice"):
            score += 8

        # Datos del hogar (20 puntos)
        if user_context.get("home_type"):
            score += 5
        if user_context.get("num_inhabitants"):
            score += 5
        if user_context.get("post_code_prefix"):
            score += 5
        if any(
            [
                user_context.get("has_ac"),
                user_context.get("has_pool"),
                user_context.get("heating_type"),
            ]
        ):
            score += 5

        # Aprendizaje automático (10 puntos)
        if user_context.get("ai_learned_patterns"):
            score += 10

        return min(100, score)

    def _should_consult_expert_bot(
        self, user_message: str, user_context: Optional[Dict[str, Any]]
    ) -> bool:
        """
        🎯 LÓGICA ROBUSTA PARA CONSULTAR RECOMENDACIONES DE TARIFAS

        SOLO consulta el recomendador cuando el usuario ESPECÍFICAMENTE pide:
        - Recomendaciones de tarifas
        - Comparaciones entre tarifas
        - Cambios de tarifa
        - Análisis de ahorro

        NO consulta para preguntas generales sobre precios o información
        """
        message_lower = user_message.lower()

        # 🔥 PALABRAS CLAVE ESPECÍFICAS PARA RECOMENDACIONES (SIN FALSOS POSITIVOS)
        recommendation_keywords = [
            "recomienda",
            "recomiéndame",
            "recomiendame",
            "recomendación",
            "recomendaciones",
            "mejor tarifa",
            "qué tarifa",
            "qué tarifas",
            "que tarifas",
            "cuál tarifa",
            "cual tarifa",
            "cuáles tarifas",
            "cuales tarifas",
            "dime tarifas",
            "cambiar tarifa",
            "cambio tarifa",
            "cambio de tarifa",
            "cambiar de tarifa",
            "comparar tarifas",
            "comparar tarifa",
            "alternativas tarifas",
            "otras tarifas",
            "otras opciones tarifas",
            # 🔥 AÑADIR PALABRAS CLAVE PARA PRECIOS ACTUALES
            "precio actual",
            "precio de la luz",
            "precio energía",
            "precio luz",
            "precios actuales",
            "precio hoy",
            "precio ahora",
            "cuánto cuesta",
            "cuanto cuesta",
            "coste actual",
            "coste energía",
            "tarifa actual",
            "precio kwh",
            "precio por kwh",
        ]

        # 🔥 PALABRAS CLAVE DE AHORRO CON CONTEXTO ESPECÍFICO
        savings_with_context = [
            "ahorrar tarifa",
            "ahorro tarifa",
            "ahorrar con tarifa",
            "ahorro con tarifa",
            "ahorrar cambiando",
            "ahorro cambiando",
        ]

        # 🔥 VERIFICAR RECOMENDACIONES ESPECÍFICAS
        has_recommendation_intent = any(
            keyword in message_lower for keyword in recommendation_keywords
        )

        # 🔥 VERIFICAR AHORRO CON CONTEXTO ESPECÍFICO
        has_savings_intent = any(
            keyword in message_lower for keyword in savings_with_context
        )

        # 🔥 VERIFICAR SOLICITUDES DIRECTAS DE TARIFAS DISPONIBLES
        direct_tariff_requests = [
            "tarifas hay",
            "qué tarifas hay",
            "que tarifas hay",
            "tarifas existen",
            "tarifas disponibles",
            "opciones de tarifas",
            "opciones tarifas",
        ]

        has_direct_tariff_request = any(
            phrase in message_lower for phrase in direct_tariff_requests
        )

        # 🔥 CONDICIÓN ROBUSTA: SOLO CONSULTAR SI HAY INTENCIÓN CLARA DE RECOMENDACIÓN
        should_consult = bool(
            has_recommendation_intent or has_savings_intent or has_direct_tariff_request
        )

        if should_consult:
            logging.info(
                f"🎯 Consultando recomendaciones de tarifas para: '{user_message[:50]}...'"
            )
        else:
            logging.info(
                f"ℹ️ Pregunta general sin necesidad de recomendaciones: '{user_message[:50]}...'"
            )

        return should_consult

    def _consult_expert_bot(
        self, user_message: str, user_context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Consulta endpoint de datos del mercado de tarifas para precios actuales"""
        try:
            from flask import g

            # Verificar si tenemos token de autorización
            if not hasattr(g, "token") or not g.token:
                logging.warning(
                    "⚠️ No hay token disponible para consultar datos del mercado"
                )
                return {}

            # URL del endpoint correcto - DATOS DEL MERCADO CON PRECIOS REALES
            energy_ia_api_url = "http://localhost:8002"  # URL local del servicio actual

            market_data_url = f"{energy_ia_api_url}/api/v1/energy/tariffs/market-data"

            headers = {
                "Authorization": f"Bearer {g.token}",
                "Content-Type": "application/json",
            }

            response = requests.get(market_data_url, headers=headers, timeout=15)

            if response.status_code == 200:
                result: Dict[str, Any] = response.json()
                logging.info("✅ Datos del mercado de tarifas obtenidos exitosamente")
                return result.get("data", {})
            else:
                logging.warning(
                    f"⚠️ Endpoint market-data respuesta: {response.status_code}"
                )
                return {}

        except Exception as e:
            logging.error(f"❌ Error consultando datos del mercado: {str(e)}")
            return {}

    def _integrate_expert_response(
        self, enhanced_message: str, expert_response: Dict[str, Any]
    ) -> str:
        """Integra datos del mercado de tarifas en el mensaje empresarial"""
        if not expert_response:
            return enhanced_message

        # ⚡ PROCESAR DATOS DEL MERCADO DE TARIFAS
        if expert_response.get("tariffs"):
            tariffs = expert_response["tariffs"]
            market_stats = expert_response.get("market_statistics", {})

            market_data_context = (
                "\n\n=== ⚡ DATOS ACTUALES DEL MERCADO ELÉCTRICO ===\n"
            )

            # Agregar estadísticas del mercado
            if market_stats:
                total_tariffs = market_stats.get("total_tariffs", 0)
                providers = market_stats.get("providers", 0)
                last_updated = market_stats.get("last_updated", "")

                market_data_context += f"📊 Tarifas disponibles: {total_tariffs} de {providers} proveedores\n"
                if last_updated:
                    market_data_context += (
                        f"📅 Última actualización: {last_updated}\n\n"
                    )

            # Procesar tarifas con precios actuales
            pvpc_tariffs = []
            fixed_tariffs = []

            for tariff in tariffs[:10]:  # Top 10 tarifas
                provider = tariff.get("provider_name", "Proveedor")
                name = tariff.get("tariff_name", "Tarifa")
                tariff_type = tariff.get("tariff_type", "fixed")

                # Precios por kWh
                price_flat = tariff.get("kwh_price_flat")
                price_peak = tariff.get("kwh_price_peak")
                price_valley = tariff.get("kwh_price_valley")
                is_pvpc = tariff.get("is_pvpc", False)

                tariff_info = f"🏢 {provider} - {name}\n"

                if is_pvpc:
                    tariff_info += "   💡 PVPC (Precio Variable del Mercado)\n"
                    pvpc_tariffs.append(tariff)
                else:
                    tariff_info += f"   💡 Tarifa {tariff_type.upper()}\n"
                    fixed_tariffs.append(tariff)

                # Mostrar precios según disponibilidad
                if price_peak and price_valley:
                    tariff_info += f"   ⚡ Punta: {price_peak:.3f}€/kWh\n"
                    tariff_info += f"   🌙 Valle: {price_valley:.3f}€/kWh\n"
                elif price_flat:
                    tariff_info += f"   ⚡ Precio fijo: {price_flat:.3f}€/kWh\n"

                tariff_info += "\n"
                market_data_context += tariff_info

            # Agregar análisis de mercado
            if pvpc_tariffs and fixed_tariffs:
                market_data_context += (
                    "💡 ANÁLISIS: Disponibles tarifas fijas y variables (PVPC)\n"
                )
            elif pvpc_tariffs:
                market_data_context += (
                    "💡 ANÁLISIS: Principalmente tarifas variables (PVPC)\n"
                )
            elif fixed_tariffs:
                market_data_context += "💡 ANÁLISIS: Principalmente tarifas fijas\n"

            market_data_context += "\nINSTRUCCIÓN: USA estos datos REALES del mercado para responder sobre precios actuales de la energía.\n"
            enhanced_message += market_data_context

        # Compatibilidad con respuestas de recomendaciones legacy
        elif expert_response.get("recommendations"):
            recommendations = expert_response["recommendations"]
            analysis_summary = expert_response.get("analysis_summary", {})

            tariff_recommendations = (
                "\n\n=== 🎯 RECOMENDACIONES ESPECÍFICAS DE TARIFAS ===\n"
            )

            # Agregar resumen del análisis
            if analysis_summary:
                current_cost = analysis_summary.get("current_monthly_cost", 0)
                best_savings = analysis_summary.get("best_potential_savings", 0)
                tariff_recommendations += f"💰 Coste actual: {current_cost}€/mes\n"
                tariff_recommendations += (
                    f"💸 Mejor ahorro potencial: {best_savings}€/año\n\n"
                )

            # Agregar top 3 recomendaciones
            for i, rec in enumerate(recommendations[:3], 1):
                provider = rec.get("provider_name", "Proveedor")
                tariff = rec.get("tariff_name", "Tarifa")
                monthly_cost = rec.get("cost_analysis", {}).get("monthly_cost", 0)
                savings = rec.get("potential_savings", 0)

                tariff_recommendations += f"{i}. {provider} - {tariff}\n"
                tariff_recommendations += f"   💵 Coste: {monthly_cost}€/mes\n"
                tariff_recommendations += f"   💰 Ahorro: {savings}€/año\n\n"

            tariff_recommendations += "INSTRUCCIÓN: USA estas recomendaciones EXACTAS con nombres específicos y ahorros calculados.\n"
            enhanced_message += tariff_recommendations

        # Mantener compatibilidad con respuestas legacy
        elif expert_response.get("analysis"):
            enhanced_message += (
                f"\n\n=== 🎯 ANÁLISIS EXPERT_BOT ===\n{expert_response['analysis']}"
            )

        return enhanced_message

    def _analyze_response_quality(
        self, user_message: str, response: str, user_context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analiza calidad de la respuesta generada"""
        try:
            # Métricas básicas de calidad
            response_length = len(response)
            question_answered = "?" in user_message and len(response) > 50
            specific_data_used = bool(
                user_context
                and any(
                    str(value) in response
                    for value in [
                        user_context.get("last_invoice", {}).get("kwh_consumidos"),
                        user_context.get("last_invoice", {}).get("coste_total"),
                        user_context.get("user_name"),
                    ]
                    if value
                )
            )

            # Cálculo de score de calidad
            quality_score = 0.0
            if response_length > 100:
                quality_score += 0.3
            if question_answered:
                quality_score += 0.3
            if specific_data_used:
                quality_score += 0.4

            return {
                "quality_score": min(1.0, quality_score),
                "response_length": response_length,
                "question_answered": question_answered,
                "specific_data_used": specific_data_used,
                "timestamp": now_spanish_iso(),
            }

        except Exception as e:
            logging.error(f"❌ Error analizando calidad: {str(e)}")
            return {"quality_score": 0.0, "error": str(e)}

    def _log_enterprise_interaction(
        self,
        user_message: str,
        response: str,
        user_context: Optional[Dict[str, Any]],
        sentiment_analysis: Dict[str, Any],
        response_analysis: Dict[str, Any],
        response_time: float,
    ) -> Dict[str, Any]:
        """Registra interacción con métricas empresariales"""
        try:
            interaction_id = str(uuid.uuid4())

            interaction_data = {
                "interaction_id": interaction_id,
                "timestamp": now_spanish_iso(),
                "user_message": user_message,
                "response": response,
                "response_time": response_time,
                "sentiment_score": sentiment_analysis.get("score", 0.0),
                "quality_score": response_analysis.get("quality_score", 0.0),
                "context_completeness": len(user_context) if user_context else 0,
                "personalization_level": self._calculate_personalization_level(
                    user_context
                ),
                "user_id": user_context.get("uid") if user_context else None,
                "service": "energy_ia_api_copy",
            }

            # Log a BigQuery si está disponible
            if self.bigquery_client:
                self._log_to_bigquery(interaction_data)

            logging.info(f"📊 Interacción empresarial registrada: {interaction_id}")

            return interaction_data

        except Exception as e:
            logging.error(f"❌ Error logging empresarial: {str(e)}")
            return {"interaction_id": "error", "error": str(e)}

    def _log_to_bigquery(self, interaction_data: Dict[str, Any]) -> None:
        """Registra en BigQuery para análisis empresarial - USANDO CAMPOS CORRECTOS DE conversations_log"""
        try:
            if not self.bigquery_client:
                return

            table_ref = self.bigquery_client.dataset(self.bq_dataset_id).table(
                self.interaction_log_table
            )

            # USAR SOLO CAMPOS EXACTOS DE conversations_log - 16 CAMPOS COMPLETOS
            row = {
                "conversation_id": interaction_data.get("interaction_id", ""),
                "message_id": f"{interaction_data.get('interaction_id', '')}_msg",
                "user_id": interaction_data.get("user_id", ""),
                "timestamp_utc": interaction_data["timestamp"],
                "sender": "user",
                "message_text": interaction_data.get("user_message", ""),
                "intent_detected": interaction_data.get("intent", ""),
                "bot_action": "response",
                "sentiment": interaction_data.get("sentiment_score", "neutral"),
                "deleted": False,
                "deleted_at": None,
                "response_text": interaction_data.get("response", ""),
                "context_completeness": interaction_data.get(
                    "personalization_level", 0
                ),
                "response_time_ms": int(
                    interaction_data.get("response_time", 0) * 1000
                ),
                "session_info": json.dumps(
                    {
                        "user_agent": "energy_ia_chatbot",
                        "platform": "web",
                        "version": "2025.1",
                        "api_version": "v1",
                    }
                ),
                "metadata": json.dumps(
                    {
                        "service": "energy_ia_api",
                        "endpoint": "generative_chat",
                        "features_used": interaction_data.get("features_used", []),
                        "personalization_data": interaction_data.get(
                            "personalization_data", {}
                        ),
                    }
                ),
            }

            errors = self.bigquery_client.insert_rows_json(table_ref, [row])
            if errors:
                logging.error(f"❌ Error insertando en BigQuery: {errors}")
            else:
                logging.info(
                    f"✅ Interacción guardada en BigQuery: {interaction_data.get('interaction_id', 'unknown')}"
                )

        except Exception as e:
            logging.error(f"❌ Error logging BigQuery: {str(e)}")

    def _update_learning_patterns(
        self, user_context: Dict[str, Any], interaction_data: Dict[str, Any]
    ) -> None:
        """Actualiza patrones de aprendizaje automático"""
        try:
            if not user_context or not user_context.get("uid"):
                return

            # Actualizar patrones de comunicación
            if "ai_learned_patterns" not in user_context:
                user_context["ai_learned_patterns"] = {}

            patterns = user_context["ai_learned_patterns"]

            # Actualizar estilo de comunicación
            if "communication_style" not in patterns:
                patterns["communication_style"] = {
                    "data": {},
                    "updated": now_spanish_iso(),
                }

            comm_style = patterns["communication_style"]["data"]

            # Analizar longitud de mensaje preferida
            message_length = len(interaction_data["user_message"])
            if message_length > 200:
                comm_style["message_length_preference"] = "long"
            elif message_length < 50:
                comm_style["message_length_preference"] = "short"
            else:
                comm_style["message_length_preference"] = "medium"

            # Actualizar nivel de satisfacción
            if "satisfaction_history" not in patterns:
                patterns["satisfaction_history"] = {
                    "data": [],
                    "updated": now_spanish_iso(),
                }

            satisfaction_data = patterns["satisfaction_history"]["data"]
            satisfaction_data.append(
                {
                    "timestamp": interaction_data["timestamp"],
                    "sentiment_score": interaction_data["sentiment_score"],
                    "quality_score": interaction_data["quality_score"],
                }
            )

            # Mantener solo últimos 10 registros
            if len(satisfaction_data) > 10:
                satisfaction_data = satisfaction_data[-10:]

            patterns["satisfaction_history"]["data"] = satisfaction_data

            logging.info(f"🧠 Patrones de aprendizaje actualizados para usuario")

        except Exception as e:
            logging.error(f"❌ Error actualizando patrones: {str(e)}")

    def _calculate_personalization_level(
        self, user_context: Optional[Dict[str, Any]]
    ) -> str:
        """Calcula nivel de personalización aplicado"""
        if not user_context:
            return "none"

        score = 0

        if user_context.get("user_name"):
            score += 1
        if user_context.get("last_invoice"):
            score += 2
        if user_context.get("ai_learned_patterns"):
            score += 3
        if user_context.get("home_type"):
            score += 1

        if score >= 6:
            return "maximum"
        elif score >= 4:
            return "high"
        elif score >= 2:
            return "medium"
        elif score >= 1:
            return "low"
        else:
            return "none"

    def _serialize_chat_history(self, history: List[Any]) -> List[Dict[str, Any]]:
        """Serializa historial de chat"""
        try:
            serializable_history = []

            for content in history:
                try:
                    serializable_history.append(
                        {
                            "role": content.role,
                            "parts": [
                                part.text if hasattr(part, "text") else str(part)
                                for part in content.parts
                            ],
                            "timestamp": now_spanish_iso(),
                        }
                    )
                except Exception as e:
                    logging.warning(f"⚠️ Error serializando historial: {str(e)}")

            return serializable_history

        except Exception as e:
            logging.error(f"❌ Error serializando historial: {str(e)}")
            return []

    def _add_links_if_user_requests(self, user_message: str, response_text: str) -> str:
        """
        🔗 Añade enlaces SOLO cuando el usuario los solicita específicamente

        Args:
            user_message: Mensaje original del usuario
            response_text: Respuesta generada por el chatbot

        Returns:
            str: Respuesta con enlaces HTML solo si el usuario los solicitó
        """
        try:
            if not user_message or not response_text:
                return response_text

            user_message_lower = user_message.lower()

            # Solo añadir enlaces si el usuario EXPLÍCITAMENTE los solicita
            user_requests_help = any(
                word in user_message_lower
                for word in [
                    "ayuda",
                    "ayúdame",
                    "help",
                    "soporte",
                    "contacto",
                    "contactar",
                ]
            )

            user_requests_articles = any(
                word in user_message_lower
                for word in [
                    "artículo",
                    "artículos",
                    "blog",
                    "leer más",
                    "más información",
                    "información adicional",
                ]
            )

            user_requests_tools = any(
                word in user_message_lower
                for word in [
                    "calculadora",
                    "calcular",
                    "herramienta",
                    "simular",
                    "simulación",
                ]
            )

            # Solo aplicar enlaces si hay solicitud específica del usuario
            if user_requests_help or user_requests_articles or user_requests_tools:
                return self.links_service.analyze_and_enhance_response(response_text)

            # Si no hay solicitud específica, devolver respuesta original
            return response_text

        except Exception as e:
            logging.error(f"❌ Error en análisis contextual de enlaces: {str(e)}")
            return response_text

    def get_enterprise_metrics(self) -> Dict[str, Any]:
        """Obtiene métricas empresariales del servicio"""
        try:
            base_metrics = {
                "service_status": "active",
                "model_initialized": self.model is not None,
                "bigquery_connected": self.bigquery_client is not None,
                "auth_system": "active",
                "ai_learning_service_connected": self.ai_learning_service is not None,
                "timestamp": now_spanish_iso(),
                "version": "2025_enterprise",
            }

            # 🧠 MÉTRICAS AVANZADAS DEL AI LEARNING SERVICE
            if self.ai_learning_service:
                try:
                    ai_metrics = (
                        self.ai_learning_service.get_enterprise_performance_metrics()
                    )
                    base_metrics["ai_learning_metrics"] = ai_metrics
                    base_metrics["ai_learning_status"] = "active"
                except Exception as e:
                    logging.warning(
                        f"⚠️ Error obteniendo métricas AI Learning: {str(e)}"
                    )
                    base_metrics["ai_learning_status"] = "error"
                    base_metrics["ai_learning_error"] = str(e)
            else:
                base_metrics["ai_learning_status"] = "not_available"

            return base_metrics

        except Exception as e:
            logging.error(f"❌ Error obteniendo métricas: {str(e)}")
            return {"service_status": "error", "error": str(e)}


# 🏢 FUNCIÓN FACTORY EMPRESARIAL PARA CHAT SERVICE
# Esta función garantiza compatibilidad con toda la aplicación

# Instancia singleton para compatibilidad empresarial
_enterprise_chat_service_instance = None


def get_enterprise_chat_service():
    """
    Factory function empresarial para obtener instancia de Chat Service

    Returns:
        EnterpriseGenerativeChatService: Instancia singleton del servicio

    Raises:
        AppError: Si hay problemas de configuración o inicialización
    """
    global _enterprise_chat_service_instance

    if _enterprise_chat_service_instance is None:
        try:
            _enterprise_chat_service_instance = EnterpriseGenerativeChatService()
            logger.info(
                "🏢 Factory function: EnterpriseGenerativeChatService inicializado"
            )
        except Exception as e:
            logger.error(f"❌ Error en factory function Chat: {str(e)}")
            raise AppError(f"Error inicializando Chat service: {str(e)}", 500)

    return _enterprise_chat_service_instance


logger = logging.getLogger(__name__)
logger.info("✅ Módulo EnterpriseGenerativeChatService cargado correctamente")

# 🔄 ALIAS DE COMPATIBILIDAD EMPRESARIAL
# Mantiene compatibilidad con código existente que usa GenerativeChatService
GenerativeChatService = EnterpriseGenerativeChatService

logger.info("✅ Alias de compatibilidad GenerativeChatService creado")
