S C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\DOCUMENTACION Y SCRPT\MINISERVICIOS_SCRIPS\VERIFICACION REAL ENDOPOIN PRODUCCION> gcloud logging read 'resource.type="cloud_run_revision" AND resource.labels.service_name="energy-ia-api"' --project=smatwatt --format="json" --limit=30 
[
  {
    "insertId": "689221c000061fa794fa5bcd",
    "labels": {
      "instanceId": "0069c7a988c0fd7cf9090e88991ae64949dee5ff961ee56203b2a30a4d6b7c7a7147832ca54ddf1d5d1a1fce304cd8974c19dd3d847cff4696f3de0cc6e0c4e339db5be9e312a0b0d2868a2e786256"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstderr",
    "receiveTimestamp": "2025-08-05T15:22:40.404229855Z",
    "resource": {
      "labels": {
        "configuration_name": "energy-ia-api",        
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "energy-ia-api-00117-gzb",   
        "service_name": "energy-ia-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "[2025-08-05 15:22:40 +0000] [8] [INFO] Worker exiting (pid: 8)",
    "timestamp": "2025-08-05T15:22:40.401319Z"        
  },
  {
    "insertId": "689221c000061fa23580fc14",
    "labels": {
      "instanceId": "0069c7a988c0fd7cf9090e88991ae64949dee5ff961ee56203b2a30a4d6b7c7a7147832ca54ddf1d5d1a1fce304cd8974c19dd3d847cff4696f3de0cc6e0c4e339db5be9e312a0b0d2868a2e786256"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstderr",
    "receiveTimestamp": "2025-08-05T15:22:40.404229855Z",
    "resource": {
      "labels": {
        "configuration_name": "energy-ia-api",        
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "energy-ia-api-00117-gzb",   
        "service_name": "energy-ia-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "[2025-08-05 15:22:40 +0000] [7] [INFO] Worker exiting (pid: 7)",
    "timestamp": "2025-08-05T15:22:40.401314Z"        
  },
  {
    "insertId": "689221c000061f7576ac3c60",
    "labels": {
      "instanceId": "0069c7a988c0fd7cf9090e88991ae64949dee5ff961ee56203b2a30a4d6b7c7a7147832ca54ddf1d5d1a1fce304cd8974c19dd3d847cff4696f3de0cc6e0c4e339db5be9e312a0b0d2868a2e786256"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstderr",
    "receiveTimestamp": "2025-08-05T15:22:40.404229855Z",
    "resource": {
      "labels": {
        "configuration_name": "energy-ia-api",        
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "energy-ia-api-00117-gzb",   
        "service_name": "energy-ia-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "[2025-08-05 15:22:40 +0000] [10] [INFO] Worker exiting (pid: 10)",
    "timestamp": "2025-08-05T15:22:40.401269Z"        
  },
  {
    "insertId": "68921e3b000d888167d94f44",
    "labels": {
      "instanceId": "0069c7a988c0fd7cf9090e88991ae64949dee5ff961ee56203b2a30a4d6b7c7a7147832ca54ddf1d5d1a1fce304cd8974c19dd3d847cff4696f3de0cc6e0c4e339db5be9e312a0b0d2868a2e786256"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstdout",
    "receiveTimestamp": "2025-08-05T15:07:40.037281394Z",
    "resource": {
      "labels": {
        "configuration_name": "energy-ia-api",        
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "energy-ia-api-00117-gzb",   
        "service_name": "energy-ia-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "169.254.169.126 - - [05/Aug/2025:15:07:39 +0000] \"GET /api/v1/links/direct/admin HTTP/1.1\" 404 156 \"-\" \"SmarWatt-Production-Tester/1.0\"",
    "timestamp": "2025-08-05T15:07:39.886913Z"        
  },
  {
    "insertId": "68921e3b000d85abf660a816",
    "labels": {
      "instanceId": "0069c7a988c0fd7cf9090e88991ae64949dee5ff961ee56203b2a30a4d6b7c7a7147832ca54ddf1d5d1a1fce304cd8974c19dd3d847cff4696f3de0cc6e0c4e339db5be9e312a0b0d2868a2e786256"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstderr",
    "receiveTimestamp": "2025-08-05T15:07:39.949988792Z",
    "resource": {
      "labels": {
        "configuration_name": "energy-ia-api",        
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "energy-ia-api-00117-gzb",   
        "service_name": "energy-ia-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "2025-08-05 15:07:39,887 - app - INFO - ? RESPONSE [req_1754406459] 404 - 0.000s",       
    "timestamp": "2025-08-05T15:07:39.886187Z"        
  },
  {
    "insertId": "68921e3b000d84dad33f0ab2",
    "labels": {
      "instanceId": "0069c7a988c0fd7cf9090e88991ae64949dee5ff961ee56203b2a30a4d6b7c7a7147832ca54ddf1d5d1a1fce304cd8974c19dd3d847cff4696f3de0cc6e0c4e339db5be9e312a0b0d2868a2e786256"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstderr",
    "receiveTimestamp": "2025-08-05T15:07:39.949988792Z",
    "resource": {
      "labels": {
        "configuration_name": "energy-ia-api",        
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "energy-ia-api-00117-gzb",   
        "service_name": "energy-ia-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "2025-08-05 15:07:39,887 - app - INFO - ? REQUEST [req_1754406459] GET /api/v1/links/direct/admin",
    "timestamp": "2025-08-05T15:07:39.885978Z"        
  },
  {
    "httpRequest": {
      "latency": "0.004225306s",
      "protocol": "HTTP/1.1",
      "remoteIp": "88.18.220.132",
      "requestMethod": "GET",
      "requestSize": "366",
      "requestUrl": "https://energy-ia-api-1010012211318.europe-west1.run.app/api/v1/links/direct/admin",   
      "responseSize": "546",
      "serverIp": "34.143.76.2",
      "status": 404,
      "userAgent": "SmarWatt-Production-Tester/1.0"   
    },
    "insertId": "68921e3b000d8a151395b1c6",
    "labels": {
      "instanceId": "0069c7a988c0fd7cf9090e88991ae64949dee5ff961ee56203b2a30a4d6b7c7a7147832ca54ddf1d5d1a1fce304cd8974c19dd3d847cff4696f3de0cc6e0c4e339db5be9e312a0b0d2868a2e786256"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Frequests",
    "receiveTimestamp": "2025-08-05T15:07:40.042844834Z",
    "resource": {
      "labels": {
        "configuration_name": "energy-ia-api",        
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "energy-ia-api-00117-gzb",   
        "service_name": "energy-ia-api"
      },
      "type": "cloud_run_revision"
    },
    "severity": "WARNING",
    "spanId": "132721046f2b2753",
    "timestamp": "2025-08-05T15:07:39.881063Z",       
    "trace": "projects/smatwatt/traces/809ae0267fc30728463685b778bf4e88"
  },
  {
    "insertId": "68921e3b00033e661169880c",
    "labels": {
      "instanceId": "0069c7a988c0fd7cf9090e88991ae64949dee5ff961ee56203b2a30a4d6b7c7a7147832ca54ddf1d5d1a1fce304cd8974c19dd3d847cff4696f3de0cc6e0c4e339db5be9e312a0b0d2868a2e786256"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstdout",
    "receiveTimestamp": "2025-08-05T15:07:39.373336856Z",
    "resource": {
      "labels": {
        "configuration_name": "energy-ia-api",        
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "energy-ia-api-00117-gzb",   
        "service_name": "energy-ia-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "169.254.169.126 - - [05/Aug/2025:15:07:39 +0000] \"GET /api/v1/links/status HTTP/1.1\" 200 188 \"-\" \"SmarWatt-Production-Tester/1.0\"",     
    "timestamp": "2025-08-05T15:07:39.212582Z"        
  },
  {
    "insertId": "68921e3b00033d1a1bf0e0cf",
    "labels": {
      "instanceId": "0069c7a988c0fd7cf9090e88991ae64949dee5ff961ee56203b2a30a4d6b7c7a7147832ca54ddf1d5d1a1fce304cd8974c19dd3d847cff4696f3de0cc6e0c4e339db5be9e312a0b0d2868a2e786256"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstderr",
    "receiveTimestamp": "2025-08-05T15:07:39.280474734Z",
    "resource": {
      "labels": {
        "configuration_name": "energy-ia-api",        
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "energy-ia-api-00117-gzb",   
        "service_name": "energy-ia-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "2025-08-05 15:07:39,213 - app - INFO - ? RESPONSE [req_1754406459] 200 - 0.000s",       
    "timestamp": "2025-08-05T15:07:39.212250Z"        
  },
  {
    "insertId": "68921e3b00033ba2075ad084",
    "labels": {
      "instanceId": "0069c7a988c0fd7cf9090e88991ae64949dee5ff961ee56203b2a30a4d6b7c7a7147832ca54ddf1d5d1a1fce304cd8974c19dd3d847cff4696f3de0cc6e0c4e339db5be9e312a0b0d2868a2e786256"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstderr",
    "receiveTimestamp": "2025-08-05T15:07:39.280474734Z",
    "resource": {
      "labels": {
        "configuration_name": "energy-ia-api",        
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "energy-ia-api-00117-gzb",   
        "service_name": "energy-ia-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "2025-08-05 15:07:39,213 - app - INFO - ? REQUEST [req_1754406459] GET /api/v1/links/status",
    "timestamp": "2025-08-05T15:07:39.211874Z"        
  },
  {
    "httpRequest": {
      "latency": "0.003300862s",
      "protocol": "HTTP/1.1",
      "remoteIp": "88.18.220.132",
      "requestMethod": "GET",
      "requestSize": "360",
      "requestUrl": "https://energy-ia-api-1010012211318.europe-west1.run.app/api/v1/links/status",
      "responseSize": "578",
      "serverIp": "34.143.76.2",
      "status": 200,
      "userAgent": "SmarWatt-Production-Tester/1.0"   
    },
    "insertId": "68921e3b0003405713863406",
    "labels": {
      "instanceId": "0069c7a988c0fd7cf9090e88991ae64949dee5ff961ee56203b2a30a4d6b7c7a7147832ca54ddf1d5d1a1fce304cd8974c19dd3d847cff4696f3de0cc6e0c4e339db5be9e312a0b0d2868a2e786256"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Frequests",
    "receiveTimestamp": "2025-08-05T15:07:39.374324527Z",
    "resource": {
      "labels": {
        "configuration_name": "energy-ia-api",        
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "energy-ia-api-00117-gzb",   
        "service_name": "energy-ia-api"
      },
      "type": "cloud_run_revision"
    },
    "severity": "INFO",
    "spanId": "87d4ffbeedeb0215",
    "timestamp": "2025-08-05T15:07:39.207945Z",       
    "trace": "projects/smatwatt/traces/8244d555a3756a0baa7adc41636a3b0f"
  },
  {
    "insertId": "68921e3a0008be956f830da8",
    "labels": {
      "instanceId": "0069c7a988c0fd7cf9090e88991ae64949dee5ff961ee56203b2a30a4d6b7c7a7147832ca54ddf1d5d1a1fce304cd8974c19dd3d847cff4696f3de0cc6e0c4e339db5be9e312a0b0d2868a2e786256"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstdout",
    "receiveTimestamp": "2025-08-05T15:07:38.706659935Z",
    "resource": {
      "labels": {
        "configuration_name": "energy-ia-api",        
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "energy-ia-api-00117-gzb",   
        "service_name": "energy-ia-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "169.254.169.126 - - [05/Aug/2025:15:07:38 +0000] \"POST /api/v1/links/test HTTP/1.1\" 400 61 \"-\" \"SmarWatt-Production-Tester/1.0\"",       
    "timestamp": "2025-08-05T15:07:38.573077Z"        
  },
  {
    "insertId": "68921e3a0008bc3140b0ac5b",
    "labels": {
      "instanceId": "0069c7a988c0fd7cf9090e88991ae64949dee5ff961ee56203b2a30a4d6b7c7a7147832ca54ddf1d5d1a1fce304cd8974c19dd3d847cff4696f3de0cc6e0c4e339db5be9e312a0b0d2868a2e786256"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstderr",
    "receiveTimestamp": "2025-08-05T15:07:38.614376204Z",
    "resource": {
      "labels": {
        "configuration_name": "energy-ia-api",        
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "energy-ia-api-00117-gzb",   
        "service_name": "energy-ia-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "2025-08-05 15:07:38,573 - app - INFO - ? RESPONSE [req_1754406458] 400 - 0.001s",       
    "timestamp": "2025-08-05T15:07:38.572465Z"        
  },
  {
    "insertId": "68921e3a0008bac0e38fff81",
    "labels": {
      "instanceId": "0069c7a988c0fd7cf9090e88991ae64949dee5ff961ee56203b2a30a4d6b7c7a7147832ca54ddf1d5d1a1fce304cd8974c19dd3d847cff4696f3de0cc6e0c4e339db5be9e312a0b0d2868a2e786256"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstderr",
    "receiveTimestamp": "2025-08-05T15:07:38.614376204Z",
    "resource": {
      "labels": {
        "configuration_name": "energy-ia-api",        
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "energy-ia-api-00117-gzb",   
        "service_name": "energy-ia-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "2025-08-05 15:07:38,573 - app - INFO - ? REQUEST [req_1754406458] POST /api/v1/links/test",
    "timestamp": "2025-08-05T15:07:38.572096Z"        
  },
  {
    "httpRequest": {
      "latency": "0.003499073s",
      "protocol": "HTTP/1.1",
      "remoteIp": "88.18.220.132",
      "requestMethod": "POST",
      "requestSize": "424",
      "requestUrl": "https://energy-ia-api-1010012211318.europe-west1.run.app/api/v1/links/test",
      "responseSize": "450",
      "serverIp": "34.143.76.2",
      "status": 400,
      "userAgent": "SmarWatt-Production-Tester/1.0"   
    },
    "insertId": "68921e3a0008bfb1ca61ce14",
    "labels": {
      "instanceId": "0069c7a988c0fd7cf9090e88991ae64949dee5ff961ee56203b2a30a4d6b7c7a7147832ca54ddf1d5d1a1fce304cd8974c19dd3d847cff4696f3de0cc6e0c4e339db5be9e312a0b0d2868a2e786256"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Frequests",
    "receiveTimestamp": "2025-08-05T15:07:38.708544536Z",
    "resource": {
      "labels": {
        "configuration_name": "energy-ia-api",        
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "energy-ia-api-00117-gzb",   
        "service_name": "energy-ia-api"
      },
      "type": "cloud_run_revision"
    },
    "severity": "WARNING",
    "spanId": "109dc75614b217f0",
    "timestamp": "2025-08-05T15:07:38.568260Z",       
    "trace": "projects/smatwatt/traces/c648d8ab4615a8e10e7fb38512ea95df"
  },
  {
    "insertId": "68921e39000e13de42cce4d9",
    "labels": {
      "instanceId": "0069c7a988c0fd7cf9090e88991ae64949dee5ff961ee56203b2a30a4d6b7c7a7147832ca54ddf1d5d1a1fce304cd8974c19dd3d847cff4696f3de0cc6e0c4e339db5be9e312a0b0d2868a2e786256"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstdout",
    "receiveTimestamp": "2025-08-05T15:07:38.044930548Z",
    "resource": {
      "labels": {
        "configuration_name": "energy-ia-api",        
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "energy-ia-api-00117-gzb",   
        "service_name": "energy-ia-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "169.254.169.126 - - [05/Aug/2025:15:07:37 +0000] \"POST /api/v1/energy/tariffs/compare HTTP/1.1\" 500 244 \"-\" \"SmarWatt-Production-Tester/1.0\"",
    "timestamp": "2025-08-05T15:07:37.922590Z"        
  },
  {
    "insertId": "68921e39000e1194eafd810d",
    "labels": {
      "instanceId": "0069c7a988c0fd7cf9090e88991ae64949dee5ff961ee56203b2a30a4d6b7c7a7147832ca54ddf1d5d1a1fce304cd8974c19dd3d847cff4696f3de0cc6e0c4e339db5be9e312a0b0d2868a2e786256"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstderr",
    "receiveTimestamp": "2025-08-05T15:07:37.947485192Z",
    "resource": {
      "labels": {
        "configuration_name": "energy-ia-api",        
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "energy-ia-api-00117-gzb",   
        "service_name": "energy-ia-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "2025-08-05 15:07:37,923 - app - INFO - ? RESPONSE [req_1754406457] 500 - 0.001s",       
    "timestamp": "2025-08-05T15:07:37.922004Z"        
  },
  {
    "insertId": "68921e39000e1085d1a735c5",
    "labels": {
      "instanceId": "0069c7a988c0fd7cf9090e88991ae64949dee5ff961ee56203b2a30a4d6b7c7a7147832ca54ddf1d5d1a1fce304cd8974c19dd3d847cff4696f3de0cc6e0c4e339db5be9e312a0b0d2868a2e786256"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstderr",
    "receiveTimestamp": "2025-08-05T15:07:37.947485192Z",
    "resource": {
      "labels": {
        "configuration_name": "energy-ia-api",        
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "energy-ia-api-00117-gzb",   
        "service_name": "energy-ia-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "2025-08-05 15:07:37,923 - utils.error_handlers - INFO - ? Error cr?tico reportado: 55abdbd4",
    "timestamp": "2025-08-05T15:07:37.921733Z"        
  },
  {
    "insertId": "68921e39000e10181b1797a7",
    "labels": {
      "instanceId": "0069c7a988c0fd7cf9090e88991ae64949dee5ff961ee56203b2a30a4d6b7c7a7147832ca54ddf1d5d1a1fce304cd8974c19dd3d847cff4696f3de0cc6e0c4e339db5be9e312a0b0d2868a2e786256"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstderr",
    "receiveTimestamp": "2025-08-05T15:07:37.947485192Z",
    "resource": {
      "labels": {
        "configuration_name": "energy-ia-api",        
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "energy-ia-api-00117-gzb",   
        "service_name": "energy-ia-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "2025-08-05 15:07:37,922 - utils.error_handlers - INFO - ? Error cr?tico reportado: 55abdbd4",
    "timestamp": "2025-08-05T15:07:37.921624Z"        
  },
  {
    "insertId": "68921e39000e100f272923c8",
    "labels": {
      "instanceId": "0069c7a988c0fd7cf9090e88991ae64949dee5ff961ee56203b2a30a4d6b7c7a7147832ca54ddf1d5d1a1fce304cd8974c19dd3d847cff4696f3de0cc6e0c4e339db5be9e312a0b0d2868a2e786256"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstderr",
    "receiveTimestamp": "2025-08-05T15:07:37.947485192Z",
    "resource": {
      "labels": {
        "configuration_name": "energy-ia-api",        
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "energy-ia-api-00117-gzb",   
        "service_name": "energy-ia-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "2025-08-05 15:07:37,922 - utils.error_handlers - ERROR - AppError[55abdbd4]: Error interno del servidor (Status: 500)",
    "timestamp": "2025-08-05T15:07:37.921615Z"        
  },
  {
    "insertId": "68921e39000e0d21982923c3",
    "labels": {
      "instanceId": "0069c7a988c0fd7cf9090e88991ae64949dee5ff961ee56203b2a30a4d6b7c7a7147832ca54ddf1d5d1a1fce304cd8974c19dd3d847cff4696f3de0cc6e0c4e339db5be9e312a0b0d2868a2e786256"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstderr",
    "receiveTimestamp": "2025-08-05T15:07:37.947485192Z",
    "resource": {
      "labels": {
        "configuration_name": "energy-ia-api",        
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "energy-ia-api-00117-gzb",   
        "service_name": "energy-ia-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "2025-08-05 15:07:37,922 - root - ERROR - Error en autenticaci?n empresarial: Falta el token de autorizaci?n",
    "timestamp": "2025-08-05T15:07:37.920865Z"        
  },
  {
    "insertId": "68921e39000e0cb7bf84bf3b",
    "labels": {
      "instanceId": "0069c7a988c0fd7cf9090e88991ae64949dee5ff961ee56203b2a30a4d6b7c7a7147832ca54ddf1d5d1a1fce304cd8974c19dd3d847cff4696f3de0cc6e0c4e339db5be9e312a0b0d2868a2e786256"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstderr",
    "receiveTimestamp": "2025-08-05T15:07:37.947485192Z",
    "resource": {
      "labels": {
        "configuration_name": "energy-ia-api",        
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "energy-ia-api-00117-gzb",   
        "service_name": "energy-ia-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "2025-08-05 15:07:37,921 - app - INFO - ? REQUEST [req_1754406457] POST /api/v1/energy/tariffs/compare",
    "timestamp": "2025-08-05T15:07:37.920759Z"        
  },
  {
    "httpRequest": {
      "latency": "0.006539014s",
      "protocol": "HTTP/1.1",
      "remoteIp": "88.18.220.132",
      "requestMethod": "POST",
      "requestSize": "448",
      "requestUrl": "https://energy-ia-api-1010012211318.europe-west1.run.app/api/v1/energy/tariffs/compare",
      "responseSize": "634",
      "serverIp": "34.143.76.2",
      "status": 500,
      "userAgent": "SmarWatt-Production-Tester/1.0"   
    },
    "insertId": "68921e39000e1e60a6a5ee53",
    "labels": {
      "instanceId": "0069c7a988c0fd7cf9090e88991ae64949dee5ff961ee56203b2a30a4d6b7c7a7147832ca54ddf1d5d1a1fce304cd8974c19dd3d847cff4696f3de0cc6e0c4e339db5be9e312a0b0d2868a2e786256"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Frequests",
    "receiveTimestamp": "2025-08-05T15:07:38.042484160Z",
    "resource": {
      "labels": {
        "configuration_name": "energy-ia-api",        
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "energy-ia-api-00117-gzb",   
        "service_name": "energy-ia-api"
      },
      "type": "cloud_run_revision"
    },
    "severity": "ERROR",
    "spanId": "2c9b698896b10dc4",
    "timestamp": "2025-08-05T15:07:37.904940Z",       
    "trace": "projects/smatwatt/traces/925ac4b59e7a5a2e28aa64284a0740af"
  },
  {
    "insertId": "68921e39000397e48cd8464a",
    "labels": {
      "instanceId": "0069c7a988c0fd7cf9090e88991ae64949dee5ff961ee56203b2a30a4d6b7c7a7147832ca54ddf1d5d1a1fce304cd8974c19dd3d847cff4696f3de0cc6e0c4e339db5be9e312a0b0d2868a2e786256"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstdout",
    "receiveTimestamp": "2025-08-05T15:07:37.374128795Z",
    "resource": {
      "labels": {
        "configuration_name": "energy-ia-api",        
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "energy-ia-api-00117-gzb",   
        "service_name": "energy-ia-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "169.254.169.126 - - [05/Aug/2025:15:07:37 +0000] \"POST /api/v1/energy/admin/tariffs/batch-add HTTP/1.1\" 500 244 \"-\" \"SmarWatt-Production-Tester/1.0\"",
    "timestamp": "2025-08-05T15:07:37.235492Z"        
  },
  {
    "insertId": "68921e390003961975032ef6",
    "labels": {
      "instanceId": "0069c7a988c0fd7cf9090e88991ae64949dee5ff961ee56203b2a30a4d6b7c7a7147832ca54ddf1d5d1a1fce304cd8974c19dd3d847cff4696f3de0cc6e0c4e339db5be9e312a0b0d2868a2e786256"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstderr",
    "receiveTimestamp": "2025-08-05T15:07:37.284229962Z",
    "resource": {
      "labels": {
        "configuration_name": "energy-ia-api",        
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "energy-ia-api-00117-gzb",   
        "service_name": "energy-ia-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "2025-08-05 15:07:37,236 - app - INFO - ? RESPONSE [req_1754406457] 500 - 0.001s",       
    "timestamp": "2025-08-05T15:07:37.235033Z"        
  },
  {
    "insertId": "68921e3900039558ce3ffc4a",
    "labels": {
      "instanceId": "0069c7a988c0fd7cf9090e88991ae64949dee5ff961ee56203b2a30a4d6b7c7a7147832ca54ddf1d5d1a1fce304cd8974c19dd3d847cff4696f3de0cc6e0c4e339db5be9e312a0b0d2868a2e786256"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstderr",
    "receiveTimestamp": "2025-08-05T15:07:37.284229962Z",
    "resource": {
      "labels": {
        "configuration_name": "energy-ia-api",        
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "energy-ia-api-00117-gzb",   
        "service_name": "energy-ia-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "2025-08-05 15:07:37,236 - utils.error_handlers - INFO - ? Error cr?tico reportado: 39baca9d",
    "timestamp": "2025-08-05T15:07:37.234840Z"        
  },
  {
    "insertId": "68921e3900039552285fba80",
    "labels": {
      "instanceId": "0069c7a988c0fd7cf9090e88991ae64949dee5ff961ee56203b2a30a4d6b7c7a7147832ca54ddf1d5d1a1fce304cd8974c19dd3d847cff4696f3de0cc6e0c4e339db5be9e312a0b0d2868a2e786256"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstderr",
    "receiveTimestamp": "2025-08-05T15:07:37.284229962Z",
    "resource": {
      "labels": {
        "configuration_name": "energy-ia-api",        
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "energy-ia-api-00117-gzb",   
        "service_name": "energy-ia-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "2025-08-05 15:07:37,236 - utils.error_handlers - INFO - ? Error cr?tico reportado: 39baca9d",
    "timestamp": "2025-08-05T15:07:37.234834Z"        
  },
  {
    "insertId": "68921e390003954372633ba4",
    "labels": {
      "instanceId": "0069c7a988c0fd7cf9090e88991ae64949dee5ff961ee56203b2a30a4d6b7c7a7147832ca54ddf1d5d1a1fce304cd8974c19dd3d847cff4696f3de0cc6e0c4e339db5be9e312a0b0d2868a2e786256"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstderr",
    "receiveTimestamp": "2025-08-05T15:07:37.284229962Z",
    "resource": {
      "labels": {
        "configuration_name": "energy-ia-api",        
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "energy-ia-api-00117-gzb",   
        "service_name": "energy-ia-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "2025-08-05 15:07:37,236 - utils.error_handlers - ERROR - AppError[39baca9d]: Error interno del servidor (Status: 500)",
    "timestamp": "2025-08-05T15:07:37.234819Z"        
  },
  {
    "insertId": "68921e39000391bf523646e7",
    "labels": {
      "instanceId": "0069c7a988c0fd7cf9090e88991ae64949dee5ff961ee56203b2a30a4d6b7c7a7147832ca54ddf1d5d1a1fce304cd8974c19dd3d847cff4696f3de0cc6e0c4e339db5be9e312a0b0d2868a2e786256"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstderr",
    "receiveTimestamp": "2025-08-05T15:07:37.284229962Z",
    "resource": {
      "labels": {
        "configuration_name": "energy-ia-api",        
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "energy-ia-api-00117-gzb",   
        "service_name": "energy-ia-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "2025-08-05 15:07:37,235 - root - ERROR - Error en autenticaci?n empresarial: Falta el token de autorizaci?n",
    "timestamp": "2025-08-05T15:07:37.233919Z"        
  },
  {
    "insertId": "68921e390003914da8d6c836",
    "labels": {
      "instanceId": "0069c7a988c0fd7cf9090e88991ae64949dee5ff961ee56203b2a30a4d6b7c7a7147832ca54ddf1d5d1a1fce304cd8974c19dd3d847cff4696f3de0cc6e0c4e339db5be9e312a0b0d2868a2e786256"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstderr",
    "receiveTimestamp": "2025-08-05T15:07:37.284229962Z",
    "resource": {
      "labels": {
        "configuration_name": "energy-ia-api",        
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "energy-ia-api-00117-gzb",   
        "service_name": "energy-ia-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "2025-08-05 15:07:37,235 - app - INFO - ? REQUEST [req_1754406457] POST /api/v1/energy/admin/tariffs/batch-add",
    "timestamp": "2025-08-05T15:07:37.233805Z"        
  }
]
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\DOCUMENTACION Y SCRPT\MINISERVICIOS_SCRIPS\VERIFICACION REAL ENDOPOIN PRODUCCION>

PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\DOCUMENTACION Y SCRPT\MINISERVICIOS_SCRIPS\VERIFICACION REAL ENDOPOIN PRODUCCION> gcloud logging read 'resource.type="cloud_run_revision" AND resource.labels.service_name="expert-bot-api"' --project=smatwatt --format="json" --limit=30
[
  {
    "insertId": "689221d8000d110a97e003f5",
    "labels": {
      "instanceId": "0069c7a988139d0881bf0ab749c491a87937f653435e87d348e2300ee13adb7d56f2599fa95510ea593ec3629300279354d32fcffc063c16bfecfebba1ab0f8d2652278fae9d0c957d2be60e8ff815"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstderr",
    "receiveTimestamp": "2025-08-05T15:23:04.858976253Z",
    "resource": {
      "labels": {
        "configuration_name": "expert-bot-api",       
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "expert-bot-api-00125-9md",  
        "service_name": "expert-bot-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "[2025-08-05 15:23:04 +0000] [8] [INFO] Worker exiting (pid: 8)",
    "timestamp": "2025-08-05T15:23:04.856330Z"        
  },
  {
    "insertId": "689221d8000d110917a4c642",
    "labels": {
      "instanceId": "0069c7a988139d0881bf0ab749c491a87937f653435e87d348e2300ee13adb7d56f2599fa95510ea593ec3629300279354d32fcffc063c16bfecfebba1ab0f8d2652278fae9d0c957d2be60e8ff815"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstderr",
    "receiveTimestamp": "2025-08-05T15:23:04.858976253Z",
    "resource": {
      "labels": {
        "configuration_name": "expert-bot-api",       
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "expert-bot-api-00125-9md",  
        "service_name": "expert-bot-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "[2025-08-05 15:23:04 +0000] [7] [INFO] Worker exiting (pid: 7)",
    "timestamp": "2025-08-05T15:23:04.856329Z"        
  },
  {
    "insertId": "689221d8000d11064ba4dcf3",
    "labels": {
      "instanceId": "0069c7a988139d0881bf0ab749c491a87937f653435e87d348e2300ee13adb7d56f2599fa95510ea593ec3629300279354d32fcffc063c16bfecfebba1ab0f8d2652278fae9d0c957d2be60e8ff815"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstderr",
    "receiveTimestamp": "2025-08-05T15:23:04.858976253Z",
    "resource": {
      "labels": {
        "configuration_name": "expert-bot-api",       
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "expert-bot-api-00125-9md",  
        "service_name": "expert-bot-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "[2025-08-05 15:23:04 +0000] [9] [INFO] Worker exiting (pid: 9)",
    "timestamp": "2025-08-05T15:23:04.856326Z"        
  },
  {
    "insertId": "689221d8000d10f58bda902a",
    "labels": {
      "instanceId": "0069c7a988139d0881bf0ab749c491a87937f653435e87d348e2300ee13adb7d56f2599fa95510ea593ec3629300279354d32fcffc063c16bfecfebba1ab0f8d2652278fae9d0c957d2be60e8ff815"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstderr",
    "receiveTimestamp": "2025-08-05T15:23:04.858976253Z",
    "resource": {
      "labels": {
        "configuration_name": "expert-bot-api",       
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "expert-bot-api-00125-9md",  
        "service_name": "expert-bot-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "[2025-08-05 15:23:04 +0000] [10] [INFO] Worker exiting (pid: 10)",
    "timestamp": "2025-08-05T15:23:04.856309Z"        
  },
  {
    "insertId": "68921e51000c63ee1f324a14",
    "labels": {
      "instanceId": "0069c7a988139d0881bf0ab749c491a87937f653435e87d348e2300ee13adb7d56f2599fa95510ea593ec3629300279354d32fcffc063c16bfecfebba1ab0f8d2652278fae9d0c957d2be60e8ff815"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstdout",
    "receiveTimestamp": "2025-08-05T15:08:01.858797768Z",
    "resource": {
      "labels": {
        "configuration_name": "expert-bot-api",       
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "expert-bot-api-00125-9md",  
        "service_name": "expert-bot-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "169.254.169.126 - - [05/Aug/2025:15:08:01 +0000] \"POST /api/v1/energy/consumption HTTP/1.1\" 500 192 \"-\" \"SmarWatt-Production-Tester/1.0\"",
    "timestamp": "2025-08-05T15:08:01.812014Z"        
  },
  {
    "insertId": "68921e51000c3c4753825d7b",
    "labels": {
      "instanceId": "0069c7a988139d0881bf0ab749c491a87937f653435e87d348e2300ee13adb7d56f2599fa95510ea593ec3629300279354d32fcffc063c16bfecfebba1ab0f8d2652278fae9d0c957d2be60e8ff815"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstdout",
    "receiveTimestamp": "2025-08-05T15:08:01.858797768Z",
    "resource": {
      "labels": {
        "configuration_name": "expert-bot-api",       
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "expert-bot-api-00125-9md",  
        "service_name": "expert-bot-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "2025-08-05 15:08:01,802 - utils.error_handlers - ERROR - {\"error_id\": \"07756138-7aff-44d5-b0a8-3687268079cb\", \"timestamp\": \"2025-08-05T15:08:01.795268+00:00\", \"level\": \"high\", \"category\": \"authentication\", \"message\": \"Error de autenticaci\\u00f3n\", \"user_id\": \"testing_production_user_2025\", \"endpoint\": \"expert_energy_routes.upload_consumption_data\", \"method\": \"POST\", \"ip_address\": \"169.254.169.126\"}",
    "timestamp": "2025-08-05T15:08:01.801863Z"        
  },
  {
    "insertId": "68921e51000c1eb115fa23a4",
    "labels": {
      "instanceId": "0069c7a988139d0881bf0ab749c491a87937f653435e87d348e2300ee13adb7d56f2599fa95510ea593ec3629300279354d32fcffc063c16bfecfebba1ab0f8d2652278fae9d0c957d2be60e8ff815"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstdout",
    "receiveTimestamp": "2025-08-05T15:08:01.858797768Z",
    "resource": {
      "labels": {
        "configuration_name": "expert-bot-api",       
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "expert-bot-api-00125-9md",  
        "service_name": "expert-bot-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "2025-08-05 15:08:01,793 - root - ERROR - Error en decorador token_required: 'AILearningService' object has no attribute 'process_invoice_upload_patterns'",
    "timestamp": "2025-08-05T15:08:01.794289Z"        
  },
  {
    "insertId": "68921e51000c174546573a7b",
    "labels": {
      "instanceId": "0069c7a988139d0881bf0ab749c491a87937f653435e87d348e2300ee13adb7d56f2599fa95510ea593ec3629300279354d32fcffc063c16bfecfebba1ab0f8d2652278fae9d0c957d2be60e8ff815"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstdout",
    "receiveTimestamp": "2025-08-05T15:08:01.858797768Z",
    "resource": {
      "labels": {
        "configuration_name": "expert-bot-api",       
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "expert-bot-api-00125-9md",  
        "service_name": "expert-bot-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "2025-08-05 15:08:01,792 - root - ERROR - Error publicando a Pub/Sub: 403 User not authorized to perform this action.",
    "timestamp": "2025-08-05T15:08:01.792389Z"        
  },
  {
    "insertId": "68921e51000c165893162782",
    "labels": {
      "instanceId": "0069c7a988139d0881bf0ab749c491a87937f653435e87d348e2300ee13adb7d56f2599fa95510ea593ec3629300279354d32fcffc063c16bfecfebba1ab0f8d2652278fae9d0c957d2be60e8ff815"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstdout",
    "receiveTimestamp": "2025-08-05T15:08:01.858797768Z",
    "resource": {
      "labels": {
        "configuration_name": "expert-bot-api",       
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "expert-bot-api-00125-9md",  
        "service_name": "expert-bot-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "2025-08-05 15:08:01,792 - root - ERROR - Error Pub/Sub - Intento 3: 403 User not authorized to perform this action.",
    "timestamp": "2025-08-05T15:08:01.792152Z"        
  },
  {
    "insertId": "68921e4f0009022b0740be28",
    "labels": {
      "instanceId": "0069c7a988139d0881bf0ab749c491a87937f653435e87d348e2300ee13adb7d56f2599fa95510ea593ec3629300279354d32fcffc063c16bfecfebba1ab0f8d2652278fae9d0c957d2be60e8ff815"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstdout",
    "receiveTimestamp": "2025-08-05T15:07:59.857518908Z",
    "resource": {
      "labels": {
        "configuration_name": "expert-bot-api",       
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "expert-bot-api-00125-9md",  
        "service_name": "expert-bot-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "2025-08-05 15:07:59,591 - root - ERROR - Error Pub/Sub - Intento 2: 403 User not authorized to perform this action.",
    "timestamp": "2025-08-05T15:07:59.590379Z"        
  },
  {
    "insertId": "68921e4e000603fda2a55573",
    "labels": {
      "instanceId": "0069c7a988139d0881bf0ab749c491a87937f653435e87d348e2300ee13adb7d56f2599fa95510ea593ec3629300279354d32fcffc063c16bfecfebba1ab0f8d2652278fae9d0c957d2be60e8ff815"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstdout",
    "receiveTimestamp": "2025-08-05T15:07:58.527744951Z",
    "resource": {
      "labels": {
        "configuration_name": "expert-bot-api",       
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "expert-bot-api-00125-9md",  
        "service_name": "expert-bot-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "2025-08-05 15:07:58,395 - root - ERROR - Error Pub/Sub - Intento 1: 403 User not authorized to perform this action.",
    "timestamp": "2025-08-05T15:07:58.394237Z"        
  },
  {
    "insertId": "68921e4e0002175ab372ec91",
    "labels": {
      "instanceId": "0069c7a988139d0881bf0ab749c491a87937f653435e87d348e2300ee13adb7d56f2599fa95510ea593ec3629300279354d32fcffc063c16bfecfebba1ab0f8d2652278fae9d0c957d2be60e8ff815"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstdout",
    "receiveTimestamp": "2025-08-05T15:07:58.194766428Z",
    "resource": {
      "labels": {
        "configuration_name": "expert-bot-api",       
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "expert-bot-api-00125-9md",  
        "service_name": "expert-bot-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "2025-08-05 15:07:58,138 - root - INFO - ? Perfil empresarial actualizado para testing_production_user_2025 en Firestore (ambas colecciones) y BigQuery",
    "timestamp": "2025-08-05T15:07:58.137050Z"        
  },
  {
    "insertId": "68921e4e000216fd9048074c",
    "labels": {
      "instanceId": "0069c7a988139d0881bf0ab749c491a87937f653435e87d348e2300ee13adb7d56f2599fa95510ea593ec3629300279354d32fcffc063c16bfecfebba1ab0f8d2652278fae9d0c957d2be60e8ff815"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstdout",
    "receiveTimestamp": "2025-08-05T15:07:58.194766428Z",
    "resource": {
      "labels": {
        "configuration_name": "expert-bot-api",       
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "expert-bot-api-00125-9md",  
        "service_name": "expert-bot-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "2025-08-05 15:07:58,138 - root - INFO - ? Colecci?n user_profiles_enriched actualizada en Firestore: testing_production_user_2025",
    "timestamp": "2025-08-05T15:07:58.136957Z"        
  },
  {
    "insertId": "68921e4e0000f892acc95d87",
    "labels": {
      "instanceId": "0069c7a988139d0881bf0ab749c491a87937f653435e87d348e2300ee13adb7d56f2599fa95510ea593ec3629300279354d32fcffc063c16bfecfebba1ab0f8d2652278fae9d0c957d2be60e8ff815"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstdout",
    "receiveTimestamp": "2025-08-05T15:07:58.194766428Z",
    "resource": {
      "labels": {
        "configuration_name": "expert-bot-api",       
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "expert-bot-api-00125-9md",  
        "service_name": "expert-bot-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "Job ID: dff1a1e9-f8be-421e-854e-14e33d9d8229",
    "timestamp": "2025-08-05T15:07:58.063634Z"        
  },
  {
    "insertId": "68921e4e0000f88d7986d98d",
    "labels": {
      "instanceId": "0069c7a988139d0881bf0ab749c491a87937f653435e87d348e2300ee13adb7d56f2599fa95510ea593ec3629300279354d32fcffc063c16bfecfebba1ab0f8d2652278fae9d0c957d2be60e8ff815"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstdout",
    "receiveTimestamp": "2025-08-05T15:07:58.194766428Z",
    "resource": {
      "labels": {
        "configuration_name": "expert-bot-api",       
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "expert-bot-api-00125-9md",  
        "service_name": "expert-bot-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "Location: None",
    "timestamp": "2025-08-05T15:07:58.063629Z"        
  },
  {
    "insertId": "68921e4e0000f878f8f46bb5",
    "labels": {
      "instanceId": "0069c7a988139d0881bf0ab749c491a87937f653435e87d348e2300ee13adb7d56f2599fa95510ea593ec3629300279354d32fcffc063c16bfecfebba1ab0f8d2652278fae9d0c957d2be60e8ff815"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstdout",
    "receiveTimestamp": "2025-08-05T15:07:58.194766428Z",
    "resource": {
      "labels": {
        "configuration_name": "expert-bot-api",       
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "expert-bot-api-00125-9md",  
        "service_name": "expert-bot-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "2025-08-05 15:07:58,064 - root - ERROR - Error insertando/actualizando perfil en BigQuery para testing_production_user_2025: 400 POST https://bigquery.googleapis.com/bigquery/v2/projects/smatwatt/jobs?prettyPrint=false: Invalid value for type: BOOLEAN is not a valid value",
    "timestamp": "2025-08-05T15:07:58.063608Z"        
  },
  {
    "insertId": "68921e4d000ed70c00fbabe3",
    "labels": {
      "instanceId": "0069c7a988139d0881bf0ab749c491a87937f653435e87d348e2300ee13adb7d56f2599fa95510ea593ec3629300279354d32fcffc063c16bfecfebba1ab0f8d2652278fae9d0c957d2be60e8ff815"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstdout",
    "receiveTimestamp": "2025-08-05T15:07:58.194766428Z",
    "resource": {
      "labels": {
        "configuration_name": "expert-bot-api",       
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "expert-bot-api-00125-9md",  
        "service_name": "expert-bot-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "2025-08-05 15:07:57,973 - root - INFO - ? Documento d1c9e6c4-f81a-4e73-9702-f5061618479a logueado en BigQuery",
    "timestamp": "2025-08-05T15:07:57.972556Z"        
  },
  {
    "insertId": "68921e4d0009ae87ca3c53da",
    "labels": {
      "instanceId": "0069c7a988139d0881bf0ab749c491a87937f653435e87d348e2300ee13adb7d56f2599fa95510ea593ec3629300279354d32fcffc063c16bfecfebba1ab0f8d2652278fae9d0c957d2be60e8ff815"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstdout",
    "receiveTimestamp": "2025-08-05T15:07:57.860892254Z",
    "resource": {
      "labels": {
        "configuration_name": "expert-bot-api",       
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "expert-bot-api-00125-9md",  
        "service_name": "expert-bot-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "2025-08-05 15:07:57,635 - root - INFO - ? Documento empresarial subido: gs://smatwatt-model-exports-smatwatt-final/users/testing_production_user_2025/invoices/2025/08/05/0fe2f0c3-d7b3-43fe-8a82-0219ac41f9ba-fed199f9-test_factura.pdf",
    "timestamp": "2025-08-05T15:07:57.634503Z"        
  },
  {
    "insertId": "68921e4d00066f2e70e89af1",
    "labels": {
      "instanceId": "0069c7a988139d0881bf0ab749c491a87937f653435e87d348e2300ee13adb7d56f2599fa95510ea593ec3629300279354d32fcffc063c16bfecfebba1ab0f8d2652278fae9d0c957d2be60e8ff815"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstdout",
    "receiveTimestamp": "2025-08-05T15:07:57.526728851Z",
    "resource": {
      "labels": {
        "configuration_name": "expert-bot-api",       
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "expert-bot-api-00125-9md",  
        "service_name": "expert-bot-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "2025-08-05 15:07:57,422 - root - INFO - ? Gemini Vision exitoso - Intento 1",
    "timestamp": "2025-08-05T15:07:57.421678Z"        
  },
  {
    "insertId": "68921e430009349438aaeafa",
    "labels": {
      "instanceId": "0069c7a988139d0881bf0ab749c491a87937f653435e87d348e2300ee13adb7d56f2599fa95510ea593ec3629300279354d32fcffc063c16bfecfebba1ab0f8d2652278fae9d0c957d2be60e8ff815"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstdout",
    "receiveTimestamp": "2025-08-05T15:07:47.869515961Z",
    "resource": {
      "labels": {
        "configuration_name": "expert-bot-api",       
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "expert-bot-api-00125-9md",  
        "service_name": "expert-bot-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "2025-08-05 15:07:47,603 - root - INFO - ? Intento 1 - Procesando con Gemini Vision empresarial",
    "timestamp": "2025-08-05T15:07:47.603284Z"        
  },
  {
    "insertId": "68921e4300092c3f2c5763d1",
    "labels": {
      "instanceId": "0069c7a988139d0881bf0ab749c491a87937f653435e87d348e2300ee13adb7d56f2599fa95510ea593ec3629300279354d32fcffc063c16bfecfebba1ab0f8d2652278fae9d0c957d2be60e8ff815"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstdout",
    "receiveTimestamp": "2025-08-05T15:07:47.869515961Z",
    "resource": {
      "labels": {
        "configuration_name": "expert-bot-api",       
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "expert-bot-api-00125-9md",  
        "service_name": "expert-bot-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "2025-08-05 15:07:47,601 - root - INFO - ? Iniciando procesamiento OCR empresarial",     
    "timestamp": "2025-08-05T15:07:47.601151Z"        
  },
  {
    "insertId": "68921e4300092b20781ec567",
    "labels": {
      "instanceId": "0069c7a988139d0881bf0ab749c491a87937f653435e87d348e2300ee13adb7d56f2599fa95510ea593ec3629300279354d32fcffc063c16bfecfebba1ab0f8d2652278fae9d0c957d2be60e8ff815"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstdout",
    "receiveTimestamp": "2025-08-05T15:07:47.869515961Z",
    "resource": {
      "labels": {
        "configuration_name": "expert-bot-api",       
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "expert-bot-api-00125-9md",  
        "service_name": "expert-bot-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "2025-08-05 15:07:47,601 - root - INFO - ? AILearningService Empresarial inicializado correctamente",
    "timestamp": "2025-08-05T15:07:47.600864Z"        
  },
  {
    "insertId": "68921e4300092adf7207a1cb",
    "labels": {
      "instanceId": "0069c7a988139d0881bf0ab749c491a87937f653435e87d348e2300ee13adb7d56f2599fa95510ea593ec3629300279354d32fcffc063c16bfecfebba1ab0f8d2652278fae9d0c957d2be60e8ff815"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstdout",
    "receiveTimestamp": "2025-08-05T15:07:47.869515961Z",
    "resource": {
      "labels": {
        "configuration_name": "expert-bot-api",       
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "expert-bot-api-00125-9md",  
        "service_name": "expert-bot-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "2025-08-05 15:07:47,601 - root - INFO - ? Tabla AI empresarial ai_business_metrics ya existe",
    "timestamp": "2025-08-05T15:07:47.600799Z"        
  },
  {
    "insertId": "68921e4300078f97165d7f0e",
    "labels": {
      "instanceId": "0069c7a988139d0881bf0ab749c491a87937f653435e87d348e2300ee13adb7d56f2599fa95510ea593ec3629300279354d32fcffc063c16bfecfebba1ab0f8d2652278fae9d0c957d2be60e8ff815"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstdout",
    "receiveTimestamp": "2025-08-05T15:07:47.537565577Z",
    "resource": {
      "labels": {
        "configuration_name": "expert-bot-api",       
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "expert-bot-api-00125-9md",  
        "service_name": "expert-bot-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "2025-08-05 15:07:47,495 - root - INFO - ? Tabla AI empresarial ai_predictions ya existe",
    "timestamp": "2025-08-05T15:07:47.495511Z"        
  },
  {
    "insertId": "68921e43000634b9433825e5",
    "labels": {
      "instanceId": "0069c7a988139d0881bf0ab749c491a87937f653435e87d348e2300ee13adb7d56f2599fa95510ea593ec3629300279354d32fcffc063c16bfecfebba1ab0f8d2652278fae9d0c957d2be60e8ff815"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstdout",
    "receiveTimestamp": "2025-08-05T15:07:47.537565577Z",
    "resource": {
      "labels": {
        "configuration_name": "expert-bot-api",       
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "expert-bot-api-00125-9md",  
        "service_name": "expert-bot-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "2025-08-05 15:07:47,406 - root - INFO - ? Tabla AI empresarial ai_user_patterns ya existe",
    "timestamp": "2025-08-05T15:07:47.406713Z"        
  },
  {
    "insertId": "68921e4300047e83767d1e12",
    "labels": {
      "instanceId": "0069c7a988139d0881bf0ab749c491a87937f653435e87d348e2300ee13adb7d56f2599fa95510ea593ec3629300279354d32fcffc063c16bfecfebba1ab0f8d2652278fae9d0c957d2be60e8ff815"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstdout",
    "receiveTimestamp": "2025-08-05T15:07:47.537565577Z",
    "resource": {
      "labels": {
        "configuration_name": "expert-bot-api",       
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "expert-bot-api-00125-9md",  
        "service_name": "expert-bot-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "2025-08-05 15:07:47,294 - root - INFO - ? Tabla AI empresarial ai_sentiment_analysis ya existe",
    "timestamp": "2025-08-05T15:07:47.294531Z"        
  },
  {
    "insertId": "68921e430002cbe5349855c7",
    "labels": {
      "instanceId": "0069c7a988139d0881bf0ab749c491a87937f653435e87d348e2300ee13adb7d56f2599fa95510ea593ec3629300279354d32fcffc063c16bfecfebba1ab0f8d2652278fae9d0c957d2be60e8ff815"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstdout",
    "receiveTimestamp": "2025-08-05T15:07:47.203677600Z",
    "resource": {
      "labels": {
        "configuration_name": "expert-bot-api",       
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "expert-bot-api-00125-9md",  
        "service_name": "expert-bot-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "2025-08-05 15:07:47,183 - root - INFO - ? EnergyService Empresarial inicializado correctamente",
    "timestamp": "2025-08-05T15:07:47.183269Z"        
  },
  {
    "insertId": "68921e430002c91eebf29fdc",
    "labels": {
      "instanceId": "0069c7a988139d0881bf0ab749c491a87937f653435e87d348e2300ee13adb7d56f2599fa95510ea593ec3629300279354d32fcffc063c16bfecfebba1ab0f8d2652278fae9d0c957d2be60e8ff815"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstdout",
    "receiveTimestamp": "2025-08-05T15:07:47.203677600Z",
    "resource": {
      "labels": {
        "configuration_name": "expert-bot-api",       
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "expert-bot-api-00125-9md",  
        "service_name": "expert-bot-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "2025-08-05 15:07:47,182 - root - INFO - ? Servicios GCP inicializados - Intento 1",     
    "timestamp": "2025-08-05T15:07:47.182558Z"        
  },
  {
    "insertId": "68921e430002752398ec7c23",
    "labels": {
      "instanceId": "0069c7a988139d0881bf0ab749c491a87937f653435e87d348e2300ee13adb7d56f2599fa95510ea593ec3629300279354d32fcffc063c16bfecfebba1ab0f8d2652278fae9d0c957d2be60e8ff815"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstdout",
    "receiveTimestamp": "2025-08-05T15:07:47.203677600Z",
    "resource": {
      "labels": {
        "configuration_name": "expert-bot-api",       
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "expert-bot-api-00125-9md",  
        "service_name": "expert-bot-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "2025-08-05 15:07:47,161 - expert_bot_api.energy_routes - INFO - Acceso an?nimo a energy endpoint: expert_energy_routes.upload_consumption_data",
    "timestamp": "2025-08-05T15:07:47.161059Z"        
  },
  {
    "insertId": "68921e43000274c44dd4c0b3",
    "labels": {
      "instanceId": "0069c7a988139d0881bf0ab749c491a87937f653435e87d348e2300ee13adb7d56f2599fa95510ea593ec3629300279354d32fcffc063c16bfecfebba1ab0f8d2652278fae9d0c957d2be60e8ff815"
    },
    "logName": "projects/smatwatt/logs/run.googleapis.com%2Fstdout",
    "receiveTimestamp": "2025-08-05T15:07:47.203677600Z",
    "resource": {
      "labels": {
        "configuration_name": "expert-bot-api",       
        "location": "europe-west1",
        "project_id": "smatwatt",
        "revision_name": "expert-bot-api-00125-9md",  
        "service_name": "expert-bot-api"
      },
      "type": "cloud_run_revision"
    },
    "textPayload": "2025-08-05 15:07:47,161 - expert_bot_api - INFO - Request: POST /api/v1/energy/consumption - IP: 169.254.169.126",
    "timestamp": "2025-08-05T15:07:47.160964Z"        
  }
]
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\DOCUMENTACION Y SCRPT\MINISERVICIOS_SCRIPS\VERIFICACION REAL ENDOPOIN PRODUCCION>