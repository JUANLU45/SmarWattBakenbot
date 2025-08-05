PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\energy_ia_api_COPY> gcloud logging read 'resource.type="cloud_run_revision" AND resource.labels.service_name="energy-ia-api" AND timestamp>="2025-01-03T13:00:00+00:00"' --limit=50 --format="table(timestamp,severity,textPayload)" --project=smatwatt
TIMESTAMP SEVERITY TEXT_PAYLOAD
2025-08-03T12:38:03.745587Z 169.254.169.126 - - [03/Aug/2025:12:38:03 +0000] "POST /api/v1/chatbot/message/v2 HTTP/1.1" 200 24180 "<https://smarwatt.com/>" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
2025-08-03T12:38:03.744849Z 2025-08-03 12:38:03,745 - app - INFO - ? RESPONSE [req_1754224667] 200 - 16.122s
2025-08-03T12:38:03.744153Z 2025-08-03 12:38:03,744 - root - INFO - ?? Pregunta general sin necesidad de recomendaciones: 'Hola....'
2025-08-03T12:38:03.743561Z 2025-08-03 12:38:03,743 - root - INFO - ? Patrones de aprendizaje actualizados para usuario
2025-08-03T12:38:03.743557Z 2025-08-03 12:38:03,743 - root - INFO - ? Interacci?n empresarial registrada: 74149bf2-4858-4c6c-a803-7ac2e7aec3b3
2025-08-03T12:38:03.743546Z 2025-08-03 12:38:03,743 - root - ERROR - ? Error insertando en BigQuery: [{'index': 0, 'errors': [{'reason': 'invalid', 'location': 'context_completeness', 'debugInfo': '', 'message': 'Cannot convert value to integer (bad value): medium'}]}]
2025-08-03T12:38:03.632004Z 2025-08-03 12:38:03,632 - root - INFO - ? Streaming exitoso - Respuesta: 1130 chars
2025-08-03T12:38:01.433906Z 2025-08-03 12:38:01,434 - root - INFO - ?? Pregunta general sin necesidad de recomendaciones: 'Hola....'
2025-08-03T12:37:49.542001Z 2025-08-03 12:37:49,542 - root - INFO - ? Nueva sesi?n de chat empresarial iniciada
2025-08-03T12:37:49.539987Z 2025-08-03 12:37:49,540 - app.chatbot_routes - INFO - ? Contexto meteorol?gico obtenido para 03,ES
2025-08-03T12:37:49.511754Z 2025-08-03 12:37:49,512 - app.services.vertex_ai_service - INFO - ? EnterpriseVertexAIService inicializado
2025-08-03T12:37:49.511233Z 2025-08-03 12:37:49,511 - app.services.vertex_ai_service - INFO - ? Cliente Vertex AI empresarial inicializado
2025-08-03T12:37:49.456400Z 2025-08-03 12:37:49,457 - app.services.vertex_ai_service - INFO - ? Cliente BigQuery empresarial inicializado
2025-08-03T12:37:47.869880Z 2025-08-03 12:37:47,870 - app.chatbot_routes - INFO - ? EnterpriseChatbotService inicializado
2025-08-03T12:37:47.864370Z 2025-08-03 12:37:47,864 - app.services.generative_chat_service - INFO - ? Factory function: EnterpriseGenerativeChatService inicializado
2025-08-03T12:37:47.864301Z 2025-08-03 12:37:47,864 - root - INFO - ? EnterpriseGenerativeChatService inicializado con IA avanzada
2025-08-03T12:37:47.864253Z 2025-08-03 12:37:47,864 - root - INFO - ? Cliente BigQuery empresarial inicializado
2025-08-03T12:37:47.859107Z 2025-08-03 12:37:47,859 - root - INFO - ? Modelo Gemini empresarial inicializado
2025-08-03T12:37:47.855831Z 2025-08-03 12:37:47,855 - root - WARNING - ?? AI Learning Service no disponible - usando an?lisis b?sico
2025-08-03T12:37:47.855419Z 2025-08-03 12:37:47,855 - root - WARNING - ?? AI Learning Service no disponible: No module named 'app.services.ai_learning_service'
2025-08-03T12:37:47.854994Z 2025-08-03 12:37:47,855 - app.services.enterprise_links_service - INFO - ? EnterpriseLinkService singleton inicializado
2025-08-03T12:37:47.854896Z 2025-08-03 12:37:47,855 - app.services.enterprise_links_service - INFO - ? Enterprise Link Service inicializado correctamente
2025-08-03T12:37:47.623082Z 2025-08-03 12:37:47,623 - app - INFO - ? REQUEST [req_1754224667] POST /api/v1/chatbot/message/v2  
2025-08-03T12:37:47.618212Z INFO
2025-08-03T12:37:47.571847Z 169.254.169.126 - - [03/Aug/2025:12:37:47 +0000] "OPTIONS /api/v1/chatbot/message/v2 HTTP/1.1" 200 0 "<https://smarwatt.com/>" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
2025-08-03T12:37:47.550608Z 2025-08-03 12:37:47,550 - app - INFO - ? RESPONSE [req_1754224667] 200 - 0.001s
2025-08-03T12:37:47.549642Z 2025-08-03 12:37:47,550 - app - INFO - ? REQUEST [req_1754224667] OPTIONS /api/v1/chatbot/message/v2
2025-08-03T12:37:47.505600Z INFO
2025-08-03T12:36:47.833023Z 169.254.169.126 - - [03/Aug/2025:12:36:47 +0000] "POST /api/v1/chatbot/message/v2 HTTP/1.1" 200 18015 "<https://smarwatt.com/>" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
2025-08-03T12:36:47.832072Z 2025-08-03 12:36:47,833 - app - INFO - ? RESPONSE [req_1754224597] 200 - 10.029s
2025-08-03T12:36:47.831502Z 2025-08-03 12:36:47,832 - root - INFO - ?? Pregunta general sin necesidad de recomendaciones: 'Hola....'
2025-08-03T12:36:47.830719Z 2025-08-03 12:36:47,831 - root - INFO - ? Patrones de aprendizaje actualizados para usuario
2025-08-03T12:36:47.830562Z 2025-08-03 12:36:47,831 - root - INFO - ? Interacci?n empresarial registrada: a1e728de-6715-4fbf-bea0-e58ecce9e3ad
2025-08-03T12:36:47.830536Z 2025-08-03 12:36:47,831 - root - ERROR - ? Error insertando en BigQuery: [{'index': 0, 'errors': [{'reason': 'invalid', 'location': 'context_completeness', 'debugInfo': '', 'message': 'Cannot convert value to integer (bad value): medium'}]}]
2025-08-03T12:36:47.622085Z 2025-08-03 12:36:47,623 - root - INFO - ? Streaming exitoso - Respuesta: 1224 chars
2025-08-03T12:36:44.979921Z 2025-08-03 12:36:44,981 - root - INFO - ?? Pregunta general sin necesidad de recomendaciones: 'Hola....'
2025-08-03T12:36:39.624731Z 2025-08-03 12:36:39,626 - root - INFO - ? Nueva sesi?n de chat empresarial iniciada
2025-08-03T12:36:39.622596Z 2025-08-03 12:36:39,623 - app.chatbot_routes - INFO - ? Contexto meteorol?gico obtenido para 03,ES
2025-08-03T12:36:39.554975Z 2025-08-03 12:36:39,556 - app.services.vertex_ai_service - INFO - ? EnterpriseVertexAIService inicializado
2025-08-03T12:36:39.554475Z 2025-08-03 12:36:39,555 - app.services.vertex_ai_service - INFO - ? Cliente Vertex AI empresarial inicializado
2025-08-03T12:36:39.453887Z 2025-08-03 12:36:39,455 - app.services.vertex_ai_service - INFO - ? Cliente BigQuery empresarial inicializado
2025-08-03T12:36:38.152733Z 2025-08-03 12:36:38,154 - app.chatbot_routes - INFO - ? EnterpriseChatbotService inicializado
2025-08-03T12:36:38.145775Z 2025-08-03 12:36:38,147 - app.services.generative_chat_service - INFO - ? Factory function: EnterpriseGenerativeChatService inicializado
2025-08-03T12:36:38.145726Z 2025-08-03 12:36:38,147 - root - INFO - ? EnterpriseGenerativeChatService inicializado con IA avanzada
2025-08-03T12:36:38.145642Z 2025-08-03 12:36:38,147 - root - INFO - ? Cliente BigQuery empresarial inicializado
2025-08-03T12:36:38.139390Z 2025-08-03 12:36:38,141 - root - INFO - ? Modelo Gemini empresarial inicializado
2025-08-03T12:36:38.136016Z 2025-08-03 12:36:38,137 - root - WARNING - ?? AI Learning Service no disponible - usando an?lisis b?sico
2025-08-03T12:36:38.135958Z 2025-08-03 12:36:38,137 - root - WARNING - ?? AI Learning Service no disponible: No module named 'app.services.ai_learning_service'
2025-08-03T12:36:38.135657Z 2025-08-03 12:36:38,137 - app.services.enterprise_links_service - INFO - ? EnterpriseLinkService singleton inicializado
2025-08-03T12:36:38.135609Z 2025-08-03 12:36:38,137 - app.services.enterprise_links_service - INFO - ? Enterprise Link Service inicializado correctamente
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\energy_ia_api_COPY>

AND resource.labels.service_name="expert-bot-api" AND timestamp>="2025-01-03T13:00:00+00:00"' --limit=50 --format="table(timestamp,severity,textPayload)" --project=smatwatt
TIMESTAMP SEVERITY TEXT_PAYLOAD
2025-08-03T12:53:12.632590Z [2025-08-03 12:53:12 +0000] [8] [INFO] Worker exiting (pid: 8)
2025-08-03T12:53:12.632586Z [2025-08-03 12:53:12 +0000] [9] [INFO] Worker exiting (pid: 9)
2025-08-03T12:53:12.632560Z [2025-08-03 12:53:12 +0000] [10] [INFO] Worker exiting (pid: 10)
2025-08-03T12:38:04.316971Z 169.254.169.126 - - [03/Aug/2025:12:38:04 +0000] "POST /api/v1/chatbot/new-conversation HTTP/1.1" 200 395 "<https://smarwatt.com/>" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
2025-08-03T12:38:04.316603Z 2025-08-03 12:38:04,316 - expert_bot_api.routes - INFO - Nueva conversaci?n creada para usuario: 56bE1dNrjef8kO0Erg1qKQytKAq2, nueva ID: 0fea0b3e-2648-4d86-bc19-8c7f806fe666
2025-08-03T12:38:04.315720Z 2025-08-03 12:38:04,316 - app.services.chat_service - INFO - ? Nueva conversaci?n creada - ID: 0fea0b3e-2648-4d86-bc19-8c7f806fe666 - Usuario: 56bE1dNrjef8kO0Erg1qKQytKAq2 - Anterior: ninguna
2025-08-03T12:38:04.315637Z 2025-08-03 12:38:04,316 - root - INFO - ? Datos insertados correctamente en conversations_log
2025-08-03T12:38:04.221091Z 2025-08-03 12:38:04,222 - root - INFO - ? Servicio de enlaces deshabilitado en Expert Bot para evitar redundancia
2025-08-03T12:38:04.220911Z 2025-08-03 12:38:04,221 - expert_bot_api.routes - INFO - Creando nueva conversaci?n para usuario: 56bE1dNrjef8kO0Erg1qKQytKAq2, conversaci?n actual: None
2025-08-03T12:38:04.051851Z 2025-08-03 12:38:04,052 - expert_bot_api.routes - INFO - Acceso an?nimo a chat_routes.create_new_conversation
2025-08-03T12:38:04.051688Z 2025-08-03 12:38:04,052 - expert_bot_api - INFO - Request: POST /api/v1/chatbot/new-conversation - IP: 169.254.169.126
2025-08-03T12:38:04.047530Z INFO
2025-08-03T12:38:03.998614Z 169.254.169.126 - - [03/Aug/2025:12:38:03 +0000] "OPTIONS /api/v1/chatbot/new-conversation HTTP/1.1" 200 0 "<https://smarwatt.com/>" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
2025-08-03T12:38:03.998058Z 2025-08-03 12:38:03,999 - expert_bot_api.routes - INFO - Acceso an?nimo a chat_routes.create_new_conversation
2025-08-03T12:38:03.998044Z 2025-08-03 12:38:03,998 - expert_bot_api - INFO - Request: OPTIONS /api/v1/chatbot/new-conversation - IP: 169.254.169.126
2025-08-03T12:38:03.992784Z INFO
2025-08-03T12:37:49.442762Z 169.254.169.126 - - [03/Aug/2025:12:37:49 +0000] "GET /api/v1/energy/users/profile HTTP/1.1" 200 1540 "-" "python-requests/2.32.4"
2025-08-03T12:37:49.441682Z 2025-08-03 12:37:49,442 - expert_bot_api.energy_routes - INFO - Perfil de usuario obtenido correctamente: 56bE1dNrjef8kO0Erg1qKQytKAq2
2025-08-03T12:37:49.441609Z 2025-08-03 12:37:49,442 - root - INFO - ? Perfil empresarial obtenido desde Firestore user_profiles_enriched para 56bE1dNrjef8kO0Erg1qKQytKAq2
2025-08-03T12:37:49.441531Z 2025-08-03 12:37:49,442 - root - WARNING - No se pudieron obtener documentos para 56bE1dNrjef8kO0Erg1qKQytKAq2: no row field 'extraction_status'
2025-08-03T12:37:48.579817Z Job ID: 0b560a5d-863e-4671-8ff5-94d66c514a5b
2025-08-03T12:37:48.579813Z Location: EU
2025-08-03T12:37:48.579798Z 2025-08-03 12:37:48,580 - root - ERROR - Error consultando perfil en BigQuery: 400 Unrecognized name: last_invoice_data at [19:21]; reason: invalidQuery, location: query, message: Unrecognized name: last_invoice_data at [19:21]
2025-08-03T12:37:48.113553Z 2025-08-03 12:37:48,114 - root - INFO - ? EnergyService Empresarial inicializado correctamente
2025-08-03T12:37:48.113216Z 2025-08-03 12:37:48,114 - root - INFO - ? Servicios GCP inicializados - Intento 1
2025-08-03T12:37:47.902680Z 2025-08-03 12:37:47,904 - expert_bot_api.energy_routes - INFO - Acceso an?nimo a energy endpoint: expert_energy_routes.get_user_profile
2025-08-03T12:37:47.902499Z 2025-08-03 12:37:47,903 - expert_bot_api - INFO - Request: GET /api/v1/energy/users/profile - IP: 169.254.169.126
2025-08-03T12:37:47.891272Z INFO
2025-08-03T12:36:48.891291Z 169.254.169.126 - - [03/Aug/2025:12:36:48 +0000] "POST /api/v1/chatbot/new-conversation HTTP/1.1" 200 395 "<https://smarwatt.com/>" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
2025-08-03T12:36:48.889017Z 2025-08-03 12:36:48,890 - expert_bot_api.routes - INFO - Nueva conversaci?n creada para usuario: 56bE1dNrjef8kO0Erg1qKQytKAq2, nueva ID: 8dd7102c-b4f2-4332-8596-6362990776ce
2025-08-03T12:36:48.889010Z 2025-08-03 12:36:48,890 - app.services.chat_service - INFO - ? Nueva conversaci?n creada - ID: 8dd7102c-b4f2-4332-8596-6362990776ce - Usuario: 56bE1dNrjef8kO0Erg1qKQytKAq2 - Anterior: ninguna
2025-08-03T12:36:48.888547Z 2025-08-03 12:36:48,889 - root - INFO - ? Datos insertados correctamente en conversations_log
2025-08-03T12:36:48.813340Z 2025-08-03 12:36:48,814 - root - INFO - ? Sistema de Aprendizaje Autom?tico Empresarial inicializado
2025-08-03T12:36:48.812889Z 2025-08-03 12:36:48,814 - root - INFO - ? AILearningService Empresarial inicializado correctamente
2025-08-03T12:36:48.812284Z 2025-08-03 12:36:48,813 - root - INFO - ? Tabla AI empresarial ai_business_metrics ya existe
2025-08-03T12:36:48.696608Z 2025-08-03 12:36:48,697 - root - INFO - ? Tabla AI empresarial ai_predictions ya existe
2025-08-03T12:36:48.581050Z 2025-08-03 12:36:48,582 - root - INFO - ? Tabla AI empresarial ai_user_patterns ya existe
2025-08-03T12:36:48.482726Z 2025-08-03 12:36:48,483 - root - INFO - ? Tabla AI empresarial ai_sentiment_analysis ya existe
2025-08-03T12:36:48.362341Z 2025-08-03 12:36:48,363 - root - INFO - ? Cliente BigQuery AI inicializado - Intento 1
2025-08-03T12:36:48.354145Z 2025-08-03 12:36:48,354 - root - INFO - ? Cliente BigQuery inicializado correctamente - Intento 1  
2025-08-03T12:36:48.345029Z 2025-08-03 12:36:48,346 - root - INFO - ? Servicio de enlaces deshabilitado en Expert Bot para evitar redundancia
2025-08-03T12:36:48.343678Z 2025-08-03 12:36:48,344 - expert_bot_api.routes - INFO - Creando nueva conversaci?n para usuario: 56bE1dNrjef8kO0Erg1qKQytKAq2, conversaci?n actual: None
2025-08-03T12:36:48.138761Z 2025-08-03 12:36:48,139 - expert_bot_api.routes - INFO - Acceso an?nimo a chat_routes.create_new_conversation
2025-08-03T12:36:48.138049Z 2025-08-03 12:36:48,138 - expert_bot_api - INFO - Request: POST /api/v1/chatbot/new-conversation - IP: 169.254.169.126
2025-08-03T12:36:48.118109Z INFO
2025-08-03T12:36:48.075799Z 169.254.169.126 - - [03/Aug/2025:12:36:48 +0000] "OPTIONS /api/v1/chatbot/new-conversation HTTP/1.1" 200 0 "<https://smarwatt.com/>" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
2025-08-03T12:36:48.073250Z 2025-08-03 12:36:48,073 - expert_bot_api.routes - INFO - Acceso an?nimo a chat_routes.create_new_conversation
2025-08-03T12:36:48.072107Z 2025-08-03 12:36:48,072 - expert_bot_api - INFO - Request: OPTIONS /api/v1/chatbot/new-conversation - IP: 169.254.169.126
2025-08-03T12:36:48.050750Z INFO
2025-08-03T12:36:39.441247Z 169.254.169.126 - - [03/Aug/2025:12:36:39 +0000] "GET /api/v1/energy/users/profile HTTP/1.1" 200 1540 "-" "python-requests/2.32.4"
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\energy_ia_api_COPY>
