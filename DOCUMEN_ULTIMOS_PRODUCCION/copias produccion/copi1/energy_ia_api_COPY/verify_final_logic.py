# VERIFICACIÓN FINAL DE LA LÓGICA CORREGIDA
import re

# Mensajes del usuario para verificar
test_messages = [
    # ❌ ESTOS NO DEBEN ACTIVAR EL RECOMENDADOR
    "Dime el precio de la energía",
    "Cuanto cuesta el kWh ahora",
    "Precio actual de la electricidad",
    "Qué precio tiene la energía",
    "Factura muy cara este mes",
    "Consumo mucho en casa",
    # ✅ ESTOS SÍ DEBEN ACTIVAR EL RECOMENDADOR
    "Recomiéndame una tarifa mejor",
    "Qué tarifas hay disponibles",
    "Cambiar de tarifa",
    "Otras opciones de tarifas",
    "Ahorrar con tarifa diferente",
    "Comparar tarifas",
    "Cuál es la mejor tarifa para mi",
    "Tarifas disponibles ahora",
]


# Nueva lógica CORREGIDA
def should_consult_expert_bot_new(user_message):
    message_lower = user_message.lower()

    # Palabras clave específicas para recomendaciones (SIN FALSOS POSITIVOS)
    recommendation_keywords = [
        "recomienda",
        "recomiendame",
        "recomiéndame",
        "recomendación",
        "recomendaciones",
        "mejor tarifa",
        "qué tarifa",
        "qué tarifas",
        "que tarifas",
        "cuál tarifa",
        "cual tarifa",
        "cuáles tarifas",
        "cuales tarifas",
        "dime tarifas",
        "cambiar tarifa",
        "cambio tarifa",
        "cambio de tarifa",
        "cambiar de tarifa",
        "comparar tarifas",
        "comparar tarifa",
        "alternativas tarifas",
        "otras tarifas",
        "otras opciones tarifas",
    ]

    # Palabras clave de ahorro con contexto específico
    savings_with_context = [
        "ahorrar tarifa",
        "ahorro tarifa",
        "ahorrar con tarifa",
        "ahorro con tarifa",
        "ahorrar cambiando",
        "ahorro cambiando",
    ]

    # Verificar recomendaciones específicas
    has_recommendation_intent = any(
        keyword in message_lower for keyword in recommendation_keywords
    )

    # Verificar ahorro con contexto específico
    has_savings_intent = any(
        keyword in message_lower for keyword in savings_with_context
    )

    # Verificar solicitudes directas de tarifas disponibles
    direct_tariff_requests = [
        "tarifas hay",
        "qué tarifas hay",
        "que tarifas hay",
        "tarifas existen",
        "tarifas disponibles",
        "opciones de tarifas",
        "opciones tarifas",
    ]

    has_direct_tariff_request = any(
        phrase in message_lower for phrase in direct_tariff_requests
    )

    # Condición robusta: SOLO consultar si hay intención clara de recomendación
    should_consult = bool(
        has_recommendation_intent or has_savings_intent or has_direct_tariff_request
    )

    return should_consult


print("🔍 VERIFICACIÓN FINAL DE LA LÓGICA CORREGIDA")
print("=" * 60)

no_debe_activar = []
si_debe_activar = []

for i, message in enumerate(test_messages):
    result = should_consult_expert_bot_new(message)
    print(f"{i+1:2d}. {'✅' if result else '❌'} {message}")

    if i < 6:  # Primeros 6 NO deben activar
        if result:
            no_debe_activar.append(message)
    else:  # Últimos SÍ deben activar
        if not result:
            si_debe_activar.append(message)

print(f"\n📊 RESULTADO FINAL:")
print(f"❌ Falsos positivos (NO deben activar pero activan): {len(no_debe_activar)}")
print(f"❌ Falsos negativos (SÍ deben activar pero no activan): {len(si_debe_activar)}")

if len(no_debe_activar) == 0 and len(si_debe_activar) == 0:
    print("🎉 ¡PERFECTO! La lógica funciona correctamente para todos los casos")
else:
    if no_debe_activar:
        print("⚠️ Problemas con falsos positivos:")
        for msg in no_debe_activar:
            print(f"   - {msg}")
    if si_debe_activar:
        print("⚠️ Problemas con falsos negativos:")
        for msg in si_debe_activar:
            print(f"   - {msg}")
