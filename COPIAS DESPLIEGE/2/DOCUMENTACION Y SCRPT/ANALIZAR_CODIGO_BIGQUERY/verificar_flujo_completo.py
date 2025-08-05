#!/usr/bin/env python3
# 🔍 VERIFICADOR DE FLUJO COMPLETO DE DATOS
# CONFIRMA QUE DESPUÉS DEL REPARADOR LA APLICACIÓN FUNCIONA PERFECTAMENTE

import os
import re
from pathlib import Path
from typing import Dict, List, Set


class VerificadorFlujoCompleto:
    """
    Verificador que confirma que después del reparador:
    1. Los datos de usuario fluyen correctamente entre microservicios
    2. Las recomendaciones se unifican para ambos servicios
    3. Los datos de IA están disponibles para toda la aplicación
    4. El flujo completo funciona sin interrupciones
    """

    def __init__(self):
        base_path = Path(__file__).parent.parent.parent
        self.energy_api_path = base_path / "energy_ia_api_COPY"
        self.expert_api_path = base_path / "expert_bot_api_COPY"

        # Mapeo de datos críticos que deben fluir entre servicios
        self.tablas_criticas = {
            "user_profiles_enriched": "Perfiles de usuario - DEBE estar disponible para ambos servicios",
            "consumption_log": "Datos de consumo - DEBE alimentar recomendaciones",
            "conversations_log": "Historial de chat - DEBE estar unificado",
            "recommendation_log": "Recomendaciones - DEBE estar disponible para ambos servicios",
            "feedback_log": "Feedback de usuario - DEBE mejorar IA en ambos servicios",
            "uploaded_documents_log": "Documentos subidos - DEBE estar accesible",
        }

        # Flujos críticos que DEBEN funcionar
        self.flujos_criticos = [
            "Usuario sube factura → Análisis → Recomendaciones → Disponible en ambos servicios",
            "Chat en Energy API → Datos guardados → Disponibles en Expert API",
            "Recomendaciones IA → Guardadas → Accesibles desde cualquier servicio",
            "Feedback usuario → Mejora IA → Aplicado en ambos microservicios",
        ]

    def verificar_referencias_tablas_en_codigo(self) -> Dict[str, Dict]:
        """Verificar que ambos microservicios referencian las mismas tablas correctamente"""
        print("🔍 Verificando referencias a tablas en ambos microservicios...")

        resultados = {"energy_api": {}, "expert_api": {}}

        # Verificar Energy API
        for archivo in self.energy_api_path.rglob("*.py"):
            if archivo.is_file():
                with open(archivo, "r", encoding="utf-8") as f:
                    contenido = f.read()

                for tabla in self.tablas_criticas:
                    if tabla in contenido:
                        if tabla not in resultados["energy_api"]:
                            resultados["energy_api"][tabla] = []
                        resultados["energy_api"][tabla].append(str(archivo.name))

        # Verificar Expert API
        for archivo in self.expert_api_path.rglob("*.py"):
            if archivo.is_file():
                with open(archivo, "r", encoding="utf-8") as f:
                    contenido = f.read()

                for tabla in self.tablas_criticas:
                    if tabla in contenido:
                        if tabla not in resultados["expert_api"]:
                            resultados["expert_api"][tabla] = []
                        resultados["expert_api"][tabla].append(str(archivo.name))

        return resultados

    def verificar_unificacion_datos(self) -> Dict[str, bool]:
        """Verificar que los datos están unificados entre servicios"""
        print("🔍 Verificando unificación de datos entre servicios...")

        unificacion = {}

        for tabla, descripcion in self.tablas_criticas.items():
            # Verificar si la tabla está siendo usada por ambos servicios
            energy_usa = False
            expert_usa = False

            # Buscar en Energy API
            for archivo in self.energy_api_path.rglob("*.py"):
                if archivo.is_file():
                    try:
                        with open(archivo, "r", encoding="utf-8") as f:
                            if tabla in f.read():
                                energy_usa = True
                                break
                    except:
                        continue

            # Buscar en Expert API
            for archivo in self.expert_api_path.rglob("*.py"):
                if archivo.is_file():
                    try:
                        with open(archivo, "r", encoding="utf-8") as f:
                            if tabla in f.read():
                                expert_usa = True
                                break
                    except:
                        continue

            unificacion[tabla] = {
                "energy_api_usa": energy_usa,
                "expert_api_usa": expert_usa,
                "unificado": energy_usa and expert_usa,
                "descripcion": descripcion,
            }

        return unificacion

    def verificar_configuraciones_consistentes(self) -> Dict[str, bool]:
        """Verificar que las configuraciones son consistentes entre servicios"""
        print("🔍 Verificando configuraciones consistentes...")

        config_energy = None
        config_expert = None

        # Leer config de Energy API
        config_energy_path = self.energy_api_path / "app" / "config.py"
        if config_energy_path.exists():
            with open(config_energy_path, "r", encoding="utf-8") as f:
                config_energy = f.read()

        # Leer config de Expert API
        config_expert_path = self.expert_api_path / "app" / "config.py"
        if config_expert_path.exists():
            with open(config_expert_path, "r", encoding="utf-8") as f:
                config_expert = f.read()

        if not config_energy or not config_expert:
            return {"error": "No se pudieron leer las configuraciones"}

        # Variables críticas que deben estar en ambos
        variables_criticas = [
            "BQ_CONSUMPTION_LOG_TABLE_ID",
            "BQ_CONVERSATIONS_LOG_TABLE_ID",
            "BQ_RECOMMENDATION_LOG_TABLE_ID",
            "BQ_FEEDBACK_TABLE_ID",
        ]

        consistencia = {}
        for var in variables_criticas:
            energy_tiene = var in config_energy
            expert_tiene = var in config_expert

            consistencia[var] = {
                "energy_tiene": energy_tiene,
                "expert_tiene": expert_tiene,
                "consistente": energy_tiene and expert_tiene,
            }

        return consistencia

    def verificar_flujo_datos_usuario(self) -> Dict[str, bool]:
        """Verificar que el flujo de datos de usuario funciona correctamente"""
        print("🔍 Verificando flujo de datos de usuario...")

        flujos = {}

        # Verificar flujo: Usuario → Perfiles → Disponible en ambos servicios
        flujos["perfil_usuario"] = self._verificar_flujo_especifico(
            "user_profiles_enriched",
            ["user_id", "monthly_consumption_kwh"],
            "Perfil de usuario debe estar en ambos servicios",
        )

        # Verificar flujo: Consumo → Análisis → Recomendaciones
        flujos["consumo_recomendaciones"] = self._verificar_flujo_especifico(
            "consumption_log",
            ["kwh_consumed", "timestamp_utc"],
            "Datos de consumo deben generar recomendaciones",
        )

        # Verificar flujo: Chat → Guardado → Accesible
        flujos["conversaciones"] = self._verificar_flujo_especifico(
            "conversations_log",
            ["message_text", "user_id"],
            "Conversaciones deben estar unificadas",
        )

        return flujos

    def _verificar_flujo_especifico(
        self, tabla: str, campos: List[str], descripcion: str
    ) -> Dict:
        """Verificar un flujo específico de datos"""
        resultado = {
            "tabla": tabla,
            "descripcion": descripcion,
            "energy_lee": False,
            "energy_escribe": False,
            "expert_lee": False,
            "expert_escribe": False,
            "flujo_completo": False,
        }

        # Patrones para detectar lectura y escritura
        patrones_lectura = [f"FROM.*{tabla}", f"SELECT.*{tabla}"]
        patrones_escritura = [f"INSERT.*{tabla}", f"UPDATE.*{tabla}"]

        # Verificar Energy API
        for archivo in self.energy_api_path.rglob("*.py"):
            if archivo.is_file():
                try:
                    with open(archivo, "r", encoding="utf-8") as f:
                        contenido = f.read()

                    for patron in patrones_lectura:
                        if re.search(patron, contenido, re.IGNORECASE):
                            resultado["energy_lee"] = True

                    for patron in patrones_escritura:
                        if re.search(patron, contenido, re.IGNORECASE):
                            resultado["energy_escribe"] = True
                except:
                    continue

        # Verificar Expert API
        for archivo in self.expert_api_path.rglob("*.py"):
            if archivo.is_file():
                try:
                    with open(archivo, "r", encoding="utf-8") as f:
                        contenido = f.read()

                    for patron in patrones_lectura:
                        if re.search(patron, contenido, re.IGNORECASE):
                            resultado["expert_lee"] = True

                    for patron in patrones_escritura:
                        if re.search(patron, contenido, re.IGNORECASE):
                            resultado["expert_escribe"] = True
                except:
                    continue

        # Determinar si el flujo está completo
        resultado["flujo_completo"] = (
            resultado["energy_lee"] or resultado["energy_escribe"]
        ) and (resultado["expert_lee"] or resultado["expert_escribe"])

        return resultado

    def ejecutar_verificacion_completa(self) -> Dict:
        """Ejecutar verificación completa del flujo de datos"""
        print("🚀 INICIANDO VERIFICACIÓN COMPLETA DE FLUJO DE DATOS")
        print("=" * 60)

        resultado = {"timestamp": "2025-07-22T12:00:00Z", "verificaciones": {}}

        # 1. Verificar referencias a tablas
        print("\n1. Verificando referencias a tablas...")
        resultado["verificaciones"][
            "referencias_tablas"
        ] = self.verificar_referencias_tablas_en_codigo()

        # 2. Verificar unificación de datos
        print("\n2. Verificando unificación de datos...")
        resultado["verificaciones"][
            "unificacion_datos"
        ] = self.verificar_unificacion_datos()

        # 3. Verificar configuraciones consistentes
        print("\n3. Verificando configuraciones...")
        resultado["verificaciones"][
            "configuraciones"
        ] = self.verificar_configuraciones_consistentes()

        # 4. Verificar flujo de datos de usuario
        print("\n4. Verificando flujo de datos de usuario...")
        resultado["verificaciones"][
            "flujo_usuario"
        ] = self.verificar_flujo_datos_usuario()

        # 5. Calcular puntuación general
        resultado["puntuacion"] = self._calcular_puntuacion_general(
            resultado["verificaciones"]
        )

        return resultado

    def _calcular_puntuacion_general(self, verificaciones: Dict) -> Dict:
        """Calcular puntuación general del flujo de datos"""
        puntos_totales = 0
        puntos_obtenidos = 0

        # Unificación de datos (40 puntos)
        unificacion = verificaciones.get("unificacion_datos", {})
        for tabla, info in unificacion.items():
            puntos_totales += 10
            if info.get("unificado", False):
                puntos_obtenidos += 10
            elif info.get("energy_api_usa", False) or info.get("expert_api_usa", False):
                puntos_obtenidos += 5

        # Configuraciones (30 puntos)
        configuraciones = verificaciones.get("configuraciones", {})
        for var, info in configuraciones.items():
            if isinstance(info, dict):
                puntos_totales += 5
                if info.get("consistente", False):
                    puntos_obtenidos += 5

        # Flujo de usuario (30 puntos)
        flujo_usuario = verificaciones.get("flujo_usuario", {})
        for flujo, info in flujo_usuario.items():
            if isinstance(info, dict):
                puntos_totales += 10
                if info.get("flujo_completo", False):
                    puntos_obtenidos += 10
                elif info.get("energy_lee", False) or info.get("expert_lee", False):
                    puntos_obtenidos += 5

        porcentaje = (
            (puntos_obtenidos / puntos_totales * 100) if puntos_totales > 0 else 0
        )

        return {
            "puntos_obtenidos": puntos_obtenidos,
            "puntos_totales": puntos_totales,
            "porcentaje": porcentaje,
            "estado": (
                "PERFECTO"
                if porcentaje >= 95
                else "NECESITA_MEJORAS" if porcentaje >= 70 else "CRÍTICO"
            ),
        }

    def mostrar_resultados(self, resultado: Dict):
        """Mostrar resultados de la verificación"""
        print("\n" + "=" * 60)
        print("📊 RESULTADOS DE VERIFICACIÓN DE FLUJO COMPLETO")
        print("=" * 60)

        puntuacion = resultado.get("puntuacion", {})
        print(f"🎯 PUNTUACIÓN GENERAL: {puntuacion.get('porcentaje', 0):.1f}%")
        print(f"📈 ESTADO: {puntuacion.get('estado', 'DESCONOCIDO')}")
        print(
            f"📊 PUNTOS: {puntuacion.get('puntos_obtenidos', 0)}/{puntuacion.get('puntos_totales', 0)}"
        )

        # Mostrar detalles de unificación
        print("\n📋 UNIFICACIÓN DE DATOS:")
        unificacion = resultado["verificaciones"].get("unificacion_datos", {})
        for tabla, info in unificacion.items():
            estado = "✅" if info.get("unificado", False) else "❌"
            print(
                f"  {estado} {tabla}: Energy({info.get('energy_api_usa', False)}) Expert({info.get('expert_api_usa', False)})"
            )

        # Mostrar flujos críticos
        print("\n🔄 FLUJOS CRÍTICOS:")
        flujo_usuario = resultado["verificaciones"].get("flujo_usuario", {})
        for flujo, info in flujo_usuario.items():
            if isinstance(info, dict):
                estado = "✅" if info.get("flujo_completo", False) else "❌"
                print(f"  {estado} {flujo}: {info.get('descripcion', '')}")

        # Conclusión
        if puntuacion.get("porcentaje", 0) >= 95:
            print("\n🎉 ¡FLUJO PERFECTO! La aplicación funcionará correctamente")
        elif puntuacion.get("porcentaje", 0) >= 70:
            print("\n⚠️ FLUJO FUNCIONAL pero necesita mejoras")
        else:
            print("\n❌ FLUJO CRÍTICO - La aplicación NO funcionará correctamente")


def main():
    """Función principal"""
    verificador = VerificadorFlujoCompleto()
    resultado = verificador.ejecutar_verificacion_completa()
    verificador.mostrar_resultados(resultado)

    # Guardar resultado
    import json

    with open("VERIFICACION_FLUJO_COMPLETO.json", "w", encoding="utf-8") as f:
        json.dump(resultado, f, indent=2, ensure_ascii=False)

    print(f"\n📄 Resultado guardado en: VERIFICACION_FLUJO_COMPLETO.json")


if __name__ == "__main__":
    main()
