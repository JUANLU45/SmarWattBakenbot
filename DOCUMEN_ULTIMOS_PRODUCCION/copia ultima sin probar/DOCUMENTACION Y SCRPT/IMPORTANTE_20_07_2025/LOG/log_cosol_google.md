DEFAULT 2025-07-23T08:45:34.855882Z [2025-07-23 08:45:27 +0000] [10] [INFO] Booting worker with pid: 10
INFO 2025-07-23T08:45:36.009566Z [httpRequest.requestMethod: OPTIONS] [httpRequest.status: 200] [httpRequest.responseSize: 369 B] [httpRequest.latency: 23 ms] [httpRequest.userAgent: Chrome 138.0.0.0] <https://expert-bot-api-1010012211318.europe-west1.run.app/api/v1/chatbot/session/start>
DEFAULT 2025-07-23T08:45:36.028720Z 2025-07-23 08:45:36,029 - expert_bot_api - INFO - Request: OPTIONS /api/v1/chatbot/session/start - IP: 169.254.169.126
DEFAULT 2025-07-23T08:45:36.028926Z 2025-07-23 08:45:36,029 - expert_bot_api.routes - INFO - Acceso anónimo a chat_routes.start_chat_session
DEFAULT 2025-07-23T08:45:36.035486Z 169.254.169.126 - - [23/Jul/2025:08:45:36 +0000] "OPTIONS /api/v1/chatbot/session/start HTTP/1.1" 200 0 "<https://smarwatt.com/>" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
INFO 2025-07-23T08:45:36.089767Z [httpRequest.requestMethod: POST] [httpRequest.status: 200] [httpRequest.responseSize: 419 B] [httpRequest.latency: 3.478 s] [httpRequest.userAgent: Chrome 138.0.0.0] <https://expert-bot-api-1010012211318.europe-west1.run.app/api/v1/chatbot/session/start>
DEFAULT 2025-07-23T08:45:36.093731Z 2025-07-23 08:45:36,094 - expert_bot_api - INFO - Request: POST /api/v1/chatbot/session/start - IP: 169.254.169.126
DEFAULT 2025-07-23T08:45:36.093867Z 2025-07-23 08:45:36,094 - expert_bot_api.routes - INFO - Acceso anónimo a chat_routes.start_chat_session
DEFAULT 2025-07-23T08:45:36.426668Z 2025-07-23 08:45:36,427 - expert_bot_api.routes - INFO - Iniciando sesión de chat para usuario: 56bE1dNrjef8kO0Erg1qKQytKAq2
DEFAULT 2025-07-23T08:45:36.428968Z 2025-07-23 08:45:36,429 - app.services.enterprise_links_service - INFO - 🏢 Enterprise Link Service inicializado correctamente
DEFAULT 2025-07-23T08:45:36.429248Z 2025-07-23 08:45:36,429 - app.services.enterprise_links_service - INFO - 🏢 EnterpriseLinkService singleton inicializado
DEFAULT 2025-07-23T08:45:36.436239Z 2025-07-23 08:45:36,436 - root - INFO - 🏢 Cliente BigQuery inicializado correctamente - Intento 1
DEFAULT 2025-07-23T08:45:36.441251Z 2025-07-23 08:45:36,441 - root - INFO - 🏢 Cliente BigQuery AI inicializado - Intento 1
DEFAULT 2025-07-23T08:45:36.629169Z 2025-07-23 08:45:36,630 - root - INFO - ✅ Tabla AI empresarial ai_sentiment_analysis ya existe
DEFAULT 2025-07-23T08:45:36.782389Z 2025-07-23 08:45:36,783 - root - INFO - ✅ Tabla AI empresarial ai_user_patterns ya existe
DEFAULT 2025-07-23T08:45:36.908393Z 2025-07-23 08:45:36,909 - root - INFO - ✅ Tabla AI empresarial ai_predictions ya existe
DEFAULT 2025-07-23T08:45:36.993606Z 2025-07-23 08:45:36,994 - root - INFO - ✅ Tabla AI empresarial ai_business_metrics ya existe
DEFAULT 2025-07-23T08:45:36.993722Z 2025-07-23 08:45:36,995 - root - INFO - 🏢 AILearningService Empresarial inicializado correctamente
DEFAULT 2025-07-23T08:45:36.993807Z 2025-07-23 08:45:36,995 - root - INFO - 🧠 Sistema de Aprendizaje Automático Empresarial inicializado
DEFAULT 2025-07-23T08:45:37.326908Z 2025-07-23 08:45:37,328 - root - ERROR - Errores en inserción BigQuery - Intento 1: [{'index': 0, 'errors': [{'reason': 'invalid', 'location': 'session_info', 'debugInfo': '', 'message': 'This field: session_info is not a record.'}]}]
DEFAULT 2025-07-23T08:45:38.527530Z 2025-07-23 08:45:38,528 - root - ERROR - Errores en inserción BigQuery - Intento 2: [{'index': 0, 'errors': [{'reason': 'invalid', 'location': 'session_info', 'debugInfo': '', 'message': 'This field: session_info is not a record.'}]}]
DEFAULT 2025-07-23T08:45:39.567833Z 2025-07-23 08:45:39,569 - root - ERROR - Errores en inserción BigQuery - Intento 3: [{'index': 0, 'errors': [{'reason': 'invalid', 'location': 'session_info', 'debugInfo': '', 'message': 'This field: session_info is not a record.'}]}]
DEFAULT 2025-07-23T08:45:39.567921Z 2025-07-23 08:45:39,569 - root - INFO - 🏢 Sesión empresarial iniciada - ID: 1d834a54-f2e8-4c05-865a-f82016e428f3 - Usuario: 56bE1dNrjef8kO0Erg1qKQytKAq2
DEFAULT 2025-07-23T08:45:39.568014Z 2025-07-23 08:45:39,569 - expert_bot_api.routes - INFO - Sesión de chat iniciada correctamente para usuario: 56bE1dNrjef8kO0Erg1qKQytKAq2
DEFAULT 2025-07-23T08:45:39.568925Z 169.254.169.126 - - [23/Jul/2025:08:45:39 +0000] "POST /api/v1/chatbot/session/start HTTP/1.1" 200 219 "<https://smarwatt.com/>" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
INFO 2025-07-23T08:47:04.167497Z [httpRequest.requestMethod: OPTIONS] [httpRequest.status: 200] [httpRequest.responseSize: 351 B] [httpRequest.latency: 4 ms] [httpRequest.userAgent: Chrome 138.0.0.0] <https://expert-bot-api-1010012211318.europe-west1.run.app/api/v1/chatbot/new-conversation>
DEFAULT 2025-07-23T08:47:04.180858Z 2025-07-23 08:47:04,182 - expert_bot_api - INFO - Request: OPTIONS /api/v1/chatbot/new-conversation - IP: 169.254.169.126
DEFAULT 2025-07-23T08:47:04.180923Z 2025-07-23 08:47:04,182 - expert_bot_api.routes - INFO - Acceso anónimo a chat_routes.create_new_conversation
10:45:39.568
169.254.169.126 - - [23/Jul/2025:08:45:39 +0000] "POST /api/v1/chatbot/session/start HTTP/1.1" 200 219 "<https://smarwatt.com/>" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"

{
insertId: "6880a1330008ae5d5a4970fb"
labels: {1}
logName: "projects/smatwatt/logs/run.googleapis.com%2Fstdout"
receiveTimestamp: "2025-07-23T08:45:39.694216762Z"
resource: {2}
textPayload: "169.254.169.126 - - [23/Jul/2025:08:45:39 +0000] "POST /api/v1/chatbot/session/start HTTP/1.1" 200 219 "<https://smarwatt.com/>" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36""
timestamp: "2025-07-23T08:45:39.568925Z"
}
10:47:04.167

OPTIONS

200

351 B

4 ms

Chrome 138.0.0.0
<https://expert-bot-api-1010012211318.europe-west1.run.app/api/v1/chatbot/new-conversation>

{
httpRequest: {11}
insertId: "6880a1880002c7ad57d785d1"
labels: {1}
logName: "projects/smatwatt/logs/run.googleapis.com%2Frequests"
receiveTimestamp: "2025-07-23T08:47:04.185317640Z"
resource: {2}
severity: "INFO"
spanId: "d34ac5638fda4e42"
timestamp: "2025-07-23T08:47:04.167497Z"
trace: "projects/smatwatt/traces/3f2c919ab642feaaa71a1e7a644167ba"
traceSampled: true
}
10:47:04.180
2025-07-23 08:47:04,182 - expert_bot_api - INFO - Request: OPTIONS /api/v1/chatbot/new-conversation - IP: 169.254.169.126
10:47:04.180
2025-07-23 08:47:04,182 - expert_bot_api.routes - INFO - Acceso anónimo a chat_routes.create_new_conversation

{
insertId: "6880a1880002c2bb7ead5551"
labels: {1}
logName: "projects/smatwatt/logs/run.googleapis.com%2Fstdout"
receiveTimestamp: "2025-07-23T08:47:04.182872732Z"
resource: {2}
textPayload: "2025-07-23 08:47:04,182 - expert_bot_api.routes - INFO - Acceso anónimo a chat_routes.create_new_conversation"
timestamp: "2025-07-23T08:47:04.180923Z"
}
10:47:04.181
169.254.169.126 - - [23/Jul/2025:08:47:04 +0000] "OPTIONS /api/v1/chatbot/new-conversation HTTP/1.1" 200 0 "<https://smarwatt.com/>" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"

{
insertId: "6880a1880002c6209ca4e4de"
labels: {1}
logName: "projects/smatwatt/logs/run.googleapis.com%2Fstdout"
receiveTimestamp: "2025-07-23T08:47:04.515938739Z"
resource: {2}
textPayload: "169.254.169.126 - - [23/Jul/2025:08:47:04 +0000] "OPTIONS /api/v1/chatbot/new-conversation HTTP/1.1" 200 0 "<https://smarwatt.com/>" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36""
timestamp: "2025-07-23T08:47:04.181792Z"
}
10:47:04.233

POST

500

392 B

2.615 s

Chrome 138.0.0.0
<https://expert-bot-api-1010012211318.europe-west1.run.app/api/v1/chatbot/new-conversation>
{
httpRequest: {
latency: "2.615866019s"
protocol: "HTTP/1.1"
referer: "<https://smarwatt.com/>"
remoteIp: "88.18.43.60"
requestMethod: "POST"
requestSize: "3331"
requestUrl: "<https://expert-bot-api-1010012211318.europe-west1.run.app/api/v1/chatbot/new-conversation>"
responseSize: "392"
serverIp: "34.143.78.2"
status: 500
userAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
}
insertId: "6880a18a000cfdb0612772ae"
labels: {1}
logName: "projects/smatwatt/logs/run.googleapis.com%2Frequests"
receiveTimestamp: "2025-07-23T08:47:07.182466994Z"
resource: {2}
severity: "ERROR"
spanId: "c408b3c5b7d97be3"
timestamp: "2025-07-23T08:47:04.233881Z"
trace: "projects/smatwatt/traces/fd02c702b101673fa71a1e7a64416814"
}
10:47:04.237
2025-07-23 08:47:04,238 - expert_bot_api - INFO - Request: POST /api/v1/chatbot/new-conversation - IP: 169.254.169.126

{
insertId: "6880a18800039e61fb9d07ed"
labels: {1}
logName: "projects/smatwatt/logs/run.googleapis.com%2Fstdout"
receiveTimestamp: "2025-07-23T08:47:04.515938739Z"
resource: {2}
textPayload: "2025-07-23 08:47:04,238 - expert_bot_api - INFO - Request: POST /api/v1/chatbot/new-conversation - IP: 169.254.169.126"
timestamp: "2025-07-23T08:47:04.237153Z"
}
10:47:04.237
2025-07-23 08:47:04,238 - expert_bot_api.routes - INFO - Acceso anónimo a chat_routes.create_new_conversation
{
insertId: "6880a18800039ebb8aeb756a"
labels: {1}
logName: "projects/smatwatt/logs/run.googleapis.com%2Fstdout"
receiveTimestamp: "2025-07-23T08:47:04.515938739Z"
resource: {2}
textPayload: "2025-07-23 08:47:04,238 - expert_bot_api.routes - INFO - Acceso anónimo a chat_routes.create_new_conversation"
timestamp: "2025-07-23T08:47:04.237243Z"
}
10:47:04.569
2025-07-23 08:47:04,571 - expert_bot_api.routes - INFO - Creando nueva conversación para usuario: 56bE1dNrjef8kO0Erg1qKQytKAq2, conversación actual: None
10:47:04.674
2025-07-23 08:47:04,675 - root - ERROR - Errores en inserción BigQuery - Intento 1: [{'index': 0, 'errors': [{'reason': 'invalid', 'location': 'session_info', 'debugInfo': '', 'message': 'This field: session_info is not a record.'}]}]
{
insertId: "6880a188000a48fe9a71e87a"
labels: {1}
logName: "projects/smatwatt/logs/run.googleapis.com%2Fstdout"
receiveTimestamp: "2025-07-23T08:47:04.850447279Z"
resource: {2}
textPayload: "2025-07-23 08:47:04,675 - root - ERROR - Errores en inserción BigQuery - Intento 1: [{'index': 0, 'errors': [{'reason': 'invalid', 'location': 'session_info', 'debugInfo': '', 'message': 'This field: session_info is not a record.'}]}]"
timestamp: "2025-07-23T08:47:04.674046Z"
}
10:47:05.781
2025-07-23 08:47:05,782 - root - ERROR - Errores en inserción BigQuery - Intento 2: [{'index': 0, 'errors': [{'reason': 'invalid', 'location': 'session_info', 'debugInfo': '', 'message': 'This field: session_info is not a record.'}]}]
{
insertId: "6880a189000bed5146d9dd38"
labels: {1}
logName: "projects/smatwatt/logs/run.googleapis.com%2Fstdout"
receiveTimestamp: "2025-07-23T08:47:05.848661620Z"
resource: {2}
textPayload: "2025-07-23 08:47:05,782 - root - ERROR - Errores en inserción BigQuery - Intento 2: [{'index': 0, 'errors': [{'reason': 'invalid', 'location': 'session_info', 'debugInfo': '', 'message': 'This field: session_info is not a record.'}]}]"
timestamp: "2025-07-23T08:47:05.781649Z"
}
10:47:06.838
2025-07-23 08:47:06,839 - root - ERROR - Errores en inserción BigQuery - Intento 3: [{'index': 0, 'errors': [{'reason': 'invalid', 'location': 'session_info', 'debugInfo': '', 'message': 'This field: session_info is not a record.'}]}]

{
insertId: "6880a18a000cc9913d950e18"
labels: {
instanceId: "0069c7a98893df2b86453244dc3539eaf04dc70f1d6f189276cc0e75c46de2a374a4950a49b623c8ae8f32c4039893aca60bf5ee4e46b934b32da2457901e5ab31d7928d89cd5de263c2bb2e9d30044c"
}
logName: "projects/smatwatt/logs/run.googleapis.com%2Fstdout"
receiveTimestamp: "2025-07-23T08:47:06.847446895Z"
resource: {2}
textPayload: "2025-07-23 08:47:06,839 - root - ERROR - Errores en inserción BigQuery - Intento 3: [{'index': 0, 'errors': [{'reason': 'invalid', 'location': 'session_info', 'debugInfo': '', 'message': 'This field: session_info is not a record.'}]}]"
timestamp: "2025-07-23T08:47:06.838033Z"
}
10:47:06.838
2025-07-23 08:47:06,839 - expert_bot_api.routes - ERROR - Error creando nueva conversación: name 'logger' is not defined
{
insertId: "6880a18a000ccafa9f843c34"
labels: {1}
logName: "projects/smatwatt/logs/run.googleapis.com%2Fstdout"
receiveTimestamp: "2025-07-23T08:47:06.847446895Z"
resource: {2}
textPayload: "2025-07-23 08:47:06,839 - expert_bot_api.routes - ERROR - Error creando nueva conversación: name 'logger' is not defined"
timestamp: "2025-07-23T08:47:06.838394Z"
}
10:47:06.838
2025-07-23 08:47:06,840 - root - ERROR - Error en decorador token_required: Error interno creando nueva conversación: name 'logger' is not defined
10:47:06.849
2025-07-23 08:47:06,850 - utils.error_handlers - ERROR - {"error_id": "d6ac4a6e-7497-4996-bc0b-51c832a7ee2f", "timestamp": "2025-07-23T08:47:06.840527+00:00", "level": "high", "category": "authentication", "message": "Error de autenticaci\u00f3n", "user_id": "56bE1dNrjef8kO0Erg1qKQytKAq2", "endpoint": "chat_routes.create_new_conversation", "method": "POST", "ip_address": "169.254.169.126"}
10:47:06.852
169.254.169.126 - - [23/Jul/2025:08:47:06 +0000] "POST /api/v1/chatbot/new-conversation HTTP/1.1" 500 192 "<https://smarwatt.com/>" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"

{
insertId: "6880a18a000d004905f8aaff"
labels: {1}
logName: "projects/smatwatt/logs/run.googleapis.com%2Fstdout"
receiveTimestamp: "2025-07-23T08:47:07.181532187Z"
resource: {2}
textPayload: "169.254.169.126 - - [23/Jul/2025:08:47:06 +0000] "POST /api/v1/chatbot/new-conversation HTTP/1.1" 500 192 "<https://smarwatt.com/>" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36""
timestamp: "2025-07-23T08:47:06.852041Z"
}
11:02:08.172
[2025-07-23 09:02:08 +0000] [7] [INFO] Worker exiting (pid: 7)
{
insertId: "6880a5100002a2dadee4ec0f"
labels: {1}
logName: "projects/smatwatt/logs/run.googleapis.com%2Fstderr"
receiveTimestamp: "2025-07-23T09:02:08.174985475Z"
resource: {2}
textPayload: "[2025-07-23 09:02:08 +0000] [7] [INFO] Worker exiting (pid: 7)"
timestamp: "2025-07-23T09:02:08.172762Z"
}
11:02:08.177
[2025-07-23 09:02:08 +0000] [9] [INFO] Worker exiting (pid: 9)

{
insertId: "6880a5100002b5008a6a7c92"
labels: {1}
logName: "projects/smatwatt/logs/run.googleapis.com%2Fstderr"
receiveTimestamp: "2025-07-23T09:02:08.509563992Z"
resource: {2}
textPayload: "[2025-07-23 09:02:08 +0000] [9] [INFO] Worker exiting (pid: 9)"
timestamp: "2025-07-23T09:02:08.177408Z"
}
11:02:08.177
[2025-07-23 09:02:08 +0000] [8] [INFO] Worker exiting (pid: 8)

{
insertId: "6880a5100002b749c63c4dd6"
labels: {1}
logName: "projects/smatwatt/logs/run.googleapis.com%2Fstderr"
receiveTimestamp: "2025-07-23T09:02:08.509563992Z"
resource: {2}
textPayload: "[2025-07-23 09:02:08 +0000] [8] [INFO] Worker exiting (pid: 8)"
timestamp: "2025-07-23T09:02:08.177993Z"
}
11:02:08.178
[2025-07-23 09:02:08 +0000] [10] [INFO] Worker exiting (pid: 10)
Para ver más resultados, expande el intervalo de tiempo de esta consulta.
