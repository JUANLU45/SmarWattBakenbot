# Documentación Técnica y Funcional del Sistema SmarWatt

## 1. Arquitectura General

El sistema SmarWatt opera sobre una arquitectura de microservicios robusta, diseñada para la escalabilidad y la especialización de tareas. Los dos componentes principales son:

-   **`expert_bot_api`**: Actúa como el *cerebro orquestador* (backend for frontend). Gestiona todas las interacciones directas con el usuario, maneja la lógica de las conversaciones y orquesta las llamadas a otros servicios.
-   **`energy_ia_api`**: Es el *núcleo de inteligencia artificial*. Contiene la lógica de negocio pesada, los algoritmos de recomendación, y es el único servicio que interactúa directamente con las APIs de IA de Google Cloud (como Natural Language y, en el futuro, Vertex AI).

Esta separación garantiza que la experiencia de usuario sea fluida y rápida, mientras que los procesos de IA complejos se ejecutan en un servicio optimizado para ello.

---

## 2. Microservicio: `expert_bot_api`

**Responsabilidad Principal:** Gestionar la lógica de la conversación y el perfil del usuario.

### Descripción de Endpoints

| Método | Endpoint | Autenticación | Descripción Funcional |
| :--- | :--- | :--- | :--- |
| `POST` | `/session/start` | Requerida | Inicia una nueva sesión de chat. Devuelve un `session_id` y un mensaje de bienvenida personalizado. **Inicia una tarea asíncrona para sincronizar el perfil del usuario de Firestore a BigQuery.** |
| `POST` | `/message` | Requerida | Recibe un mensaje del usuario. Orquesta la llamada al `energy_ia_api` para obtener una respuesta inteligente y registra la interacción en BigQuery. |
| `DELETE` | `/conversation/<id>` | Requerida | Marca una conversación como eliminada en BigQuery (soft delete). Devuelve un mensaje de confirmación: `{"status": "success", "message": "La conversación ha sido eliminada correctamente."}`. |
| `POST` | `/consumption` | Requerida | Gestiona la subida de una factura. Llama a `EnergyService` para procesar el archivo. **Inicia una tarea asíncrona para sincronizar el perfil.** Devuelve: `{"status": "success", "message": "Factura recibida. Te notificaremos..."}`. |
| `POST` | `/manual-data` | Requerida | Permite al usuario introducir datos de consumo manualmente. **Inicia una tarea asíncrona para sincronizar el perfil.** Devuelve: `{"status": "success", "message": "Datos guardados correctamente."}`. |
| `GET` | `/users/profile` | Requerida | Obtiene el perfil energético completo y los datos del usuario desde Firestore. Es utilizado por `energy_ia_api` para obtener el contexto necesario para las recomendaciones. |

---

## 3. Microservicio: `energy_ia_api`

**Responsabilidad Principal:** Ejecutar todos los análisis de datos e inteligencia artificial.

### Descripción de Endpoints

| Método | Endpoint | Autenticación | Descripción Funcional |
| :--- | :--- | :--- | :--- |
| `GET` | `/tariffs/recommendations` | Requerida | **Endpoint principal del recomendador.** Obtiene el perfil del usuario desde `expert_bot_api`, consulta las tarifas en BigQuery y aplica el algoritmo de recomendación para devolver la mejor opción y alternativas. |
| `GET` | `/tariffs/market-data` | Requerida | Devuelve todas las tarifas activas y actualizadas desde la tabla `market_electricity_tariffs` en BigQuery. |
| `POST` | `/api/v1/analysis/sentiment` | Interna (Servicio-a-Servicio) | **Endpoint del Análisis de Sentimiento.** Recibe un texto, llama al `VertexAIService` para obtener un análisis real de Google Cloud AI y devuelve el resultado estructurado. |
| `POST` | `/admin/tariffs/add` | Admin Requerida | Permite a un administrador añadir una nueva tarifa eléctrica directamente a la base de datos de BigQuery. |
| `POST` | `/admin/tariffs/batch-add` | Admin Requerida | Permite a un administrador añadir múltiples tarifas en un solo lote. |

---

## 4. Integración de Inteligencia Artificial

### 4.1. Análisis de Sentimiento (100% Real)

El análisis de sentimiento es un proceso real, no simulado, que sigue este flujo:

1.  **Orquestación (`expert_bot_api`):** Cuando un usuario envía un mensaje, el `ChatService` lanza una tarea asíncrona al `AILearningService`.
2.  **Llamada a IA (`expert_bot_api` -> `energy_ia_api`):** El `AILearningService` realiza una llamada HTTP segura al endpoint `/api/v1/analysis/sentiment` en `energy_ia_api`, enviando el texto a analizar.
3.  **Análisis Real (`energy_ia_api`):** El `VertexAIService` recibe la petición y utiliza el cliente de **Google Cloud Natural Language API** (`language_v1`) para realizar un análisis de sentimiento real y robusto del texto.
4.  **Respuesta y Persistencia:** `energy_ia_api` devuelve el resultado (score, magnitud, etiqueta) a `AILearningService`, que finalmente lo registra de forma estructurada en la tabla `ai_sentiment_analysis` de BigQuery para su posterior análisis y reentrenamiento.

### 4.2. Recomendador de Tarifas (Modo Híbrido: Matemático + IA)

El sistema de recomendación está diseñado para funcionar en un **modo híbrido**, garantizando que **siempre ofrezca recomendaciones de alta calidad**, incluso si los modelos avanzados de Vertex AI están desconectados para ahorrar costes.

#### **Funcionamiento con Vertex AI Desconectado (Modo Actual de Producción)**

Este es el modo por defecto, optimizado para dar el máximo valor con el mínimo coste.

1.  **Análisis Matemático y Estadístico:** El `TariffRecommenderService` obtiene las tarifas actualizadas de BigQuery y el perfil de consumo del usuario.
2.  **Algoritmo de Coste:** Aplica un **algoritmo matemático preciso** para calcular el coste anual estimado de **cada una** de las tarifas del mercado para ese perfil de usuario específico.
3.  **Score de Idoneidad:** Calcula un "score de idoneidad" basado en reglas de negocio expertas (ej. un usuario con alto consumo en horas punta se beneficia más de tarifas con discriminación horaria).
4.  **Ranking y Respuesta:** El sistema ordena las tarifas combinando el **coste anual (menor es mejor)** y el **score de idoneidad (mayor es mejor)**, devolviendo la recomendación óptima y las mejores alternativas.

> **Garantía de Funcionamiento:** Este enfoque es **perfectamente funcional y robusto por sí mismo**. No depende de Vertex AI para ofrecer recomendaciones valiosas y precisas, basadas en datos reales del mercado y un análisis determinístico.

#### **Funcionamiento con Vertex AI Conectado**

Cuando la variable de entorno `VERTEX_AI_ENABLED` se activa en el despliegue, el sistema enriquece su análisis sin cambiar el flujo principal:

1.  **Análisis Adicional:** Además del análisis matemático, el `TariffRecommenderService` llama al `VertexAIService`.
2.  **Insights de ML:** El `VertexAIService` (que estaría conectado a un modelo entrenado) proporcionaría insights adicionales, como la **probabilidad de que al usuario le guste una tarifa** o la **predicción de su consumo futuro**.
3.  **Recomendación Enriquecida:** El resultado del modelo de IA se utiliza para **refinar el ranking** y añadir "insights de IA" a la recomendación final que se presenta al usuario.

La diferencia para el usuario final se resume en una mayor personalización y precisión, pero la funcionalidad base siempre está garantizada.

### 4.3. Aprendizaje Automático (Feedback Loop)

El sistema está preparado para el aprendizaje y la mejora continua:

1.  **Recopilación de Datos:** Cada interacción, recomendación, análisis de sentimiento y feedback del usuario se almacena de forma estructurada en tablas dedicadas en BigQuery (`feedback_log`, `recommendation_log`, etc.).
2.  **Reentrenamiento:** Estos datasets son la base para reentrenar y perfeccionar los modelos de IA en Vertex AI. El `AILearningService` contiene la lógica para procesar este feedback y, en futuras implementaciones, disparar los pipelines de reentrenamiento.

Este ciclo de retroalimentación asegura que el sistema se vuelva más inteligente y preciso con cada interacción del usuario.
