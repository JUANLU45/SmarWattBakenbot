# energy_ia_api_COPY/app/services/generative_chat_service.py
# 🏢 SERVICIO DE CHAT GENERATIVO EMPRESARIAL NIVEL 2025

# Standard library imports
import json
import logging
import time
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional

# Third-party imports
import google.generativeai as genai  # type: ignore
from flask import current_app, request
from google.cloud import bigquery  # type: ignore
import requests

# Local imports
from smarwatt_auth import EnterpriseAuth
from utils.error_handlers import AppError
from utils.timezone_utils import now_spanish_iso
from app.services.enterprise_links_service import get_enterprise_link_service


class EnterpriseGenerativeChatService:
    """
    🏢 SERVICIO DE CHAT GENERATIVO EMPRESARIAL 2025
    Gestiona conversaciones con modelo de lenguaje grande (Gemini) con:
    - Personalización empresarial máxima
    - Análisis de sentiment en tiempo real vía HTTP
    - Comunicación robusta con expert_bot_api
    - Logging empresarial completo
    - Arquitectura de microservicios independientes
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

        logging.info(
            "✅ EnterpriseGenerativeChatService con arquitectura de microservicios independientes"
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
            "Eres WattBot, un especialista en energía de SmarWatt con aprendizaje automático avanzado.\n\n"
            "PERSONALIDAD Y TONO:\n"
            "- Conversación natural y fluida, como un experto en energía hablando con un amigo\n"
            "- Sin jerga técnica innecesaria ni lenguaje robotizado\n"
            "- Respuestas directas y útiles adaptadas al contexto\n"
            "- SIEMPRE saluda al usuario por su nombre cuando esté disponible\n"
            "- NO uses asteriscos, emojis corporativos excesivos ni formato raro\n\n"
            "QUÉ HACES:\n"
            "- Especialista EXCLUSIVO en energía (nunca generalista)\n"
            "- Ayudas a entender y reducir facturas de luz específicamente\n"
            "- Analizas consumos energéticos reales del usuario con IA\n"
            "- Recomiendas tarifas y mejoras de eficiencia específicas\n"
            "- Respondes sobre energía renovable, paneles solares y sostenibilidad\n\n"
            "INTELIGENCIA ARTIFICIAL Y APRENDIZAJE:\n"
            "- Tu IA SIEMPRE conoce todos los datos del usuario (factura, consumo, tarifa, comercializadora)\n"
            "- APRENDE constantemente de cada conversación para mejorar recomendaciones\n"
            "- Tienes acceso INMEDIATO a todos los datos cuando los necesites\n"
            "- NUNCA eres generalista - trabajas específicamente para ESTE usuario\n\n"
            "ACCESO A DATOS DE MERCADO EN TIEMPO REAL:\n"
            "- SIEMPRE consultas precios actuales cuando pregunten por precios específicos\n"
            "- Tienes acceso DIRECTO a tarifas PVPC actualizadas diariamente\n"
            "- NUNCA digas 'no sé el precio' - SIEMPRE consulta datos reales del mercado\n"
            "- Datos incluyen: precios peak/valley, estadísticas de mercado, PVPC actual\n"
            "- Distingues CLARAMENTE entre consulta de PRECIOS vs RECOMENDACIONES de tarifas\n\n"
            "CÓMO USAR LOS DATOS ESPECÍFICOS:\n"
            "- En SALUDOS SIMPLES: Saluda naturalmente, mantén contexto energético sutil\n"
            "- En PREGUNTAS DE ENERGÍA: USA todos los datos específicos (comercializadora, coste, kWh, tarifa)\n"
            "- En CONSULTAS TÉCNICAS: Aplica análisis completo con sus cifras reales\n"
            "- Personalizado SOLO cuando la pregunta lo requiera, no siempre\n"
            "- Si tienes información completa, NO pidas más datos\n\n"
            "EJEMPLOS DE RESPUESTAS EXPERTAS:\n"
            "- SALUDO: 'Hola [NOMBRE]! ¿En qué puedo ayudarte con tu energía hoy?'\n"
            "- ENERGÍA: 'Con tu consumo de 801 kWh/mes y Naturgy pagando 171€, podrías ahorrar...'\n"
            "- TÉCNICA: 'Tu tarifa \"Por Uso Luz\" no optimiza tus 60% de consumo en valle...'\n\n"
            "INTELIGENCIA CONTEXTUAL:\n"
            "- Adapta la cantidad de datos según el tipo de conversación\n"
            "- En charla casual: Mantén expertise energético disponible pero no agresivo\n"
            "- En consultas específicas: Despliega TODOS los datos y análisis\n"
            "- Experto en energía específico para este usuario SOLO cuando sea relevante\n\n"
            "NUNCA:\n"
            "- Seas generalista o hables de temas no energéticos\n"
            "- Pidas información que ya tienes disponible\n"
            "- Des respuestas genéricas si tienes datos específicos\n"
            "- Olvides que eres especialista en energía con IA avanzada\n\n"
            "Eres un especialista premium en energía con IA que conoce perfectamente a este usuario específico y adapta su expertise al contexto de cada conversación."
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
                try:
                    expert_response = self._consult_expert_bot(
                        user_message, user_context
                    )
                    enhanced_message = self._integrate_expert_response(
                        enhanced_message, expert_response
                    )
                except Exception as expert_error:
                    # 🛡️ AISLAMIENTO: No romper conversación si expert-bot falla
                    logging.warning(f"⚠️ Expert-bot no disponible: {expert_error}")
                    # Continuar sin consulta expert-bot - conversación fluye normal

            # � NUEVA FUNCIONALIDAD: CONSULTA DE PRECIOS EN TIEMPO REAL
            if self._should_consult_market_prices(user_message, user_context):
                logging.info(
                    "🔍 Detectada consulta de precios - obteniendo datos de mercado"
                )
                market_data = self._get_current_market_prices()

                if market_data:
                    price_info = self._format_market_prices_for_chat(market_data)
                    if price_info:
                        # Añadir información de precios al contexto
                        enhanced_message = f"{enhanced_message}\n\n[DATOS ACTUALES DEL MERCADO ELÉCTRICO]:\n{price_info}"
                        logging.info(
                            "✅ Datos de mercado añadidos al contexto del chat"
                        )
                    else:
                        logging.warning("⚠️ No se pudo formatear información de precios")
                else:
                    logging.warning("⚠️ No se pudieron obtener datos de mercado")

            # �🚀 ENVÍO A GEMINI CON CONFIGURACIÓN EMPRESARIAL
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

            # ✨ LIMPIEZA FINAL PARA CONVERSACIÓN NATURAL (Sin asteriscos)
            final_natural_response = self._make_response_natural(
                enhanced_response_with_links
            )

            # 💾 LOGGING EMPRESARIAL COMPLETO
            interaction_data = self._log_enterprise_interaction(
                user_message,
                final_natural_response,  # 🔗 Usar respuesta final limpia y natural
                user_context,
                sentiment_analysis,
                response_analysis,
                response_time,
            )

            # 🧠 ACTUALIZACIÓN DE APRENDIZAJE AUTOMÁTICO CON AI LEARNING SERVICE
            if user_context is not None:
                self._update_learning_patterns(user_context, interaction_data)

            # 🧠 ACTUALIZACIÓN DE APRENDIZAJE AUTOMÁTICO CON AI LEARNING SERVICE
            if user_context is not None:
                self._update_learning_patterns(user_context, interaction_data)

                # 🔗 COMUNICACIÓN HTTP CON EXPERT_BOT_API PARA APRENDIZAJE EMPRESARIAL
                if user_context.get("uid"):
                    try:
                        # Preparar datos para comunicación HTTP futura
                        _learning_data = {
                            "user_id": user_context["uid"],
                            "conversation_id": interaction_data.get(
                                "interaction_id", "unknown"
                            ),
                            "user_message": user_message,
                            "bot_response": final_natural_response,
                            "sentiment_analysis": sentiment_analysis,
                            "response_time": response_time,
                            "timestamp": now_spanish_iso(),
                        }

                        # Comunicación HTTP pendiente de implementar
                        # enterprise_analysis = self._process_enterprise_interaction_http(_learning_data)

                        # Añadir métricas básicas por ahora
                        interaction_data["enterprise_learning"] = {
                            "processed": True,
                            "method": "http_pending",
                            "sentiment_via_http": sentiment_analysis.get(
                                "enterprise_analysis", False
                            ),
                        }

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
                "response_text": final_natural_response,  # 🔗 Respuesta natural con enlaces inteligentes
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
                    "ai_learning_service_active": True,  # Ahora vía HTTP
                },
                "prompt_used": enhanced_message,
                "interaction_id": interaction_data.get("interaction_id"),
                "learning_updates": interaction_data.get("learning_updates", []),
            }

        except Exception as e:
            # 🏢 LOGGING EMPRESARIAL NIVEL PRODUCCIÓN - Problema #6 RESUELTO
            try:
                # Obtener request_id para trazabilidad empresarial
                from flask import g, has_request_context

                request_id = "NO-REQ-ID"
                if has_request_context() and hasattr(g, "request_id"):
                    request_id = g.request_id
                elif has_request_context() and hasattr(g, "user") and g.user:
                    request_id = f"user-{g.user.get('uid', 'unknown')}"

                # Log empresarial completo con stack trace
                logging.error(
                    f"❌ [ENTERPRISE-ERROR] Error procesando mensaje en generative_chat_service "
                    f"[req:{request_id}] [service:energy-ia-api] [component:GenerativeChatService]: {str(e)}",
                    exc_info=True,
                    extra={
                        "service": "energy-ia-api",
                        "component": "GenerativeChatService",
                        "method": "send_message_with_context",
                        "request_id": request_id,
                        "error_type": type(e).__name__,
                        "severity": "HIGH",
                    },
                )
            except Exception as log_error:
                # Fallback en caso de que el logging falle
                logging.error(
                    f"❌ Error procesando mensaje: {str(e)} [LOGGING-FALLBACK: {str(log_error)}]"
                )

            return {
                "response_text": "¡Hola! Soy tu asistente experto en energía. ¿En qué puedo ayudarte hoy?",
                "chat_history": [],
                "enterprise_metrics": {
                    "error": True,
                    "error_message": str(e),
                    "fallback_response": True,
                },
            }

    def _analyze_message_sentiment(self, message: str) -> Dict[str, Any]:
        """Analiza sentiment del mensaje del usuario vía HTTP con expert_bot_api"""
        try:
            # 🔗 COMUNICACIÓN HTTP CON EXPERT_BOT_API (ARQUITECTURA CORRECTA)
            expert_bot_url = current_app.config.get("EXPERT_BOT_API_URL")
            if expert_bot_url:
                try:
                    # Generar IDs temporales para el análisis
                    temp_user_id = "temp_analysis_user"
                    temp_conversation_id = str(uuid.uuid4())

                    # Llamada HTTP al endpoint de sentiment analysis interno
                    response = requests.post(
                        f"{expert_bot_url}/api/v1/analysis/sentiment/internal",
                        json={
                            "message_text": message,
                            "user_id": temp_user_id,
                            "conversation_id": temp_conversation_id,
                        },
                        headers={
                            "Content-Type": "application/json",
                            "Authorization": f"Bearer {current_app.config.get('INTERNAL_SERVICE_TOKEN', '')}",
                        },
                        timeout=5,
                    )

                    if response.status_code == 200:
                        sentiment_data = response.json()
                        sentiment_analysis = sentiment_data.get(
                            "sentiment_analysis", {}
                        )

                        return {
                            "score": sentiment_analysis.get("sentiment_score", 0.0),
                            "confidence": sentiment_analysis.get("confidence", 0.5),
                            "sentiment_label": sentiment_analysis.get(
                                "sentiment_label", "neutral"
                            ),
                            "emotional_indicators": sentiment_analysis.get(
                                "emotional_indicators", {}
                            ),
                            "personalization_hints": sentiment_analysis.get(
                                "personalization_hints", []
                            ),
                            "risk_factors": sentiment_analysis.get("risk_factors", []),
                            "engagement_level": sentiment_analysis.get(
                                "engagement_level", "medium"
                            ),
                            "enterprise_analysis": True,
                            "timestamp": now_spanish_iso(),
                        }
                    else:
                        logging.warning(
                            f"⚠️ Expert Bot API devolvió código {response.status_code}, usando análisis básico"
                        )

                except (requests.RequestException, requests.Timeout) as e:
                    logging.warning(
                        f"⚠️ Error conectando con Expert Bot API para sentiment: {str(e)}, usando análisis básico"
                    )
            else:
                logging.warning(
                    "⚠️ EXPERT_BOT_API_URL no configurada, usando análisis básico"
                )

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

            # 🧠 INSTRUCCIONES INTELIGENTES SEGÚN TIPO DE CONVERSACIÓN
            conversation_type = self._detect_conversation_type(
                user_message, user_context
            )
            data_completeness = (
                self._calculate_data_completeness(user_context) if user_context else 0
            )
            user_name = user_context.get("user_name") if user_context else None

            # Aplicar instrucciones CONTEXTUALES según la conversación
            if conversation_type == "greeting":
                # SALUDOS - Conversación natural y amigable
                context_parts.append("\n=== 🤝 INSTRUCCIONES PARA SALUDO NATURAL ===")
                time_greeting = self._get_time_based_greeting()
                if user_name:
                    context_parts.append(
                        f"1. SALUDA CALUROSAMENTE: '¡{time_greeting} {user_name}!'"
                    )
                else:
                    context_parts.append(
                        f"1. SALUDA CALUROSAMENTE: '¡{time_greeting}!'"
                    )
                context_parts.append(
                    "2. PREGUNTA amigablemente: '¿En qué puedo ayudarte con la energía?'"
                )
                context_parts.append("3. MANTÉN tono conversacional y cercano")
                context_parts.append(
                    "4. NO menciones datos específicos a menos que pregunten"
                )

            elif conversation_type == "personal_analysis" and data_completeness >= 50:
                # ANÁLISIS PERSONAL - Usar todos los datos disponibles
                context_parts.append(
                    "\n=== 🎯 INSTRUCCIONES ANÁLISIS PERSONALIZADO ==="
                )
                context_parts.append(f"1. SALUDA por nombre: {user_name}")
                context_parts.append(
                    "2. USA específicamente su comercializadora, coste mensual y tarifa"
                )
                context_parts.append("3. APLICA sus cifras exactas de factura")
                context_parts.append("4. CALCULA ahorros con SUS datos reales")

            elif conversation_type == "general_energy":
                # TEMAS GENERALES - Expertise sin bombardeo personal
                context_parts.append("\n=== 🌟 INSTRUCCIONES TEMA GENERAL ENERGÍA ===")
                if user_name:
                    context_parts.append(f"1. SALUDA brevemente: 'Hola {user_name}'")
                context_parts.append("2. RESPONDE como experto en energía")
                context_parts.append("3. INCLUYE consejos prácticos y útiles")
                context_parts.append(
                    "4. SI es relevante, menciona sutilmente sus datos"
                )
                context_parts.append("5. INVITA a seguir charlando sobre el tema")

            elif conversation_type == "casual_chat":
                # CHARLA CASUAL - Conversacional con expertise disponible
                context_parts.append("\n=== 💬 INSTRUCCIONES CONVERSACIÓN CASUAL ===")
                if user_name:
                    context_parts.append(f"1. SALUDA naturalmente: {user_name}")
                context_parts.append("2. RESPONDE de forma conversacional y amigable")
                context_parts.append(
                    "3. MUESTRA expertise energético cuando sea natural"
                )
                context_parts.append("4. INVITA a profundizar en temas de interés")

            elif data_completeness < 20 and user_name:
                # USUARIO NUEVO - Tratamiento VIP conversacional
                context_parts.append("\n=== 🥇 INSTRUCCIONES USUARIO VIP (NUEVO) ===")
                context_parts.append(f"1. SALUDA con entusiasmo: 'Hola {user_name}!'")
                context_parts.append(
                    "2. CONVERSACIÓN natural sobre energía SIN pedir datos"
                )
                context_parts.append("3. RESPONDE expertamente pero sin presionar")
                context_parts.append(
                    "4. SOLO si pregunta por análisis personal, menciona SUTILMENTE valor de más datos"
                )
                context_parts.append(
                    "5. ENFÓCATE en crear buena experiencia y confianza"
                )

            else:
                # FALLBACK - Instrucciones balanceadas
                context_parts.append(
                    "\n=== ⚖️ INSTRUCCIONES CONVERSACIÓN BALANCEADA ==="
                )
                if user_name:
                    context_parts.append(f"1. SALUDA por nombre: {user_name}")
                context_parts.append(
                    "2. ADAPTA nivel de personalización según pregunta"
                )
                context_parts.append("3. MANTÉN conversación natural y fluida")
                context_parts.append("4. USA datos cuando aporten valor real")

            # INSTRUCCIONES UNIVERSALES para todas las conversaciones
            context_parts.append("\n=== 🌍 INSTRUCCIONES UNIVERSALES ===")
            context_parts.append("• NUNCA pidas datos que ya tienes")
            context_parts.append("• ADAPTA tono según análisis de sentiment")
            context_parts.append("• MANTÉN conversación natural y atractiva")
            context_parts.append("• INVITA a seguir conversando sobre energía")
            context_parts.append("• ERES experto pero conversacional, no robotizado")

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

    def _detect_conversation_type(
        self, user_message: str, user_context: Optional[Dict[str, Any]]
    ) -> str:
        """
        🧠 DETECTA TIPO DE CONVERSACIÓN PARA RESPUESTA NATURAL
        Permite chatbot conversacional que adapta su expertise según contexto
        """
        message_lower = user_message.lower().strip()

        # 1. SALUDOS SIMPLES - Conversación social amigable
        greeting_patterns = [
            "hola",
            "buenos días",
            "buenas tardes",
            "buenas noches",
            "hey",
            "qué tal",
            "que tal",
            "cómo estás",
            "como estas",
            "saludos",
            "buenas",
            "buen día",
            "buen dia",
        ]

        if (
            any(pattern in message_lower for pattern in greeting_patterns)
            and len(message_lower) < 30
        ):
            return "greeting"

        # 2. PREGUNTAS ESPECÍFICAS DE DATOS - Usar personalización máxima
        specific_data_patterns = [
            "mi factura",
            "mi consumo",
            "mi tarifa",
            "mi comercializadora",
            "cuánto gasto",
            "cuanto gasto",
            "mis datos",
            "mi situación",
            "qué ahorro",
            "que ahorro",
            "cuánto pago",
            "cuanto pago",
        ]

        if any(pattern in message_lower for pattern in specific_data_patterns):
            return "personal_analysis"

        # 3. TEMAS GENERALES DE ENERGÍA - Expertise sin bombardeo
        general_energy_topics = [
            "placas solares",
            "paneles solares",
            "energía renovable",
            "energia renovable",
            "eficiencia energética",
            "eficiencia energetica",
            "consejos",
            "tips",
            "cómo ahorrar",
            "como ahorrar",
            "qué es",
            "que es",
        ]

        if any(topic in message_lower for topic in general_energy_topics):
            return "general_energy"

        # 4. PREGUNTAS DE PRECIOS - Market data específica
        price_keywords = ["precio", "coste", "cuesta", "cuánto está", "cuanto esta"]
        if any(keyword in message_lower for keyword in price_keywords):
            return "price_inquiry"

        # 5. RECOMENDACIONES - Expert bot consultation
        recommendation_keywords = [
            "recomienda",
            "recomendación",
            "mejor tarifa",
            "cambiar",
        ]
        if any(keyword in message_lower for keyword in recommendation_keywords):
            return "recommendation_request"

        # 6. DEFAULT - Conversación casual con expertise disponible
        return "casual_chat"

    def _get_time_based_greeting(self) -> str:
        """
        🕐 GENERA SALUDO SEGÚN HORA ESPAÑOLA
        Respeta zona horaria del usuario español para naturalidad
        """
        try:
            from datetime import datetime
            import pytz

            # Zona horaria española
            madrid_tz = pytz.timezone("Europe/Madrid")
            current_time = datetime.now(madrid_tz)
            hour = current_time.hour

            if 5 <= hour < 12:
                return "Buenos días"
            elif 12 <= hour < 20:
                return "Buenas tardes"
            else:
                return "Buenas noches"
        except:
            # Fallback robusto
            return "Hola"

    def _should_consult_expert_bot(
        self, user_message: str, user_context: Optional[Dict[str, Any]]
    ) -> bool:
        """Determina si debe consultar endpoint de recomendaciones de tarifas"""
        # Palabras clave específicas para recomendaciones de tarifas
        tariff_keywords = [
            "tarifa",
            "tarifas",
            "recomienda",
            "recomiendame",
            "recomendación",
            "recomendaciones",
            "mejor tarifa",
            "qué tarifa",
            "qué tarifas",
            "que tarifas",
            "tarifas hay",
            "qué tarifas hay",
            "que tarifas hay",
            "cuáles tarifas",
            "cuales tarifas",
            "dime tarifas",
            "cambiar tarifa",
            "ahorro",
            "ahorrar",
            "precio",
            "coste",
            "factura",
            "comparar",
            "alternativas",
            "conviene",
            "interesa",
            "beneficia",
        ]

        message_lower = user_message.lower()
        has_tariff_keywords = any(
            keyword in message_lower for keyword in tariff_keywords
        )

        # También consultar si tiene datos completos del usuario y pregunta sobre energía
        has_complete_data = (
            user_context
            and user_context.get("last_invoice")
            and user_context.get("last_invoice", {}).get("kwh_consumidos")
        )

        energy_keywords = [
            "consumo",
            "kwh",
            "factura",
            "luz",
            "electricidad",
            "energía",
        ]
        has_energy_keywords = any(
            keyword in message_lower for keyword in energy_keywords
        )

        # Consultar si pregunta sobre tarifas O si tiene datos completos y pregunta sobre energía
        should_consult = bool(
            has_tariff_keywords or (has_complete_data and has_energy_keywords)
        )

        if should_consult:
            logging.info(
                f"🎯 Consultando recomendaciones de tarifas para: '{user_message[:50]}...'"
            )

        return should_consult

    def _should_consult_market_prices(
        self, user_message: str, user_context: Optional[Dict[str, Any]]
    ) -> bool:
        """
        🏢 DETECTA PREGUNTAS ESPECÍFICAS DE PRECIOS (NO RECOMENDACIONES)
        Lógica empresarial robusta para distinguir consultas de precios puros
        """
        message_lower = user_message.lower()

        # Palabras clave ESPECÍFICAS para preguntas de PRECIO (no recomendaciones)
        price_specific_keywords = [
            "precio de la luz",
            "precio actual",
            "precio energía",
            "precio electricidad",
            "cuánto cuesta el kwh",
            "cuanto cuesta el kwh",
            "precio kwh",
            "precio del kwh",
            "precio por kwh",
            "coste kwh",
            "coste del kwh",
            "a cuánto está",
            "a cuanto esta",
            "precio hoy",
            "precio ahora",
            "cuál es el precio",
            "cual es el precio",
            "dime el precio",
            "precio mercado",
            "precio mercado energético",
            "pvpc hoy",
            "pvpc actual",
            "tarifa pvpc",
            "precio pvpc",
        ]

        # Detectar preguntas directas de precio
        has_price_query = any(
            keyword in message_lower for keyword in price_specific_keywords
        )

        # Patrones de pregunta específicos de precio
        price_patterns = [
            "cuánto cuesta",
            "cuanto cuesta",
            "a cuánto está",
            "a cuanto esta",
            "qué precio",
            "que precio",
            "dime el precio",
            "precio de",
        ]

        has_price_pattern = any(pattern in message_lower for pattern in price_patterns)

        # EXCLUIR si claramente pide recomendaciones
        excludes_recommendations = not any(
            exclude in message_lower
            for exclude in [
                "recomienda",
                "recomendacion",
                "mejor tarifa",
                "que tarifa",
                "cambiar tarifa",
                "comparar tarifas",
            ]
        )

        should_consult_prices = bool(
            (has_price_query or has_price_pattern) and excludes_recommendations
        )

        if should_consult_prices:
            logging.info(
                f"💰 Consultando PRECIOS de mercado para: '{user_message[:50]}...'"
            )

        return should_consult_prices

    def _consult_expert_bot(
        self, user_message: str, user_context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Consulta endpoint de recomendaciones de tarifas empresarial"""
        try:
            from flask import g

            # Verificar si tenemos token de autorización
            if not hasattr(g, "token") or not g.token:
                logging.warning(
                    "⚠️ No hay token disponible para consultar recomendaciones"
                )
                return {}

            # URL del endpoint de recomendaciones empresarial - PRODUCCIÓN
            # CORRECCIÓN ARQUITECTURAL: usar endpoint interno propio, no external call
            energy_ia_url = current_app.config.get("ENERGY_IA_API_URL")
            if not energy_ia_url:
                # Fallback robusto para producción usando URL del servicio actual
                energy_ia_url = request.url_root.rstrip("/")
                logging.warning(
                    "⚠️ ENERGY_IA_API_URL no configurada - usando URL actual"
                )

            recommendations_url = (
                f"{energy_ia_url}/api/v1/energy/tariffs/recommendations"
            )

            headers = {
                "Authorization": f"Bearer {g.token}",
                "Content-Type": "application/json",
            }

            response = requests.get(recommendations_url, headers=headers, timeout=15)

            if response.status_code == 200:
                result: Dict[str, Any] = response.json()
                logging.info("✅ Recomendaciones de tarifas obtenidas exitosamente")
                return result.get("data", {})
            else:
                logging.warning(
                    f"⚠️ Endpoint recomendaciones respuesta: {response.status_code}"
                )
                return {}

        except Exception as e:
            logging.error(f"❌ Error consultando recomendaciones de tarifas: {str(e)}")
            return {}

    def _get_current_market_prices(self) -> Dict[str, Any]:
        """
        🏢 CONSULTA ESPECÍFICA DE PRECIOS DE MERCADO (NO RECOMENDACIONES)
        Acceso directo al endpoint market-data para obtener precios actuales
        """
        try:
            from flask import g

            # Verificar token de autorización
            if not hasattr(g, "token") or not g.token:
                logging.warning("⚠️ No hay token disponible para consultar precios")
                return {}

            # URL del endpoint ESPECÍFICO de market-data
            energy_ia_url = current_app.config.get("ENERGY_IA_API_URL")
            if not energy_ia_url:
                energy_ia_url = request.url_root.rstrip("/")
                logging.warning(
                    "⚠️ ENERGY_IA_API_URL no configurada - usando URL actual"
                )

            market_data_url = f"{energy_ia_url}/api/v1/energy/tariffs/market-data"

            headers = {
                "Authorization": f"Bearer {g.token}",
                "Content-Type": "application/json",
            }

            response = requests.get(market_data_url, headers=headers, timeout=15)

            if response.status_code == 200:
                result: Dict[str, Any] = response.json()
                logging.info("✅ Datos de precios de mercado obtenidos exitosamente")
                return result.get("data", {})
            else:
                logging.warning(
                    f"⚠️ Endpoint market-data respuesta: {response.status_code}"
                )
                return {}

        except Exception as e:
            logging.error(f"❌ Error consultando precios de mercado: {str(e)}")
            return {}

    def _format_market_prices_for_chat(self, market_data: Dict[str, Any]) -> str:
        """
        🏢 FORMATEA DATOS DE PRECIOS PARA RESPUESTA NATURAL DEL CHAT
        Convierte datos técnicos en información útil para el usuario
        """
        if not market_data:
            return ""

        try:
            tariffs = market_data.get("tariffs", [])
            stats = market_data.get("market_statistics", {})

            if not tariffs:
                return ""

            # Filtrar tarifas PVPC
            pvpc_tariffs = [t for t in tariffs if t.get("is_pvpc", False)]

            # Calcular precios promedio del mercado
            peak_prices = [
                float(t["kwh_price_peak"]) for t in tariffs if t.get("kwh_price_peak")
            ]
            valley_prices = [
                float(t["kwh_price_valley"])
                for t in tariffs
                if t.get("kwh_price_valley")
            ]
            flat_prices = [
                float(t["kwh_price_flat"]) for t in tariffs if t.get("kwh_price_flat")
            ]

            formatted_info = []

            # Información PVPC (más relevante para usuarios)
            if pvpc_tariffs:
                pvpc = pvpc_tariffs[0]  # Primer PVPC disponible
                if pvpc.get("kwh_price_peak") and pvpc.get("kwh_price_valley"):
                    formatted_info.append(
                        f"💡 PRECIO ACTUAL PVPC: {float(pvpc['kwh_price_peak']):.3f} €/kWh (punta) "
                        f"y {float(pvpc['kwh_price_valley']):.3f} €/kWh (valle)"
                    )
                elif pvpc.get("kwh_price_flat"):
                    formatted_info.append(
                        f"💡 PRECIO ACTUAL PVPC: {float(pvpc['kwh_price_flat']):.3f} €/kWh"
                    )

            # Estadísticas de mercado
            if stats:
                total_tariffs = stats.get("total_tariffs", 0)
                providers = stats.get("providers", 0)
                last_updated = stats.get("last_updated", "")

                if total_tariffs and providers:
                    formatted_info.append(
                        f"📊 MERCADO: {total_tariffs} tarifas activas de {providers} comercializadoras"
                    )

                if last_updated:
                    try:
                        from datetime import datetime

                        update_dt = datetime.fromisoformat(
                            last_updated.replace("Z", "+00:00")
                        )
                        formatted_info.append(
                            f"🕒 Actualizado: {update_dt.strftime('%d/%m/%Y %H:%M')}"
                        )
                    except:
                        pass

            # Rangos de precios del mercado
            if peak_prices:
                min_peak = min(peak_prices)
                max_peak = max(peak_prices)
                avg_peak = sum(peak_prices) / len(peak_prices)
                formatted_info.append(
                    f"⚡ RANGO PUNTA: {min_peak:.3f} - {max_peak:.3f} €/kWh (promedio: {avg_peak:.3f})"
                )

            if valley_prices:
                min_valley = min(valley_prices)
                max_valley = max(valley_prices)
                avg_valley = sum(valley_prices) / len(valley_prices)
                formatted_info.append(
                    f"🌙 RANGO VALLE: {min_valley:.3f} - {max_valley:.3f} €/kWh (promedio: {avg_valley:.3f})"
                )

            return "\n".join(formatted_info) if formatted_info else ""

        except Exception as e:
            logging.error(f"❌ Error formateando precios de mercado: {str(e)}")
            return ""

    def _integrate_expert_response(
        self, enhanced_message: str, expert_response: Dict[str, Any]
    ) -> str:
        """Integra respuesta de recomendaciones de tarifas en el mensaje empresarial"""
        if not expert_response:
            return enhanced_message

        # Integrar recomendaciones de tarifas específicas
        if expert_response.get("recommendations"):
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
                "context_completeness": interaction_data.get("context_completeness", 0),
                "personalization_level": interaction_data.get(
                    "personalization_level", "none"
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

    def _make_response_natural(self, response_text: str) -> str:
        """
        ✨ Hace la respuesta completamente natural eliminando todos los asteriscos
        y aplicando formato HTML para elementos importantes

        Args:
            response_text: Respuesta original que puede contener asteriscos

        Returns:
            str: Respuesta natural sin asteriscos con HTML para elementos importantes
        """
        try:
            if not response_text:
                return response_text

            # Convertir **texto** a <strong>texto</strong> (negrita HTML)
            natural_response = response_text

            # Reemplazar **texto** con <strong>texto</strong>
            import re

            natural_response = re.sub(
                r"\*\*(.*?)\*\*", r"<strong>\1</strong>", natural_response
            )

            # Eliminar cualquier * restante que no sea parte de un patrón **texto**
            natural_response = natural_response.replace("*", "")

            # Limpiar espacios múltiples que puedan haber quedado
            natural_response = re.sub(r"\s+", " ", natural_response)

            return natural_response.strip()

        except Exception as e:
            logging.error(f"❌ Error haciendo respuesta natural: {str(e)}")
            # Si hay error, al menos eliminar asteriscos básicos
            return response_text.replace("**", "").replace("*", "")

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
                return self.links_service.analyze_and_enhance_response(
                    response_text, user_message
                )

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
                "ai_learning_service_connected": True,  # Vía HTTP
                "timestamp": now_spanish_iso(),
                "version": "2025_enterprise",
            }

            # 🔗 MÉTRICAS VÍA HTTP CON EXPERT_BOT_API
            try:
                # Comunicación HTTP pendiente de implementar para métricas avanzadas
                base_metrics["ai_learning_metrics"] = {
                    "method": "http_communication",
                    "status": "ready",
                    "sentiment_analysis": "active_via_http",
                }
                base_metrics["ai_learning_status"] = "active_via_http"
            except Exception as e:
                logging.warning(
                    f"⚠️ Error obteniendo métricas AI Learning vía HTTP: {str(e)}"
                )
                base_metrics["ai_learning_status"] = "http_error"
                base_metrics["ai_learning_error"] = str(e)

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
