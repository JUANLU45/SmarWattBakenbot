Parte 1: La Inteligencia en el Backend (El "Cuándo" Proponer la Subida)
La decisión de pedir la factura no debe ser aleatoria, debe ser una conclusión lógica basada en la conversación. La lógica para esto debe residir en el generative_chat_service.py, dentro del método send_message.

El proceso sería el siguiente:

Análisis de Intención (Ya lo tienes): El sistema ya analiza el mensaje del usuario para detectar la intención (ahorro, consulta, etc.).

Verificación de Contexto (Paso Clave): Antes de decidir, el servicio debe hacerse dos preguntas:

¿El usuario está pidiendo algo que necesita los datos de una factura para ser respondido con precisión? (Ej: "cuánto puedo ahorrar", "por qué pago tanto").

¿Ya tenemos datos de una factura reciente y completa para este usuario?

Para implementar esto, modificaríamos el generative_chat_service.py para incluir una nueva función de decisión:

Python

# Dentro de la clase EnterpriseGenerativeChatService en generative_chat_service.py

def \_should_request_invoice(self, user_message: str, user_context: Dict[str, Any]) -> bool:
"""
Determina si es el momento oportuno para solicitar la factura al usuario.
""" # Condición 1: El usuario no tiene datos completos. # El dato `data_completeness` ya lo calculas en chatbot_routes.py. # Si la completitud es baja (ej. < 70%), es un buen candidato.
is_data_incomplete = user_context.get("data_completeness", 0) < 70

    # Condición 2: El tema de la conversación lo justifica.
    # Palabras clave que indican una necesidad de análisis.
    keywords = ["ahorrar", "factura", "consumo", "coste", "caro", "pagando", "analizar"]
    is_topic_relevant = any(keyword in user_message.lower() for keyword in keywords)

    # Condición 3: No hemos preguntado recientemente.
    # (Lógica a implementar para evitar ser pesado, ej. usando el historial del chat)

    # Decisión final: Solo si los datos son incompletos Y el tema es relevante.
    return is_data_incomplete and is_topic_relevant

Luego, en la función send_message, usarías este método para decidir qué hacer:

Python

# Dentro del método send_message en generative_chat_service.py

# ... (después de obtener el user_context)

if self.\_should_request_invoice(user_message, user_context): # Si se debe pedir la factura, NO se envía el mensaje a Gemini. # En su lugar, se construye una respuesta estructurada para el frontend. # (Ver Parte 2 a continuación)
else: # Si no, se procede con el flujo normal de la conversación. # ... (código existente que envía el mensaje a Gemini)
Este enfoque garantiza que el bot no será pesado. Solo pedirá la factura cuando sea estrictamente necesario y justificado por la conversación, aportando valor en lugar de ser una molestia.
