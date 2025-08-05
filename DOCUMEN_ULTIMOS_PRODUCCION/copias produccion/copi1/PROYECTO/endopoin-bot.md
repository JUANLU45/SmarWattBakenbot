ENDPOINT 1: /api/v1/chatbot/message/v2
🎯 PROPÓSITO EMPRESARIAL:
Función Principal: Envío de mensajes al chatbot con IA generativa empresarial
Tipo: POST - Envía una pregunta del usuario y recibe respuesta del chatbot
Ubicación: chatbot_routes.py línea 711
🔧 PROCESAMIENTO TÉCNICO DETALLADO:
Entrada de Datos:

message: Pregunta/mensaje del usuario
history: Historial de conversación (opcional)
user_context: Contexto del usuario (opcional)
Proceso Interno:

Obtiene contexto del usuario llamando a Expert Bot API /api/v1/energy/users/profile
Consulta modelo Gemini AI con el mensaje enriquecido
Añade enlaces inteligentes automáticamente en la respuesta
Registra interacción en BigQuery tabla conversations_log
Aplica análisis de sentiment en tiempo real
Datos que Utiliza del Usuario:

Consumo energético (monthly_consumption_kwh)
Potencia contratada (contracted_power_kw)
Última factura (last_invoice)
Datos de documentos subidos
Perfil energético completo de BigQuery
Respuesta:

{  "response_text": "Respuesta con IA + enlaces inteligentes",  "chat_history": [],  "enterprise_metrics": {    "context_used": true,    "ai_learning_applied": true,    "sentiment_score": 0.85,    "response_time": 1.2,    "expert_bot_consulted": true  }}
📊 ENDPOINT 2: /api/v1/chatbot/conversations
🎯 PROPÓSITO EMPRESARIAL:
Función Principal: Obtener historial de conversaciones del usuario
Tipo: GET - Lista todas las conversaciones previas del usuario
Ubicación: chatbot_routes.py línea 804
🔧 PROCESAMIENTO TÉCNICO DETALLADO:
Entrada de Datos:

limit: Número máximo de conversaciones (máx 100)
page: Página de resultados (paginación)
Token de usuario automático
Proceso Interno:

Consulta directa a BigQuery tabla conversations_log
Filtra por user_id del token autenticado
Ordena por timestamp descendente (más recientes primero)
Excluye conversaciones eliminadas (deleted = false)
Query SQL Exacto:

SELECT     conversation_id,    message_text,    response_text,    context_completeness,    response_time_ms,    timestamp_utcFROM `{project_id}.{dataset_id}.conversations_log`WHERE user_id = @user_id   AND (deleted IS NULL OR deleted = false)ORDER BY timestamp_utc DESCLIMIT @limit
Respuesta:

{  "status": "success",  "data": {    "conversations": [      {        "conversation_id": "uuid",        "message_text": "Pregunta del usuario",        "response_text": "Respuesta del chatbot",        "context_completeness": 85,        "response_time_ms": 1200,        "timestamp": "2025-07-24T14:16:59Z"      }    ],    "total_count": 25  }}
⚡ DIFERENCIAS CLAVE MILIMÉTRICAS:
🎯 FUNCIONALIDAD OPUESTA:
/message/v2: CREA nuevas conversaciones
/conversations: LEE conversaciones existentes
🔄 FLUJO DE DATOS:
/message/v2: Usuario → Gemini AI → Expert Bot → BigQuery → Usuario
/conversations: Usuario → BigQuery → Usuario
💾 FUENTES DE DATOS:
/message/v2:
Expert Bot API (user_profiles_enriched)
Modelo Gemini AI
BigQuery (escritura)
/conversations:
Solo BigQuery (conversations_log - lectura)
⚙️ COMPLEJIDAD TÉCNICA:
/message/v2: ALTA - 8 componentes integrados
/conversations: BAJA - Solo consulta SQL
🔗 DEPENDENCIAS EXTERNAS:
/message/v2: Expert Bot API + Gemini AI + BigQuery
/conversations: Solo BigQuery
📈 ANÁLISIS DE RENDIMIENTO:
/message/v2: ~1-3 segundos (AI + contexto)
/conversations: ~200-500ms (solo SQL)
🎯 CASOS DE USO:
/message/v2: Chatear, preguntar, obtener consejos energéticos
/conversations: Ver historial, revisión de conversaciones pasadas
🏢 CONCLUSIÓN EMPRESARIAL: Son endpoints COMPLEMENTARIOS - uno para conversación activa y otro para gestión de histori
Endpoint: GET /api/v1/energy/users/profile
URL Completa: <https://expert-bot-api-1010012211318.europe-west1.run.app/api/v1/energy/users/profile>

Este endpoint devuelve:

✅ Perfil completo del usuario
✅ uploaded_documents - Lista de documentos subidos por el usuario
✅ Datos extraídos de cada documento (kWh, coste, potencia, tarifa)
El método_get_user_documents() consulta BigQuery tabla uploaded_docs y devuelve:

document_id
filename
upload_date
file_type
exue va a: POST /api/v1/

chatbot/new-conversation
Expert Bot API: ✅ SÍ EXISTE - línea 142 en routes.pytracted_kwh
extracted_cost
extracted_power

Endpoint: DELETE /api/v1/chatbot/conversation/{conversation_id}
URL Completa: <https://expert-bot-api-1010012211318.europe-west1.run.app/api/v1/chatbot/conversation/{conversation_id}>
Función: deleteConversation(conversationId) (línea 122)
