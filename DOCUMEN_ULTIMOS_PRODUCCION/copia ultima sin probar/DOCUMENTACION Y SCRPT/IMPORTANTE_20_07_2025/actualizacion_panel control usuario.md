.Es muy importante muy importante utilizar. Utilizar las. De los componentes y los componentes que haya. Cambiar los nombres cambiar los nombres a los componentes y reutilizarlos no. Y té y pestañas nuevas A no ser que sea necesario. Necesario y no haya. Ya hechos componentes o pestañas Muy importante también verificar los endopoint en el archivoC:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\Y DOCUMENTACION\documentacion_para_fronten\endopin_final.md Ya que aquí puede ser que estén equivocados. Lo originales y los nombres correctos están en el archivo. Anterior.

Este es el documento maestro. La guía completa para tu equipo de frontend. El plano final para construir el panel de control energético más profesional y valioso posible, basado en la arquitectura robusta que has creado.

🚀 Guía Maestra de Implementación Definitiva: El Panel de Control Energético Profesional de Smarwatt
Filosofía Central: Este panel es un centro de mando de inteligencia financiera. No es un visor de datos. Su único propósito es convertir el análisis complejo del backend en decisiones estratégicas claras que le ahorren dinero al usuario. Cada píxel debe justificar su existencia aportando valor tangible.

1. Arquitectura del Panel: Dashboard Ejecutivo + 4 Centros de Análisis (Pestañas)
   La estructura es un Dashboard Principal para el diagnóstico ejecutivo inmediato, seguido de cuatro Pestañas que funcionan como centros de análisis y acción especializados.

2. Pantalla Principal: El Dashboard Ejecutivo
   La primera vista. Impecable, profesional y directa. Responde a las preguntas: "¿Cuál es mi estado financiero energético?" y "¿Cuál es mi acción más rentable ahora mismo?".

Tarjeta 1: Diagnóstico de Rendimiento Financiero 💡 (El KPI Principal)
Propósito: Mostrar el impacto económico final, el resultado.

Visualización:

Título: "Potencial de Optimización Anual"

Dato Principal (grande y claro): "220€"

Subtítulo: "Ahorro Estimado Identificado"

Barra de Progreso Profesional: "Nivel de Optimización Actual: 75%"

Fuente de Datos y Conexión:

Endpoint: GET /dashboard (expert-bot-api).

Lógica: Este es el endpoint maestro del panel. Al cargar la página, el frontend realiza una única llamada. El backend orquesta la información y devuelve en la respuesta el ahorro_potencial_anual y el nivel_optimizacion, ya calculados.

Tarjeta 2: Recomendación Estratégica 🎯
Propósito: Presentar la acción de mayor impacto como una decisión de negocio.

Visualización:

Título: "Línea de Actuación Prioritaria: Re-evaluación de Contrato Energético"

Descripción: "Su tarifa actual presenta un sobrecoste del 18% frente a la oferta óptima del mercado para su perfil de consumo."

Botón: Analizar Propuesta

Fuente de Datos y Conexión:

Endpoint: La información ya debe venir en la respuesta del GET /dashboard.

Lógica Frontend: Al hacer clic, se abre un modal (pop-up) que muestra una comparativa profesional: "Contrato Actual" vs. "Propuesta Optimizada", detallando precios, permanencia y ahorro.

Tarjeta 3: Benchmarking de Mercado 📊
Propósito: Ofrecer contexto competitivo.

Visualización:

Título: "Posicionamiento de Coste (Precio por kWh)"

Gráfico de barras: "Su Coste" vs. "Media de su Segmento" vs. "Mejor Oferta del Mercado".

Texto de conclusión: "Actualmente, su coste por kWh es un 18% superior a la media de hogares similares."

Fuente de Datos y Conexión:

Endpoint: Toda la información debe venir del GET /dashboard. El backend se encarga de calcular el coste del usuario y obtener los promedios del mercado desde el energy-ia-api.

3. Pestañas: Centros de Análisis y Acción
   Pestaña 1: "Análisis de Consumo y Costes" 📈
   Propósito: Herramientas de Business Intelligence para que el usuario entienda el "porqué" de sus gastos.

Componentes y Fuentes de Datos:

Desglose de Costes (Cost Breakdown):

Visualización: Gráfico de cascada (Término Potencia -> Término Consumo -> Impuestos -> Coste Total).

Endpoint: GET /dashboard. La respuesta debe incluir el desglose de la última factura.

Matriz Horaria de Consumo:

Visualización: Mapa de calor interactivo (Día vs. Hora).

Endpoint: GET /api/v1/energy/consumption/history (expert-bot-api). El frontend procesará el historial devuelto para construir el mapa de calor.

Histórico y Proyecciones:

Visualización: Gráfico de líneas con el coste de los últimos 12 meses y una proyección a 3 meses.

Endpoint: GET /api/v1/energy/consumption/history. El backend debe enriquecer la respuesta de este endpoint con una clave proyeccion calculada por el AILearningService.

Pestaña 2: "Plan de Optimización" ✅
Propósito: Un plan de acción con iniciativas estratégicas.

Componentes y Fuentes de Datos:

Lista de Iniciativas:

Visualización: Tarjetas con "Impacto Financiero Estimado" y "Complejidad de Implementación".

Iniciativa 1: Re-evaluación de Contrato:

Endpoint: GET /api/v1/energy/consumption/recommendations (expert-bot-api).

Iniciativa 2: Ajuste de Potencia:

Endpoint: GET /api/v1/energy/dashboard. El backend debe devolver la potencia_contratada y la potencia_maxima_demandada.

Iniciativa 3: Reasignación de Cargas de Consumo:

Endpoint: GET /api/v1/energy/consumption/history. El frontend identifica los picos en el historial.

Pestaña 3: "Mi Perfil y Documentación" 📂
Propósito: El centro de control de datos del usuario. Transparencia y gestión.

Componentes y Fuentes de Datos:

Gestión de Perfil Energético:

Visualización: Formulario para ver y actualizar los datos del perfil.

Endpoints:

Lectura: GET /api/v1/energy/users/profile (expert-bot-api).

Escritura (Actualización): PUT /api/v1/energy/consumption/update (expert-bot-api).

Archivo de Documentos:

Visualización: Listado de facturas subidas con fecha y estado.

Endpoint y Lógica (La Solución Definitiva y Verificada): El backend debe adaptar la respuesta del endpoint GET /api/v1/energy/users/profile para que, además de los datos del perfil, incluya una nueva clave uploaded_documents con la lista de documentos del usuario. Es la solución más eficiente y respeta la arquitectura final.

Generar Informe de Rendimiento (La Función Profesional para Compartir):

Visualización: Botón Generar Informe de Rendimiento.

Endpoint: POST /api/v1/energy/consumption/analyze (expert-bot-api).

Lógica: El frontend envía una petición a este endpoint solicitando un "informe para compartir". El backend genera el PDF o la imagen profesional con el resumen del ahorro y la reducción de CO2, y devuelve la URL para su descarga.

Pestaña 4: "Asesor Virtual" 🤖 (La Pestaña de Interacción Guiada)
Propósito: Unir la potencia del análisis de datos del panel con la inteligencia conversacional del chatbot. Guiar al usuario hacia las consultas de mayor valor.

Visualización: Dos columnas: a la izquierda, la interfaz del chat; a la derecha, una sección titulada "Consultas Inteligentes".

Componente "Consultas Inteligentes": Una lista de botones que inician conversaciones.

Botón: "Analizar mis recomendaciones de tarifa"

Endpoint: POST /message/v2 del microservicio energy-ia-api.

Lógica Frontend: Al hacer clic, el frontend envía una petición a este endpoint con el siguiente payload, usando el contexto de usuario que ya tiene cargado del dashboard:

JSON

{
"message": "Hola, explícame en detalle mis recomendaciones de tarifa actuales.",
"user_context": { ... } // Objeto completo de contexto del usuario
}
Botón: "Explicar mi consumo en horas punta"

Endpoint: POST /message/v2 del energy-ia-api.

Lógica Frontend: Misma lógica, con el message adaptado:

JSON

{
"message": "Analiza mi consumo en horas punta y explícame por qué es alto y cómo puedo reducirlo.",
"user_context": { ... }
}
Verificación Final: Esta implementación es perfecta y robusta. El endpoint POST /message/v2 está explícitamente diseñado para recibir el user_context directamente, lo que hace que esta interacción sea increíblemente eficiente y potente. Conecta de forma nativa los dos pilares de tu aplicación.
Es muy importante muy importante utilizar. Utilizar las. De los componentes y los componentes que haya. Cambiar los nombres cambiar los nombres a los componentes y reutilizarlos no. Y té y pestañas nuevas A no ser que sea necesario. Necesario y no haya. Ya hechos componentes o pestañasMuy importante también verificar los endopoint en el archivoC:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\Y DOCUMENTACION\documentacion_para_fronten\endopin_final.md Ya que aquí puede ser que estén equivocados. Lo originales y los nombres correctos están en el archivo. Anterior. Y recordar que la página del tiempo en la pestaña del tiempo, la pestaña que hay del tiempo de las 5 que hay la del tiempo se mantiene.
