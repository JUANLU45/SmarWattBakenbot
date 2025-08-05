# src/profile_generator.py
# Lógica para crear perfiles de usuario sintéticos

import sys
import os
import logging
from typing import Dict, Any, List

# Añadir el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.es_data_generators import (
    generate_realistic_profile_data,
    generate_synthetic_user_id,
    generate_user_context,
    validate_profile_data,
    generate_batch_profiles,
)

logger = logging.getLogger(__name__)


class ProfileGenerator:
    """
    Generador de perfiles de usuario sintéticos para el simulador de entrenamiento.
    Utiliza datos realistas del mercado español.
    """

    def __init__(self):
        """Inicializa el generador de perfiles."""
        self.generated_profiles = []
        logger.info("ProfileGenerator inicializado")

    def generate_single_profile(self) -> Dict[str, Any]:
        """
        Genera un único perfil de usuario sintético.

        Returns:
            Diccionario con datos del perfil validados
        """
        try:
            # Generar datos básicos del perfil
            profile_data = generate_realistic_profile_data()
            user_id = generate_synthetic_user_id()

            # Crear perfil completo
            complete_profile = {
                "user_id": user_id,
                "profile_data": profile_data,
                "user_context": generate_user_context(profile_data),
                "generated_at": user_id.split("_")[1]
                + "_"
                + user_id.split("_")[2],  # timestamp
                "is_simulation": True,
            }

            # Validar datos
            if not validate_profile_data(profile_data):
                logger.warning(f"Perfil generado no válido para usuario {user_id}")
                return self.generate_single_profile()  # Reintentar

            # Almacenar perfil generado
            self.generated_profiles.append(complete_profile)

            logger.debug(
                f"Perfil generado para usuario {user_id}: {profile_data['comercializadora']}, {profile_data['kwh_consumidos']} kWh"
            )

            return complete_profile

        except Exception as e:
            logger.error(f"Error generando perfil: {e}")
            raise

    def generate_batch_profiles(self, num_profiles: int) -> List[Dict[str, Any]]:
        """
        Genera un lote de perfiles de usuario.

        Args:
            num_profiles: Número de perfiles a generar

        Returns:
            Lista de perfiles generados
        """
        logger.info(f"Generando lote de {num_profiles} perfiles...")

        profiles = []
        for i in range(num_profiles):
            try:
                profile = self.generate_single_profile()
                profiles.append(profile)

                if (i + 1) % 10 == 0:
                    logger.info(f"Generados {i + 1}/{num_profiles} perfiles")

            except Exception as e:
                logger.error(f"Error generando perfil {i + 1}: {e}")
                continue

        logger.info(f"✅ Lote completado: {len(profiles)} perfiles generados")
        return profiles

    def generate_diverse_profiles(self, num_profiles: int) -> List[Dict[str, Any]]:
        """
        Genera perfiles diversos para cubrir diferentes casos de uso.

        Args:
            num_profiles: Número total de perfiles a generar

        Returns:
            Lista de perfiles diversos
        """
        profiles = []

        # Calcular distribución
        profiles_per_type = max(1, num_profiles // 8)

        scenarios = [
            {
                "home_type": "apartment",
                "num_inhabitants": 1,
                "description": "Joven profesional",
            },
            {
                "home_type": "apartment",
                "num_inhabitants": 2,
                "description": "Pareja sin hijos",
            },
            {
                "home_type": "apartment",
                "num_inhabitants": 4,
                "description": "Familia urbana",
            },
            {
                "home_type": "house",
                "num_inhabitants": 3,
                "description": "Familia suburbana",
            },
            {
                "home_type": "house",
                "num_inhabitants": 5,
                "description": "Familia numerosa",
            },
            {
                "home_type": "chalet",
                "num_inhabitants": 2,
                "description": "Pareja senior",
            },
            {
                "home_type": "chalet",
                "num_inhabitants": 4,
                "description": "Familia acomodada",
            },
            {"home_type": "studio", "num_inhabitants": 1, "description": "Estudiante"},
        ]

        for scenario in scenarios:
            for _ in range(profiles_per_type):
                try:
                    profile = self.generate_single_profile()

                    # Ajustar según escenario
                    profile["profile_data"]["home_type"] = scenario["home_type"]
                    profile["profile_data"]["num_inhabitants"] = scenario[
                        "num_inhabitants"
                    ]
                    profile["scenario_description"] = scenario["description"]

                    profiles.append(profile)

                except Exception as e:
                    logger.error(
                        f"Error generando perfil para escenario {scenario['description']}: {e}"
                    )
                    continue

        # Completar con perfiles aleatorios si es necesario
        remaining = num_profiles - len(profiles)
        if remaining > 0:
            additional_profiles = self.generate_batch_profiles(remaining)
            profiles.extend(additional_profiles)

        logger.info(f"✅ Perfiles diversos generados: {len(profiles)} total")
        return profiles[:num_profiles]  # Asegurar número exacto

    def get_profile_statistics(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas de los perfiles generados.

        Returns:
            Diccionario con estadísticas
        """
        if not self.generated_profiles:
            return {"total_profiles": 0}

        # Extraer datos para estadísticas
        comercializadoras = [
            p["profile_data"]["comercializadora"] for p in self.generated_profiles
        ]
        provincias = [p["profile_data"]["provincia"] for p in self.generated_profiles]
        tipos_vivienda = [
            p["profile_data"]["home_type"] for p in self.generated_profiles
        ]
        consumos = [
            p["profile_data"]["kwh_consumidos"] for p in self.generated_profiles
        ]

        # Calcular estadísticas
        stats = {
            "total_profiles": len(self.generated_profiles),
            "comercializadoras": {
                com: comercializadoras.count(com) for com in set(comercializadoras)
            },
            "provincias": {prov: provincias.count(prov) for prov in set(provincias)},
            "tipos_vivienda": {
                tipo: tipos_vivienda.count(tipo) for tipo in set(tipos_vivienda)
            },
            "consumo_promedio": round(sum(consumos) / len(consumos), 2),
            "consumo_min": min(consumos),
            "consumo_max": max(consumos),
        }

        return stats

    def export_profiles(self, filename: str) -> bool:
        """
        Exporta los perfiles generados a un archivo JSON.

        Args:
            filename: Nombre del archivo de salida

        Returns:
            True si la exportación fue exitosa
        """
        try:
            import json

            with open(filename, "w", encoding="utf-8") as f:
                json.dump(
                    self.generated_profiles,
                    f,
                    indent=2,
                    ensure_ascii=False,
                    default=str,
                )

            logger.info(f"✅ Perfiles exportados a {filename}")
            return True

        except Exception as e:
            logger.error(f"❌ Error exportando perfiles: {e}")
            return False

    def clear_profiles(self):
        """Limpia los perfiles generados de la memoria."""
        self.generated_profiles.clear()
        logger.info("Perfiles limpiados de la memoria")


# Funciones de conveniencia
def create_profile_generator() -> ProfileGenerator:
    """Crea una instancia del generador de perfiles."""
    return ProfileGenerator()


def generate_training_profiles(num_profiles: int) -> List[Dict[str, Any]]:
    """
    Función de conveniencia para generar perfiles de entrenamiento.

    Args:
        num_profiles: Número de perfiles a generar

    Returns:
        Lista de perfiles generados
    """
    generator = create_profile_generator()
    return generator.generate_diverse_profiles(num_profiles)


# Test del módulo
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    print("🧪 Testando ProfileGenerator...")

    # Crear generador
    generator = create_profile_generator()

    # Generar algunos perfiles de prueba
    test_profiles = generator.generate_batch_profiles(5)

    print(f"\n📊 Perfiles generados: {len(test_profiles)}")

    # Mostrar estadísticas
    stats = generator.get_profile_statistics()
    print(f"\n📈 Estadísticas:")
    print(f"  Total: {stats['total_profiles']}")
    print(f"  Consumo promedio: {stats['consumo_promedio']} kWh")
    print(f"  Comercializadoras: {list(stats['comercializadoras'].keys())}")

    # Exportar perfiles de prueba
    generator.export_profiles("test_profiles.json")

    print("\n✅ Test completado correctamente")
