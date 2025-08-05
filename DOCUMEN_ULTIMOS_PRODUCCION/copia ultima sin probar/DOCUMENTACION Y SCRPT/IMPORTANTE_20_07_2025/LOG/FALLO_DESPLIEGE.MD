xpert-bot-api --region=europe-west1

+ Service expert-bot-api in region europe-west1

URL:     https://expert-bot-api-1010012211318.europe-west1.run.app      
Ingress: all
Traffic:
  100% LATEST (currently expert-bot-api-00095-d74)

Scaling: Auto (Min: 0)

Last updated on 2025-07-25T15:13:58.023762Z by tomatesjuanlu@gmail.com: 
  Revision expert-bot-api-00095-d74 
  Container None
    Image:           europe-west1-docker.pkg.dev/smatwatt/cloud-run-source-deploy/expert-bot-api@sha256:c868f03b56659f356e366c59996c1fcf06620079e326a99fa9629b6780b920f3
    Port:            8081
    Memory:          4Gi
    CPU:             2
    Env vars:
      AI_LEARNING_ENABLED true      
      BQ_AI_BUSINESS_METRICS_TABLE_ID ai_business_metrics
      BQ_AI_OPTIMIZATION_TABLE_ID ai_prompt_optimization
      BQ_AI_PATTERNS_TABLE_ID ai_user_patterns
      BQ_AI_PREDICTIONS_TABLE_ID ai_predictions
      BQ_AI_SENTIMENT_TABLE_ID ai_sentiment_analysis
      BQ_ASYNC_TASKS_TABLE_ID async_tasks
      BQ_CONSUMPTION_LOG_TABLE_ID consumption_log
      BQ_CONVERSATIONS_TABLE_ID conversations_log
      BQ_DATASET_ID  smartwatt_data
      BQ_FEEDBACK_TABLE_ID feedback_log
      BQ_MARKET_TARIFFS_TABLE_ID market_electricity_tariffs
      BQ_RECOMMENDATION_LOG_TABLE_ID recommendation_log
      BQ_UPLOADED_DOCS_TABLE_ID uploaded_documents_log
      BQ_USER_PROFILES_TABLE_ID user_profiles_enriched
      BQ_WORKER_METRICS_TABLE_ID worker_metrics
      CORS_ORIGINS   https://smarwatt.com
      ENERGY_IA_API_URL https://energy-ia-api-1010012211318.europe-west1.run.app
      FLASK_CONFIG   production
      GCP_LOCATION   eu
      GCP_PROJECT_ID smatwatt       
      GCS_INVOICE_BUCKET smatwatt-model-exports-smatwatt-final
      GEMINI_API_KEY AIzaSyCONKtpEAWHM5xtq-C3YTX8xsmFnHo0goE
      OPENWEATHER_API_KEY 8f91cb80de36de44e701ff196ea256e8
      PUBSUB_CONSUMPTION_TOPIC_ID consumption-topic
      SECRET_KEY     MTvrA_NDjZ11l6wCEFcxVr6A7R1iI8AAeyQG6oRUv2I        
    Secrets:
      /credentials   firebase-adminsdk-key:1
      /secrets       expert-bot-api-sa-key:1
    Startup Probe:
      TCP every 240s
      Port:          8081
      Initial delay: 0s
      Timeout:       240s
      Failure threshold: 1
      Type:          Default
  Service account:   firebase-adminsdk-fbsvc@smatwatt.iam.gserviceaccount.com
  Concurrency:       80
  Max instances:     5
  Timeout:           900s
PS C:\Smarwatt_2\SmarWatt_2\web-app-smartwatt-energy\src\components\dashboard>

                                   
  MESSAGE
2025-07-25T15:29:01.687154Z         
   [2025-07-25 15:29:01 +0000] [8] [INFO] Worker exiting (pid: 8)       
2025-07-25T15:29:01.687151Z         
   [2025-07-25 15:29:01 +0000] [7] [INFO] Worker exiting (pid: 7)       
2025-07-25T15:29:01.687145Z         
   [2025-07-25 15:29:01 +0000] [9] [INFO] Worker exiting (pid: 9)       
2025-07-25T15:29:01.686595Z         
   [2025-07-25 15:29:01 +0000] [10] [INFO] Worker exiting (pid: 10)     
2025-07-25T15:14:12.148770Z         
   [2025-07-25 15:13:56 +0000] [8] [INFO] Booting worker with pid: 8    
2025-07-25T15:14:04.200704Z         
   [2025-07-25 15:14:04 +0000] [10] [INFO] Booting worker with pid: 10  
2025-07-25T15:13:58.040529Z  INFO   
2025-07-25T15:13:57.067008Z         
   [2025-07-25 15:13:57 +0000] [9] [INFO] Booting worker with pid: 9    
2025-07-25T15:13:56.850001Z         
   [2025-07-25 15:13:56 +0000] [7] [INFO] Booting worker with pid: 7    
2025-07-25T15:13:56.753892Z  INFO   
2025-07-25T15:13:56.661630Z  INFO      Default STARTUP TCP probe succeeded after 1 attempt for container "expert-bot-api-1" on port 8081.       
2025-07-25T15:13:56.660573Z         
   [2025-07-25 15:13:56 +0000] [3] [INFO] Using worker: sync
2025-07-25T15:13:56.660521Z         
   [2025-07-25 15:13:56 +0000] [3] [INFO] Listening at: http://0.0.0.0:8081 (3)
2025-07-25T15:13:56.658966Z         
   [2025-07-25 15:13:56 +0000] [3] [INFO] Starting gunicorn 23.0.0      
2025-07-25T15:13:56.658500Z         
   2025-07-25 15:13:56,659 - expert_bot_api - INFO - Aplicaci?n Expert Bot API inicializada correctamente en modo empresarial
2025-07-25T15:13:56.658417Z         
   2025-07-25 15:13:56,659 - expert_bot_api - INFO - Aplicaci?n Expert Bot API creada correctamente en modo empresarial
2025-07-25T15:13:56.657628Z         
   2025-07-25 15:13:56,658 - expert_bot_api - INFO - Manejadores de errores empresariales registrados correctamente
2025-07-25T15:13:56.657494Z         
   2025-07-25 15:13:56,658 - expert_bot_api - INFO - Blueprint de procesamiento as?ncrono empresarial registrado correctamente
2025-07-25T15:13:56.606682Z         
   2025-07-25 15:13:56,607 - expert_bot_api - INFO - Blueprint de enlaces empresariales registrado correctamente
2025-07-25T15:13:56.605132Z         
   2025-07-25 15:13:56,606 - app.links_routes - INFO - ? Blueprint de enlaces empresariales cargado correctamente
2025-07-25T15:13:56.599255Z         
   2025-07-25 15:13:56,600 - expert_bot_api - INFO - Blueprint de energ?a registrado correctamente
2025-07-25T15:13:54.834337Z         
   2025-07-25 15:13:54,835 - expert_bot_api - INFO - Blueprint de chat registrado correctamente
2025-07-25T15:13:54.830300Z         
   2025-07-25 15:13:54,831 - app.services.enterprise_links_service - INFO - ? M?dulo EnterpriseLinkService cargado correctamente
2025-07-25T15:13:51.658103Z         
   2025-07-25 15:13:51,659 - expert_bot_api - INFO - CORS configurado correctamente para modo empresarial   
2025-07-25T15:13:51.657934Z         
   2025-07-25 15:13:51,659 - expert_bot_api - INFO - Firebase Admin SDK configurado correctamente en modo empresarial
2025-07-25T15:13:51.657895Z         
   2025-07-25 15:13:51,658 - app - INFO - Firebase Admin SDK inicializado correctamente para proyecto: smatwatt
2025-07-25T15:13:51.656457Z         
   2025-07-25 15:13:51,657 - expert_bot_api - INFO - Iniciando creaci?n de aplicaci?n con configuraci?n: production
2025-07-25T15:13:51.656386Z         
   2025-07-25 15:13:51,656 - expert_bot_api - INFO - Iniciando aplicaci?n con configuraci?n: production     
2025-07-25T15:13:51.655016Z         
   2025-07-25 15:13:51,656 - expert_bot_api - INFO - Todas las variables de entorno requeridas est?n configuradas
2025-07-25T15:13:51.654936Z         
   2025-07-25 15:13:51,655 - expert_bot_api - INFO - Sistema de logging empresarial iniciado correctamente  
2025-07-25T15:13:15.780803Z  NOTICE 
2025-07-25T14:19:43.442828Z         
   [2025-07-25 14:19:43 +0000] [8] [INFO] Worker exiting (pid: 8)       
2025-07-25T14:19:43.442823Z         
   [2025-07-25 14:19:43 +0000] [7] [INFO] Worker exiting (pid: 7)       
2025-07-25T14:19:43.442818Z         
   [2025-07-25 14:19:43 +0000] [9] [INFO] Worker exiting (pid: 9)       
2025-07-25T14:19:43.442785Z         
   [2025-07-25 14:19:43 +0000] [10] [INFO] Worker exiting (pid: 10)     
2025-07-25T14:04:43.380148Z         
   169.254.169.126 - - [25/Jul/2025:14:04:43 +0000] "OPTIONS /consumption/history?timeRange=month&granularity=daily&includeProjections=true&timestamp=2025-07-25T14:04:42.543Z HTTP/1.1" 404 177 "https://smarwatt.com/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
2025-07-25T14:04:43.379902Z         
   2025-07-25 14:04:43,381 - utils.error_handlers - INFO - {"error_id": "394c9f0f-1d5b-466a-aefc-cd3e5c762265", "timestamp": "2025-07-25T14:04:43.380691+00:00", "level": "low", "category": "system", "message": "Recurso no encontrado", "user_id": null, "endpoint": null, "method": "OPTIONS", "ip_address": "169.254.169.126"} 
2025-07-25T14:04:43.379044Z         
   2025-07-25 14:04:43,380 - expert_bot_api - INFO - Request: OPTIONS /consumption/history - IP: 169.254.169.126
2025-07-25T14:04:43.377387Z         
   169.254.169.126 - - [25/Jul/2025:14:04:43 +0000] "OPTIONS /users/profile?includeDocuments=true&includePreferences=true&includeHistory=false&timestamp=2025-07-25T14:04:42.542Z HTTP/1.1" 404 177 "https://smarwatt.com/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
2025-07-25T14:04:43.376850Z         
   2025-07-25 14:04:43,378 - utils.error_handlers - INFO - {"error_id": "9d894f7b-2d8e-49b1-8678-1e00d3ba7cf1", "timestamp": "2025-07-25T14:04:43.377890+00:00", "level": "low", "category": "system", "message": "Recurso no encontrado", "user_id": null, "endpoint": null, "method": "OPTIONS", "ip_address": "169.254.169.126"} 
2025-07-25T14:04:43.376242Z         
   2025-07-25 14:04:43,377 - expert_bot_api - INFO - Request: OPTIONS /users/profile - IP: 169.254.169.126  
2025-07-25T14:04:43.375781Z  WARNING
2025-07-25T14:04:43.374082Z         
   169.254.169.126 - - [25/Jul/2025:14:04:43 +0000] "OPTIONS /metrics HTTP/1.1" 404 177 "https://smarwatt.com/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
2025-07-25T14:04:43.373388Z  WARNING
2025-07-25T14:04:43.373341Z         
   2025-07-25 14:04:43,374 - utils.error_handlers - INFO - {"error_id": "1078cb83-ac29-4bfc-960b-129bfc0bfa60", "timestamp": "2025-07-25T14:04:43.374098+00:00", "level": "low", "category": "system", "message": "Recurso no encontrado", "user_id": null, "endpoint": null, "method": "OPTIONS", "ip_address": "169.254.169.126"} 
2025-07-25T14:04:43.372395Z         
   2025-07-25 14:04:43,373 - expert_bot_api - INFO - Request: OPTIONS /metrics - IP: 169.254.169.126        
2025-07-25T14:04:43.371319Z         
   169.254.169.126 - - [25/Jul/2025:14:04:43 +0000] "OPTIONS /dashboard HTTP/1.1" 404 177 "https://smarwatt.com/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
2025-07-25T14:04:43.370730Z         
   169.254.169.126 - - [25/Jul/2025:14:04:43 +0000] "OPTIONS /consumption/recommendations?analysisLevel=comprehensive&priorityFocus=cost_reduction&includeInvestment=true&timestamp=2025-07-25T14:04:42.542Z HTTP/1.1" 404 177 "https://smarwatt.com/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
2025-07-25T14:04:43.370411Z         
   2025-07-25 14:04:43,371 - utils.error_handlers - INFO - {"error_id": "8b5687c5-fc51-45f0-9c90-719fc8e2c623", "timestamp": "2025-07-25T14:04:43.371188+00:00", "level": "low", "category": "system", "message": "Recurso no encontrado", "user_id": null, "endpoint": null, "method": "OPTIONS", "ip_address": "169.254.169.126"} 
2025-07-25T14:04:43.369986Z         
   2025-07-25 14:04:43,371 - utils.error_handlers - INFO - {"error_id": "f0f43cca-60d0-4186-a428-28469543ea62", "timestamp": "2025-07-25T14:04:43.370799+00:00", "level": "low", "category": "system", "message": "Recurso no encontrado", "user_id": null, "endpoint": null, "method": "OPTIONS", "ip_address": "169.254.169.126"} 
PS C:\Smarwatt_2\SmarWatt_2\web-app-smartwatt-energy\src\components\dashboard>.type=build" --limit=20 --format="table(timestamp,severity,textPayload)" --project=smatwatt
TIMESTAMP                       SEVERITY  TEXT_PAYLOAD
2025-07-25T15:12:34.958947Z     NOTICE
2025-07-25T15:12:21.382114192Z  INFO      DONE
2025-07-25T15:12:21.135663352Z  INFO      latest: digest: sha256:c868f03b56659f356e366c59996c1fcf06620079e326a99fa9629b6780b920f3 size: 2423    
2025-07-25T15:12:20.644269885Z  INFO      d4735b729d15: Pushed
2025-07-25T15:11:30.196894447Z  INFO      b129f07f1f86: Pushed
2025-07-25T15:11:29.485126455Z  INFO      21e5cb0df92d: Pushed
2025-07-25T15:11:26.174018243Z  INFO      7cc7fe68eff6: Pushed
2025-07-25T15:11:05.341060262Z  INFO      5901fd5b7a2b: Pushed
2025-07-25T15:11:04.868725394Z  INFO      0a00f6ce5fb7: Layer already exists
2025-07-25T15:11:04.510412053Z  INFO      943faa7467a0: Layer already exists
2025-07-25T15:11:04.081536021Z  INFO      d22cc68b10d7: Layer already exists
2025-07-25T15:11:03.846618180Z  INFO      c3a4d754ac63: Pushed
2025-07-25T15:11:03.716413748Z  INFO      ff95e522e5c3: Pushed
2025-07-25T15:11:02.689240133Z  INFO      d22cc68b10d7: Waiting
2025-07-25T15:11:02.689239653Z  INFO      7cc7fe68eff6: Waiting
2025-07-25T15:11:02.689238983Z  INFO      5901fd5b7a2b: Waiting
2025-07-25T15:11:02.689238313Z  INFO      0a00f6ce5fb7: Waiting
2025-07-25T15:11:02.689231163Z  INFO      943faa7467a0: Waiting
2025-07-25T15:11:02.688478898Z  INFO      7cc7fe68eff6: Preparing       
2025-07-25T15:11:02.688478321Z  INFO      0a00f6ce5fb7: Preparing       
PS C:\Smarwatt_2\SmarWatt_2\web-app-smartwatt-energy\src\components\dashboard>