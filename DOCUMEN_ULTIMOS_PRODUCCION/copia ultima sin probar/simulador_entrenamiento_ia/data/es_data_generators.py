# data/es_data_generators.py
# Generadores de datos españoles realistas para el simulador

import random
import json
import os
from faker import Faker
from datetime import datetime, timedelta
from typing import Dict, Any, List

# Configurar Faker para España
fake = Faker("es_ES")

# === DATOS DE REFERENCIA DEL MERCADO ESPAÑOL ===

COMPANIAS_ELECTRICAS = [
    "Iberdrola",
    "Endesa",
    "Naturgy",
    "EDP",
    "Repsol",
    "TotalEnergies",
    "Holaluz",
    "Som Energia",
]

PROVINCIAS_ESPANOLAS = {
    "28": "Madrid",
    "08": "Barcelona",
    "46": "Valencia",
    "41": "Sevilla",
    "48": "Bilbao",
    "50": "Zaragoza",
    "29": "Málaga",
    "35": "Las Palmas",
    "38": "Santa Cruz de Tenerife",
    "07": "Palma de Mallorca",
}

TIPOS_VIVIENDA = ["apartment", "house", "chalet", "duplex", "studio"]

TIPOS_TARIFA = ["2.0TD", "3.0TD", "PVPC", "2.1TD", "6.1TD"]

# Rangos realistas de consumo por tipo de vivienda y habitantes
CONSUMO_RANGES = {
    "studio": {"min": 80, "max": 150},
    "apartment": {"min": 120, "max": 300},
    "house": {"min": 200, "max": 450},
    "chalet": {"min": 300, "max": 600},
    "duplex": {"min": 250, "max": 500},
}

# Potencias contratadas estándar en España
POTENCIAS_ESTANDAR = [3.45, 4.6, 5.75, 6.9, 9.2, 11.5, 14.49, 17.3]


def generate_realistic_profile_data() -> Dict[str, Any]:
    """
    Genera datos de perfil realistas que coinciden exactamente con el esquema del backend.
    Basado en patrones reales del mercado eléctrico español.
    """
    # Seleccionar tipo de vivienda y habitantes
    home_type = random.choice(TIPOS_VIVIENDA)
    num_inhabitants = random.randint(1, 6)

    # Ajustar consumo según tipo de vivienda y habitantes
    base_range = CONSUMO_RANGES[home_type]
    inhabitants_factor = 0.7 + (num_inhabitants * 0.15)  # Más habitantes = más consumo

    kwh_min = base_range["min"] * inhabitants_factor
    kwh_max = base_range["max"] * inhabitants_factor
    kwh = round(random.uniform(kwh_min, kwh_max), 2)

    # Seleccionar potencia apropiada según consumo
    if kwh < 150:
        potencia = random.choice([3.45, 4.6])
    elif kwh < 300:
        potencia = random.choice([4.6, 5.75, 6.9])
    elif kwh < 450:
        potencia = random.choice([6.9, 9.2, 11.5])
    else:
        potencia = random.choice([9.2, 11.5, 14.49])

    # Calcular coste realista (precio por kWh + término fijo)
    precio_kwh = random.uniform(0.12, 0.28)  # Rango real en España 2024-2025
    termino_fijo = potencia * random.uniform(2.8, 4.2)  # Término fijo por potencia
    coste_total = round((kwh * precio_kwh) + termino_fijo, 2)

    # Seleccionar provincia y código postal
    cp_prefix = random.choice(list(PROVINCIAS_ESPANOLAS.keys()))

    # Generar fecha de emisión reciente
    fecha_emision = fake.date_between(start_date="-3M", end_date="today")

    return {
        "kwh_consumidos": kwh,
        "potencia_contratada_kw": potencia,
        "coste_total": coste_total,
        "tariff_name_from_invoice": f"Tarifa {random.choice(TIPOS_TARIFA)}",
        "comercializadora": random.choice(COMPANIAS_ELECTRICAS),
        "home_type": home_type,
        "num_inhabitants": num_inhabitants,
        "post_code_prefix": cp_prefix,
        "provincia": PROVINCIAS_ESPANOLAS[cp_prefix],
        "fecha_emision": fecha_emision.strftime("%Y-%m-%d"),
        "periodo_facturacion": "mensual",
        "tipo_contador": random.choice(["inteligente", "tradicional"]),
        "bono_social": (
            random.choice([True, False]) if random.random() < 0.15 else False
        ),
    }


def generate_synthetic_user_id() -> str:
    """Genera un ID de usuario sintético único."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    random_suffix = random.randint(1000, 9999)
    return f"sim_user_{timestamp}_{random_suffix}"


def load_chat_messages() -> List[str]:
    """Carga mensajes de chat desde el archivo JSON."""
    try:
        messages_file = os.path.join(os.path.dirname(__file__), "chat_messages.json")
        with open(messages_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("messages", [])
    except FileNotFoundError:
        # Mensajes por defecto si no existe el archivo
        return [
            "¿Puedes ayudarme a entender mi factura de la luz?",
            "¿Cuál es la mejor tarifa para mi consumo?",
            "¿Cómo puedo ahorrar en mi factura eléctrica?",
            "¿Qué diferencia hay entre PVPC y tarifa libre?",
            "¿Conviene cambiar de comercializadora?",
        ]


def generate_random_message() -> str:
    """Genera un mensaje aleatorio de la base de datos."""
    messages = load_chat_messages()
    return random.choice(messages)


def generate_user_context(profile_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Genera un contexto de usuario completo para las peticiones de chat.
    Simula el formato esperado por el endpoint /message/v2
    """
    return {
        "user_profile": profile_data,
        "session_id": f"sim_session_{random.randint(100000, 999999)}",
        "timestamp": datetime.now().isoformat(),
        "user_preferences": {
            "language": "es",
            "notifications": random.choice([True, False]),
            "data_sharing": random.choice([True, False]),
        },
        "device_info": {
            "platform": random.choice(["web", "mobile", "tablet"]),
            "user_agent": fake.user_agent(),
        },
    }


def generate_batch_profiles(num_profiles: int) -> List[Dict[str, Any]]:
    """Genera un lote de perfiles de usuario."""
    profiles = []
    for _ in range(num_profiles):
        profile = generate_realistic_profile_data()
        profile["user_id"] = generate_synthetic_user_id()
        profiles.append(profile)
    return profiles


# === FUNCIONES DE VALIDACIÓN ===


def validate_profile_data(profile_data: Dict[str, Any]) -> bool:
    """Valida que los datos del perfil cumplan con el esquema esperado."""
    required_fields = [
        "kwh_consumidos",
        "potencia_contratada_kw",
        "coste_total",
        "tariff_name_from_invoice",
        "comercializadora",
        "home_type",
        "num_inhabitants",
        "post_code_prefix",
        "fecha_emision",
    ]

    for field in required_fields:
        if field not in profile_data:
            return False

    # Validaciones de rango
    if not (50 <= profile_data["kwh_consumidos"] <= 1000):
        return False

    if profile_data["potencia_contratada_kw"] not in POTENCIAS_ESTANDAR:
        return False

    if not (1 <= profile_data["num_inhabitants"] <= 10):
        return False

    return True


# === FUNCIONES DE TESTING ===

if __name__ == "__main__":
    # Generar y validar algunos perfiles de ejemplo
    print("🧪 Testing del generador de datos españoles...")

    for i in range(5):
        profile = generate_realistic_profile_data()
        user_id = generate_synthetic_user_id()
        message = generate_random_message()
        context = generate_user_context(profile)

        print(f"\n--- Perfil {i+1} ---")
        print(f"User ID: {user_id}")
        print(f"Consumo: {profile['kwh_consumidos']} kWh")
        print(f"Potencia: {profile['potencia_contratada_kw']} kW")
        print(f"Comercializadora: {profile['comercializadora']}")
        print(f"Provincia: {profile['provincia']}")
        print(f"Mensaje: {message}")
        print(f"Válido: {validate_profile_data(profile)}")

    print(f"\n✅ Test completado. Generador funcionando correctamente.")
