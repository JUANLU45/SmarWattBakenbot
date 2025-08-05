PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\ACTUALIZAR TARIFAS ESIOS> gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=energy-ia-api" --limit=50 --format="table(timestamp,severity,textPayload)" --project=smatwatt        
TIMESTAMP                    SEVERITY  TEXT_PAYLOAD
2025-08-02T20:02:28.688029Z            [2025-08-02 20:02:26 +0000] [30] [INFO] Booting worker with pid: 30
2025-08-02T20:00:53.688111Z            [2025-08-02 20:00:53 +0000] [3] [ERROR] Worker (pid:16) was sent SIGKILL! Perhaps out of memory?   
2025-08-02T20:00:37.527801Z            [2025-08-02 20:00:37 +0000] [16] [INFO] Worker exiting (pid: 16)
2025-08-02T20:00:37.527797Z            SystemExit: 1
2025-08-02T20:00:37.527794Z                sys.exit(1)
2025-08-02T20:00:37.527792Z              File "/opt/venv/lib/python3.11/site-packages/gunicorn/workers/base.py", line 204, in handle_abort
2025-08-02T20:00:37.527789Z              File "src/python/grpcio/grpc/_cython/_cygrpc/completion_queue.pyx.pxi", line 61, in grpc._cython.cygrpc._next
2025-08-02T20:00:37.527786Z              File "src/python/grpcio/grpc/_cython/_cygrpc/completion_queue.pyx.pxi", line 80, in grpc._cython.cygrpc._internal_latent_event
2025-08-02T20:00:37.527783Z              File "src/python/grpcio/grpc/_cython/_cygrpc/completion_queue.pyx.pxi", line 97, in grpc._cython.cygrpc._latent_event
2025-08-02T20:00:37.527780Z              File "src/python/grpcio/grpc/_cython/_cygrpc/channel.pyx.pxi", line 205, in grpc._cython.cygrpc._next_call_event
2025-08-02T20:00:37.527777Z              File "src/python/grpcio/grpc/_cython/_cygrpc/channel.pyx.pxi", line 211, in grpc._cython.cygrpc._next_call_event
2025-08-02T20:00:37.527774Z              File "src/python/grpcio/grpc/_cython/_cygrpc/channel.pyx.pxi", line 388, in grpc._cython.cygrpc.SegregatedCall.next_event
2025-08-02T20:00:37.527772Z                   
     ^^^^^^^^^^^^^^^^^
2025-08-02T20:00:37.527769Z                event = call.next_event()
2025-08-02T20:00:37.527766Z              File "/opt/venv/lib/python3.11/site-packages/grpc/_channel.py", line 1162, in _blocking
2025-08-02T20:00:37.527763Z                   
           ^^^^^^^^^^^^^^^
2025-08-02T20:00:37.527759Z                state, call = self._blocking(
2025-08-02T20:00:37.527756Z              File "/opt/venv/lib/python3.11/site-packages/grpc/_channel.py", line 1189, in with_call
2025-08-02T20:00:37.527753Z                   
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-08-02T20:00:37.527750Z                response, call = self._thunk(new_method).with_call(
2025-08-02T20:00:37.527748Z              File "/opt/venv/lib/python3.11/site-packages/grpc/_interceptor.py", line 315, in continuation    
2025-08-02T20:00:37.527745Z                   
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-08-02T20:00:37.527706Z                response = continuation(client_call_details, request)
2025-08-02T20:00:37.527703Z              File "/opt/venv/lib/python3.11/site-packages/google/ai/generativelanguage_v1beta/services/generative_service/transports/grpc.py", line 79, in intercept_unary_unary
2025-08-02T20:00:37.527699Z                   
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^  
2025-08-02T20:00:37.527696Z                call = self._interceptor.intercept_unary_unary(  
2025-08-02T20:00:37.527692Z              File "/opt/venv/lib/python3.11/site-packages/grpc/_interceptor.py", line 329, in _with_call      
2025-08-02T20:00:37.527689Z                   
                      ^^^^^^^^^^^^^^^^        
2025-08-02T20:00:37.527686Z                response, ignored_call = self._with_call(        
2025-08-02T20:00:37.527683Z              File "/opt/venv/lib/python3.11/site-packages/grpc/_interceptor.py", line 277, in __call__        
2025-08-02T20:00:37.527681Z                   
    ^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-08-02T20:00:37.527678Z                return callable_(*args, **kwargs)
2025-08-02T20:00:37.527674Z              File "/opt/venv/lib/python3.11/site-packages/google/api_core/grpc_helpers.py", line 76, in error_remapped_callable
2025-08-02T20:00:37.527671Z                   
    ^^^^^^^^^^^^^^^^^^^^^
2025-08-02T20:00:37.527668Z                return func(*args, **kwargs)
2025-08-02T20:00:37.527665Z              File "/opt/venv/lib/python3.11/site-packages/google/api_core/timeout.py", line 130, in func_with_timeout
2025-08-02T20:00:37.527661Z                   
      ^^^^^^^^
2025-08-02T20:00:37.527658Z                result = target()
2025-08-02T20:00:37.527655Z              File "/opt/venv/lib/python3.11/site-packages/google/api_core/retry/retry_unary.py", line 147, in retry_target
2025-08-02T20:00:37.527651Z                   
    ^^^^^^^^^^^^^
2025-08-02T20:00:37.527648Z                return retry_target(
2025-08-02T20:00:37.527644Z              File "/opt/venv/lib/python3.11/site-packages/google/api_core/retry/retry_unary.py", line 294, in retry_wrapped_func
2025-08-02T20:00:37.527640Z                   
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-08-02T20:00:37.527636Z                return wrapped_func(*args, **kwargs)
2025-08-02T20:00:37.527633Z              File "/opt/venv/lib/python3.11/site-packages/google/api_core/gapic_v1/method.py", line 131, in __call__
2025-08-02T20:00:37.527630Z                   
        ^^^^
2025-08-02T20:00:37.527628Z                response = rpc(
2025-08-02T20:00:37.527625Z              File "/opt/venv/lib/python3.11/site-packages/google/ai/generativelanguage_v1beta/services/generative_service/client.py", line 835, in generate_content
2025-08-02T20:00:37.527621Z                   
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^        
2025-08-02T20:00:37.527618Z                response = self._client.generate_content(        
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\ACTUALIZAR TARIFAS ESIOS>    
 -api AND severity>=ERROR" --limit=20 --format="table(timestamp,severity,textPayload)" --project=smatwatt
TIMESTAMP                    SEVERITY  TEXT_PAYLOAD
2025-08-02T20:00:37.527528Z  ERROR     Traceback (most recent call last):
                                         File "/opt/venv/lib/python3.11/site-packages/gunicorn/workers/sync.py", line 134, in handle      
                                           self.handle_request(listener, req, client, addr) 
                                         File "/opt/venv/lib/python3.11/site-packages/gunicorn/workers/sync.py", line 177, in handle_request
                                           respiter = self.wsgi(environ, resp.start_response)
2025-08-02T20:00:06.782540Z  ERROR
2025-08-02T18:46:20.778181Z  ERROR     Traceback (most recent call last):
                                         File "/opt/venv/lib/python3.11/site-packages/gunicorn/workers/sync.py", line 134, in handle      
                                           self.handle_request(listener, req, client, addr) 
                                         File "/opt/venv/lib/python3.11/site-packages/gunicorn/workers/sync.py", line 177, in handle_request
                                           respiter = self.wsgi(environ, resp.start_response)
2025-08-02T18:45:49.559848Z  ERROR
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\ACTUALIZAR TARIFAS ESIOS>     
on AND resource.labels.service_name=energy-ia-api" --limit=10 --project=smatwatt --format="value(textPayload)"
[2025-08-02 20:02:26 +0000] [30] [INFO] Booting worker with pid: 30
[2025-08-02 20:00:53 +0000] [3] [ERROR] Worker (pid:16) was sent SIGKILL! Perhaps out of memory?
[2025-08-02 20:00:37 +0000] [16] [INFO] Worker exiting (pid: 16)
SystemExit: 1
    sys.exit(1)
  File "/opt/venv/lib/python3.11/site-packages/gunicorn/workers/base.py", line 204, in handle_abort
  File "src/python/grpcio/grpc/_cython/_cygrpc/completion_queue.pyx.pxi", line 61, in grpc._cython.cygrpc._next
  File "src/python/grpcio/grpc/_cython/_cygrpc/completion_queue.pyx.pxi", line 80, in grpc._cython.cygrpc._internal_latent_event
  File "src/python/grpcio/grpc/_cython/_cygrpc/completion_queue.pyx.pxi", line 97, in grpc._cython.cygrpc._latent_event
  File "src/python/grpcio/grpc/_cython/_cygrpc/channel.pyx.pxi", line 205, in grpc._cython.cygrpc._next_call_event
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\ACTUALIZAR TARIFAS ESIOS>     
api" --limit=30 --project=smatwatt --format="table(timestamp,severity,textPayload)"        
TIMESTAMP                    SEVERITY  TEXT_PAYLOAD
2025-08-02T20:02:28.688029Z            [2025-08-02 20:02:26 +0000] [30] [INFO] Booting worker with pid: 30
2025-08-02T20:00:53.688111Z            [2025-08-02 20:00:53 +0000] [3] [ERROR] Worker (pid:16) was sent SIGKILL! Perhaps out of memory?   
2025-08-02T20:00:37.527801Z            [2025-08-02 20:00:37 +0000] [16] [INFO] Worker exiting (pid: 16)
2025-08-02T20:00:37.527797Z            SystemExit: 1
2025-08-02T20:00:37.527794Z                sys.exit(1)
2025-08-02T20:00:37.527792Z              File "/opt/venv/lib/python3.11/site-packages/gunicorn/workers/base.py", line 204, in handle_abort
2025-08-02T20:00:37.527789Z              File "src/python/grpcio/grpc/_cython/_cygrpc/completion_queue.pyx.pxi", line 61, in grpc._cython.cygrpc._next
2025-08-02T20:00:37.527786Z              File "src/python/grpcio/grpc/_cython/_cygrpc/completion_queue.pyx.pxi", line 80, in grpc._cython.cygrpc._internal_latent_event
2025-08-02T20:00:37.527783Z              File "src/python/grpcio/grpc/_cython/_cygrpc/completion_queue.pyx.pxi", line 97, in grpc._cython.cygrpc._latent_event
2025-08-02T20:00:37.527780Z              File "src/python/grpcio/grpc/_cython/_cygrpc/channel.pyx.pxi", line 205, in grpc._cython.cygrpc._next_call_event
2025-08-02T20:00:37.527777Z              File "src/python/grpcio/grpc/_cython/_cygrpc/channel.pyx.pxi", line 211, in grpc._cython.cygrpc._next_call_event
2025-08-02T20:00:37.527774Z              File "src/python/grpcio/grpc/_cython/_cygrpc/channel.pyx.pxi", line 388, in grpc._cython.cygrpc.SegregatedCall.next_event
2025-08-02T20:00:37.527772Z                   
     ^^^^^^^^^^^^^^^^^
2025-08-02T20:00:37.527769Z                event = call.next_event()
2025-08-02T20:00:37.527766Z              File "/opt/venv/lib/python3.11/site-packages/grpc/_channel.py", line 1162, in _blocking
2025-08-02T20:00:37.527763Z                   
           ^^^^^^^^^^^^^^^
2025-08-02T20:00:37.527759Z                state, call = self._blocking(
2025-08-02T20:00:37.527756Z              File "/opt/venv/lib/python3.11/site-packages/grpc/_channel.py", line 1189, in with_call
2025-08-02T20:00:37.527753Z                   
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-08-02T20:00:37.527750Z                response, call = self._thunk(new_method).with_call(
2025-08-02T20:00:37.527748Z              File "/opt/venv/lib/python3.11/site-packages/grpc/_interceptor.py", line 315, in continuation    
2025-08-02T20:00:37.527745Z                   
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-08-02T20:00:37.527706Z                response = continuation(client_call_details, request)
2025-08-02T20:00:37.527703Z              File "/opt/venv/lib/python3.11/site-packages/google/ai/generativelanguage_v1beta/services/generative_service/transports/grpc.py", line 79, in intercept_unary_unary
2025-08-02T20:00:37.527699Z                   
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^  
2025-08-02T20:00:37.527696Z                call = self._interceptor.intercept_unary_unary(  
2025-08-02T20:00:37.527692Z              File "/opt/venv/lib/python3.11/site-packages/grpc/_interceptor.py", line 329, in _with_call      
2025-08-02T20:00:37.527689Z                   
                      ^^^^^^^^^^^^^^^^        
2025-08-02T20:00:37.527686Z                response, ignored_call = self._with_call(        
2025-08-02T20:00:37.527683Z              File "/opt/venv/lib/python3.11/site-packages/grpc/_interceptor.py", line 277, in __call__        
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\ACTUALIZAR TARIFAS ESIOS>     