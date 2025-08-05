" --limit=5 --format="value(textPayload)" --project=smatwatt
[2025-07-26 08:38:54 +0000] [10] [INFO] Booting worker with pid: 10
[2025-07-26 08:38:43 +0000] [9] [INFO] Booting worker with pid: 9
[2025-07-26 08:38:15 +0000] [8] [INFO] Booting worker with pid: 8
169.254.169.126 - - [26/Jul/2025:08:33:40 +0000] "POST /api/v1/chatbot/new-conversation HTTP/1.1" 500 192 "<https://smarwatt.com/>" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
2025-07-26 08:33:40,698 - utils.error_handlers - ERROR - {"error_id": "dab4e0f4-2af4-4160-a66e-29161d863495", "timestamp": "2025-07-26T08:33:40.697318+00:00", "level": "high", "category": "authentication", "message": "Error de autenticaci\u00f3n", "user_id": "56bE1dNrjef8kO0Erg1qKQytKAq2", "endpoint": "chat_routes.create_new_conversation", "method": "POST", "ip_address": "169.254.169.126"}
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios> gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=expert-bot-api" --limit=5 --format="table(timestamp,severity,textPayload)" --project=smatwatt
TIMESTAMP SEVERITY TEXT_PAYLOAD
2025-07-26T08:39:04.320047Z [2025-07-26 08:38:54 +0000] [10] [INFO] Booting worker with pid: 10  
2025-07-26T08:38:43.971684Z [2025-07-26 08:38:43 +0000] [9] [INFO] Booting worker with pid: 9
2025-07-26T08:38:42.519295Z [2025-07-26 08:38:15 +0000] [8] [INFO] Booting worker with pid: 8
2025-07-26T08:33:40.698910Z 169.254.169.126 - - [26/Jul/2025:08:33:40 +0000] "POST /api/v1/chatbot/new-conversation HTTP/1.1" 500 192 "<https://smarwatt.com/>" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
2025-07-26T08:33:40.697892Z 2025-07-26 08:33:40,698 - utils.error_handlers - ERROR - {"error_id": "dab4e0f4-2af4-4160-a66e-29161d863495", "timestamp": "2025-07-26T08:33:40.697318+00:00", "level": "high", "category": "authentication", "message": "Error de autenticaci\u00f3n", "user_id": "56bE1dNrjef8kO0Erg1qKQytKAq2", "endpoint": "chat_routes.create_new_conversation", "method": "POST", "ip_address": "169.254.169.126"}
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios>
