#!/usr/bin/env python3
# 🔧 INSTALADOR DE DEPENDENCIAS PARA ANÁLISIS REAL

import subprocess
import sys
import os


def instalar_dependencias():
    """Instalar dependencias necesarias"""
    dependencias = ["google-cloud-bigquery", "pathlib", "ast"]

    print("📦 Instalando dependencias necesarias...")

    for dep in dependencias:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"✅ {dep} instalado")
        except Exception as e:
            print(f"⚠️  Error instalando {dep}: {e}")

    print("🚀 Dependencias instaladas. Ejecutar: python analizador_real_problemas.py")


if __name__ == "__main__":
    instalar_dependencias()
