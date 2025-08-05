vicios\DOCUMENTACION Y SCRPT\MINISERVICIOS_SCRIPS\VERIFICACION REAL ENDOPOIN PRODUCCION> gcloud logging read 'resource.type=cloud_run_revision AND resource.labels.service_name=energy-ia-api AND timestamp>="2025-08-05T14:20:00Z"' --limit=10 --format='value(textPayload,jsonPayload.message)' --project=smatwatt
169.254.169.126 - - [05/Aug/2025:14:40:20 +0000] "GET /api/v1/chatbot/conversations HTTP/1.1" 200 23714 "<https://smarwatt.com/>" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
2025-08-05 14:40:19,541 - app - INFO - ? REQUEST [req_1754404819] GET /api/v1/chatbot/conversations

2025-08-05 14:40:17,840 - app - INFO - ? REQUEST [req_1754404817] GET /api/v1/chatbot/conversations

169.254.169.126 - - [05/Aug/2025:14:40:17 +0000] "OPTIONS /api/v1/chatbot/conversations HTTP/1.1" 200 0 "<https://smarwatt.com/>" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
2025-08-05 14:40:17,764 - app - INFO - ? RESPONSE [req_1754404817] 200 - 0.001s
2025-08-05 14:40:17,763 - app - INFO - ? REQUEST [req_1754404817] OPTIONS /api/v1/chatbot/conversations

169.254.169.126 - - [05/Aug/2025:14:25:55 +0000] "GET /api/v1/links/direct/test HTTP/1.1" 404 155 "-" "SmarWatt-Production-Tester/1.0"
PS C:\Smarwatt*2\SmarWatt_2\backend\sevicio chatbot\servicios\DOCUMENTACION Y SCRPT\MINISERVICIOS_SCRIPS\VERIFICACION REAL ENDOPOIN PRODUCCION> 'resource.type=cloud_run_revision AND resource.labels.service_name=energy-ia-api AND textPayload:"Traceback"' --limit=5 --format='value(textPayload)' --project=smatwatt
Traceback (most recent call last):
File "/opt/venv/lib/python3.11/site-packages/gunicorn/workers/sync.py", line 134, in handle
self.handle_request(listener, req, client, addr)  
 File "/opt/venv/lib/python3.11/site-packages/gunicorn/workers/sync.py", line 177, in handle_request
respiter = self.wsgi(environ, resp.start_response)
Traceback (most recent call last):
File "/opt/venv/lib/python3.11/site-packages/gunicorn/workers/sync.py", line 134, in handle
self.handle_request(listener, req, client, addr)  
 File "/opt/venv/lib/python3.11/site-packages/gunicorn/workers/sync.py", line 177, in handle_request
respiter = self.wsgi(environ, resp.start_response)
Traceback (most recent call last):
File "/opt/venv/lib/python3.11/site-packages/google/api_core/retry/retry_unary.py", line 147, in retry_target
result = target()
Traceback (most recent call last):
File "/opt/venv/lib/python3.11/site-packages/google/api_core/grpc_helpers.py", line 76, in error_remapped_callable
return callable*(\*args, \*\*kwargs)
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\DOCUMENTACION Y SCRPT\MINISERVICIOS_SCRIPS\VERIFICACION REAL ENDOPOIN PRODUCCION>
att
2025-08-05 14:41:43,155 - root - ERROR - ? Error consultando recomendaciones de tarifas: Error en motor de recomendaciones: Error en recomendaci?n: Error en recomendaci?n: Consumo energ?tico requerido: especifica 'avg_kwh', 'energy_profile.monthly_consumption_kwh' o 'peak_consumption_kwh + off_peak_consumption_kwh'
2025-08-05 14:41:43,155 - utils.error_handlers - ERROR - AppError[8e53ab4e]: Error en motor de recomendaciones: Error en recomendaci?n: Error en recomendaci?n: Consumo energ?tico requerido: especifica 'avg_kwh', 'energy_profile.monthly_consumption_kwh' o 'peak_consumption_kwh + off_peak_consumption_kwh' (Status: 500)
2025-08-05 14:41:43,155 - app.routes - ERROR - ? Error generando recomendaci?n avanzada: Error en recomendaci?n: Error en recomendaci?n: Consumo energ?tico requerido: especifica 'avg_kwh', 'energy_profile.monthly_consumption_kwh' o 'peak_consumption_kwh + off_peak_consumption_kwh'
2025-08-05 14:41:43,155 - utils.error_handlers - ERROR - AppError[4d42d337]: Error en recomendaci?n: Error en recomendaci?n: Consumo energ?tico requerido: especifica 'avg_kwh', 'energy_profile.monthly_consumption_kwh' o 'peak_consumption_kwh + off_peak_consumption_kwh' (Status: 500)
2025-08-05 14:41:43,155 - app.services.vertex_ai_service - ERROR - ? Error en m?todo de compatibilidad: Error en recomendaci?n: Consumo energ?tico requerido: especifica 'avg_kwh', 'energy_profile.monthly_consumption_kwh' o 'peak_consumption_kwh + off_peak_consumption_kwh'
2025-08-05 14:41:43,155 - utils.error_handlers - ERROR - AppError[7adce970]: Error en recomendaci?n: Consumo energ?tico requerido: especifica 'avg_kwh', 'energy_profile.monthly_consumption_kwh' o 'peak_consumption_kwh + off_peak_consumption_kwh' (Status: 500)
2025-08-05 14:41:43,155 - app.services.vertex_ai_service - ERROR - ? Error en recomendaci?n empresarial: Consumo energ?tico requerido: especifica 'avg_kwh', 'energy_profile.monthly_consumption_kwh' o 'peak_consumption_kwh + off_peak_consumption_kwh'
2025-08-05 14:41:43,155 - utils.error_handlers - ERROR - AppError[d021ef1c]: Consumo energ?tico requerido: especifica 'avg_kwh', 'energy_profile.monthly_consumption_kwh' o 'peak_consumption_kwh + off_peak_consumption_kwh' (Status: 400)
2025-08-05 14:25:53,131 - utils.error_handlers - INFO - ? Error cr?tico reportado: dbfb387b
2025-08-05 14:25:53,130 - utils.error_handlers - INFO - ? Error cr?tico reportado: dbfb387b
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\DOCUMENTACION Y SCRPT\MINISERVICIOS_SCRIPS\VERIFICACION REAL ENDOPOIN PRODUCCION>
OR textPayload:"Exception" OR textPayload:"Failed")' --limit=10 --format='value(textPayload)' --project=smatwatt
2025-08-05 14:41:42,218 - root - ERROR - Error en logging as?ncrono de sentiment: Object of type datetime is not JSON serializable
2025-08-05 14:40:43,985 - root - ERROR - Error en logging as?ncrono de sentiment: Object of type datetime is not JSON serializable
2025-08-05 14:26:01,412 - utils.error_handlers - ERROR - {"error_id": "16a36f98-8405-49f5-81d4-cec51d50cd65", "timestamp": "2025-08-05T14:26:01.411825+00:00", "level": "high", "category": "authentication", "message": "Falta el token de autorizaci\u00f3n", "user_id": null, "endpoint": "expert_energy_routes.upload_consumption_data", "method": "POST", "ip_address": "169.254.169.126"}
2025-08-05 14:26:00,650 - utils.error_handlers - ERROR - {"error_id": "57783be7-70d8-47f2-b753-f6a3eb707c0c", "timestamp": "2025-08-05T14:26:00.650027+00:00", "level": "high", "category": "authentication", "message": "Falta el token de autorizaci\u00f3n", "user_id": null, "endpoint": "expert_energy_routes.upload_consumption_data", "method": "POST", "ip_address": "169.254.169.126"}
2025-08-05 14:26:00,015 - utils.error_handlers - ERROR - {"error_id": "4ac2bd0d-cbca-4358-96b9-66a39d09ac13", "timestamp": "2025-08-05T14:26:00.001637+00:00", "level": "high", "category": "authentication", "message": "Falta el token de autorizaci\u00f3n", "user_id": null, "endpoint": "chat_routes.create_new_conversation", "method": "POST", "ip_address": "169.254.169.126"}
2025-08-05 14:25:59,328 - utils.error_handlers - ERROR - {"error_id": "c6ed3bd1-edb7-4855-8079-566bcde23a5f", "timestamp": "2025-08-05T14:25:59.314925+00:00", "level": "high", "category": "authentication", "message": "Falta el token de autorizaci\u00f3n", "user_id": null, "endpoint": "chat_routes.post_message", "method": "POST", "ip_address": "169.254.169.126"}
2025-08-05 14:25:58,587 - utils.error_handlers - ERROR - {"error_id": "1d617d87-54a2-4feb-a0fa-75d3cd7967bc", "timestamp": "2025-08-05T14:25:58.587279+00:00", "level": "high", "category": "authentication", "message": "Falta el token de autorizaci\u00f3n", "user_id": null, "endpoint": "chat_routes.start_chat_session", "method": "POST", "ip_address": "169.254.169.126"}
2025-08-05 14:25:57,931 - expert_bot_api.analysis_routes - ERROR - Error en ruta de an?lisis: Endpoint exclusivo para comunicaci?n interna entre servicios
2025-08-05 14:25:57,241 - utils.error_handlers - ERROR - {"error_id": "10875d67-6300-46cd-b084-a7b5e649d576", "timestamp": "2025-08-05T14:25:57.223579+00:00", "level": "high", "category": "authentication", "message": "Falta el token de autorizaci\u00f3n", "user_id": null, "endpoint": "analysis_routes.analyze_sentiment", "method": "POST", "ip_address": "169.254.169.126"}
2025-08-05 14:24:57,270 - expert_bot_api - INFO - Manejadores de errores empresariales registrados correctamente
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\DOCUMENTACION Y SCRPT\MINISERVICIOS_SCRIPS\VERIFICACION REAL ENDOPOIN PRODUCCION>
