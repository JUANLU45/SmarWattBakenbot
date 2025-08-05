\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\expert_bot_api_COPY\app\config.py"
    BQ_CONVERSATIONS_TABLE_ID = os.environ.get(
        "BQ_CONVERSATIONS_TABLE_ID", "conversations_log"
    BQ_FEEDBACK_TABLE_ID = os.environ.get("BQ_FEEDBACK_TABLE_ID", "feedback_log")
    BQ_CONSUMPTION_LOG_TABLE_ID = os.environ.get(
        "BQ_CONSUMPTION_LOG_TABLE_ID", "consumption_log"
    BQ_UPLOADED_DOCS_TABLE_ID = os.environ.get(
        "BQ_UPLOADED_DOCS_TABLE_ID", "uploaded_documents_log"
    BQ_USER_PROFILES_TABLE_ID = os.environ.get(
        "BQ_USER_PROFILES_TABLE_ID", "user_profiles_enriched"
    BQ_AI_SENTIMENT_TABLE_ID = os.environ.get(
        "BQ_AI_SENTIMENT_TABLE_ID", "ai_sentiment_analysis"
    BQ_AI_PATTERNS_TABLE_ID = os.environ.get(  
        "BQ_AI_PATTERNS_TABLE_ID", "ai_user_patterns"
    BQ_AI_OPTIMIZATION_TABLE_ID = os.environ.get(
        "BQ_AI_OPTIMIZATION_TABLE_ID", "ai_prompt_optimization"
    BQ_AI_PREDICTIONS_TABLE_ID = os.environ.get(
        "BQ_AI_PREDICTIONS_TABLE_ID", "ai_predictions"
    BQ_AI_BUSINESS_METRICS_TABLE_ID = os.environ.get(
        "BQ_AI_BUSINESS_METRICS_TABLE_ID", "ai_business_metrics"
    BQ_ASYNC_TASKS_TABLE_ID = os.environ.get("BQ_ASYNC_TASKS_TABLE_ID", "async_tasks")
    BQ_WORKER_METRICS_TABLE_ID = os.environ.get(
        "BQ_WORKER_METRICS_TABLE_ID", "worker_metrics"
            "BQ_CONVERSATIONS_TABLE_ID": cls.BQ_CONVERSATIONS_TABLE_ID,
            "BQ_FEEDBACK_TABLE_ID": cls.BQ_FEEDBACK_TABLE_ID,
            "BQ_CONSUMPTION_LOG_TABLE_ID": cls.BQ_CONSUMPTION_LOG_TABLE_ID,
            "BQ_UPLOADED_DOCS_TABLE_ID": cls.BQ_UPLOADED_DOCS_TABLE_ID,
            "BQ_USER_PROFILES_TABLE_ID": cls.BQ_USER_PROFILES_TABLE_ID,
            "BQ_AI_SENTIMENT_TABLE_ID": cls.BQ_AI_SENTIMENT_TABLE_ID,
            "BQ_AI_PATTERNS_TABLE_ID": cls.BQ_AI_PATTERNS_TABLE_ID,
            "BQ_AI_OPTIMIZATION_TABLE_ID": cls.BQ_AI_OPTIMIZATION_TABLE_ID,
            "BQ_AI_PREDICTIONS_TABLE_ID": cls.BQ_AI_PREDICTIONS_TABLE_ID,
            "BQ_AI_BUSINESS_METRICS_TABLE_ID": cls.BQ_AI_BUSINESS_METRICS_TABLE_ID,
            "BQ_ASYNC_TASKS_TABLE_ID": cls.BQ_ASYNC_TASKS_TABLE_ID,
            "BQ_WORKER_METRICS_TABLE_ID": cls.BQ_WORKER_METRICS_TABLE_ID,
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\Y DOCUMENTACION\MINISERVICIOS_SCRIPS\BOT APY>
Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\energy_ia_api_COPY\app\config.py"
    BQ_MARKET_TARIFS_TABLE_ID = (
        os.environ.get("BQ_MARKET_TARIFS_TABLE_ID") or "market_electricity_tariffs"
    BQ_RECOMMENDATION_LOG_TABLE_ID = os.environ.get(
        "BQ_RECOMMENDATION_LOG_TABLE_ID", "recommendation_log"
    BQ_CONSUMPTION_LOG_TABLE_ID = os.environ.get(
        "BQ_CONSUMPTION_LOG_TABLE_ID", "consumption_log"
    BQ_UPLOADED_DOCS_TABLE_ID = os.environ.get(
        "BQ_UPLOADED_DOCS_TABLE_ID", "uploaded_documents_log"
    BQ_CONVERSATIONS_TABLE_ID = os.environ.get(
        "BQ_CONVERSATIONS_TABLE_ID", "conversations_log"
    BQ_FEEDBACK_TABLE_ID = os.environ.get("BQ_FEEDBACK_TABLE_ID", "feedback_log")
    BQ_USER_PROFILES_TABLE_ID = os.environ.get(
        "BQ_USER_PROFILES_TABLE_ID", "user_profiles_enriched"
        "BQ_MARKET_TARIFS_TABLE_ID",
        "BQ_RECOMMENDATION_LOG_TABLE_ID",
        "BQ_CONSUMPTION_LOG_TABLE_ID",
        "BQ_UPLOADED_DOCS_TABLE_ID",
        "BQ_CONVERSATIONS_TABLE_ID",
        "BQ_FEEDBACK_TABLE_ID",
        "BQ_USER_PROFILES_TABLE_ID",
                "market_tariffs": cls.BQ_MARKET_TARIFS_TABLE_ID,
                "recommendation_log": cls.BQ_RECOMMENDATION_LOG_TABLE_ID,
                "consumption_log": cls.BQ_CONSUMPTION_LOG_TABLE_ID,
                "uploaded_docs": cls.BQ_UPLOADED_DOCS_TABLE_ID,
                "conversations": cls.BQ_CONVERSATIONS_TABLE_ID,
                "feedback": cls.BQ_FEEDBACK_TABLE_ID,
                "user_profiles": cls.BQ_USER_PROFILES_TABLE_ID,
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\Y DOCUMENTACION\MINISERVICIOS_SCRIPS\BOT APY>
watt_2\SmarWatt_2\backend\sevicio chatbot\servicios\expert_bot_api_COPY\app\services\*.py"
c:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\expert_bot_api_COPY\app\services\ai_learning_service.py:        table_ref = self.bigquery_client.dataset(self.bq_dataset_id).table(table_name)
c:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\expert_bot_api_COPY\app\services\ai_learning_service.py:                table_ref = self.bigquery_client.dataset(self.bq_dataset_id).table(
c:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\expert_bot_api_COPY\app\services\async_processing_service.py:            table_ref = self.bigquery_client.dataset(self.bq_dataset_id).table(
c:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\expert_bot_api_COPY\app\services\async_processing_service.py:            table_ref = self.bigquery_client.dataset(self.bq_dataset_id).table(
c:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\expert_bot_api_COPY\app\services\async_processing_service.py:            table_ref = self.bigquery_client.dataset(self.bq_dataset_id).table(
c:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\expert_bot_api_COPY\app\services\async_processing_service.py:            table_ref = self.bigquery_client.dataset(self.bq_dataset_id).table(
c:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\expert_bot_api_COPY\app\services\chat_service.py:                table_ref = self.bigquery_client.dataset(self.bq_dataset_id).table(
c:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\expert_bot_api_COPY\app\services\energy_service.py:            table_ref = self.bigquery_client.dataset(self.bq_dataset_id).table(
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\Y DOCUMENTACION\MINISERVICIOS_SCRIPS\BOT APY>
watt_2\SmarWatt_2\backend\sevicio chatbot\servicios\energy_ia_api_COPY\app\services\*.py"
c:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\energy_ia_api_COPY\app\services\generative_chat_service.py:            table_ref = self.bigquery_client.dataset(self.bq_dataset_id).table(
c:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\energy_ia_api_COPY\app\services\vertex_ai_service.py:            table_ref = self.bigquery_client.dataset(self.bq_dataset_id).table(
c:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\energy_ia_api_COPY\app\services\vertex_ai_service.py:            table_ref = self.bigquery_client.dataset(self.bq_dataset_id).table(
c:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\energy_ia_api_COPY\app\services\vertex_ai_service.py:            table_ref = self.bigquery_client.dataset(self.bq_dataset_id).table(
c:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\energy_ia_api_COPY\app\services\vertex_ai_service.py:            table_ref = self.bigquery_client.dataset(self.bq_dataset_id).table(
c:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\energy_ia_api_COPY\app\services\vertex_ai_service.py:            table_ref = self.bigquery_client.dataset(self.bq_dataset_id).table(
c:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\energy_ia_api_COPY\app\services\vertex_ai_service.py:            table_ref = self.bigquery_client.dataset(self.bq_dataset_id).table(
c:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\energy_ia_api_COPY\app\services\vertex_ai_service.py:            table_ref = self.bigquery_client.dataset(self.bq_dataset_id).table(
c:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\energy_ia_api_COPY\app\services\vertex_ai_service.py:            table_ref = self.bigquery_client.dataset(self.bq_dataset_id).table(
c:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\energy_ia_api_COPY\app\services\vertex_ai_service.py:            table_ref = self.bigquery_client.dataset(self.bq_dataset_id).table(
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\Y DOCUMENTACION\MINISERVICIOS_SCRIPS\BOT APY>
att_2\SmarWatt_2\backend\sevicio chatbot\servicios\expert_bot_api_COPY\app\services\chat_service.py"
        self.bq_conversations_table_id = current_app.config.get(
            "BQ_CONVERSATIONS_TABLE_ID", "conversations_log"
        self.bq_feedback_table_id = current_app.config.get(
            "BQ_FEEDBACK_TABLE_ID", "feedback_log"
        self, table_id: str, rows: List[Dict[str, Any]]
                    table_id
                logging.info("Ô£à Datos insertados correctamente en %s", table_id)
        self._log_to_bigquery_enterprise(self.bq_conversations_table_id, [row])
        return self._log_to_bigquery_enterprise(self.bq_feedback_table_id, [row])
            FROM `{self.gcp_project_id}.{self.bq_dataset_id}.{self.bq_conversations_table_id}`
            UPDATE `{self.gcp_project_id}.{self.bq_dataset_id}.{self.bq_conversations_table_id}`
            FROM `{self.gcp_project_id}.{self.bq_dataset_id}.{self.bq_conversations_table_id}`
            FROM `{self.gcp_project_id}.{self.bq_dataset_id}.{self.bq_conversations_table_id}`
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\Y DOCUMENTACION\MINISERVICIOS_SCRIPS\BOT APY>
_2\SmarWatt_2\backend\sevicio chatbot\servicios\expert_bot_api_COPY\app\services\chat_service.py"
14:from google.cloud import bigquery
25:        ai_learning_service_unavailable = True
35:        EnergyIAApiClient = None  # type: ignore
45:        get_enterprise_link_service = None  # type: ignore
62:    _bigquery_client_instance = None
63:_ai_learning_service_instance = None
64:_lock = threading.Lock()
65:    _executor = ThreadPoolExecutor(max_workers=10)
69:        self.energy_ia_api_url = energy_ia_api_url
70:        self.gcp_project_id = current_app.config["GCP_PROJECT_ID"]
71:        self.bq_dataset_id = current_app.config.get("BQ_DATASET_ID", "smartwatt_data")
72:        self.bq_conversations_table_id = current_app.config.get(
75:        self.bq_feedback_table_id = current_app.config.get(
81:            self.energy_ia_client = EnergyIAApiClient(
82:                base_url=energy_ia_api_url, timeout=30
85:            self.energy_ia_client = None
90:            self.links_service = get_enterprise_link_service()
92:            self.links_service = None
96:        self.max_retries = 3
97:        self.timeout_seconds = 30
98:        self.conversation_cache: Dict[str, Dict[str, Any]] = {}
99:        self.current_conversation_id: Optional[str] = None
100:        self.performance_metrics = {
114:            if ChatService._bigquery_client_instance is None:
117:                        ChatService._bigquery_client_instance = bigquery.Client(
118:                            project=self.gcp_project_id
135:                        if attempt == self.max_retries - 1:
149:                    ChatService._ai_learning_service_instance = AILearningService()  # type: ignore
155:                    ChatService._ai_learning_service_instance = None
157:        self.bigquery_client = ChatService._bigquery_client_instance
158:        self.ai_learning_service = ChatService._ai_learning_service_instance
160:    def_log_to_bigquery_enterprise(
164:        if self.bigquery_client is None:
170:                table_ref = self.bigquery_client.dataset(self.bq_dataset_id).table(
173:                errors = self.bigquery_client.insert_rows_json(table_ref, rows)
181:                    if attempt == self.max_retries - 1:
191:                if attempt == self.max_retries - 1:
199:                if attempt == self.max_retries - 1:
205:    def_log_conversation_turn_to_bigquery(
210:        intent: Optional[str] = None,
211:        bot_action: Optional[str] = None,  
212:        sentiment: Optional[str] = None,
213:        conversation_id: Optional[str] = None,
214:        response_time: Optional[float] = None,
215:        metadata: Optional[Dict[str, Any]] = None,
219:            conversation_id = getattr(
222:            self.current_conversation_id = conversation_id
224:        row = {
243:        self._log_to_bigquery_enterprise(self.bq_conversations_table_id, [row])
245:    def _log_feedback_to_bigquery(
250:        comments: Optional[str] = None,
251:        rating: Optional[int] = None,
252:        conversation_id: Optional[str] = None,
255:        row = {
270:        return self._log_to_bigquery_enterprise(self.bq_feedback_table_id, [row])
274:        start_time = time.time()
277:            session_id = str(uuid.uuid4())
278:            self.current_conversation_id = session_id
285:            enterprise_context = {
298:            self._log_conversation_turn_to_bigquery(
299:                user_id=user_profile["uid"],
300:                sender="system",
301:                message_text="SESSION_START",
302:                conversation_id=session_id,
303:                response_time=time.time() - start_time,
304:                metadata=enterprise_context,
308:            self.performance_metrics["total_requests"] += 1
309:            self.performance_metrics["successful_requests"] += 1
325:            self.performance_metrics["failed_requests"] += 1
342:        start_time = time.time()
343:        user_id = user_profile["uid"]
344:        self.current_conversation_id = conversation_id
348:            self.performance_metrics["total_requests"] += 1
351:            self._log_conversation_turn_to_bigquery(
352:                user_id=user_id,
353:                sender="user",
354:                message_text=user_message,
355:                conversation_id=conversation_id,
356:                response_time=time.time() - start_time,
360:            user_context = self._get_enterprise_user_context(user_id)
365:                    enhanced_context = (
378:            intent_analysis = self._analyze_user_intent_enterprise(
383:            bot_response_data = self._orchestrate_enterprise_response(
388:            enhanced_response = self._enhance_response_enterprise(
394:                enhanced_response_with_links = (
399:                enhanced_response["response"] = enhanced_response_with_links
400:                enhanced_response["links_enhanced"] = (
402:                    != enhanced_response.get("response", "")
406:            response_time = time.time() - start_time
407:            self._log_conversation_turn_to_bigquery(
408:                user_id=user_id,
409:                sender="bot",
410:                message_text=enhanced_response.get(
413:                conversation_id=conversation_id,
414:                intent=intent_analysis.get("primary_intent"),
415:                bot_action=intent_analysis.get("strategy"),
416:                sentiment=enhanced_response.get("sentiment_analysis"),
417:                response_time=response_time,
418:                metadata={
474:        context: Dict[str, Any] = {
491:        start_time = time.time()
494:        with ThreadPoolExecutor(max_workers=5) as executor:
495:            futures = {
504:                source_type = futures[future]
506:                    result = future.result(timeout=10)
508:                        context[f"{source_type}_data"] = result
510:                        context["data_completeness"] += 20
511:                        context["enterprise_metrics"]["sources_accessed"] += 1
519:        context["enterprise_metrics"]["context_build_time"] = time.time() - start_time
520:        context["enterprise_metrics"]["data_quality_score"] = min(
539:        intent_analysis: Dict[str, Any] = {
551:        ml_patterns = {
583:        pattern_scores = {}
585:            score = sum(
588:            pattern_scores[category] = score
591:        data_completeness = user_context.get("data_completeness", 0)
592:        max_score = max(pattern_scores.values()) if pattern_scores.values() else 0
595:            intent_analysis["strategy"] = "ml_recommendations"
596:            intent_analysis["primary_intent"] = "ml_analysis"
597:            intent_analysis["confidence"] = min(
600:            intent_analysis["enterprise_analysis"]["ml_readiness"] = True
602:            intent_analysis["strategy"] = "hybrid_consultation"
603:            intent_analysis["primary_intent"] = "hybrid_analysis"
604:            intent_analysis["confidence"] = min(
608:            intent_analysis["strategy"] = "general_chat"
609:            intent_analysis["confidence"] = 0.6
612:        intent_analysis["enterprise_analysis"]["data_sufficiency"] = (
615:        intent_analysis["enterprise_analysis"]["user_engagement_level"] = (
632:        strategy = intent_analysis.get("strategy", "general_chat")
635:            if strategy == "ml_recommendations":
639:            elif strategy == "hybrid_consultation":
663:                ml_context = self._prepare_enterprise_ml_context(user_context)
666:                ml_context["user_query_analysis"] = {
678:                    "query_complexity": len(user_message.split()),
682:                auth_token = self._get_service_to_service_token()
684:                headers = {
693:                complete_url = (
697:                response = requests.get(
699:                    headers=headers,
700:                    timeout=self.timeout_seconds,
701:                    params={"enterprise_mode": "true"},
705:                ml_response = response.json()
726:                if attempt == self.max_retries - 1:
744:                gemini_context = self._prepare_enterprise_gemini_context(user_context)
747:                auth_token = self._get_service_to_service_token()
749:                headers = {
756:                payload = {
787:                complete_url = f"{self.energy_ia_api_url}/api/v1/chatbot/message/v2"
789:                response = requests.post(  
791:                    json=payload,
792:                    headers=headers,
793:                    timeout=self.timeout_seconds,
797:                gemini_response = response.json()
817:                if attempt == self.max_retries - 1:
836:            with ThreadPoolExecutor(max_workers=2) as executor:
837:                ml_future = executor.submit(
845:                explanation_prompt = f"Proporciona una explicaci├│n detallada y personalizada sobre: {user_message}"
846:                gemini_future = executor.submit(
855:                ml_result = ml_future.result(timeout=25)
856:                gemini_result = gemini_future.result(timeout=25)
859:            combined_response = self._combine_hybrid_responses(ml_result, gemini_result)  
886:            query = f"""
898:            WHERE conversation_id = @conversation_id
899:            AND user_id = @user_id
903:            job_config = bigquery.QueryJobConfig(
904:                query_parameters=[
905:                    bigquery.ScalarQueryParameter(
908:                    bigquery.ScalarQueryParameter("user_id", "STRING", user_id),
912:            if self.bigquery_client is None:
915:            query_job = self.bigquery_client.query(query, job_config=job_config)
916:            results = list(query_job.result())
918:            messages = []
957:            update_query = f"""
959:            SET metadata = JSON_SET(IFNULL(metadata, '{{}}'), '$.deleted', true, '$.deleted_at', @deleted_at)
960:            WHERE conversation_id = @conversation_id
961:            AND user_id = @user_id
964:            job_config = bigquery.QueryJobConfig(
965:                query_parameters=[
966:                    bigquery.ScalarQueryParameter(
969:                    bigquery.ScalarQueryParameter("user_id", "STRING", user_id),
970:                    bigquery.ScalarQueryParameter(
978:            if self.bigquery_client is None:
981:            query_job = self.bigquery_client.query(update_query, job_config=job_config)
982:            query_job.result()
1010:        feedback_text: Optional[str] = None,
1011:        recommendation_type: str = "general",
1016:            if not 1 <= rating <= 5:
1020:            feedback_useful = rating >= 3
1021:            success = self._log_feedback_to_bigquery(
1022:                user_id=user_id,
1023:                recommendation_type=recommendation_type,
1024:                feedback_useful=feedback_useful,
1025:                comments=feedback_text,
1026:                rating=rating,
1027:                conversation_id=conversation_id,
1035:                            user_id=user_id,
1036:                            conversation_id=conversation_id,
1037:                            rating=rating,
1038:                            feedback_text=feedback_text,
1064:            audience_url = self.energy_ia_api_url
1065:            auth_req = google.auth.transport.requests.Request()
1066:            token = google.oauth2.id_token.fetch_id_token(auth_req, audience_url)
1083:        enterprise_context = {
1091:            invoice = user_context["last_invoice"]
1092:            enterprise_context["consumption_data"] = {
1126:            learning_data = {
1146:            self.performance_metrics["successful_requests"] += 1
1148:            self.performance_metrics["failed_requests"] += 1
1151:        total_requests = self.performance_metrics["total_requests"]
1152:        current_avg = self.performance_metrics["avg_response_time"]
1154:        self.performance_metrics["avg_response_time"] = (
1161:        total_score = 0.0
1162:        weight_factors = 0.0
1165:        confidence = response_data.get("confidence", 0.0)
1166:        confidence_score = min(1.0, max(0.0, confidence)) *0.3
1167:        total_score += confidence_score
1168:        weight_factors += 0.3
1171:        data_used = response_data.get("data_used", False)
1174:            data_completeness = response_data.get("data_completeness", 0)
1175:            data_score = (data_completeness / 100.0)* 0.25
1177:            data_score = 0.1 *0.25  # Penalizaci├│n por no usar datos
1178:        total_score += data_score
1179:        weight_factors += 0.25
1182:        response_time = response_data.get("response_time_ms", 5000)
1183:        if response_time <= 1000:
1184:            time_score = 1.0* 0.2
1185:        elif response_time <= 3000:
1186:            time_score = 0.8 *0.2
1187:        elif response_time <= 5000:
1188:            time_score = 0.6* 0.2
1190:            time_score = 0.3 *0.2
1191:        total_score += time_score
1192:        weight_factors += 0.2
1195:        sentiment_analysis = response_data.get("sentiment_analysis")
1197:            sentiment_score = 1.0* 0.15
1199:            sentiment_score = 0.5 *0.15  
1200:        total_score += sentiment_score
1201:        weight_factors += 0.15
1204:        response_text = response_data.get("response", "")
1205:        response_length = len(response_text)
1206:        if 100 <= response_length <= 1000:
1207:            length_score = 1.0* 0.1
1208:        elif 50 <= response_length < 100 or 1000 < response_length <= 2000:
1209:            length_score = 0.8 *0.1
1211:            length_score = 0.4* 0.1
1213:            length_score = 0.6 *0.1
1214:        total_score += length_score
1215:        weight_factors += 0.1
1218:        final_score = total_score / weight_factors if weight_factors > 0 else 0.5
1227:        message_analysis = {
1242:        data_completeness = user_context.get("data_completeness", 0)
1243:        available_sources = user_context.get("available_sources", [])
1244:        user_name = user_context.get("user_id", "usuario")
1248:            base_response = f"Disculpe, {user_name}, estoy experimentando dificultades con el sistema de an├ílisis energ├®tico."
1250:                base_response += " Tengo acceso a parte de sus datos y trabajar├® para proporcionarle una respuesta m├ís completa."
1252:            base_response = f"Entiendo la urgencia de su consulta, {user_name}. Estoy trabajando para resolver los problemas t├®cnicos lo antes posible."
1254:            base_response = f"Lamento no poder responder su pregunta en este momento, {user_name}. Estoy experimentando dificultades t├®cnicas temporales."
1256:            base_response = "Estoy experimentando dificultades t├®cnicas temporales. Por favor, intenta nuevamente en unos momentos."
1278:        data_completeness = user_context.get("data_completeness", 0)
1279:        available_sources = user_context.get("available_sources", [])
1280:        user_name = user_context.get("user_id", "usuario")
1284:            response = f"Disculpe, {user_name}, el sistema de recomendaciones ML est├í temporalmente no disponible. Sin embargo, tengo acceso a {len(available_sources)} fuentes de sus datos para ofrecerle asistencia b├ísica."
1286:            response = f"El sistema de recomendaciones est├í en mantenimiento, {user_name}. Puedo ayudarle con informaci├│n general mientras se restablece el servicio."
1288:            response = f"El sistema de recomendaciones est├í temporalmente no disponible, {user_name}. Para obtener recomendaciones personalizadas, necesitar├¡amos m├ís informaci├│n de su perfil energ├®tico."
1313:        data_completeness = user_context.get("data_completeness", 0)
1314:        available_sources = user_context.get("available_sources", [])
1315:        user_name = user_context.get("user_id", "usuario")
1318:        personalized_response = self._generate_contextual_fallback_response(
1346:        message_lower = user_message.lower()
1350:            base_response = f"Disculpe, {user_name}, el sistema de comparaci├│n de tarifas est├í temporalmente no disponible."
1352:                base_response += " Bas├índome en su perfil energ├®tico, le sugiero consultar proveedores locales mientras restablezco el servicio."
1356:            base_response = f"Le pido disculpas, {user_name}, el an├ílisis de consumo est├í en mantenimiento."
1358:                base_response += (
1364:            base_response = f"Estimado {user_name}, el servicio de an├ílisis energ├®tico est├í temporalmente fuera de l├¡nea."
1366:                base_response += " Con base en su hist├│rico, puedo proporcionarle recomendaciones b├ísicas una vez restablecido el servicio."
1371:            base_response = f"Disculpe, {user_name}, estoy experimentando dificultades t├®cnicas temporales."
1373:                base_response += " Tengo acceso parcial a sus datos para asistirle cuando el sistema se restablezca."
1375:                base_response += " Le recomiendo intentar nuevamente en unos minutos."
1376:                base_response += " Estoy trabajando para resolver el problema y brindarle una respuesta completa."
1384:        ml_response = ml_result.get("response", "")
1385:        gemini_response = gemini_result.get("response", "")
1399:            energy_service: Any = EnergyService()  # type: ignore
1400:            result = energy_service.get_user_energy_profile(user_id)
1419:            query = f"""
1425:            WHERE user_id = @user_id
1426:            AND sender = 'user'
1427:            AND timestamp_utc >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
1428:            AND (JSON_EXTRACT(metadata, '$.deleted') IS NULL OR JSON_EXTRACT(metadata, '$.deleted') = false)
1431:            job_config = bigquery.QueryJobConfig(
1432:                query_parameters=[
1433:                    bigquery.ScalarQueryParameter("user_id", "STRING", user_id),
1437:            if self.bigquery_client is None:
1440:            query_job = self.bigquery_client.query(query, job_config=job_config)
1441:            results = list(query_job.result())
1444:                row = results[0]
1472:            db = firestore.Client(project=self.gcp_project_id)
1474:            user_ref = db.collection("users").document(user_id)
1475:            user_doc = user_ref.get()
1497:            energy_service: Any = EnergyService()  # type: ignore
1498:            result = energy_service.get_consumption_history(user_id)
1513:            query = f"""
1520:            WHERE user_id = @user_id
1521:            AND sender = 'bot'
1522:            AND timestamp_utc >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
1523:            AND (JSON_EXTRACT(metadata, '$.deleted') IS NULL OR JSON_EXTRACT(metadata, '$.deleted') = false)
1529:            job_config = bigquery.QueryJobConfig(
1530:                query_parameters=[
1531:                    bigquery.ScalarQueryParameter("user_id", "STRING", user_id),
1535:            if self.bigquery_client is None:
1538:            query_job = self.bigquery_client.query(query, job_config=job_config)
1539:            results = list(query_job.result())
1541:            interactions = []
1566:        total_score = 0.0
1567:        weight_factors = 0.0
1570:        recommendations = ml_response.get("recommendations", [])
1573:            rec_count = len(recommendations) if isinstance(recommendations, list) else 1
1574:            if rec_count >= 3:
1575:                rec_score = 1.0* 0.4
1576:            elif rec_count >= 2:
1577:                rec_score = 0.8 *0.4
1578:            elif rec_count >= 1:
1579:                rec_score = 0.6* 0.4
1581:                rec_score = 0.2 *0.4
1583:            rec_score = 0.1* 0.4
1584:        total_score += rec_score
1585:        weight_factors += 0.4
1588:        confidence = ml_response.get("confidence", 0.0)
1589:        confidence_score = min(1.0, max(0.0, confidence)) *0.3
1590:        total_score += confidence_score
1591:        weight_factors += 0.3
1594:        savings = ml_response.get("potential_savings", 0)
1597:            savings_normalized = min(1.0, savings / 200.0)
1598:            savings_score = savings_normalized* 0.2
1600:            savings_score = 0.1 *0.2
1601:        total_score += savings_score
1602:        weight_factors += 0.2
1605:        data_points = ml_response.get("data_points_used", 0)
1606:        if data_points >= 5:
1607:            data_score = 1.0* 0.1
1608:        elif data_points >= 3:
1609:            data_score = 0.8 *0.1
1610:        elif data_points >= 1:
1611:            data_score = 0.6* 0.1
1613:            data_score = 0.3 *0.1
1614:        total_score += data_score
1615:        weight_factors += 0.1
1618:        final_score = total_score / weight_factors if weight_factors > 0 else 0.4
1626:        total_score = 0.0
1627:        weight_factors = 0.0
1630:        response_text = gemini_response.get("response", "")
1631:        response_length = len(response_text)
1632:        if 200 <= response_length <= 800:
1633:            length_score = 1.0* 0.25  # Longitud ├│ptima para explicaciones energ├®ticas
1634:        elif 100 <= response_length < 200 or 800 < response_length <= 1200:
1635:            length_score = 0.8 *0.25
1636:        elif 50 <= response_length < 100 or 1200 < response_length <= 1500:
1637:            length_score = 0.6* 0.25
1639:            length_score = 0.3 *0.25  # Respuesta muy corta
1641:            length_score = 0.4* 0.25  # Respuesta muy larga
1642:        total_score += length_score
1643:        weight_factors += 0.25
1646:        sentiment = gemini_response.get("sentiment")
1648:            sentiment_confidence = gemini_response.get("sentiment_confidence", 0.5)
1649:            sentiment_score = min(1.0, sentiment_confidence) *0.25
1651:            sentiment_score = 0.4* 0.25  
1652:        total_score += sentiment_score
1653:        weight_factors += 0.25
1656:        context_used = gemini_response.get("context_used", False)
1657:        personalization_level = gemini_response.get("personalization_level", "none")
1658:        if context_used and personalization_level == "high":
1659:            context_score = 1.0 *0.2
1660:        elif context_used and personalization_level == "medium":
1661:            context_score = 0.8* 0.2
1663:            context_score = 0.6 *0.2
1665:            context_score = 0.3* 0.2
1666:        total_score += context_score
1667:        weight_factors += 0.2
1670:        energy_terms = [
1679:        energy_terms_count = sum(
1682:        if energy_terms_count >= 3:
1683:            technical_score = 1.0 *0.15  
1684:        elif energy_terms_count >= 2:
1685:            technical_score = 0.8* 0.15  
1686:        elif energy_terms_count >= 1:
1687:            technical_score = 0.6 *0.15  
1689:            technical_score = 0.4* 0.15  
1690:        total_score += technical_score
1691:        weight_factors += 0.15
1694:        response_time = gemini_response.get("response_time_ms", 3000)
1695:        if response_time <= 2000:
1696:            time_score = 1.0 *0.15
1697:        elif response_time <= 4000:
1698:            time_score = 0.8* 0.15
1699:        elif response_time <= 6000:
1700:            time_score = 0.6 *0.15
1702:            time_score = 0.4* 0.15
1703:        total_score += time_score
1704:        weight_factors += 0.15
1707:        final_score = total_score / weight_factors if weight_factors > 0 else 0.5
1717:        enhanced_response = bot_response.copy()
1720:        data_completeness = user_context.get("data_completeness", 0)
1722:            suggestions = self._generate_enterprise_suggestions(user_context)
1724:                enhanced_response["enterprise_suggestions"] = suggestions
1727:        enhanced_response["context_quality"] = {
1734:        enhanced_response["intent_analysis"] = {
1752:        suggestions = []
1753:        missing_data = user_context.get("missing_critical_data", [])
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\Y DOCUMENTACION\MINISERVICIOS_SCRIPS\BOT APY>
t_2\SmarWatt_2\backend\sevicio chatbot\servicios\expert_bot_api_COPY\app\services\chat_service.py"
9:from typing import Dict, Any, Optional, List
10:from flask import current_app
11:from datetime import datetime, timezone
12:from concurrent.futures import ThreadPoolExecutor, as_completed
14:from google.cloud import bigquery
15:from google.api_core import exceptions as google_exceptions
16:from utils.error_handlers import AppError
20:    from app.services.ai_learning_service import AILearningService
23:        from .ai_learning_service import AILearningService
25:        ai_learning_service_unavailable = True
30:    from app.services.energy_ia_client import EnergyIAApiClient
33:        from .energy_ia_client import EnergyIAApiClient
35:        EnergyIAApiClient = None  # type: ignore
40:    from app.services.enterprise_links_service import get_enterprise_link_service
43:        from .enterprise_links_service import get_enterprise_link_service
45:        get_enterprise_link_service = None  # type: ignore
58:    - Tolerancia a fallos y recuperaci├│n autom├ítica
62:_bigquery_client_instance = None
63:    _ai_learning_service_instance = None
64:    _lock = threading.Lock()
65:_executor = ThreadPoolExecutor(max_workers=10)
67:    def __init__(self, energy_ia_api_url: str) -> None:
69:        self.energy_ia_api_url = energy_ia_api_url
70:        self.gcp_project_id = current_app.config["GCP_PROJECT_ID"]
71:        self.bq_dataset_id = current_app.config.get("BQ_DATASET_ID", "smartwatt_data")
72:        self.bq_conversations_table_id = current_app.config.get(
75:        self.bq_feedback_table_id = current_app.config.get(
76:            "BQ_FEEDBACK_TABLE_ID", "feedback_log"
80:        if EnergyIAApiClient is not None:
81:            self.energy_ia_client = EnergyIAApiClient(
82:                base_url=energy_ia_api_url, timeout=30
85:            self.energy_ia_client = None
89:        if get_enterprise_link_service is not None:
90:            self.links_service = get_enterprise_link_service()
92:            self.links_service = None
95:        # Configuraci├│n empresarial
96:        self.max_retries = 3
97:        self.timeout_seconds = 30
98:        self.conversation_cache: Dict[str, Dict[str, Any]] = {}
99:        self.current_conversation_id: Optional[str] = None
100:        self.performance_metrics = {
102:            "successful_requests": 0,
103:            "failed_requests": 0,
107:        # Inicializaci├│n thread-safe empresarial
108:        self._initialize_enterprise_services()
110:    def _initialize_enterprise_services(self) -> None:
114:            if ChatService._bigquery_client_instance is None:
115:                for attempt in range(self.max_retries):
117:                        ChatService._bigquery_client_instance = bigquery.Client(
118:                            project=self.gcp_project_id
120:                        logging.info(
135:                        if attempt == self.max_retries - 1:
139:                            ) from e
140:                        time.sleep(2**attempt)  # Backoff exponencial
143:            if (
145:                and current_app.config.get("AI_LEARNING_ENABLED", True)
149:                    ChatService._ai_learning_service_instance = AILearningService()  # type: ignore
150:                    logging.info(
155:                    ChatService._ai_learning_service_instance = None
157:        self.bigquery_client = ChatService._bigquery_client_instance
158:        self.ai_learning_service = ChatService._ai_learning_service_instance
160:    def _log_to_bigquery_enterprise(
161:        self, table_id: str, rows: List[Dict[str, Any]]
164:        if self.bigquery_client is None:
168:        for attempt in range(self.max_retries):
170:                table_ref = self.bigquery_client.dataset(self.bq_dataset_id).table(
173:                errors = self.bigquery_client.insert_rows_json(table_ref, rows)
175:                if errors:
181:                    if attempt == self.max_retries - 1:
186:                logging.info("Ô£à Datos insertados correctamente en %s", table_id)
191:                if attempt == self.max_retries - 1:
199:                if attempt == self.max_retries - 1:
205:    def_log_conversation_turn_to_bigquery(
206:        self,
210:        intent: Optional[str] = None,
211:        bot_action: Optional[str] = None,  
212:        sentiment: Optional[str] = None,
213:        conversation_id: Optional[str] = None,
214:        response_time: Optional[float] = None,
215:        metadata: Optional[Dict[str, Any]] = None,
218:        if conversation_id is None:
219:            conversation_id = getattr(
220:                self, "current_conversation_id", str(uuid.uuid4())
222:            self.current_conversation_id = conversation_id
224:        row = {
228:            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
234:            "response_time_ms": int(response_time *1000) if response_time else None,
235:            "metadata": json.dumps(metadata) if metadata else None,
236:            "session_info": {
238:                "platform": "web",
243:        self._log_to_bigquery_enterprise(self.bq_conversations_table_id, [row])
245:    def_log_feedback_to_bigquery(
246:        self,
249:        feedback_useful: bool,
250:        comments: Optional[str] = None,
251:        rating: Optional[int] = None,
252:        conversation_id: Optional[str] = None,
254:        """Logging empresarial de feedback con an├ílisis avanzado."""
255:        row = {
256:            "feedback_id": str(uuid.uuid4()),
260:            "feedback_useful": feedback_useful,
263:            "submitted_at": datetime.now(timezone.utc).isoformat(),
265:                "feedback_source": "enterprise_interface",
270:        return self._log_to_bigquery_enterprise(self.bq_feedback_table_id, [row])
272:    def start_session(self, user_profile: Dict[str, Any]) -> Dict[str, Any]:
274:        start_time = time.time()
277:            session_id = str(uuid.uuid4())
278:            self.current_conversation_id = session_id
280:            # Validar perfil de usuario
281:            if not user_profile.get("uid"):
282:                raise AppError("Perfil de usuario inv├ílido", 400)
285:            enterprise_context = {
287:                "user_id": user_profile["uid"],
288:                "session_start": datetime.now(timezone.utc).isoformat(),
289:                "platform": "enterprise_web",
293:                    "feedback_analysis",
298:            self._log_conversation_turn_to_bigquery(
299:                user_id=user_profile["uid"],
300:                sender="system",
301:                message_text="SESSION_START",
302:                conversation_id=session_id,
303:                response_time=time.time() - start_time,
304:                metadata=enterprise_context,
308:            self.performance_metrics["total_requests"] += 1
309:            self.performance_metrics["successful_requests"] += 1
311:            logging.info(
314:                user_profile["uid"],
320:                "enterprise_features": enterprise_context["capabilities"],
325:            self.performance_metrics["failed_requests"] += 1
327:            raise AppError("Error al inicializar sesi├│n empresarial", 500) from e
329:    def process_user_message(
330:        self, user_profile: Dict[str, Any], user_message: str, conversation_id: str
342:        start_time = time.time()
343:        user_id = user_profile["uid"]
344:        self.current_conversation_id = conversation_id
348:            self.performance_metrics["total_requests"] += 1
351:            self._log_conversation_turn_to_bigquery(
352:                user_id=user_id,
353:                sender="user",
354:                message_text=user_message,
355:                conversation_id=conversation_id,
356:                response_time=time.time() - start_time,
360:            user_context = self._get_enterprise_user_context(user_id)
363:            if self.ai_learning_service:
365:                    enhanced_context = (
366:                        self.ai_learning_service.enhance_user_context_with_learning(
371:                    logging.info(
378:            intent_analysis = self._analyze_user_intent_enterprise(
383:            bot_response_data = self._orchestrate_enterprise_response(
388:            enhanced_response = self._enhance_response_enterprise(
393:            if self.links_service and enhanced_response.get("response"):
394:                enhanced_response_with_links = (
395:                    self.links_service.analyze_and_enhance_response(
399:                enhanced_response["response"] = enhanced_response_with_links
400:                enhanced_response["links_enhanced"] = (
402:                    != enhanced_response.get("response", "")
406:            response_time = time.time() - start_time
407:            self._log_conversation_turn_to_bigquery(
408:                user_id=user_id,
409:                sender="bot",
410:                message_text=enhanced_response.get(
413:                conversation_id=conversation_id,
414:                intent=intent_analysis.get("primary_intent"),
415:                bot_action=intent_analysis.get("strategy"),
416:                sentiment=enhanced_response.get("sentiment_analysis"),
417:                response_time=response_time,
418:                metadata={
419:                    "performance_score": enhanced_response.get("performance_score", 0),
421:                    "strategy_confidence": intent_analysis.get("confidence", 0),
429:            if self.ai_learning_service:
431:                    self._process_enterprise_learning(
443:            self._update_performance_metrics(response_time, True)
445:            # 10. A├▒adir informaci├│n empresarial a la respuesta
450:                        "performance_score": self._calculate_performance_score(
453:                        "ai_confidence": intent_analysis.get("confidence", 0),
457:                    "timestamp": datetime.now(timezone.utc).isoformat(),
464:            self._update_performance_metrics(time.time() - start_time, False)
468:            return self._get_enterprise_fallback_response(
469:                user_message, user_context if "user_context" in locals() else {}
472:    def _get_enterprise_user_context(self, user_id: str) -> Dict[str, Any]:
473:        """­ƒÅó Obtenci├│n empresarial de contexto con m├║ltiples fuentes."""
474:        context: Dict[str, Any] = {
479:            "energy_profile": {},
481:            "preferences": {},
491:        start_time = time.time()
494:        with ThreadPoolExecutor(max_workers=5) as executor:
495:            futures = {
496:                executor.submit(self._get_energy_profile, user_id): "energy_profile",
497:                executor.submit(self._get_analytics_summary, user_id): "analytics",
498:                executor.submit(self._get_user_preferences, user_id): "preferences",
499:                executor.submit(self._get_consumption_history, user_id): "consumption",
500:                executor.submit(self._get_recent_interactions, user_id): "interactions",  
503:            for future in as_completed(futures):
504:                source_type = futures[future]
506:                    result = future.result(timeout=10)
507:                    if result:
508:                        context[f"{source_type}_data"] = result
510:                        context["data_completeness"] += 20
511:                        context["enterprise_metrics"]["sources_accessed"] += 1
519:        context["enterprise_metrics"]["context_build_time"] = time.time() - start_time
520:        context["enterprise_metrics"]["data_quality_score"] = min(
524:        logging.info(
525:            "­ƒÅó Contexto empresarial obtenido: %d%% - Fuentes: %d - Tiempo: %.2fs",
533:    def_analyze_user_intent_enterprise(
534:        self, user_message: str, user_context: Dict[str, Any]
539:        intent_analysis: Dict[str, Any] = {
542:            "confidence": 0.0,
545:                "data_sufficiency": False,
551:        ml_patterns = {
552:            "tariff_optimization": [
553:                "tarifa",
563:                "factura",
583:        pattern_scores = {}
584:        for category, patterns in ml_patterns.items():
585:            score = sum(
586:                2 if pattern in user_message.lower() else 0 for pattern in patterns
588:            pattern_scores[category] = score
591:        data_completeness = user_context.get("data_completeness", 0)
592:        max_score = max(pattern_scores.values()) if pattern_scores.values() else 0
594:        if max_score > 4 and data_completeness > 50:
595:            intent_analysis["strategy"] = "ml_recommendations"
596:            intent_analysis["primary_intent"] = "ml_analysis"
597:            intent_analysis["confidence"] = min(
600:            intent_analysis["enterprise_analysis"]["ml_readiness"] = True
601:        elif max_score > 2 and data_completeness > 30:
602:            intent_analysis["strategy"] = "hybrid_consultation"
603:            intent_analysis["primary_intent"] = "hybrid_analysis"
604:            intent_analysis["confidence"] = min(
608:            intent_analysis["strategy"] = "general_chat"
609:            intent_analysis["confidence"] = 0.6
612:        intent_analysis["enterprise_analysis"]["data_sufficiency"] = (
615:        intent_analysis["enterprise_analysis"]["user_engagement_level"] = (
617:            if len(user_message) > 50
618:            else "medium" if len(user_message) > 20 else "low"
623:    def _orchestrate_enterprise_response(  
624:        self,
632:        strategy = intent_analysis.get("strategy", "general_chat")
635:            if strategy == "ml_recommendations":
636:                return self._handle_ml_recommendations_enterprise(
639:            elif strategy == "hybrid_consultation":
640:                return self._handle_hybrid_consultation_enterprise(
644:                return self._handle_general_chat_enterprise(
649:            return self._get_enterprise_fallback_response(user_message, user_context)
651:    def_handle_ml_recommendations_enterprise(
652:        self,
658:        """­ƒñû Recomendaciones ML empresariales con tolerancia a fallos."""
660:        for attempt in range(self.max_retries):
663:                ml_context = self._prepare_enterprise_ml_context(user_context)
666:                ml_context["user_query_analysis"] = {
671:                        for word in ["urgente", "rapido", "inmediato", "ya"]
673:                    "contains_cost_focus": any(
675:                        for word in ["barato", "economico", "ahorro", "coste"]
677:                    "intent_confidence": intent_analysis.get("confidence", 0),
678:                    "query_complexity": len(user_message.split()),
682:                auth_token = self._get_service_to_service_token()
684:                headers = {
685:                    "Authorization": f"Bearer {auth_token}",
689:                    "X-Intent-Confidence": str(intent_analysis.get("confidence", 0)),
693:                complete_url = (
694:                    f"{self.energy_ia_api_url}/api/v1/energy/tariffs/recommendations"
697:                response = requests.get(
699:                    headers=headers,
700:                    timeout=self.timeout_seconds,
701:                    params={"enterprise_mode": "true"},
703:                response.raise_for_status()
705:                ml_response = response.json()
716:                    "performance_score": self._calculate_ml_performance_score(
719:                    "confidence": intent_analysis.get("confidence", 0.8),
726:                if attempt == self.max_retries - 1:
727:                    return self._get_enterprise_ml_fallback(user_context)
730:        return self._get_enterprise_ml_fallback(user_context)
732:    def_handle_general_chat_enterprise(
733:        self,
741:        for attempt in range(self.max_retries):
744:                gemini_context = self._prepare_enterprise_gemini_context(user_context)
747:                auth_token = self._get_service_to_service_token()
749:                headers = {
750:                    "Authorization": f"Bearer {auth_token}",
756:                payload = {
769:                    "enterprise_features": {
777:                        "confidence": intent_analysis.get("confidence", 0),
787:                complete_url = f"{self.energy_ia_api_url}/api/v1/chatbot/message/v2"
789:                response = requests.post(  
791:                    json=payload,
792:                    headers=headers,
793:                    timeout=self.timeout_seconds,
795:                response.raise_for_status()
797:                gemini_response = response.json()
807:                    "performance_score": self._calculate_gemini_performance_score(
817:                if attempt == self.max_retries - 1:
818:                    return self._get_enterprise_gemini_fallback(
823:        return self._get_enterprise_gemini_fallback(user_message, user_context)
825:    def_handle_hybrid_consultation_enterprise(
826:        self,
836:            with ThreadPoolExecutor(max_workers=2) as executor:
837:                ml_future = executor.submit(
838:                    self._handle_ml_recommendations_enterprise,
845:                explanation_prompt = f"Proporciona una explicaci├│n detallada y personalizada sobre: {user_message}"
846:                gemini_future = executor.submit(
847:                    self._handle_general_chat_enterprise,
855:                ml_result = ml_future.result(timeout=25)
856:                gemini_result = gemini_future.result(timeout=25)
858:            # Combinar respuestas de forma inteligente
859:            combined_response = self._combine_hybrid_responses(ml_result, gemini_result)  
868:                "performance_score": (
869:                    ml_result.get("performance_score", 0)
870:                    + gemini_result.get("performance_score", 0)
877:            return self._get_enterprise_fallback_response(user_message, user_context)
881:    def get_conversation_history(
882:        self, user_id: str, conversation_id: str
886:            query = f"""
897:            FROM `{self.gcp_project_id}.{self.bq_dataset_id}.{self.bq_conversations_table_id}`
898:            WHERE conversation_id = @conversation_id
899:            AND user_id = @user_id
903:            job_config = bigquery.QueryJobConfig(
904:                query_parameters=[
905:                    bigquery.ScalarQueryParameter(
908:                    bigquery.ScalarQueryParameter("user_id", "STRING", user_id),
912:            if self.bigquery_client is None:
915:            query_job = self.bigquery_client.query(query, job_config=job_config)
916:            results = list(query_job.result())
918:            messages = []
919:            for row in results:
930:                        "metadata": json.loads(row.metadata) if row.metadata else {},
953:    def delete_conversation(self, user_id: str, conversation_id: str) -> Dict[str, Any]:  
954:        """­ƒùæ´©Å Eliminar conversaci├│n empresarial (soft delete)."""
956:            # Marcar como eliminada en lugar de borrar f├¡sicamente
957:            update_query = f"""
958:            UPDATE `{self.gcp_project_id}.{self.bq_dataset_id}.{self.bq_conversations_table_id}`
959:            SET metadata = JSON_SET(IFNULL(metadata, '{{}}'), '$.deleted', true, '$.deleted_at', @deleted_at)
960:            WHERE conversation_id = @conversation_id
961:            AND user_id = @user_id
964:            job_config = bigquery.QueryJobConfig(
965:                query_parameters=[
966:                    bigquery.ScalarQueryParameter(
969:                    bigquery.ScalarQueryParameter("user_id", "STRING", user_id),
970:                    bigquery.ScalarQueryParameter(
973:                        datetime.now(timezone.utc).isoformat(),
978:            if self.bigquery_client is None:
981:            query_job = self.bigquery_client.query(update_query, job_config=job_config)
982:            query_job.result()
984:            logging.info(
1005:    def submit_conversation_feedback(
1006:        self,
1010:        feedback_text: Optional[str] = None,
1011:        recommendation_type: str = "general",
1013:        """Ô¡É Enviar feedback de conversaci├│n empresarial."""
1016:            if not 1 <= rating <= 5:
1019:            # Registrar feedback
1020:            feedback_useful = rating >= 3
1021:            success = self._log_feedback_to_bigquery(
1022:                user_id=user_id,
1023:                recommendation_type=recommendation_type,
1024:                feedback_useful=feedback_useful,
1025:                comments=feedback_text,
1026:                rating=rating,
1027:                conversation_id=conversation_id,
1030:            if success:
1031:                # ­ƒºá Procesar feedback para aprendizaje autom├ítico
1032:                if self.ai_learning_service:
1034:                        self.ai_learning_service.process_feedback_learning(
1035:                            user_id=user_id,
1036:                            conversation_id=conversation_id,
1037:                            rating=rating,
1038:                            feedback_text=feedback_text,
1041:                        logging.error("Error procesando feedback para ML: %s", e)
1044:                    "feedback_id": str(uuid.uuid4()),
1050:                return {"error": "Error al registrar el feedback", "status": "error"}
1053:            logging.error("Error enviando feedback: %s", e)
1054:            return {"error": "No se pudo procesar el feedback", "status": "error"}
1058:    def _get_service_to_service_token(self) -> str:
1064:            audience_url = self.energy_ia_api_url
1065:            auth_req = google.auth.transport.requests.Request()
1066:            token = google.oauth2.id_token.fetch_id_token(auth_req, audience_url)
1068:            if not token:
1074:            raise AppError("Dependencias de autenticaci├│n no disponibles", 500) from e  
1077:            raise AppError("Error de autenticaci├│n entre servicios", 500) from e
1079:    def_prepare_enterprise_ml_context(
1080:        self, user_context: Dict[str, Any]
1083:        enterprise_context = {
1084:            "user_profile": {
1090:        if user_context.get("last_invoice"):
1091:            invoice = user_context["last_invoice"]
1092:            enterprise_context["consumption_data"] = {
1100:    def _prepare_enterprise_gemini_context(
1101:        self, user_context: Dict[str, Any]
1108:            "user_profile": user_context.get("energy_profile", {}),
1109:            "preferences": user_context.get("preferences", {}),
1112:    def_process_enterprise_learning(
1113:        self,
1122:        if not self.ai_learning_service:  
1126:            learning_data = {
1133:                "confidence": intent_analysis.get("confidence", 0),
1135:                "performance_score": bot_response.get("performance_score", 0),
1138:            self.ai_learning_service.process_enterprise_interaction(learning_data)
1143:    def _update_performance_metrics(self, response_time: float, success: bool) -> None:  
1145:        if success:
1146:            self.performance_metrics["successful_requests"] += 1
1148:            self.performance_metrics["failed_requests"] += 1
1151:        total_requests = self.performance_metrics["total_requests"]
1152:        current_avg = self.performance_metrics["avg_response_time"]
1154:        self.performance_metrics["avg_response_time"] = (
1158:    def _calculate_performance_score(self, response_data: Dict[str, Any]) -> float:
1161:        total_score = 0.0
1162:        weight_factors = 0.0
1164:        # Factor 1: Confianza de respuesta (peso 30%)
1165:        confidence = response_data.get("confidence", 0.0)
1166:        confidence_score = min(1.0, max(0.0, confidence))* 0.3
1167:        total_score += confidence_score
1168:        weight_factors += 0.3
1171:        data_used = response_data.get("data_used", False)
1172:        if data_used:
1174:            data_completeness = response_data.get("data_completeness", 0)
1175:            data_score = (data_completeness / 100.0) *0.25
1177:            data_score = 0.1* 0.25  # Penalizaci├│n por no usar datos
1178:        total_score += data_score
1179:        weight_factors += 0.25
1182:        response_time = response_data.get("response_time_ms", 5000)
1183:        if response_time <= 1000:
1184:            time_score = 1.0 *0.2
1185:        elif response_time <= 3000:
1186:            time_score = 0.8* 0.2
1187:        elif response_time <= 5000:
1188:            time_score = 0.6 *0.2
1190:            time_score = 0.3* 0.2
1191:        total_score += time_score
1192:        weight_factors += 0.2
1195:        sentiment_analysis = response_data.get("sentiment_analysis")
1196:        if sentiment_analysis:
1197:            sentiment_score = 1.0 *0.15  
1199:            sentiment_score = 0.5* 0.15  
1200:        total_score += sentiment_score
1201:        weight_factors += 0.15
1204:        response_text = response_data.get("response", "")
1205:        response_length = len(response_text)
1206:        if 100 <= response_length <= 1000:
1207:            length_score = 1.0 *0.1
1208:        elif 50 <= response_length < 100 or 1000 < response_length <= 2000:
1209:            length_score = 0.8* 0.1
1210:        elif response_length < 50:
1211:            length_score = 0.4 *0.1
1213:            length_score = 0.6* 0.1
1214:        total_score += length_score
1215:        weight_factors += 0.1
1217:        # Normalizar score final
1218:        final_score = total_score / weight_factors if weight_factors > 0 else 0.5
1219:        return min(1.0, max(0.0, final_score))
1221:    def_get_enterprise_fallback_response(
1222:        self, user_message: str, user_context: Dict[str, Any]
1227:        message_analysis = {
1233:                for word in ["urgente", "rapido", "inmediato", "ya"]
1237:                for term in ["tarifa", "kwh", "factura", "consumo", "energia"]
1242:        data_completeness = user_context.get("data_completeness", 0)
1243:        available_sources = user_context.get("available_sources", [])
1244:        user_name = user_context.get("user_id", "usuario")
1247:        if message_analysis["technical_terms"]:
1248:            base_response = f"Disculpe, {user_name}, estoy experimentando dificultades con el sistema de an├ílisis energ├®tico."
1249:            if data_completeness > 50:
1250:                base_response += " Tengo acceso a parte de sus datos y trabajar├® para proporcionarle una respuesta m├ís completa."
1251:        elif message_analysis["urgency_detected"]:
1252:            base_response = f"Entiendo la urgencia de su consulta, {user_name}. Estoy trabajando para resolver los problemas t├®cnicos lo antes posible."
1253:        elif message_analysis["contains_question"]:
1254:            base_response = f"Lamento no poder responder su pregunta en este momento, {user_name}. Estoy experimentando dificultades t├®cnicas temporales."
1256:            base_response = "Estoy experimentando dificultades t├®cnicas temporales. Por favor, intenta nuevamente en unos momentos."
1260:            "intent": "enterprise_fallback",
1262:            "source": "enterprise_fallback_system",
1263:            "status": "fallback_activated",
1272:    def _get_enterprise_ml_fallback(
1273:        self, user_context: Dict[str, Any]
1278:        data_completeness = user_context.get("data_completeness", 0)
1279:        available_sources = user_context.get("available_sources", [])
1280:        user_name = user_context.get("user_id", "usuario")
1283:        if data_completeness > 60:
1284:            response = f"Disculpe, {user_name}, el sistema de recomendaciones ML est├í temporalmente no disponible. Sin embargo, tengo acceso a {len(available_sources)} fuentes de sus datos para ofrecerle asistencia b├ísica."
1285:        elif data_completeness > 30:
1286:            response = f"El sistema de recomendaciones est├í en mantenimiento, {user_name}. Puedo ayudarle con informaci├│n general mientras se restablece el servicio."
1288:            response = f"El sistema de recomendaciones est├í temporalmente no disponible, {user_name}. Para obtener recomendaciones personalizadas, necesitar├¡amos m├ís informaci├│n de su perfil energ├®tico."
1292:            "intent": "ml_fallback",
1293:            "action": "ml_service_fallback",
1294:            "source": "enterprise_ml_fallback",
1300:                    if data_completeness > 60
1301:                    else "medium" if data_completeness > 30 else "low"
1303:                "fallback_quality": "enhanced" if data_completeness > 30 else "basic",
1307:    def_get_enterprise_gemini_fallback(  
1308:        self, user_message: str, user_context: Dict[str, Any]
1313:        data_completeness = user_context.get("data_completeness", 0)
1314:        available_sources = user_context.get("available_sources", [])
1315:        user_name = user_context.get("user_id", "usuario")
1318:        personalized_response = self._generate_contextual_fallback_response(
1324:            "intent": "gemini_fallback",  
1325:            "action": "gemini_service_fallback",
1326:            "source": "enterprise_gemini_fallback",
1327:            "fallback_metadata": {
1336:    def_generate_contextual_fallback_response(
1337:        self,
1339:        data_completeness: float,
1343:        """­ƒÅó Genera respuesta de fallback contextual empresarial."""
1346:        message_lower = user_message.lower()
1348:        # ­ƒÄ» Respuestas contextuales espec├¡ficas
1349:        if "tarifa" in message_lower or "precio" in message_lower:
1350:            base_response = f"Disculpe, {user_name}, el sistema de comparaci├│n de tarifas est├í temporalmente no disponible."
1351:            if data_completeness > 0.5:
1352:                base_response += " Bas├índome en su perfil energ├®tico, le sugiero consultar proveedores locales mientras restablezco el servicio."
1355:        elif "consumo" in message_lower or "factura" in message_lower:
1356:            base_response = f"Le pido disculpas, {user_name}, el an├ílisis de consumo est├í en mantenimiento."
1357:            if "billing" in available_sources:
1358:                base_response += (
1359:                    " Sus datos de facturaci├│n est├ín disponibles para consulta manual."
1363:        elif "energia" in message_lower or "renovable" in message_lower:
1364:            base_response = f"Estimado {user_name}, el servicio de an├ílisis energ├®tico est├í temporalmente fuera de l├¡nea."
1365:            if data_completeness > 0.7:
1366:                base_response += " Con base en su hist├│rico, puedo proporcionarle recomendaciones b├ísicas una vez restablecido el servicio."
1371:            base_response = f"Disculpe, {user_name}, estoy experimentando dificultades t├®cnicas temporales."
1372:            if len(available_sources) > 2:
1373:                base_response += " Tengo acceso parcial a sus datos para asistirle cuando el sistema se restablezca."
1375:                base_response += " Le recomiendo intentar nuevamente en unos minutos."
1376:                base_response += " Estoy trabajando para resolver el problema y brindarle una respuesta completa."
1380:    def _combine_hybrid_responses(
1381:        self, ml_result: Dict[str, Any], gemini_result: Dict[str, Any]
1384:        ml_response = ml_result.get("response", "")
1385:        gemini_response = gemini_result.get("response", "")
1387:        return f"{ml_response}\n\n­ƒÆí An├ílisis detallado:\n{gemini_response}"
1391:    def_get_energy_profile(self, user_id: str) -> Dict[str, Any]:
1392:        """ÔÜí Obtener perfil energ├®tico del usuario."""
1395:                from app.services.energy_service import EnergyService
1397:                from app.services.energy_service import EnergyService
1399:            energy_service: Any = EnergyService()  # type: ignore
1400:            result = energy_service.get_user_energy_profile(user_id)
1401:            return result if isinstance(result, dict) else {}
1409:            logging.warning("Error obteniendo perfil energ├®tico: %s", e)
1412:    def get_user_analytics(self, user_id: str) -> Dict[str, Any]:
1414:        return self._get_analytics_summary(user_id)
1416:    def _get_analytics_summary(self, user_id: str) -> Dict[str, Any]:
1419:            query = f"""
1424:            FROM `{self.gcp_project_id}.{self.bq_dataset_id}.{self.bq_conversations_table_id}`
1425:            WHERE user_id = @user_id
1426:            AND sender = 'user'
1427:            AND timestamp_utc >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
1428:            AND (JSON_EXTRACT(metadata, '$.deleted') IS NULL OR JSON_EXTRACT(metadata, '$.deleted') = false)
1431:            job_config = bigquery.QueryJobConfig(
1432:                query_parameters=[
1433:                    bigquery.ScalarQueryParameter("user_id", "STRING", user_id),
1437:            if self.bigquery_client is None:
1440:            query_job = self.bigquery_client.query(query, job_config=job_config)
1441:            results = list(query_job.result())
1443:            if results:
1444:                row = results[0]
1450:                        "high" if row.total_conversations > 10 else "medium"
1463:    def_get_user_preferences(self, user_id: str) -> Dict[str, Any]:
1464:        """­ƒæñ Obtener preferencias del usuario."""
1467:                from google.cloud import firestore
1472:            db = firestore.Client(project=self.gcp_project_id)
1474:            user_ref = db.collection("users").document(user_id)
1475:            user_doc = user_ref.get()
1477:            if user_doc.exists:
1478:                return user_doc.to_dict().get("preferences", {})
1485:            logging.warning("Error obteniendo preferencias: %s", e)
1489:    def _get_consumption_history(self, user_id: str) -> Dict[str, Any]:
1493:                from app.services.energy_service import EnergyService
1495:                from .energy_service import EnergyService
1497:            energy_service: Any = EnergyService()  # type: ignore
1498:            result = energy_service.get_consumption_history(user_id)
1499:            return result if isinstance(result, dict) else {}
1510:    def_get_recent_interactions(self, user_id: str) -> Dict[str, Any]:
1513:            query = f"""
1518:                COUNT(*) as frequency
1519:            FROM `{self.gcp_project_id}.{self.bq_dataset_id}.{self.bq_conversations_table_id}`
1520:            WHERE user_id = @user_id
1521:            AND sender = 'bot'
1522:            AND timestamp_utc >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
1523:            AND (JSON_EXTRACT(metadata, '$.deleted') IS NULL OR JSON_EXTRACT(metadata, '$.deleted') = false)
1525:            ORDER BY frequency DESC
1529:            job_config = bigquery.QueryJobConfig(
1530:                query_parameters=[
1531:                    bigquery.ScalarQueryParameter("user_id", "STRING", user_id),
1535:            if self.bigquery_client is None:
1538:            query_job = self.bigquery_client.query(query, job_config=job_config)
1539:            results = list(query_job.result())
1541:            interactions = []
1542:            for row in results:
1548:                        "frequency": row.frequency,
1563:    def_calculate_ml_performance_score(self, ml_response: Dict[str, Any]) -> float:
1566:        total_score = 0.0
1567:        weight_factors = 0.0
1570:        recommendations = ml_response.get("recommendations", [])
1571:        if recommendations:
1573:            rec_count = len(recommendations) if isinstance(recommendations, list) else 1
1574:            if rec_count >= 3:
1575:                rec_score = 1.0* 0.4
1576:            elif rec_count >= 2:
1577:                rec_score = 0.8 *0.4
1578:            elif rec_count >= 1:
1579:                rec_score = 0.6* 0.4
1581:                rec_score = 0.2 *0.4
1583:            rec_score = 0.1* 0.4
1584:        total_score += rec_score
1585:        weight_factors += 0.4
1587:        # Factor 2: Confianza del modelo ML (peso 30%)
1588:        confidence = ml_response.get("confidence", 0.0)
1589:        confidence_score = min(1.0, max(0.0, confidence)) *0.3
1590:        total_score += confidence_score
1591:        weight_factors += 0.3
1594:        savings = ml_response.get("potential_savings", 0)
1595:        if savings > 0:
1597:            savings_normalized = min(1.0, savings / 200.0)
1598:            savings_score = savings_normalized* 0.2
1600:            savings_score = 0.1 *0.2
1601:        total_score += savings_score
1602:        weight_factors += 0.2
1605:        data_points = ml_response.get("data_points_used", 0)
1606:        if data_points >= 5:
1607:            data_score = 1.0* 0.1
1608:        elif data_points >= 3:
1609:            data_score = 0.8 *0.1
1610:        elif data_points >= 1:
1611:            data_score = 0.6* 0.1
1613:            data_score = 0.3 *0.1
1614:        total_score += data_score
1615:        weight_factors += 0.1
1617:        # Normalizar score final
1618:        final_score = total_score / weight_factors if weight_factors > 0 else 0.4
1619:        return min(1.0, max(0.2, final_score))
1621:    def _calculate_gemini_performance_score(
1622:        self, gemini_response: Dict[str, Any]
1623:    ) -> float:
1626:        total_score = 0.0
1627:        weight_factors = 0.0
1630:        response_text = gemini_response.get("response", "")
1631:        response_length = len(response_text)
1632:        if 200 <= response_length <= 800:
1633:            length_score = 1.0* 0.25  # Longitud ├│ptima para explicaciones energ├®ticas
1634:        elif 100 <= response_length < 200 or 800 < response_length <= 1200:
1635:            length_score = 0.8 *0.25
1636:        elif 50 <= response_length < 100 or 1200 < response_length <= 1500:
1637:            length_score = 0.6* 0.25
1638:        elif response_length < 50:
1639:            length_score = 0.3 *0.25  # Respuesta muy corta
1641:            length_score = 0.4* 0.25  # Respuesta muy larga
1642:        total_score += length_score
1643:        weight_factors += 0.25
1646:        sentiment = gemini_response.get("sentiment")
1647:        if sentiment:
1648:            sentiment_confidence = gemini_response.get("sentiment_confidence", 0.5)
1649:            sentiment_score = min(1.0, sentiment_confidence) *0.25
1651:            sentiment_score = 0.4* 0.25  
1652:        total_score += sentiment_score
1653:        weight_factors += 0.25
1656:        context_used = gemini_response.get("context_used", False)
1657:        personalization_level = gemini_response.get("personalization_level", "none")
1658:        if context_used and personalization_level == "high":
1659:            context_score = 1.0 *0.2
1660:        elif context_used and personalization_level == "medium":
1661:            context_score = 0.8* 0.2
1662:        elif context_used:
1663:            context_score = 0.6 *0.2
1665:            context_score = 0.3* 0.2
1666:        total_score += context_score
1667:        weight_factors += 0.2
1670:        energy_terms = [
1672:            "tarifa",
1676:            "factura",
1679:        energy_terms_count = sum(
1680:            1 for term in energy_terms if term in response_text.lower()
1682:        if energy_terms_count >= 3:
1683:            technical_score = 1.0 *0.15  
1684:        elif energy_terms_count >= 2:
1685:            technical_score = 0.8* 0.15  
1686:        elif energy_terms_count >= 1:
1687:            technical_score = 0.6 *0.15  
1689:            technical_score = 0.4* 0.15  
1690:        total_score += technical_score
1691:        weight_factors += 0.15
1694:        response_time = gemini_response.get("response_time_ms", 3000)
1695:        if response_time <= 2000:
1696:            time_score = 1.0 *0.15
1697:        elif response_time <= 4000:
1698:            time_score = 0.8* 0.15
1699:        elif response_time <= 6000:
1700:            time_score = 0.6 *0.15
1702:            time_score = 0.4* 0.15
1703:        total_score += time_score
1704:        weight_factors += 0.15
1706:        # Normalizar score final
1707:        final_score = total_score / weight_factors if weight_factors > 0 else 0.5
1708:        return min(1.0, max(0.3, final_score))
1710:    def _enhance_response_enterprise(
1711:        self,
1717:        enhanced_response = bot_response.copy()
1720:        data_completeness = user_context.get("data_completeness", 0)
1721:        if data_completeness < 50:
1722:            suggestions = self._generate_enterprise_suggestions(user_context)
1723:            if suggestions:
1724:                enhanced_response["enterprise_suggestions"] = suggestions
1726:        # A├▒adir informaci├│n de contexto
1727:        enhanced_response["context_quality"] = {
1730:            "personalization_level": "high" if data_completeness > 60 else "medium",
1734:        enhanced_response["intent_analysis"] = {
1737:            "confidence": intent_analysis.get("confidence", 0.0),
1748:    def _generate_enterprise_suggestions(
1749:        self, user_context: Dict[str, Any]
1752:        suggestions = []
1753:        missing_data = user_context.get("missing_critical_data", [])
1755:        if "energy_profile" in missing_data:
1757:                "Completa tu perfil energ├®tico para recomendaciones personalizadas"
1760:        if "invoice_data" in missing_data:
1761:            suggestions.append("Sube tu ├║ltima factura para an├ílisis detallado")
1763:        if "consumption" in missing_data:
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\Y DOCUMENTACION\MINISERVICIOS_SCRIPS\BOT APY>
IPS\BOT APY> findstr /N "conversations_table_id" "c:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\expert_bot_api_COPY\app\services\chat_service.py"
72:        self.bq_conversations_table_id = current_app.config.get(
243:        self._log_to_bigquery_enterprise(self.bq_conversations_table_id, [row])
897:            FROM `{self.gcp_project_id}.{self.bq_dataset_id}.{self.bq_conversations_table_id}`
958:            UPDATE `{self.gcp_project_id}.{self.bq_dataset_id}.{self.bq_conversations_table_id}`
1424:            FROM `{self.gcp_project_id}.{self.bq_dataset_id}.{self.bq_conversations_table_id}`
1519:            FROM `{self.gcp_project_id}.{self.bq_dataset_id}.{self.bq_conversations_table_id}`
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\Y DOCUMENTACION\MINISERVICIOS_SCRIPS\BOT APY>
servicios\expert_bot_api_COPY\app\services\chat_service.py"
75:        self.bq_feedback_table_id = current_app.config.get(
270:        return self._log_to_bigquery_enterprise(self.bq_feedback_table_id, [row])
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\Y DOCUMENTACION\MINISERVICIOS_SCRIPS\BOT APY>
rwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\energy_ia_api_COPY\app\chatbot_routes.py"
38:        self.conversations_table = current_app.config["BQ_CONVERSATIONS_TABLE_ID"]
601:        FROM `{current_app.config['GCP_PROJECT_ID']}.{current_app.config['BQ_DATASET_ID']}.{current_app.config['BQ_CONVERSATIONS_TABLE_ID']}`
670:            UPDATE `{current_app.config['GCP_PROJECT_ID']}.{current_app.config['BQ_DATASET_ID']}.{current_app.config['BQ_CONVERSATIONS_TABLE_ID']}`
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\Y DOCUMENTACION\MINISERVICIOS_SCRIPS\BOT APY>
2\SmarWatt_2\backend\sevicio chatbot\servicios\energy_ia_api_COPY\app\chatbot_routes.py"
13:from google.cloud import bigquery
23:logging.basicConfig(level=logging.INFO)
24:logger = logging.getLogger(__name__)
27:chatbot_bp = Blueprint("chatbot_routes", __name__)
34:        self.chat_service = get_enterprise_chat_service()
35:        self.bq_client = bigquery.Client()  
36:        self.project_id = current_app.config["GCP_PROJECT_ID"]
37:        self.dataset_id = current_app.config["BQ_DATASET_ID"]
38:        self.conversations_table = current_app.config["BQ_CONVERSATIONS_TABLE_ID"]
39:        self.expert_bot_url = current_app.config.get(
46:        self, user_token: str, timeout: int = 5
50:            headers = {"Authorization": f"Bearer {user_token}"}
53:            response = requests.get(
55:                headers=headers,
56:                timeout=timeout,
59:            if response.status_code == 200:
60:                profile_data = response.json().get("data", {})
64:            elif response.status_code == 404:
86:        last_invoice = profile_data.get("last_invoice_data", {})
89:        user_name = profile_data.get("name", "")
92:        context = {
120:        context_parts = []
140:        household_info = []
168:        score = 0
172:            score += 10
174:            score += 10
176:            score += 10
179:        last_invoice = profile_data.get("last_invoice_data", {})
181:            score += 25
183:            score += 25
185:            score += 20
191:        sources = []
205:            headers = {"Authorization": f"Bearer {user_token}"}
206:            response = requests.get(
208:                headers=headers,
209:                timeout=3,
212:            if response.status_code == 200:
213:                basic_data = response.json().get("data", {})
233:            user_id = self._extract_user_id_from_token(user_token)
237:            query = f"""
245:                WHERE user_id = @user_id
251:            job_config = bigquery.QueryJobConfig(
252:                query_parameters=[
253:                    bigquery.ScalarQueryParameter("user_id", "STRING", user_id),
257:            query_job = self.bq_client.query(query, job_config=job_config)
258:            results = list(query_job.result())
261:                row = results[0]
262:                context_data = json.loads(row.context_data) if row.context_data else {}
285:            decoded = jwt.decode(token, options={"verify_signature": False})
306:            context_string = user_context.get("context_string", "")
313:                context_message = {"role": "user", "parts": [{"text": context_string}]}
317:            result = self.chat_service.send_message(
318:                user_message=user_message,
319:                user_context=user_context,
320:                chat_history=chat_history,
324:            result["context_info"] = {
341:            table_id = f"{self.project_id}.{self.dataset_id}.{self.conversations_table}"  
342:            table = self.bq_client.get_table(table_id)
344:            log_data = {
368:            headers = {"Authorization": f"Bearer {token}"}
369:            payload = {
375:            response = requests.post(
377:                json=payload,
378:                headers=headers,
379:                timeout=10,
382:            if response.status_code == 200:
396:chat_service = None
403:        chat_service = EnterpriseChatbotService()
407:# === ENDPOINTS EMPRESARIALES ===
410:@chatbot_bp.route("/message", methods=["POST"])
414:    start_time = time.time()
418:        json_data = request.get_json()
422:        user_message = json_data["message"]
423:        chat_history = json_data.get("history", [])
424:        user_id = g.user.get("uid")
429:        service = get_chat_service()
432:        user_context = service.get_user_context_robust(g.token)
435:        result = service.send_message_with_context(
440:        response_time = (time.time() - start_time) *1000
443:        conversation_data = {
454:        result["meta"] = {
490:@chatbot_bp.route("/message/v2", methods=["POST"])
494:    start_time = time.time()
497:        json_data = request.get_json()
501:        user_message = json_data["message"]
502:        chat_history = json_data.get("history", [])
503:        user_context = json_data.get("user_context", {})  # Contexto directo
504:        user_id = g.user.get("uid")
507:        service = get_chat_service()
511:            user_context = service.get_user_context_robust(g.token)
514:        result = service.send_message_with_context(
519:        response_time = (time.time() - start_time)* 1000
520:        result["meta"] = {
539:@chatbot_bp.route("/cross-service", methods=["POST"])
544:        json_data = request.get_json()
548:        user_id = g.user.get("uid")
549:        message = json_data["message"]
550:        source_service = json_data.get("source", "unknown")
553:        service = get_chat_service()
556:        if source_service == "expert_bot_api":
558:            user_context = service.get_user_context_robust(g.token)
559:            result = service.send_message_with_context(message, [], user_context)
562:            result = service.communicate_with_expert_bot(user_id, message, g.token)
584:@chatbot_bp.route("/conversations", methods=["GET"])
589:        user_id = g.user.get("uid")
590:        limit = request.args.get("limit", 50, type=int)
593:        query = f"""
602:        WHERE user_id = @user_id
607:        job_config = bigquery.QueryJobConfig(
608:            query_parameters=[

  791:                            if "bigquery" not in str(health_status["issues"])
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\Y DOCUMENTACION\MINISERVICIOS_SCRIPS\BOT APY> gcloud alpha bq tables describe conversations_log --dataset=smartwatt_data --format="value(schema.fields[].name)"
conversation_id;message_id;user_id;timestamp_utc;sender;message_text;intent_detected;bot_action;sentiment
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\Y DOCUMENTACION\MINISERVICIOS_SCRIPS\BOT APY>
PS\BOT APY> gcloud alpha bq tables describe feedback_log --dataset=smartwatt_data --format="table(schema.fields[].name, schema.fields[].type, schema.fields[].mode)"
NAME

    TYPE                                       
                       MODE
['feedback_id', 'user_id', 'recommendation_type', 'feedback_useful', 'comments', 'submitted_at']  ['STRING', 'STRING', 'STRING', 'BOOLEAN', 'STRING', 'TIMESTAMP']  ['REQUIRED', 'REQUIRED', 'REQUIRED', 'REQUIRED', None, 'REQUIRED']
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\Y DOCUMENTACION\MINISERVICIOS_SCRIPS\BOT APY>
onversations_log --dataset=smartwatt_data --format="table(schema.fields[].name, schema.fields[].type, schema.fields[].mode)"
NAME

                                         TYPE                                                 
                                          MODE 
['conversation_id', 'message_id', 'user_id', 'timestamp_utc', 'sender', 'message_text', 'intent_detected', 'bot_action', 'sentiment']  ['STRING', 'STRING', 'STRING', 'TIMESTAMP', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING']  ['REQUIRED', 'REQUIRED', 'REQUIRED', 'REQUIRED', 'REQUIRED', 'REQUIRED', None, None, None]
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\Y DOCUMENTACION\MINISERVICIOS_SCRIPS\BOT APY>
