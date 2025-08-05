Paso 1: Añadir el Interruptor en el Archivo de Configuración
Abre el archivo energy_ia_api_COPY/app/config.py y añade esta línea para que la aplicación sepa leer el nuevo interruptor.

Python

# AÑADIR ESTA LÍNEA

USE_VERTEX_AI_RECOMMENDER = str(os.getenv('USE_VERTEX_AI_RECOMMENDER', 'false')).lower() in ('true', '1', 't')
Propósito: Permite que la aplicación lea la variable de entorno y la convierta en un True o False seguro.

Paso 2: Aplicar la Lógica Condicional en el Servicio
Abre energy_ia_api_COPY/app/services/vertex_ai_service.py y modifica la función que da las recomendaciones para que obedezca al interruptor.

Python

# DENTRO DEL EnterpriseVertexAIService

def get_tariff_recommendations(self, user_profile, consumption_data): # ... (todo tu código actual que calcula costes y el score de idoneidad) ... # Esta parte no cambia y es la base de todo.

    # === INICIO DE LOS CAMBIOS ===

    # Leemos el interruptor desde la configuración
    use_vertex_ai = current_app.config['USE_VERTEX_AI_RECOMMENDER']

    if not use_vertex_ai:
        # MODO ESTÁNDAR (SIN VERTEX AI):
        # Ordenamos las tarifas por el 'suitability_score' que ya hemos calculado.
        sorted_tariffs = sorted(all_tariffs_with_scores, key=lambda x: x['suitability_score'], reverse=True)
        # Devolvemos las 3 mejores. Esto es robusto y no tiene coste de IA.
        return {"recommendations": sorted_tariffs[:3], "source": "standard_logic"}

    # MODO PREMIUM (CON VERTEX AI):
    # Si el interruptor está activado, se ejecuta el código que ya tienes.
    # ... (tu código actual que llama al endpoint de Vertex AI) ...
    # ...

    return {"recommendations": vertex_results, "source": "vertex_ai_enhanced"}

    # === FIN DE LOS CAMBIOS ===

Propósito: Esta es la bifurcación. El código tomará un camino u otro basándose en el interruptor. El camino "estándar" es 100% determinista y no llama a ninguna API externa de IA.

Paso 3: Actualizar el Comando de Despliegue
Finalmente, en tu archivo DEPLOY_COMMANDS_UPDATED.md, modifica el comando para energy-ia-api y añade la nueva variable de entorno, poniéndola en false para empezar.

Bash

# Comando para energy-ia-api

--set-env-vars="...CORS_ORIGINS=<https://smarwatt.com,SECRET_KEY=...,USE_VERTEX_AI_RECOMMENDER=false>" # ^^^^^ AÑADIR ESTO
Propósito: Inyecta la configuración en el entorno de producción, diciéndole a tu aplicación qué modo de recomendación usar al arrancar.

Conclusión
