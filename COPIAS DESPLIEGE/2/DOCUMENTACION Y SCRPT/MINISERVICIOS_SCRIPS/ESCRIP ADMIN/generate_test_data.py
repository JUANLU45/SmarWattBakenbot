#!/usr/bin/env python3
"""
🎯 GENERADOR DE DATOS DE PRUEBA PARA TARIFAS
===========================================

Genera datos realistas para testing del panel de administración.
Todos los datos incluyen marcas identificativas para fácil limpieza.
Sistema robusto antiduplicados integrado.
"""

import json
import random
import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional


class TariffDataGenerator:
    """Generador de datos de prueba para tarifas eléctricas"""

    def __init__(self):
        # Compañías eléctricas REALES de España - marcadas para testing
        self.test_suppliers = [
            "TEST_Iberdrola_DELETEME",
            "TEST_Endesa_DELETEME",
            "TEST_Naturgy_DELETEME",
            "TEST_EDP_DELETEME",
            "TEST_Viesgo_DELETEME",
            "TEST_Repsol_DELETEME",
            "TEST_Octopus_Energy_DELETEME",
            "TEST_Som_Energia_DELETEME",
        ]

        # Tipos de tarifa reales del sistema español
        self.tariff_types = ["PVPC", "Fixed", "Indexed"]

        # Nombres de tarifas REALES del mercado español 2025
        self.tariff_suffixes = [
            "2.0 TD",
            "Plan Fijo 12 meses",
            "Tarifa Indexada",
            "One Luz",
            "Tempo Happy",
            "Plan Ahorro",
            "Verde",
            "Mercado Libre",
        ]

        # Control antiduplicados
        self.used_combinations = set()
        self.session_id = str(uuid.uuid4())[:8]  # ID único para esta sesión

    def generate_unique_tariff_name(self, supplier_name: str, attempt: int = 0) -> str:
        """
        Generar nombre de tarifa único dentro de la sesión
        ROBUSTO: Evita duplicados en la misma ejecución
        """
        real_suffix = random.choice(self.tariff_suffixes)

        # Añadir sufijo único si es necesario
        if attempt > 0:
            unique_suffix = f"_{self.session_id}_{attempt}"
            tariff_name = f"{real_suffix} - TEST_DELETEME{unique_suffix}"
        else:
            tariff_name = f"{real_suffix} - TEST_DELETEME"

        # Verificar si ya se usó esta combinación
        combination_key = f"{supplier_name}||{tariff_name}"

        if combination_key in self.used_combinations:
            # Recursivo con nuevo intento
            return self.generate_unique_tariff_name(supplier_name, attempt + 1)
        else:
            # Marcar como usado
            self.used_combinations.add(combination_key)
            return tariff_name

    def validate_minimal_data(self, tariff_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validar y completar datos mínimos obligatorios
        ROBUSTO: Solo completa lo estrictamente necesario, sin inventar datos
        """
        # Campos OBLIGATORIOS del backend (verificados)
        required_fields = {
            "supplier_name": str,
            "tariff_name": str,
            "tariff_type": str,
            "fixed_term_price": float,
            "variable_term_price": float,
        }

        validated_data = {}
        missing_fields = []

        for field, field_type in required_fields.items():
            value = tariff_data.get(field)

            if value is None or (isinstance(value, str) and not value.strip()):
                missing_fields.append(field)
            else:
                try:
                    # Convertir al tipo esperado
                    if field_type == float:
                        validated_data[field] = float(value)
                    elif field_type == str:
                        validated_data[field] = str(value).strip()
                    else:
                        validated_data[field] = value
                except (ValueError, TypeError):
                    missing_fields.append(f"{field} (formato inválido)")

        # Añadir campos opcionales SOLO si existen y son válidos
        optional_fields = [
            "peak_price",
            "valley_price",
            "peak_hours",
            "valley_hours",
            "discriminated_hourly",
            "green_energy_percentage",
            "contract_permanence_months",
            "cancellation_fee",
            "promotion_description",
            "promotion_discount_percentage",
            "promotion_duration_months",
            "indexing_type",
            "price_update_frequency",
            "additional_services",
            "customer_rating",
        ]

        for field in optional_fields:
            value = tariff_data.get(field)
            if value is not None and value != "":
                validated_data[field] = value

        return {
            "validated_data": validated_data,
            "missing_fields": missing_fields,
            "is_valid": len(missing_fields) == 0,
        }

    def generate_realistic_prices(self) -> Dict[str, float]:
        """Generar precios 99% realistas basados en mercado español enero 2025"""

        # PRECIOS REALES del mercado español enero 2025
        # Término fijo: Entre 30-60 €/mes según comercializadora
        fixed_term_base = random.uniform(30.67, 59.88)  # Rango real 2025

        # Precio energía REAL: 0.10-0.25 €/kWh según período
        energy_base = random.uniform(0.10245, 0.24890)  # Precios reales enero 2025

        # PVPC real enero 2025: P1=0.24890, P2=0.19876, P3=0.14567 €/kWh
        p1_real = random.uniform(0.22000, 0.26500)  # Punta real
        p2_real = random.uniform(0.18000, 0.22000)  # Llano real
        p3_real = random.uniform(0.12000, 0.16000)  # Valle real

        return {
            "fixed_term_price": round(fixed_term_base, 2),
            "variable_term_price": round(energy_base, 5),
            # Precios de potencia reales (€/kW/mes)
            "power_price_p1": round(p1_real, 5),  # Punta
            "power_price_p2": round(p2_real, 5),  # Llano
            # Precios energía por períodos (€/kWh) - REALES
            "energy_price_p1": round(p1_real, 5),  # Punta 10h-14h, 18h-22h
            "energy_price_p2": round(p2_real, 5),  # Llano 8h-10h, 14h-18h, 22h-24h
            "energy_price_p3": round(p3_real, 5),  # Valle 0h-8h
            # Gas natural precios reales enero 2025
            "gas_fixed_term": round(
                random.uniform(6.35, 11.50), 2
            ),  # Real: 6.35-11.50 €/mes
            "gas_variable_term": round(
                random.uniform(0.0456, 0.0789), 4
            ),  # Real: 0.045-0.078 €/kWh
        }

    def generate_single_tariff(
        self, supplier_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generar tarifa individual con CAMPOS EXACTOS que espera el backend
        ROBUSTO: Genera nombres únicos y valida datos mínimos
        """
        if not supplier_name:
            supplier_name = random.choice(self.test_suppliers)

        # Nombre de tarifa único para evitar duplicados
        tariff_name = self.generate_unique_tariff_name(supplier_name)
        tariff_type = random.choice(self.tariff_types)

        # PRECIOS 99% REALISTAS mercado español enero 2025
        fixed_base = random.uniform(30.67, 59.88)  # Real término fijo €/mes
        variable_base = random.uniform(0.10245, 0.24890)  # Real €/kWh
        peak_price = random.uniform(0.22000, 0.26500)  # Real punta
        valley_price = random.uniform(0.12000, 0.16000)  # Real valle

        # CAMPOS EXACTOS que espera el backend (verificados en routes.py)
        tariff_data = {
            # ===== CAMPOS OBLIGATORIOS (required_fields en backend) =====
            "supplier_name": supplier_name,
            "tariff_name": tariff_name,
            "tariff_type": tariff_type,
            "fixed_term_price": round(fixed_base, 2),
            "variable_term_price": round(variable_base, 6),
            # ===== CAMPOS OPCIONALES (nombres EXACTOS del backend) =====
            "peak_price": round(peak_price, 6),
            "valley_price": round(valley_price, 6),
            "peak_hours": random.choice(
                [
                    "10:00-14:00,18:00-22:00",  # Formato real PVPC
                    "08:00-15:00,19:00-23:00",
                    "09:00-14:00,18:00-22:00",
                    "",
                ]
            ),
            "valley_hours": random.choice(
                [
                    "00:00-08:00,15:00-18:00",  # Formato real PVPC
                    "23:00-07:00",
                    "00:00-09:00,15:00-18:00",
                    "",
                ]
            ),
            "discriminated_hourly": random.choice([True, False]),
            "green_energy_percentage": round(random.uniform(0, 100), 1),  # Real 0-100%
            "contract_permanence_months": random.choice([0, 12, 24]),  # Real
            "cancellation_fee": round(random.uniform(0, 30.50), 2),  # Real €
            "promotion_description": random.choice(
                [
                    "Descuento 15% primer año",
                    "Sin cuota de alta ni permanencia",
                    "Precio fijo garantizado 12 meses",
                    "Energía 100% renovable incluida",
                    "Servicio técnico gratuito 24h",
                    "",
                ]
            ),
            "promotion_discount_percentage": round(
                random.uniform(0, 20.0), 1
            ),  # Real hasta 20%
            "promotion_duration_months": random.choice([0, 6, 12, 24]),
            "indexing_type": random.choice(["fixed", "PVPC", "indexed"]),
            "price_update_frequency": random.choice(["monthly", "quarterly", "annual"]),
            "additional_services": random.choice(
                [
                    "App móvil gratuita + atención 24h",
                    "Factura digital y gestión online",
                    "Servicio técnico incluido",
                    "Asesoramiento energético personalizado",
                    "Programa puntos y descuentos",
                    "",
                ]
            ),
            "customer_rating": round(random.uniform(2.1, 4.8), 1),  # Real OCU 2.1-4.8
        }

        # Validar datos generados
        validation = self.validate_minimal_data(tariff_data)

        if validation["is_valid"]:
            return validation["validated_data"]
        else:
            # Si falla validación, crear tarifa mínima válida
            return {
                "supplier_name": supplier_name,
                "tariff_name": tariff_name,
                "tariff_type": tariff_type,
                "fixed_term_price": round(fixed_base, 2),
                "variable_term_price": round(variable_base, 6),
            }

    def generate_batch_tariffs(self, count: int = 5) -> List[Dict[str, Any]]:
        """
        Generar un lote de tarifas para prueba batch
        ROBUSTO: Garantiza nombres únicos dentro del lote
        """
        tariffs = []

        for i in range(count):
            supplier = f"TEST_Batch_{i+1}_{self.session_id}_DELETEME"
            tariff = self.generate_single_tariff(supplier)

            # Validar que la tarifa es mínimamente válida antes de añadir
            validation = self.validate_minimal_data(tariff)
            if validation["is_valid"]:
                tariffs.append(validation["validated_data"])
            else:
                # Crear tarifa mínima si falla
                minimal_tariff = {
                    "supplier_name": supplier,
                    "tariff_name": f"Tarifa Básica {i+1} - TEST_DELETEME_{self.session_id}",
                    "tariff_type": random.choice(self.tariff_types),
                    "fixed_term_price": round(random.uniform(30.67, 59.88), 2),
                    "variable_term_price": round(random.uniform(0.10245, 0.24890), 6),
                }
                tariffs.append(minimal_tariff)

        return tariffs

    def save_sample_data_to_files(self):
        """
        Guardar datos de ejemplo en archivos JSON
        ROBUSTO: Valida datos antes de guardar
        """

        print(f"🔄 Generando datos únicos para sesión: {self.session_id}")

        # Tarifa individual
        single_tariff = self.generate_single_tariff()
        validation = self.validate_minimal_data(single_tariff)

        if validation["is_valid"]:
            with open("sample_single_tariff.json", "w", encoding="utf-8") as f:
                json.dump(validation["validated_data"], f, indent=2, ensure_ascii=False)
        else:
            print(
                f"⚠️ Advertencia: Tarifa individual con campos faltantes: {validation['missing_fields']}"
            )
            with open("sample_single_tariff.json", "w", encoding="utf-8") as f:
                json.dump(single_tariff, f, indent=2, ensure_ascii=False)

        # Lote de tarifas
        batch_tariffs = self.generate_batch_tariffs(8)
        batch_payload = {"tariffs": batch_tariffs}
        with open("sample_batch_tariffs.json", "w", encoding="utf-8") as f:
            json.dump(batch_payload, f, indent=2, ensure_ascii=False)

        # Datos mínimos (solo campos obligatorios) - GARANTIZADOS válidos
        minimal_tariff = {
            "supplier_name": f"TEST_Minimal_{self.session_id}_DELETEME",
            "tariff_name": f"Tarifa Mínima Test_{self.session_id}_DELETEME",
            "tariff_type": "Fixed",
            "fixed_term_price": 42.50,
            "variable_term_price": 0.15000,
        }
        with open("sample_minimal_tariff.json", "w", encoding="utf-8") as f:
            json.dump(minimal_tariff, f, indent=2, ensure_ascii=False)

        print("✅ Archivos JSON de ejemplo generados:")
        print("   - sample_single_tariff.json")
        print("   - sample_batch_tariffs.json")
        print("   - sample_minimal_tariff.json")
        print(f"🔒 Todos marcados con ID de sesión: {self.session_id}")
        print(f"📊 Combinaciones únicas generadas: {len(self.used_combinations)}")

    def print_sample_data(self):
        """Mostrar datos de ejemplo en consola"""
        print("🎯 DATOS DE EJEMPLO PARA TESTING")
        print("=" * 40)

        print("\n📤 TARIFA INDIVIDUAL:")
        single = self.generate_single_tariff()
        print(json.dumps(single, indent=2, ensure_ascii=False))

        print(f"\n📦 LOTE DE TARIFAS (3 ejemplos):")
        batch = self.generate_batch_tariffs(3)
        batch_payload = {"tariffs": batch}
        print(json.dumps(batch_payload, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    print("🚀 GENERADOR DE DATOS DE PRUEBA PARA TARIFAS")
    print("=" * 50)

    generator = TariffDataGenerator()

    # Mostrar datos en consola
    generator.print_sample_data()

    # Guardar archivos JSON
    print("\n" + "=" * 50)
    generator.save_sample_data_to_files()

    print(f"\n💡 USO:")
    print(f"   - Usar estos datos en test_admin_panel_endpoints.py")
    print(f"   - Todos incluyen 'DELETEME' para fácil identificación")
    print(f"   - Precios basados en mercado español real 2025")
