# expert_bot_api_COPY/app/services/chat_service.py

import logging
import time
import json
import uuid
import threading
import requests
from typing import Dict, Any, Optional, List
from flask import current_app
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed

from google.cloud import bigquery
from google.api_core import exceptions as google_exceptions

# Configurar logger
logger = logging.getLogger(__name__)
from utils.error_handlers import AppError

# 🧠 IMPORTAR SISTEMA DE APRENDIZAJE AUTOMÁTICO EMPRESARIAL
try:
    from app.services.ai_learning_service import AILearningService
except ImportError:
    try:
        from .ai_learning_service import AILearningService
    except ImportError:
        ai_learning_service_unavailable = True
        logging.warning("🔴 AILearningService no disponible")

# 🔧 IMPORTAR CLIENTE API ROBUSTO EMPRESARIAL
try:
    from app.services.energy_ia_client import EnergyIAApiClient
except ImportError:
    try:
        from .energy_ia_client import EnergyIAApiClient
    except ImportError:
        EnergyIAApiClient = None  # type: ignore
        logging.warning("🔴 EnergyIAApiClient no disponible")

# 🔗 ENLACES EMPRESARIALES: Gestionados centralmente por Energy-IA-API
# ✅ DECISIÓN ARQUITECTÓNICA: Expert-Bot se enfoca solo en análisis experto


class ChatService:
    """
    🏢 SERVICIO DE CHAT EMPRESARIAL DE NIVEL PROFESIONAL 2025

    Características empresariales:
    - Aprendizaje automático totalmente integrado
    - Comunicación robusta entre microservicios
    - Gestión avanzada de conversaciones
    - Monitoreo y logging empresarial
    - Tolerancia a fallos y recuperación automática
    - Escalabilidad y rendimiento optimizado
    """

    _bigquery_client_instance = None
    _ai_learning_service_instance = None
    _lock = threading.Lock()
    _executor = ThreadPoolExecutor(max_workers=10)

    def __init__(self, energy_ia_api_url: str) -> None:
        """Inicialización empresarial con validación completa."""
        self.energy_ia_api_url = energy_ia_api_url
        self.project_id = current_app.config["GCP_PROJECT_ID"]
        self.bq_dataset_id = current_app.config.get("BQ_DATASET_ID", "smartwatt_data")
        self.bq_conversations_table_id = current_app.config.get(
            "BQ_CONVERSATIONS_TABLE_ID", "conversations_log"
        )
        self.bq_feedback_table_id = current_app.config.get(
            "BQ_FEEDBACK_TABLE_ID", "feedback_log"
        )

        # 🔧 INICIALIZAR CLIENTE API ROBUSTO EMPRESARIAL
        if EnergyIAApiClient is not None:
            self.energy_ia_client = EnergyIAApiClient(
                base_url=energy_ia_api_url, timeout=30
            )
        else:
            self.energy_ia_client = None
            logging.warning("🔴 EnergyIAApiClient no disponible - modo degradado")

        # 🔗 DESHABILITADO: SERVICIO DE ENLACES EMPRESARIAL (EVITAR REDUNDANCIA)
        # ✅ CORRECCIÓN: Energy IA ya maneja enlaces, evitamos duplicación
        self.links_service = None
        logging.info(
            "� Servicio de enlaces deshabilitado en Expert Bot para evitar redundancia"
        )

        # Configuración empresarial
        self.max_retries = 3
        self.timeout_seconds = 30
        self.conversation_cache: Dict[str, Dict[str, Any]] = {}
        self.current_conversation_id: Optional[str] = None
        self.performance_metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "avg_response_time": 0.0,
        }

        # Inicialización thread-safe empresarial
        self._initialize_enterprise_services()

    def _initialize_enterprise_services(self) -> None:
        """Inicialización robusta de servicios empresariales."""
        with ChatService._lock:
            # Inicializar BigQuery con reintentos
            if ChatService._bigquery_client_instance is None:
                for attempt in range(self.max_retries):
                    try:
                        ChatService._bigquery_client_instance = bigquery.Client(
                            project=self.project_id
                        )
                        logging.info(
                            "🏢 Cliente BigQuery inicializado correctamente - Intento %d",
                            attempt + 1,
                        )
                        break
                    except (
                        google_exceptions.GoogleAPICallError,
                        OSError,
                        ValueError,
                    ) as e:
                        logging.error(
                            "Error al inicializar BigQuery - Intento %d: %s",
                            attempt + 1,
                            e,
                        )
                        if attempt == self.max_retries - 1:
                            raise AppError(
                                "Error crítico: No se pudo conectar a BigQuery después de múltiples intentos.",
                                500,
                            ) from e
                        time.sleep(2**attempt)  # Backoff exponencial

            # Inicializar AI Learning Service empresarial
            if (
                ChatService._ai_learning_service_instance is None
                and current_app.config.get("AI_LEARNING_ENABLED", True)
                and AILearningService is not None
            ):
                try:
                    ChatService._ai_learning_service_instance = AILearningService()  # type: ignore
                    logging.info(
                        "🧠 Sistema de Aprendizaje Automático Empresarial inicializado"
                    )
                except (ImportError, AttributeError, TypeError) as e:
                    logging.error("Error al inicializar AILearningService: %s", e)
                    ChatService._ai_learning_service_instance = None

        self.bigquery_client = ChatService._bigquery_client_instance
        self.ai_learning_service = ChatService._ai_learning_service_instance

    def _log_to_bigquery_enterprise(
        self, table_id: str, rows: List[Dict[str, Any]]
    ) -> bool:
        """Logging empresarial a BigQuery con reintentos y validación."""
        if self.bigquery_client is None:
            logging.error("Cliente BigQuery no disponible - escalando error")
            return False

        for attempt in range(self.max_retries):
            try:
                table_ref = self.bigquery_client.dataset(self.bq_dataset_id).table(
                    table_id
                )
                errors = self.bigquery_client.insert_rows_json(table_ref, rows)

                if errors:
                    logging.error(
                        "Errores en inserción BigQuery - Intento %d: %s",
                        attempt + 1,
                        errors,
                    )
                    if attempt == self.max_retries - 1:
                        return False
                    time.sleep(1)
                    continue

                logging.info("✅ Datos insertados correctamente en %s", table_id)
                return True

            except google_exceptions.GoogleAPICallError as e:
                logging.error("Error API BigQuery - Intento %d: %s", attempt + 1, e)
                if attempt == self.max_retries - 1:
                    return False
                time.sleep(2**attempt)

            except (ValueError, TypeError, ConnectionError) as e:
                logging.error(
                    "Error inesperado BigQuery - Intento %d: %s", attempt + 1, e
                )
                if attempt == self.max_retries - 1:
                    return False
                time.sleep(1)

        return False

    def _log_to_bigquery_with_auto_schema(
        self, table_id: str, rows: List[Dict[str, Any]]
    ) -> bool:
        """Logging empresarial con auto-creación de columnas faltantes."""
        if self.bigquery_client is None:
            logging.error("Cliente BigQuery no disponible - escalando error")
            return False

        for attempt in range(self.max_retries):
            try:
                table_ref = self.bigquery_client.dataset(self.bq_dataset_id).table(
                    table_id
                )

                job_config = bigquery.LoadJobConfig(
                    source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
                    schema_update_options=[
                        bigquery.SchemaUpdateOption.ALLOW_FIELD_ADDITION,
                        bigquery.SchemaUpdateOption.ALLOW_FIELD_RELAXATION,
                    ],
                    write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
                    autodetect=True,
                )

                job = self.bigquery_client.load_table_from_json(
                    rows, table_ref, job_config=job_config
                )

                job.result()
                logging.info("✅ Datos insertados con auto-schema en %s", table_id)
                return True

            except google_exceptions.GoogleAPICallError as e:
                logging.error(
                    "Error API BigQuery auto-schema - Intento %d: %s", attempt + 1, e
                )
                if attempt == self.max_retries - 1:
                    logging.info("🔄 Fallback a método estándar para %s", table_id)
                    return self._log_to_bigquery_enterprise(table_id, rows)
                time.sleep(2**attempt)

            except (ValueError, TypeError, ConnectionError) as e:
                logging.error(
                    "Error inesperado auto-schema - Intento %d: %s", attempt + 1, e
                )
                if attempt == self.max_retries - 1:
                    logging.info("🔄 Fallback a método estándar para %s", table_id)
                    return self._log_to_bigquery_enterprise(table_id, rows)
                time.sleep(1)
                time.sleep(1)

        return False

    def _log_conversation_turn_to_bigquery(
        self,
        user_id: str,
        sender: str,
        message_text: str,
        intent: Optional[str] = None,
        bot_action: Optional[str] = None,
        sentiment: Optional[str] = None,
        conversation_id: Optional[str] = None,
        response_time: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None,
        response_text: Optional[str] = None,  # 🔥 PARÁMETRO CRÍTICO AÑADIDO
    ) -> None:
        """🚀 Logging empresarial de conversaciones con metadatos enriquecidos y response_text corregido."""
        if conversation_id is None:
            conversation_id = getattr(
                self, "current_conversation_id", str(uuid.uuid4())
            )
            self.current_conversation_id = conversation_id

        row = {
            "conversation_id": conversation_id,
            "message_id": str(uuid.uuid4()),
            "user_id": user_id,
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "sender": sender,
            "message_text": message_text,
            "intent_detected": intent,
            "bot_action": bot_action,
            "sentiment": sentiment,
            "deleted": False,
            "deleted_at": None,
            "response_text": response_text,  # 🔥 CORREGIDO: Usar parámetro real en lugar de None
            "context_completeness": None,  # Se calcula si es necesario
            "response_time_ms": int(response_time * 1000) if response_time else None,
            "session_info": json.dumps(
                {
                    "user_agent": "enterprise_chatbot",
                    "platform": "web",
                    "version": "2025.1",
                }
            ),
            "metadata": json.dumps(metadata) if metadata else None,
        }

        self._log_to_bigquery_enterprise(self.bq_conversations_table_id, [row])

        # 🧠 REGISTRAR EN AI_SENTIMENT_ANALYSIS SI ES MENSAJE DE USUARIO
        if sender == "user" and self.ai_learning_service:
            self._log_sentiment_analysis(
                user_id=user_id,
                conversation_id=conversation_id,
                message_text=message_text,
                sentiment_label=sentiment if sentiment else "neutral",
            )

    def _log_sentiment_analysis(
        self,
        user_id: str,
        conversation_id: str,
        message_text: str,
        sentiment_label: str = "neutral",
    ) -> None:
        """🧠 Registrar análisis de sentiment en ai_sentiment_analysis con campos exactos."""
        try:
            if self.ai_learning_service:
                # Usar el método del ai_learning_service para análisis completo
                sentiment_analysis = (
                    self.ai_learning_service.analyze_sentiment_enterprise(
                        user_id=user_id,
                        conversation_id=conversation_id,
                        message_text=message_text,
                    )
                )
                logging.info(f"✅ Sentiment analysis registrado para user {user_id}")
        except Exception as e:
            logging.error(f"❌ Error registrando sentiment analysis: {e}")

    def _log_feedback_to_bigquery(
        self,
        user_id: str,
        recommendation_type: str,
        feedback_useful: bool,
        comments: Optional[str] = None,
        rating: Optional[int] = None,
        conversation_id: Optional[str] = None,
    ) -> bool:
        """Logging empresarial de feedback con análisis avanzado."""
        row = {
            "feedback_id": str(uuid.uuid4()),
            "user_id": user_id,
            "conversation_id": conversation_id,
            "recommendation_type": recommendation_type,
            "feedback_useful": feedback_useful,
            "rating": rating,
            "comments": comments,
            "submitted_at": datetime.now(timezone.utc).isoformat(),
            "analysis_metadata": {
                "feedback_source": "enterprise_interface",
                "processed_version": "2025.1",
            },
        }

        return self._log_to_bigquery_enterprise(self.bq_feedback_table_id, [row])

    def start_session(self, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """🚀 Inicio de sesión empresarial con validación completa y saludo personalizado."""
        start_time = time.time()

        try:
            session_id = str(uuid.uuid4())
            self.current_conversation_id = session_id

            # Validar perfil de usuario
            if not user_profile.get("uid"):
                raise AppError("Perfil de usuario inválido", 400)

            # 🎯 OBTENER DATOS DEL USUARIO PARA SALUDO PERSONALIZADO
            user_context = self._get_user_context_for_welcome(user_profile["uid"])

            # 🎯 GENERAR SALUDO PERSONALIZADO PREMIUM CON HORA
            welcome_message = self._generate_personalized_welcome(user_context)

            # Inicializar contexto empresarial
            enterprise_context = {
                "session_id": session_id,
                "user_id": user_profile["uid"],
                "session_start": datetime.now(timezone.utc).isoformat(),
                "platform": "enterprise_web",
                "capabilities": [
                    "ml_recommendations",
                    "hybrid_consultation",
                    "feedback_analysis",
                ],
                "user_context": user_context,
            }

            # Logging empresarial
            self._log_conversation_turn_to_bigquery(
                user_id=user_profile["uid"],
                sender="system",
                message_text="SESSION_START",
                conversation_id=session_id,
                response_time=time.time() - start_time,
                metadata=enterprise_context,
                response_text=None,  # Eventos del sistema no tienen response_text
            )

            # Actualizar métricas
            self.performance_metrics["total_requests"] += 1
            self.performance_metrics["successful_requests"] += 1

            logging.info(
                "🏢 Sesión empresarial iniciada - ID: %s - Usuario: %s",
                session_id,
                user_profile["uid"],
            )

            return {
                "session_id": session_id,
                "welcomeMessage": welcome_message,
                "message": "Sesión empresarial iniciada correctamente",
                "enterprise_features": enterprise_context["capabilities"],
                "status": "success",
            }

        except (ValueError, TypeError, ConnectionError, AppError) as e:
            self.performance_metrics["failed_requests"] += 1
            logging.error("Error al iniciar sesión empresarial: %s", e)
            raise AppError("Error al inicializar sesión empresarial", 500) from e

    def _get_user_context_for_welcome(self, user_id: str) -> Dict[str, Any]:
        """🎯 Obtiene contexto específico del usuario para saludo personalizado"""
        try:
            from app.energy_service import EnergyService

            energy_service = EnergyService()

            # Obtener perfil completo del usuario desde Firestore
            user_doc = energy_service.db.collection("users").document(user_id).get()

            if not user_doc.exists:
                return {"user_name": "", "has_data": False}

            user_data = user_doc.to_dict()

            if user_data is None:
                return {"user_name": "", "has_data": False}

            # Extraer datos relevantes para el saludo
            context = {
                "user_name": user_data.get("displayName", "")
                or user_data.get("email", ""),
                "has_data": True,
                "last_invoice_data": user_data.get("last_invoice_data", {}),
                "consumption_data": {
                    "monthly_kwh": user_data.get("monthly_consumption_kwh", 0),
                    "contracted_power": user_data.get("contracted_power_kw", 0),
                },
                "user_plan": user_data.get("subscription", {}).get("plan", "basic"),
            }

            return context

        except Exception as e:
            import logging

            logging.warning(f"Error obteniendo contexto para saludo: {e}")
            return {"user_name": "", "has_data": False}

    def _generate_personalized_welcome(
        self, user_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """🎯 Genera saludo personalizado milimétricamente perfecto con hora española y datos específicos"""
        from datetime import datetime, timezone, timedelta

        # 🇪🇸 HORA ESPAÑOLA SIMPLIFICADA Y ROBUSTA
        # En julio 2025, España está en horario de verano (UTC+2)
        spain_tz = timezone(timedelta(hours=2))  # UTC+2 (horario de verano español)
        current_time = datetime.now(spain_tz)

        # Determinar saludo según la hora española
        hour = current_time.hour
        if 5 <= hour < 12:
            time_greeting = "Buenos días"
        elif 12 <= hour < 19:
            time_greeting = "Buenas tardes"
        else:
            time_greeting = "Buenas noches"

        time_str = current_time.strftime("%H:%M")

        user_name = user_context.get("user_name", "")
        last_invoice = user_context.get("last_invoice_data", {})

        # 🎯 SALUDO PERSONALIZADO PREMIUM CON DATOS REALES
        if user_name and last_invoice.get("comercializadora"):
            comercializadora = last_invoice.get("comercializadora", "")
            coste_total = last_invoice.get("coste_total", 0)
            tarifa = last_invoice.get("tariff_name_from_invoice", "")

            content = f"""{time_greeting} {user_name}, son las {time_str}.

Soy WattBot, tu asistente energético personalizado. He revisado tu perfil y veo que tienes contratado el servicio con {comercializadora}. 

📊 Tu situación actual:
• Factura mensual: {coste_total}€
• Tarifa contratada: {tarifa}
• Consumo registrado: {last_invoice.get('kwh_consumidos', 0)} kWh/mes

Como usuario Premium, puedo ayudarte con análisis personalizados, recomendaciones específicas para tu consumo y optimización de tu factura energética.

¿En qué puedo ayudarte hoy?"""

        elif user_name:
            content = f"""{time_greeting} {user_name}, son las {time_str}.

Soy WattBot, tu asistente energético personalizado. Estoy aquí para ayudarte con cualquier consulta sobre energía, tarifas y optimización de consumo.

¿En qué puedo ayudarte hoy?"""

        else:
            content = f"""{time_greeting}, son las {time_str}.

Soy WattBot, tu asistente energético. Puedo ayudarte con consultas sobre energía, análisis de consumo y recomendaciones para optimizar tu factura.

¿En qué puedo ayudarte hoy?"""

        return {
            "id": f"welcome_{int(current_time.timestamp())}",
            "type": "bot",
            "content": content,
            "timestamp": current_time.isoformat(),
            "personalized": bool(user_name),
            "premium_data": bool(last_invoice.get("comercializadora")),
        }

    def create_new_conversation(
        self,
        user_profile: Dict[str, Any],
        current_conversation_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """🆕 Crear nueva conversación guardando la actual - EMPRESARIAL."""
        start_time = time.time()

        try:
            user_id = user_profile.get("uid")
            if not user_id:
                raise AppError("Perfil de usuario inválido", 400)

            # Paso 1: Marcar conversación actual como completada si existe
            if current_conversation_id:
                self._mark_conversation_as_completed(user_id, current_conversation_id)
                logger.info(
                    "✅ Conversación %s marcada como completada para usuario: %s",
                    current_conversation_id,
                    user_id,
                )

            # Paso 2: Generar nuevo conversation_id
            new_session_id = str(uuid.uuid4())
            self.current_conversation_id = new_session_id

            # Paso 3: Inicializar contexto empresarial
            enterprise_context = {
                "session_id": new_session_id,
                "user_id": user_id,
                "session_start": datetime.now(timezone.utc).isoformat(),
                "platform": "enterprise_web",
                "previous_conversation_saved": bool(current_conversation_id),
                "previous_conversation_id": current_conversation_id,
                "conversation_type": "new_conversation_request",
                "capabilities": [
                    "ml_recommendations",
                    "hybrid_consultation",
                    "conversation_management",
                ],
            }

            # Paso 4: Registrar inicio de nueva conversación
            self._log_conversation_turn_to_bigquery(
                user_id=user_id,
                sender="system",
                message_text="NEW_CONVERSATION_START",
                conversation_id=new_session_id,
                response_time=time.time() - start_time,
                response_text=None,  # Eventos del sistema no tienen response_text
                metadata=enterprise_context,
            )

            # Paso 5: Actualizar métricas
            self.performance_metrics["total_requests"] += 1
            self.performance_metrics["successful_requests"] += 1

            logger.info(
                "🆕 Nueva conversación creada - ID: %s - Usuario: %s - Anterior: %s",
                new_session_id,
                user_id,
                current_conversation_id or "ninguna",
            )

            return {
                "session_id": new_session_id,
                "conversation_id": new_session_id,  # Para compatibilidad
                "status": "success",
                "message": "Nueva conversación creada correctamente",
                "previous_conversation_saved": bool(current_conversation_id),
                "previous_conversation_id": current_conversation_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "enterprise_features": enterprise_context["capabilities"],
            }

        except (ValueError, TypeError, ConnectionError, AppError) as e:
            self.performance_metrics["failed_requests"] += 1
            logger.error("Error creando nueva conversación: %s", e)
            raise AppError("Error creando nueva conversación empresarial", 500) from e

    def _mark_conversation_as_completed(
        self, user_id: str, conversation_id: str
    ) -> None:
        """🏁 Marcar conversación como completada utilizando tablas existentes."""
        try:
            # Registrar evento de finalización en conversations_log
            completion_metadata = {
                "conversation_status": "completed",
                "completion_reason": "user_requested_new_conversation",
                "completion_method": "enterprise_interface",
                "total_messages": self._count_conversation_messages(
                    user_id, conversation_id
                ),
            }

            self._log_conversation_turn_to_bigquery(
                user_id=user_id,
                sender="system",
                message_text="CONVERSATION_COMPLETED",
                conversation_id=conversation_id,
                response_time=0.0,
                metadata=completion_metadata,
                response_text=None,  # Eventos del sistema no tienen response_text
            )

            logger.info(
                "✅ Conversación %s marcada como completada para usuario: %s",
                conversation_id,
                user_id,
            )

        except Exception as e:
            logger.error(
                "Error marcando conversación %s como completada: %s",
                conversation_id,
                e,
            )
            # No lanzar error aquí - es mejor crear nueva conversación aunque falle el marcado

    def _count_conversation_messages(self, user_id: str, conversation_id: str) -> int:
        """📊 Contar mensajes en conversación para estadísticas."""
        try:
            if not self.bigquery_client:
                return 0

            query = f"""
            SELECT COUNT(*) as message_count
            FROM `{self.project_id}.{self.bq_dataset_id}.{self.bq_conversations_table_id}`
            WHERE conversation_id = @conversation_id 
            AND user_id = @user_id
            AND sender = 'user'
            """

            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter(
                        "conversation_id", "STRING", conversation_id
                    ),
                    bigquery.ScalarQueryParameter("user_id", "STRING", user_id),
                ]
            )

            query_job = self.bigquery_client.query(query, job_config=job_config)
            results = list(query_job.result())

            return results[0].message_count if results else 0

        except Exception as e:
            logger.error("Error contando mensajes de conversación: %s", e)
            return 0

    def process_user_message(
        self, user_profile: Dict[str, Any], user_message: str, conversation_id: str
    ) -> Dict[str, Any]:
        """
        🏢 PROCESAMIENTO EMPRESARIAL DE MENSAJES CON ORQUESTACIÓN AVANZADA

        Características empresariales:
        - Aprendizaje automático integrado en cada paso
        - Métricas de rendimiento en tiempo real
        - Recuperación automática de errores
        - Análisis de sentiment avanzado
        - Comunicación robusta entre servicios
        """
        start_time = time.time()
        user_id = user_profile["uid"]
        self.current_conversation_id = conversation_id

        try:
            # Actualizar métricas
            self.performance_metrics["total_requests"] += 1

            # 🔥 CORREGIDO: Logging del mensaje del usuario con response_text vacío
            self._log_conversation_turn_to_bigquery(
                user_id=user_id,
                sender="user",
                message_text=user_message,
                conversation_id=conversation_id,
                response_time=time.time() - start_time,
                response_text=None,  # Usuario no tiene response_text
            )

            # 2. Obtener contexto empresarial robusto
            user_context = self._get_enterprise_user_context(user_id)

            # 🧠 3. Enriquecimiento con AI Learning empresarial
            if self.ai_learning_service:
                try:
                    enhanced_context = (
                        self.ai_learning_service.enhance_user_context_with_learning(
                            user_id, user_context
                        )
                    )
                    user_context.update(enhanced_context)
                    logging.info(
                        "🧠 Contexto enriquecido empresarialmente para %s", user_id
                    )
                except (AttributeError, TypeError, ConnectionError) as e:
                    logging.warning("Error en enriquecimiento AI (no crítico): %s", e)

            # 4. Análisis de intención empresarial
            intent_analysis = self._analyze_user_intent_enterprise(
                user_message, user_context
            )

            # 5. Orquestación empresarial con paralelización
            bot_response_data = self._orchestrate_enterprise_response(
                user_id, user_message, user_context, intent_analysis
            )

            # 6. Mejora empresarial de respuesta
            enhanced_response = self._enhance_response_enterprise(
                bot_response_data, user_context, intent_analysis
            )

            #  CORREGIDO: Logging de respuesta empresarial con response_text poblado
            response_time = time.time() - start_time
            bot_response_text = enhanced_response.get("response", "")
            self._log_conversation_turn_to_bigquery(
                user_id=user_id,
                sender="bot",
                message_text=user_message,  # 🔥 MANTENER mensaje del usuario en message_text
                conversation_id=conversation_id,
                intent=intent_analysis.get("primary_intent"),
                bot_action=intent_analysis.get("strategy"),
                sentiment=enhanced_response.get("sentiment_analysis"),
                response_time=response_time,
                response_text=bot_response_text,  # 🔥 CRÍTICO: Respuesta del bot en response_text
                metadata={
                    "performance_score": enhanced_response.get("performance_score", 0),
                    "data_completeness": user_context.get("data_completeness", 0),
                    "strategy_confidence": intent_analysis.get("confidence", 0),
                },
            )

            # 🧠 8. Aprendizaje automático empresarial
            if self.ai_learning_service:
                try:
                    self._process_enterprise_learning(
                        user_id,
                        conversation_id,
                        user_message,
                        enhanced_response,
                        user_context,
                        intent_analysis,
                    )
                except (AttributeError, TypeError, ConnectionError) as e:
                    logging.error("Error en aprendizaje empresarial: %s", e)

            # 9. Actualizar métricas de rendimiento
            self._update_performance_metrics(response_time, True)

            # 10. Añadir información empresarial a la respuesta
            enhanced_response.update(
                {
                    "enterprise_metadata": {
                        "response_time_ms": int(response_time * 1000),
                        "performance_score": self._calculate_performance_score(
                            enhanced_response
                        ),
                        "ai_confidence": intent_analysis.get("confidence", 0),
                        "data_quality": user_context.get("data_completeness", 0),
                    },
                    "conversation_id": conversation_id,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
            )

            return enhanced_response

        except (ValueError, TypeError, ConnectionError, AppError) as e:
            self._update_performance_metrics(time.time() - start_time, False)
            logging.error("Error empresarial en procesamiento: %s", e)

            # Respuesta de emergencia empresarial
            return self._get_enterprise_fallback_response(
                user_message, user_context if "user_context" in locals() else {}
            )

    def _get_enterprise_user_context(self, user_id: str) -> Dict[str, Any]:
        """🏢 Obtención empresarial de contexto con múltiples fuentes."""
        context: Dict[str, Any] = {
            "user_id": user_id,
            "data_completeness": 0,
            "available_sources": [],
            "missing_critical_data": [],
            "energy_profile": {},
            "consumption_history": {},
            "preferences": {},
            "last_invoice": {},
            "analytics_summary": {},
            "enterprise_metrics": {
                "context_build_time": 0.0,
                "sources_accessed": 0,
                "data_quality_score": 0,
            },
        }

        start_time = time.time()

        # Usar ThreadPoolExecutor para paralelización empresarial
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {
                executor.submit(self._get_energy_profile, user_id): "energy_profile",
                executor.submit(self._get_analytics_summary, user_id): "analytics",
                executor.submit(self._get_user_preferences, user_id): "preferences",
                executor.submit(self._get_consumption_history, user_id): "consumption",
                executor.submit(self._get_recent_interactions, user_id): "interactions",
            }

            for future in as_completed(futures):
                source_type = futures[future]
                try:
                    result = future.result(timeout=10)
                    if result:
                        context[f"{source_type}_data"] = result
                        context["available_sources"].append(source_type)
                        context["data_completeness"] += 20
                        context["enterprise_metrics"]["sources_accessed"] += 1
                except (TimeoutError, ConnectionError, ValueError) as e:
                    logging.warning(
                        "Error obteniendo %s para %s: %s", source_type, user_id, e
                    )
                    context["missing_critical_data"].append(source_type)

        # Calcular métricas empresariales
        context["enterprise_metrics"]["context_build_time"] = time.time() - start_time
        context["enterprise_metrics"]["data_quality_score"] = min(
            100, context["data_completeness"]
        )

        logging.info(
            "🏢 Contexto empresarial obtenido: %d%% - Fuentes: %d - Tiempo: %.2fs",
            context["data_completeness"],
            len(context["available_sources"]),
            context["enterprise_metrics"]["context_build_time"],
        )

        return context

    def _analyze_user_intent_enterprise(
        self, user_message: str, user_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """🧠 Análisis empresarial de intención con AI avanzada."""

        # Análisis base
        intent_analysis: Dict[str, Any] = {
            "primary_intent": "general_consultation",
            "strategy": "general_chat",
            "confidence": 0.0,
            "enterprise_analysis": {
                "ml_readiness": False,
                "data_sufficiency": False,
                "user_engagement_level": "low",
            },
        }

        # Patrones empresariales mejorados
        ml_patterns = {
            "tariff_optimization": [
                "tarifa",
                "cambio",
                "precio",
                "ahorro",
                "comparar",
                "optimizar",
            ],
            "cost_analysis": [
                "coste",
                "gasto",
                "factura",
                "caro",
                "barato",
                "economico",
            ],
            "consumption_analysis": [
                "consumo",
                "kwh",
                "electricidad",
                "gasto energético",
            ],
            "provider_comparison": [
                "comercializadora",
                "compañía",
                "proveedor",
                "mercado libre",
            ],
        }

        # Análisis de patrones con pesos
        pattern_scores = {}
        for category, patterns in ml_patterns.items():
            score = sum(
                2 if pattern in user_message.lower() else 0 for pattern in patterns
            )
            pattern_scores[category] = score

        # Determinar estrategia basada en datos y patrones
        data_completeness = user_context.get("data_completeness", 0)
        max_score = max(pattern_scores.values()) if pattern_scores.values() else 0

        if max_score > 4 and data_completeness > 50:
            intent_analysis["strategy"] = "ml_recommendations"
            intent_analysis["primary_intent"] = "ml_analysis"
            intent_analysis["confidence"] = min(
                0.9, (max_score + data_completeness) / 100
            )
            intent_analysis["enterprise_analysis"]["ml_readiness"] = True
        elif max_score > 2 and data_completeness > 30:
            intent_analysis["strategy"] = "hybrid_consultation"
            intent_analysis["primary_intent"] = "hybrid_analysis"
            intent_analysis["confidence"] = min(
                0.8, (max_score + data_completeness) / 120
            )
        else:
            intent_analysis["strategy"] = "general_chat"
            intent_analysis["confidence"] = 0.6

        # Análisis empresarial adicional
        intent_analysis["enterprise_analysis"]["data_sufficiency"] = (
            data_completeness > 40
        )
        intent_analysis["enterprise_analysis"]["user_engagement_level"] = (
            "high"
            if len(user_message) > 50
            else "medium" if len(user_message) > 20 else "low"
        )

        return intent_analysis

    def _orchestrate_enterprise_response(
        self,
        user_id: str,
        user_message: str,
        user_context: Dict[str, Any],
        intent_analysis: Dict[str, Any],
    ) -> Dict[str, Any]:
        """🏢 Orquestación empresarial con múltiples estrategias."""

        strategy = intent_analysis.get("strategy", "general_chat")

        try:
            if strategy == "ml_recommendations":
                return self._handle_ml_recommendations_enterprise(
                    user_id, user_message, user_context, intent_analysis
                )
            elif strategy == "hybrid_consultation":
                return self._handle_hybrid_consultation_enterprise(
                    user_id, user_message, user_context, intent_analysis
                )
            else:
                return self._handle_general_chat_enterprise(
                    user_id, user_message, user_context, intent_analysis
                )
        except (ValueError, TypeError, ConnectionError, AppError) as e:
            logging.error("Error en orquestación empresarial: %s", e)
            return self._get_enterprise_fallback_response(user_message, user_context)

    def _handle_ml_recommendations_enterprise(
        self,
        user_id: str,
        user_message: str,
        user_context: Dict[str, Any],
        intent_analysis: Dict[str, Any],
    ) -> Dict[str, Any]:
        """🤖 Recomendaciones ML empresariales con tolerancia a fallos."""

        for attempt in range(self.max_retries):
            try:
                # Preparar contexto empresarial
                ml_context = self._prepare_enterprise_ml_context(user_context)

                # 🏢 Enriquecer contexto con análisis del mensaje del usuario
                ml_context["user_query_analysis"] = {
                    "user_id": user_id,
                    "message_length": len(user_message),
                    "contains_urgency": any(
                        word in user_message.lower()
                        for word in ["urgente", "rapido", "inmediato", "ya"]
                    ),
                    "contains_cost_focus": any(
                        word in user_message.lower()
                        for word in ["barato", "economico", "ahorro", "coste"]
                    ),
                    "intent_confidence": intent_analysis.get("confidence", 0),
                    "query_complexity": len(user_message.split()),
                }

                # Autenticación robusta
                auth_token = self._get_service_to_service_token()

                headers = {
                    "Authorization": f"Bearer {auth_token}",
                    "Content-Type": "application/json",
                    "X-Enterprise-Request": "true",
                    "X-User-ID": user_id,
                    "X-Intent-Confidence": str(intent_analysis.get("confidence", 0)),
                }

                # Llamada al servicio ML
                complete_url = (
                    f"{self.energy_ia_api_url}/api/v1/energy/tariffs/recommendations"
                )

                response = requests.get(
                    complete_url,
                    headers=headers,
                    timeout=self.timeout_seconds,
                    params={"enterprise_mode": "true"},
                )
                response.raise_for_status()

                ml_response = response.json()

                # Enriquecer respuesta empresarial
                return {
                    "response": ml_response.get(
                        "response", "Recomendaciones personalizadas generadas"
                    ),
                    "intent": "ml_recommendations",
                    "action": "enterprise_ml_recommendations",
                    "data_used": ml_context,
                    "source": "energy_ia_ml_enterprise",
                    "performance_score": self._calculate_ml_performance_score(
                        ml_response
                    ),
                    "confidence": intent_analysis.get("confidence", 0.8),
                }

            except (requests.exceptions.RequestException, ValueError, TypeError) as e:
                logging.error(
                    "Error en ML empresarial - Intento %d: %s", attempt + 1, e
                )
                if attempt == self.max_retries - 1:
                    return self._get_enterprise_ml_fallback(user_context)
                time.sleep(2**attempt)

        return self._get_enterprise_ml_fallback(user_context)

    def _handle_general_chat_enterprise(
        self,
        user_id: str,
        user_message: str,
        user_context: Dict[str, Any],
        intent_analysis: Dict[str, Any],
    ) -> Dict[str, Any]:
        """💬 Chat general empresarial con contexto enriquecido."""

        for attempt in range(self.max_retries):
            try:
                # Preparar contexto empresarial para Gemini
                gemini_context = self._prepare_enterprise_gemini_context(user_context)

                # Autenticación robusta
                auth_token = self._get_service_to_service_token()

                headers = {
                    "Authorization": f"Bearer {auth_token}",
                    "Content-Type": "application/json",
                    "X-Enterprise-Request": "true",
                }

                # Payload empresarial enriquecido
                payload = {
                    "message": user_message,
                    "history": [],
                    "user_context": {
                        "data_completeness": user_context.get("data_completeness", 0),
                        "last_invoice": user_context.get("last_invoice", {}),
                        "num_inhabitants": user_context.get("num_inhabitants"),
                        "home_type": user_context.get("home_type"),
                        "available_sources": user_context.get("available_sources", []),
                        "user_name": user_id,
                        "enterprise_mode": True,
                        "personalization_level": "high",
                    },
                    "enterprise_features": {
                        "enhanced_context": True,
                        "sentiment_analysis": True,
                        "personalization": True,
                    },
                    "intent_metadata": {
                        "primary_intent": intent_analysis.get("primary_intent"),
                        "strategy": intent_analysis.get("strategy"),
                        "confidence": intent_analysis.get("confidence", 0),
                        "ml_readiness": intent_analysis.get(
                            "enterprise_analysis", {}
                        ).get("ml_readiness", False),
                        "engagement_level": intent_analysis.get(
                            "enterprise_analysis", {}
                        ).get("user_engagement_level", "medium"),
                    },
                }

                complete_url = f"{self.energy_ia_api_url}/api/v1/chatbot/message/v2"

                response = requests.post(
                    complete_url,
                    json=payload,
                    headers=headers,
                    timeout=self.timeout_seconds,
                )
                response.raise_for_status()

                gemini_response = response.json()

                return {
                    "response": gemini_response.get(
                        "response", "Respuesta personalizada generada"
                    ),
                    "intent": "general_consultation",
                    "action": "enterprise_gemini_response",
                    "context_used": bool(gemini_context),
                    "source": "energy_ia_gemini_enterprise",
                    "performance_score": self._calculate_gemini_performance_score(
                        gemini_response
                    ),
                    "sentiment_analysis": gemini_response.get("sentiment", "neutral"),
                }

            except (requests.exceptions.RequestException, ValueError, TypeError) as e:
                logging.error(
                    "Error en Gemini empresarial - Intento %d: %s", attempt + 1, e
                )
                if attempt == self.max_retries - 1:
                    return self._get_enterprise_gemini_fallback(
                        user_message, user_context
                    )
                time.sleep(2**attempt)

        return self._get_enterprise_gemini_fallback(user_message, user_context)

    def _handle_hybrid_consultation_enterprise(
        self,
        user_id: str,
        user_message: str,
        user_context: Dict[str, Any],
        intent_analysis: Dict[str, Any],
    ) -> Dict[str, Any]:
        """🔄 Consulta híbrida empresarial con orquestación avanzada."""

        try:
            # Ejecutar ML y Gemini en paralelo para máximo rendimiento
            with ThreadPoolExecutor(max_workers=2) as executor:
                ml_future = executor.submit(
                    self._handle_ml_recommendations_enterprise,
                    user_id,
                    user_message,
                    user_context,
                    intent_analysis,
                )

                explanation_prompt = f"Proporciona una explicación detallada y personalizada sobre: {user_message}"
                gemini_future = executor.submit(
                    self._handle_general_chat_enterprise,
                    user_id,
                    explanation_prompt,
                    user_context,
                    intent_analysis,
                )

                # Obtener resultados con timeout
                ml_result = ml_future.result(timeout=25)
                gemini_result = gemini_future.result(timeout=25)

            # Combinar respuestas de forma inteligente
            combined_response = self._combine_hybrid_responses(ml_result, gemini_result)

            return {
                "response": combined_response,
                "intent": "hybrid_consultation",
                "action": "enterprise_hybrid_orchestration",
                "ml_component": ml_result,
                "gemini_component": gemini_result,
                "source": "enterprise_hybrid_system",
                "performance_score": (
                    ml_result.get("performance_score", 0)
                    + gemini_result.get("performance_score", 0)
                )
                / 2,
            }

        except (ValueError, TypeError, ConnectionError, AppError, TimeoutError) as e:
            logging.error("Error en híbrido empresarial: %s", e)
            return self._get_enterprise_fallback_response(user_message, user_context)

    # 🆕 NUEVOS ENDPOINTS EMPRESARIALES PARA GESTIÓN DE CONVERSACIONES

    def get_conversation_history(
        self, user_id: str, conversation_id: str
    ) -> Dict[str, Any]:
        """📋 Obtener historial de conversación empresarial."""
        try:
            query = f"""
            SELECT 
                message_id,
                timestamp_utc,
                sender,
                message_text,
                intent_detected,
                bot_action,
                sentiment,
                response_time_ms,
                metadata
            FROM `{self.project_id}.{self.bq_dataset_id}.{self.bq_conversations_table_id}`
            WHERE conversation_id = @conversation_id 
            AND user_id = @user_id
            ORDER BY timestamp_utc ASC
            """

            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter(
                        "conversation_id", "STRING", conversation_id
                    ),
                    bigquery.ScalarQueryParameter("user_id", "STRING", user_id),
                ]
            )

            if self.bigquery_client is None:
                return {"error": "BigQuery client not available"}

            query_job = self.bigquery_client.query(query, job_config=job_config)
            results = list(query_job.result())

            messages = []
            for row in results:
                messages.append(
                    {
                        "message_id": row.message_id,
                        "timestamp": row.timestamp_utc,
                        "sender": row.sender,
                        "message": row.message_text,
                        "intent": row.intent_detected,
                        "action": row.bot_action,
                        "sentiment": row.sentiment,
                        "response_time": row.response_time_ms,
                        "metadata": json.loads(row.metadata) if row.metadata else {},
                    }
                )

            return {
                "conversation_id": conversation_id,
                "messages": messages,
                "total_messages": len(messages),
                "status": "success",
            }

        except (
            google_exceptions.GoogleAPICallError,
            ValueError,
            TypeError,
            ConnectionError,
        ) as e:
            logging.error("Error obteniendo historial de conversación: %s", e)
            return {
                "error": "No se pudo obtener el historial de conversación",
                "status": "error",
            }

    def delete_conversation(self, user_id: str, conversation_id: str) -> Dict[str, Any]:
        """🗑️ Eliminar conversación empresarial (soft delete)."""
        try:
            # Marcar como eliminada en lugar de borrar físicamente
            update_query = f"""
            UPDATE `{self.project_id}.{self.bq_dataset_id}.{self.bq_conversations_table_id}`
            SET metadata = JSON_SET(IFNULL(metadata, '{{}}'), '$.deleted', true, '$.deleted_at', @deleted_at)
            WHERE conversation_id = @conversation_id 
            AND user_id = @user_id
            """

            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter(
                        "conversation_id", "STRING", conversation_id
                    ),
                    bigquery.ScalarQueryParameter("user_id", "STRING", user_id),
                    bigquery.ScalarQueryParameter(
                        "deleted_at",
                        "STRING",
                        datetime.now(timezone.utc).isoformat(),
                    ),
                ]
            )

            if self.bigquery_client is None:
                return {"error": "BigQuery client not available"}

            query_job = self.bigquery_client.query(update_query, job_config=job_config)
            query_job.result()

            logging.info(
                "Conversación %s marcada como eliminada para usuario %s",
                conversation_id,
                user_id,
            )

            return {
                "conversation_id": conversation_id,
                "status": "deleted",
                "message": "Conversación eliminada correctamente",
            }

        except (
            google_exceptions.GoogleAPICallError,
            ValueError,
            TypeError,
            ConnectionError,
        ) as e:
            logging.error("Error eliminando conversación: %s", e)
            return {"error": "No se pudo eliminar la conversación", "status": "error"}

    def submit_conversation_feedback(
        self,
        user_id: str,
        conversation_id: str,
        rating: int,
        feedback_text: Optional[str] = None,
        recommendation_type: str = "general",
    ) -> Dict[str, Any]:
        """⭐ Enviar feedback de conversación empresarial."""
        try:
            # Validar rating
            if not 1 <= rating <= 5:
                return {"error": "Rating debe estar entre 1 y 5", "status": "error"}

            # Registrar feedback
            feedback_useful = rating >= 3
            success = self._log_feedback_to_bigquery(
                user_id=user_id,
                recommendation_type=recommendation_type,
                feedback_useful=feedback_useful,
                comments=feedback_text,
                rating=rating,
                conversation_id=conversation_id,
            )

            if success:
                # 🧠 Procesar feedback para aprendizaje automático
                if self.ai_learning_service:
                    try:
                        self.ai_learning_service.process_feedback_learning(
                            user_id=user_id,
                            conversation_id=conversation_id,
                            rating=rating,
                            feedback_text=feedback_text,
                        )
                    except (ValueError, TypeError, ConnectionError, AppError) as e:
                        logging.error("Error procesando feedback para ML: %s", e)

                return {
                    "feedback_id": str(uuid.uuid4()),
                    "status": "success",
                    "message": "Feedback registrado correctamente",
                    "rating": rating,
                }
            else:
                return {"error": "Error al registrar el feedback", "status": "error"}

        except (ValueError, TypeError, ConnectionError, AppError) as e:
            logging.error("Error enviando feedback: %s", e)
            return {"error": "No se pudo procesar el feedback", "status": "error"}

    # MÉTODOS AUXILIARES EMPRESARIALES

    def _get_service_to_service_token(self) -> str:
        """🔐 Obtener token de autenticación entre servicios."""
        try:
            import google.auth.transport.requests  # type: ignore
            import google.oauth2.id_token  # type: ignore

            audience_url = self.energy_ia_api_url
            auth_req = google.auth.transport.requests.Request()
            token = google.oauth2.id_token.fetch_id_token(auth_req, audience_url)

            if not token:
                raise AppError("No se pudo obtener token de autenticación", 500)

            return str(token)
        except ImportError as e:
            logging.error("Google Auth library no disponible: %s", e)
            raise AppError("Dependencias de autenticación no disponibles", 500) from e
        except Exception as e:
            logging.error("Error obteniendo token de servicio: %s", e)
            raise AppError("Error de autenticación entre servicios", 500) from e

    def _prepare_enterprise_ml_context(
        self, user_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """🤖 Preparar contexto empresarial para ML."""
        enterprise_context = {
            "user_profile": {
                "data_completeness": user_context.get("data_completeness", 0),
                "available_sources": user_context.get("available_sources", []),
            }
        }

        if user_context.get("last_invoice"):
            invoice = user_context["last_invoice"]
            enterprise_context["consumption_data"] = {
                "kwh_consumed": invoice.get("kwh_consumidos"),
                "contracted_power": invoice.get("potencia_contratada_kw"),
                "total_cost": invoice.get("coste_total"),
            }

        return enterprise_context

    def _prepare_enterprise_gemini_context(
        self, user_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """💬 Preparar contexto empresarial para Gemini."""
        return {
            "enterprise_mode": True,
            "personalization_level": "high",
            "data_completeness": user_context.get("data_completeness", 0),
            "user_profile": user_context.get("energy_profile", {}),
            "preferences": user_context.get("preferences", {}),
        }

    def _process_enterprise_learning(
        self,
        user_id: str,
        conversation_id: str,
        user_message: str,
        bot_response: Dict[str, Any],
        user_context: Dict[str, Any],
        intent_analysis: Dict[str, Any],
    ) -> None:
        """🧠 Procesar aprendizaje automático empresarial."""
        if not self.ai_learning_service:
            return

        try:
            learning_data = {
                "user_id": user_id,
                "conversation_id": conversation_id,
                "user_message": user_message,
                "bot_response": bot_response.get("response", ""),
                "intent": intent_analysis.get("primary_intent"),
                "strategy": intent_analysis.get("strategy"),
                "confidence": intent_analysis.get("confidence", 0),
                "data_completeness": user_context.get("data_completeness", 0),
                "performance_score": bot_response.get("performance_score", 0),
            }

            self.ai_learning_service.process_enterprise_interaction(learning_data)

        except (ValueError, TypeError, ConnectionError, AppError) as e:
            logging.error("Error en aprendizaje empresarial: %s", e)

    def _update_performance_metrics(self, response_time: float, success: bool) -> None:
        """📊 Actualizar métricas de rendimiento empresarial."""
        if success:
            self.performance_metrics["successful_requests"] += 1
        else:
            self.performance_metrics["failed_requests"] += 1

        # Actualizar tiempo promedio de respuesta
        total_requests = self.performance_metrics["total_requests"]
        current_avg = self.performance_metrics["avg_response_time"]

        self.performance_metrics["avg_response_time"] = (
            current_avg * (total_requests - 1) + response_time
        ) / total_requests

    def _calculate_performance_score(self, response_data: Dict[str, Any]) -> float:
        """📈 Calcular puntuación de rendimiento empresarial basada en métricas reales."""
        # Cálculo empresarial basado en métricas reales de rendimiento
        total_score = 0.0
        weight_factors = 0.0

        # Factor 1: Confianza de respuesta (peso 30%)
        confidence = response_data.get("confidence", 0.0)
        confidence_score = min(1.0, max(0.0, confidence)) * 0.3
        total_score += confidence_score
        weight_factors += 0.3

        # Factor 2: Uso de datos del usuario (peso 25%)
        data_used = response_data.get("data_used", False)
        if data_used:
            # Evaluar calidad de datos utilizados
            data_completeness = response_data.get("data_completeness", 0)
            data_score = (data_completeness / 100.0) * 0.25
        else:
            data_score = 0.1 * 0.25  # Penalización por no usar datos
        total_score += data_score
        weight_factors += 0.25

        # Factor 3: Tiempo de respuesta (peso 20%)
        response_time = response_data.get("response_time_ms", 5000)
        if response_time <= 1000:
            time_score = 1.0 * 0.2
        elif response_time <= 3000:
            time_score = 0.8 * 0.2
        elif response_time <= 5000:
            time_score = 0.6 * 0.2
        else:
            time_score = 0.3 * 0.2
        total_score += time_score
        weight_factors += 0.2

        # Factor 4: Análisis de sentiment (peso 15%)
        sentiment_analysis = response_data.get("sentiment_analysis")
        if sentiment_analysis:
            sentiment_score = 1.0 * 0.15
        else:
            sentiment_score = 0.5 * 0.15
        total_score += sentiment_score
        weight_factors += 0.15

        # Factor 5: Longitud y calidad de respuesta (peso 10%)
        response_text = response_data.get("response", "")
        response_length = len(response_text)
        if 100 <= response_length <= 1000:
            length_score = 1.0 * 0.1
        elif 50 <= response_length < 100 or 1000 < response_length <= 2000:
            length_score = 0.8 * 0.1
        elif response_length < 50:
            length_score = 0.4 * 0.1
        else:
            length_score = 0.6 * 0.1
        total_score += length_score
        weight_factors += 0.1

        # Normalizar score final
        final_score = total_score / weight_factors if weight_factors > 0 else 0.5
        return min(1.0, max(0.0, final_score))

    def _get_enterprise_fallback_response(
        self, user_message: str, user_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """🛡️ Respuesta de emergencia empresarial."""

        # 🏢 Análisis empresarial del mensaje para respuesta personalizada
        message_analysis = {
            "length": len(user_message),
            "complexity": len(user_message.split()),
            "contains_question": "?" in user_message,
            "urgency_detected": any(
                word in user_message.lower()
                for word in ["urgente", "rapido", "inmediato", "ya"]
            ),
            "technical_terms": any(
                term in user_message.lower()
                for term in ["tarifa", "kwh", "factura", "consumo", "energia"]
            ),
        }

        # 🎯 Personalizar respuesta basada en contexto del usuario
        data_completeness = user_context.get("data_completeness", 0)
        available_sources = user_context.get("available_sources", [])
        user_name = user_context.get("user_id", "usuario")

        # 📝 Generar respuesta contextualizada
        if message_analysis["technical_terms"]:
            base_response = f"Disculpe, {user_name}, estoy experimentando dificultades con el sistema de análisis energético."
            if data_completeness > 50:
                base_response += " Tengo acceso a parte de sus datos y trabajaré para proporcionarle una respuesta más completa."
        elif message_analysis["urgency_detected"]:
            base_response = f"Entiendo la urgencia de su consulta, {user_name}. Estoy trabajando para resolver los problemas técnicos lo antes posible."
        elif message_analysis["contains_question"]:
            base_response = f"Lamento no poder responder su pregunta en este momento, {user_name}. Estoy experimentando dificultades técnicas temporales."
        else:
            base_response = "Estoy experimentando dificultades técnicas temporales. Por favor, intenta nuevamente en unos momentos."

        return {
            "response": base_response,
            "intent": "enterprise_fallback",
            "action": "emergency_response",
            "source": "enterprise_fallback_system",
            "status": "fallback_activated",
            "message_analysis": message_analysis,
            "context_quality": {
                "data_completeness": data_completeness,
                "available_sources_count": len(available_sources),
                "personalization_applied": True,
            },
        }

    def _get_enterprise_ml_fallback(
        self, user_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """🤖 Fallback ML empresarial."""

        # 🏢 Análisis empresarial del contexto para respuesta personalizada
        data_completeness = user_context.get("data_completeness", 0)
        available_sources = user_context.get("available_sources", [])
        user_name = user_context.get("user_id", "usuario")

        # 📊 Generar respuesta contextualizada según datos disponibles
        if data_completeness > 60:
            response = f"Disculpe, {user_name}, el sistema de recomendaciones ML está temporalmente no disponible. Sin embargo, tengo acceso a {len(available_sources)} fuentes de sus datos para ofrecerle asistencia básica."
        elif data_completeness > 30:
            response = f"El sistema de recomendaciones está en mantenimiento, {user_name}. Puedo ayudarle con información general mientras se restablece el servicio."
        else:
            response = f"El sistema de recomendaciones está temporalmente no disponible, {user_name}. Para obtener recomendaciones personalizadas, necesitaríamos más información de su perfil energético."

        return {
            "response": response,
            "intent": "ml_fallback",
            "action": "ml_service_fallback",
            "source": "enterprise_ml_fallback",
            "context_analysis": {
                "data_completeness": data_completeness,
                "available_sources_count": len(available_sources),
                "personalization_level": (
                    "high"
                    if data_completeness > 60
                    else "medium" if data_completeness > 30 else "low"
                ),
                "fallback_quality": "enhanced" if data_completeness > 30 else "basic",
            },
        }

    def _get_enterprise_gemini_fallback(
        self, user_message: str, user_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """💬 Fallback Gemini empresarial."""

        # 🏢 Análisis empresarial del contexto para respuesta personalizada
        data_completeness = user_context.get("data_completeness", 0)
        available_sources = user_context.get("available_sources", [])
        user_name = user_context.get("user_id", "usuario")

        # 🧠 Generar respuesta personalizada basada en el mensaje del usuario
        personalized_response = self._generate_contextual_fallback_response(
            user_message, data_completeness, available_sources, user_name
        )

        return {
            "response": personalized_response,
            "intent": "gemini_fallback",
            "action": "gemini_service_fallback",
            "source": "enterprise_gemini_fallback",
            "fallback_metadata": {
                "user_context_used": True,
                "message_length": len(user_message),
                "data_completeness": data_completeness,
                "available_sources_count": len(available_sources),
                "personalization_level": "high",
            },
        }

    def _generate_contextual_fallback_response(
        self,
        user_message: str,
        data_completeness: float,
        available_sources: List[str],
        user_name: str,
    ) -> str:
        """🏢 Genera respuesta de fallback contextual empresarial."""

        # 📝 Análisis del tipo de consulta del usuario
        message_lower = user_message.lower()

        # 🎯 Respuestas contextuales específicas
        if "tarifa" in message_lower or "precio" in message_lower:
            base_response = f"Disculpe, {user_name}, el sistema de comparación de tarifas está temporalmente no disponible."
            if data_completeness > 0.5:
                base_response += " Basándome en su perfil energético, le sugiero consultar proveedores locales mientras restablezco el servicio."
            return base_response

        elif "consumo" in message_lower or "factura" in message_lower:
            base_response = f"Le pido disculpas, {user_name}, el análisis de consumo está en mantenimiento."
            if "billing" in available_sources:
                base_response += (
                    " Sus datos de facturación están disponibles para consulta manual."
                )
            return base_response

        elif "energia" in message_lower or "renovable" in message_lower:
            base_response = f"Estimado {user_name}, el servicio de análisis energético está temporalmente fuera de línea."
            if data_completeness > 0.7:
                base_response += " Con base en su histórico, puedo proporcionarle recomendaciones básicas una vez restablecido el servicio."
            return base_response

        else:
            # 🔧 Respuesta genérica personalizada
            base_response = f"Disculpe, {user_name}, estoy experimentando dificultades técnicas temporales."
            if len(available_sources) > 2:
                base_response += " Tengo acceso parcial a sus datos para asistirle cuando el sistema se restablezca."
            else:
                base_response += " Le recomiendo intentar nuevamente en unos minutos."
                base_response += " Estoy trabajando para resolver el problema y brindarle una respuesta completa."

            return base_response

    def _combine_hybrid_responses(
        self, ml_result: Dict[str, Any], gemini_result: Dict[str, Any]
    ) -> str:
        """🔄 Combinar respuestas híbridas empresariales."""
        ml_response = ml_result.get("response", "")
        gemini_response = gemini_result.get("response", "")

        return f"{ml_response}\n\n💡 Análisis detallado:\n{gemini_response}"

    # MÉTODOS AUXILIARES PARA OBTENCIÓN DE DATOS

    def _get_energy_profile(self, user_id: str) -> Dict[str, Any]:
        """⚡ Obtener perfil energético del usuario."""
        try:
            try:
                from app.services.energy_service import EnergyService
            except ImportError:
                from app.services.energy_service import EnergyService

            energy_service: Any = EnergyService()  # type: ignore
            result = energy_service.get_user_energy_profile(user_id)
            return result if isinstance(result, dict) else {}
        except (
            ImportError,
            AttributeError,
            ValueError,
            TypeError,
            ConnectionError,
        ) as e:
            logging.warning("Error obteniendo perfil energético: %s", e)
            return {}

    def get_user_analytics(self, user_id: str) -> Dict[str, Any]:
        """📊 Obtener análisis de usuario para endpoints públicos."""
        return self._get_analytics_summary(user_id)

    def _get_analytics_summary(self, user_id: str) -> Dict[str, Any]:
        """📊 Obtener resumen analítico del usuario CON DATOS DE SENTIMENT."""
        try:
            # 1. Obtener métricas básicas de conversaciones
            conversations_query = f"""
            SELECT 
                COUNT(*) as total_conversations,
                AVG(CHAR_LENGTH(message_text)) as avg_message_length,
                COUNT(DISTINCT DATE(timestamp_utc)) as active_days
            FROM `{self.project_id}.{self.bq_dataset_id}.{self.bq_conversations_table_id}`
            WHERE user_id = @user_id
            AND sender = 'user'
            AND timestamp_utc >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
            AND (JSON_EXTRACT(metadata, '$.deleted') IS NULL OR JSON_EXTRACT(metadata, '$.deleted') = false)
            """

            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("user_id", "STRING", user_id),
                ]
            )

            if self.bigquery_client is None:
                return {}

            # Ejecutar query de conversaciones
            conv_query_job = self.bigquery_client.query(
                conversations_query, job_config=job_config
            )
            conv_results = list(conv_query_job.result())

            analytics_data = {}
            if conv_results:
                row = conv_results[0]
                analytics_data = {
                    "total_conversations": row.total_conversations,
                    "avg_message_length": row.avg_message_length,
                    "active_days": row.active_days,
                    "engagement_level": (
                        "high" if row.total_conversations > 10 else "medium"
                    ),
                }

            # 🧠 2. Obtener métricas de SENTIMENT ANALYSIS
            try:
                sentiment_query = f"""
                SELECT 
                    AVG(sentiment_score) as avg_sentiment,
                    COUNT(*) as total_sentiment_analyzed,
                    AVG(confidence) as avg_confidence,
                    sentiment_label,
                    COUNT(sentiment_label) as sentiment_count
                FROM `{self.project_id}.{self.bq_dataset_id}.ai_sentiment_analysis`
                WHERE user_id = @user_id
                AND analyzed_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
                GROUP BY sentiment_label
                ORDER BY sentiment_count DESC
                """

                sentiment_query_job = self.bigquery_client.query(
                    sentiment_query, job_config=job_config
                )
                sentiment_results = list(sentiment_query_job.result())

                if sentiment_results:
                    sentiment_distribution = {}
                    total_sentiment_analyzed = 0
                    avg_sentiment = 0.0
                    avg_confidence = 0.0

                    for row in sentiment_results:
                        sentiment_distribution[row.sentiment_label] = (
                            row.sentiment_count
                        )
                        if row.avg_sentiment is not None:
                            avg_sentiment = float(row.avg_sentiment)
                        if row.avg_confidence is not None:
                            avg_confidence = float(row.avg_confidence)
                        total_sentiment_analyzed += row.sentiment_count

                    # Añadir métricas de sentiment
                    analytics_data.update(
                        {
                            "sentiment_analysis": {
                                "avg_sentiment_score": round(avg_sentiment, 3),
                                "avg_confidence": round(avg_confidence, 3),
                                "total_analyzed": total_sentiment_analyzed,
                                "sentiment_distribution": sentiment_distribution,
                                "primary_sentiment": (
                                    max(
                                        sentiment_distribution.keys(),
                                        key=lambda k: sentiment_distribution.get(k, 0),
                                    )
                                    if sentiment_distribution
                                    else "neutral"
                                ),
                            }
                        }
                    )

            except Exception as e:
                logging.warning(f"Error obteniendo métricas de sentiment: {e}")
                # Añadir valores por defecto si falla
                analytics_data["sentiment_analysis"] = {
                    "avg_sentiment_score": 0.0,
                    "avg_confidence": 0.0,
                    "total_analyzed": 0,
                    "sentiment_distribution": {},
                    "primary_sentiment": "neutral",
                }

            return analytics_data
        except (
            google_exceptions.GoogleAPICallError,
            ValueError,
            TypeError,
            ConnectionError,
        ) as e:
            logging.warning("Error obteniendo analytics: %s", e)

        return {}

    def _get_user_preferences(self, user_id: str) -> Dict[str, Any]:
        """👤 Obtener preferencias del usuario."""
        try:
            try:
                from google.cloud import firestore
            except ImportError:
                logging.warning("Firestore no disponible")
                return {}

            db = firestore.Client(project=self.project_id)

            user_ref = db.collection("users").document(user_id)
            user_doc = user_ref.get()

            if user_doc.exists:
                user_data = user_doc.to_dict()
                if user_data is not None:
                    return user_data.get("preferences", {})
        except (
            google_exceptions.GoogleAPICallError,
            ValueError,
            TypeError,
            ConnectionError,
        ) as e:
            logging.warning("Error obteniendo preferencias: %s", e)

        return {}

    def _get_consumption_history(self, user_id: str) -> Dict[str, Any]:
        """📈 Obtener historial de consumo."""
        try:
            try:
                from app.services.energy_service import EnergyService
            except ImportError:
                from .energy_service import EnergyService

            energy_service: Any = EnergyService()  # type: ignore
            result = energy_service.get_consumption_history(user_id)
            return result if isinstance(result, dict) else {}
        except (
            ImportError,
            AttributeError,
            ValueError,
            TypeError,
            ConnectionError,
        ) as e:
            logging.warning("Error obteniendo historial de consumo: %s", e)
            return {}

    def _get_recent_interactions(self, user_id: str) -> Dict[str, Any]:
        """🔄 Obtener interacciones recientes."""
        try:
            query = f"""
            SELECT 
                intent_detected,
                bot_action,
                sentiment,
                COUNT(*) as frequency
            FROM `{self.project_id}.{self.bq_dataset_id}.{self.bq_conversations_table_id}`
            WHERE user_id = @user_id
            AND sender = 'bot'
            AND timestamp_utc >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
            AND (JSON_EXTRACT(metadata, '$.deleted') IS NULL OR JSON_EXTRACT(metadata, '$.deleted') = false)
            GROUP BY intent_detected, bot_action, sentiment
            ORDER BY frequency DESC
            LIMIT 10
            """

            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("user_id", "STRING", user_id),
                ]
            )

            if self.bigquery_client is None:
                return {}

            query_job = self.bigquery_client.query(query, job_config=job_config)
            results = list(query_job.result())

            interactions = []
            for row in results:
                interactions.append(
                    {
                        "intent": row.intent_detected,
                        "action": row.bot_action,
                        "sentiment": row.sentiment,
                        "frequency": row.frequency,
                    }
                )

            return {"recent_interactions": interactions}

        except (
            google_exceptions.GoogleAPICallError,
            ValueError,
            TypeError,
            ConnectionError,
        ) as e:
            logging.warning("Error obteniendo interacciones recientes: %s", e)
            return {}

    def _calculate_ml_performance_score(self, ml_response: Dict[str, Any]) -> float:
        """🤖 Calcular puntuación de rendimiento ML basada en métricas empresariales reales."""
        # Cálculo empresarial basado en calidad real de las recomendaciones ML
        total_score = 0.0
        weight_factors = 0.0

        # Factor 1: Calidad de recomendaciones (peso 40%)
        recommendations = ml_response.get("recommendations", [])
        if recommendations:
            # Evaluar número y calidad de recomendaciones
            rec_count = len(recommendations) if isinstance(recommendations, list) else 1
            if rec_count >= 3:
                rec_score = 1.0 * 0.4
            elif rec_count >= 2:
                rec_score = 0.8 * 0.4
            elif rec_count >= 1:
                rec_score = 0.6 * 0.4
            else:
                rec_score = 0.2 * 0.4
        else:
            rec_score = 0.1 * 0.4
        total_score += rec_score
        weight_factors += 0.4

        # Factor 2: Confianza del modelo ML (peso 30%)
        confidence = ml_response.get("confidence", 0.0)
        confidence_score = min(1.0, max(0.0, confidence)) * 0.3
        total_score += confidence_score
        weight_factors += 0.3

        # Factor 3: Ahorro potencial calculado (peso 20%)
        savings = ml_response.get("potential_savings", 0)
        if savings > 0:
            # Normalizar ahorro potencial (asumiendo máximo realista de €200/mes)
            savings_normalized = min(1.0, savings / 200.0)
            savings_score = savings_normalized * 0.2
        else:
            savings_score = 0.1 * 0.2
        total_score += savings_score
        weight_factors += 0.2

        # Factor 4: Datos utilizados para predicción (peso 10%)
        data_points = ml_response.get("data_points_used", 0)
        if data_points >= 5:
            data_score = 1.0 * 0.1
        elif data_points >= 3:
            data_score = 0.8 * 0.1
        elif data_points >= 1:
            data_score = 0.6 * 0.1
        else:
            data_score = 0.3 * 0.1
        total_score += data_score
        weight_factors += 0.1

        # Normalizar score final
        final_score = total_score / weight_factors if weight_factors > 0 else 0.4
        return min(1.0, max(0.2, final_score))

    def _calculate_gemini_performance_score(
        self, gemini_response: Dict[str, Any]
    ) -> float:
        """💬 Calcular puntuación de rendimiento Gemini basada en métricas empresariales reales."""
        # Cálculo empresarial basado en calidad real de respuesta Gemini
        total_score = 0.0
        weight_factors = 0.0

        # Factor 1: Calidad de contenido por longitud (peso 25%)
        response_text = gemini_response.get("response", "")
        response_length = len(response_text)
        if 200 <= response_length <= 800:
            length_score = 1.0 * 0.25  # Longitud óptima para explicaciones energéticas
        elif 100 <= response_length < 200 or 800 < response_length <= 1200:
            length_score = 0.8 * 0.25
        elif 50 <= response_length < 100 or 1200 < response_length <= 1500:
            length_score = 0.6 * 0.25
        elif response_length < 50:
            length_score = 0.3 * 0.25  # Respuesta muy corta
        else:
            length_score = 0.4 * 0.25  # Respuesta muy larga
        total_score += length_score
        weight_factors += 0.25

        # Factor 2: Análisis de sentiment (peso 25%)
        sentiment = gemini_response.get("sentiment")
        if sentiment:
            sentiment_confidence = gemini_response.get("sentiment_confidence", 0.5)
            sentiment_score = min(1.0, sentiment_confidence) * 0.25
        else:
            sentiment_score = 0.4 * 0.25
        total_score += sentiment_score
        weight_factors += 0.25

        # Factor 3: Uso de contexto personalizado (peso 20%)
        context_used = gemini_response.get("context_used", False)
        personalization_level = gemini_response.get("personalization_level", "none")
        if context_used and personalization_level == "high":
            context_score = 1.0 * 0.2
        elif context_used and personalization_level == "medium":
            context_score = 0.8 * 0.2
        elif context_used:
            context_score = 0.6 * 0.2
        else:
            context_score = 0.3 * 0.2
        total_score += context_score
        weight_factors += 0.2

        # Factor 4: Términos técnicos energéticos relevantes (peso 15%)
        energy_terms = [
            "kwh",
            "tarifa",
            "consumo",
            "ahorro",
            "potencia",
            "factura",
            "distribuidora",
        ]
        energy_terms_count = sum(
            1 for term in energy_terms if term in response_text.lower()
        )
        if energy_terms_count >= 3:
            technical_score = 1.0 * 0.15
        elif energy_terms_count >= 2:
            technical_score = 0.8 * 0.15
        elif energy_terms_count >= 1:
            technical_score = 0.6 * 0.15
        else:
            technical_score = 0.4 * 0.15
        total_score += technical_score
        weight_factors += 0.15

        # Factor 5: Tiempo de respuesta (peso 15%)
        response_time = gemini_response.get("response_time_ms", 3000)
        if response_time <= 2000:
            time_score = 1.0 * 0.15
        elif response_time <= 4000:
            time_score = 0.8 * 0.15
        elif response_time <= 6000:
            time_score = 0.6 * 0.15
        else:
            time_score = 0.4 * 0.15
        total_score += time_score
        weight_factors += 0.15

        # Normalizar score final
        final_score = total_score / weight_factors if weight_factors > 0 else 0.5
        return min(1.0, max(0.3, final_score))

    def _enhance_response_enterprise(
        self,
        bot_response: Dict[str, Any],
        user_context: Dict[str, Any],
        intent_analysis: Dict[str, Any],
    ) -> Dict[str, Any]:
        """✨ Mejorar respuesta con características empresariales."""
        enhanced_response = bot_response.copy()

        # Añadir sugerencias empresariales
        data_completeness = user_context.get("data_completeness", 0)
        if data_completeness < 50:
            suggestions = self._generate_enterprise_suggestions(user_context)
            if suggestions:
                enhanced_response["enterprise_suggestions"] = suggestions

        # Añadir información de contexto
        enhanced_response["context_quality"] = {
            "data_completeness": data_completeness,
            "sources_available": len(user_context.get("available_sources", [])),
            "personalization_level": "high" if data_completeness > 60 else "medium",
        }

        # 🧠 Añadir análisis de intención empresarial
        enhanced_response["intent_analysis"] = {
            "primary_intent": intent_analysis.get("primary_intent", "general"),
            "strategy": intent_analysis.get("strategy", "general_chat"),
            "confidence": intent_analysis.get("confidence", 0.0),
            "ml_readiness": intent_analysis.get("enterprise_analysis", {}).get(
                "ml_readiness", False
            ),
            "engagement_level": intent_analysis.get("enterprise_analysis", {}).get(
                "user_engagement_level", "medium"
            ),
        }

        return enhanced_response

    def _generate_enterprise_suggestions(
        self, user_context: Dict[str, Any]
    ) -> List[str]:
        """💡 Generar sugerencias empresariales."""
        suggestions = []
        missing_data = user_context.get("missing_critical_data", [])

        if "energy_profile" in missing_data:
            suggestions.append(
                "Completa tu perfil energético para recomendaciones personalizadas"
            )

        if "invoice_data" in missing_data:
            suggestions.append("Sube tu última factura para análisis detallado")

        if "consumption" in missing_data:
            suggestions.append("Registra tu consumo habitual para mejor seguimiento")

        return suggestions[:2]  # Máximo 2 sugerencias
