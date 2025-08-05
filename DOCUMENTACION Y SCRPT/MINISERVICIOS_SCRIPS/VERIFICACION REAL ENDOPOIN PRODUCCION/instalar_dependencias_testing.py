#!/usr/bin/env python3
"""
INSTALADOR DE DEPENDENCIAS PARA TESTING DE PRODUCCIÓN
=====================================================

Script para instalar TODAS las dependencias necesarias para el testing.
Instala REALMENTE las librerías requeridas sin simulaciones.

🔒 RESTRICCIONES ABSOLUTAS:
- PROHIBIDO comandos placebo
- SOLO instalaciones REALES
- VERIFICACIÓN REAL de instalaciones

DEPENDENCIAS REQUERIDAS:
✅ requests (HTTP requests)
✅ google-cloud-bigquery (BigQuery)
✅ google-auth (Google authentication)
✅ firebase-admin (Firebase Admin SDK)

VERSIÓN: 1.0.0 - INSTALADOR REAL
FECHA: 2025-01-17
"""

import subprocess
import sys
import importlib
import logging
from typing import List, Tuple

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("DependencyInstaller")

class DependencyInstaller:
    """Instalador robusto de dependencias para testing de producción."""
    
    def __init__(self):
        """Inicializar instalador."""
        self.required_packages = [
            "requests",
            "google-cloud-bigquery",
            "google-auth", 
            "google-auth-oauthlib",
            "firebase-admin"
        ]
        
        self.installation_results = {
            "successful": [],
            "failed": [],
            "already_installed": []
        }

    def check_package_installed(self, package_name: str) -> bool:
        """Verificar REALMENTE si un paquete está instalado."""
        try:
            # Mapeo de nombres de paquetes a módulos
            module_mapping = {
                "google-cloud-bigquery": "google.cloud.bigquery",
                "google-auth": "google.auth",
                "google-auth-oauthlib": "google_auth_oauthlib",
                "firebase-admin": "firebase_admin"
            }
            
            module_name = module_mapping.get(package_name, package_name)
            importlib.import_module(module_name)
            logger.info(f"✅ {package_name} ya está instalado")
            return True
        except ImportError:
            logger.info(f"❌ {package_name} no está instalado")
            return False

    def install_package(self, package_name: str) -> Tuple[bool, str]:
        """Instalar REALMENTE un paquete usando pip."""
        try:
            logger.info(f"📦 Instalando {package_name}...")
            
            # Comando REAL de instalación
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", package_name],
                capture_output=True,
                text=True,
                timeout=300  # 5 minutos timeout
            )
            
            if result.returncode == 0:
                logger.info(f"✅ {package_name} instalado correctamente")
                return True, "Instalación exitosa"
            else:
                error_msg = result.stderr or result.stdout
                logger.error(f"❌ Error instalando {package_name}: {error_msg}")
                return False, error_msg
                
        except subprocess.TimeoutExpired:
            error_msg = f"Timeout instalando {package_name}"
            logger.error(f"⏰ {error_msg}")
            return False, error_msg
        except Exception as e:
            error_msg = f"Error inesperado: {str(e)}"
            logger.error(f"❌ {error_msg}")
            return False, error_msg

    def verify_installation(self, package_name: str) -> bool:
        """Verificar REALMENTE que la instalación fue exitosa."""
        try:
            # Verificar importando el módulo
            return self.check_package_installed(package_name)
        except Exception as e:
            logger.error(f"❌ Error verificando {package_name}: {e}")
            return False

    def install_all_dependencies(self) -> None:
        """Instalar todas las dependencias necesarias."""
        logger.info("🚀 INICIANDO INSTALACIÓN DE DEPENDENCIAS")
        logger.info("=" * 50)
        
        for package in self.required_packages:
            logger.info(f"\n📋 Procesando {package}...")
            
            # Verificar si ya está instalado
            if self.check_package_installed(package):
                self.installation_results["already_installed"].append(package)
                continue
            
            # Instalar el paquete
            success, message = self.install_package(package)
            
            if success:
                # Verificar que la instalación fue exitosa
                if self.verify_installation(package):
                    self.installation_results["successful"].append(package)
                else:
                    self.installation_results["failed"].append({
                        "package": package,
                        "error": "Instalación aparentemente exitosa pero verificación falló"
                    })
            else:
                self.installation_results["failed"].append({
                    "package": package,
                    "error": message
                })

    def generate_report(self) -> None:
        """Generar reporte REAL de instalaciones."""
        logger.info("\n📊 GENERANDO REPORTE DE INSTALACIÓN")
        logger.info("=" * 50)
        
        print("\n" + "=" * 60)
        print("📦 REPORTE DE INSTALACIÓN DE DEPENDENCIAS")
        print("=" * 60)
        
        total = len(self.required_packages)
        already_installed = len(self.installation_results["already_installed"])
        successful = len(self.installation_results["successful"])
        failed = len(self.installation_results["failed"])
        
        print(f"📊 ESTADÍSTICAS:")
        print(f"   • Total paquetes: {total}")
        print(f"   • Ya instalados: {already_installed}")
        print(f"   • Instalados ahora: {successful}")
        print(f"   • Fallidos: {failed}")
        print()
        
        if self.installation_results["already_installed"]:
            print("✅ PAQUETES YA INSTALADOS:")
            for package in self.installation_results["already_installed"]:
                print(f"   • {package}")
            print()
        
        if self.installation_results["successful"]:
            print("🎉 PAQUETES INSTALADOS EXITOSAMENTE:")
            for package in self.installation_results["successful"]:
                print(f"   • {package}")
            print()
        
        if self.installation_results["failed"]:
            print("❌ PAQUETES CON ERRORES:")
            for failure in self.installation_results["failed"]:
                print(f"   • {failure['package']}: {failure['error']}")
            print()
        
        # Resultado final
        if failed == 0:
            print("🎉 TODAS LAS DEPENDENCIAS ESTÁN DISPONIBLES")
            print("✅ El sistema está listo para ejecutar los scripts de testing")
        else:
            print("⚠️ ALGUNAS DEPENDENCIAS FALLARON")
            print("🔧 Revisa los errores arriba y intenta instalar manualmente")
        
        print("=" * 60)

    def run_installation(self) -> bool:
        """Ejecutar instalación completa de dependencias."""
        try:
            self.install_all_dependencies()
            self.generate_report()
            
            # Retornar True si todas las dependencias están disponibles
            return len(self.installation_results["failed"]) == 0
            
        except Exception as e:
            logger.error(f"❌ Error durante instalación: {e}")
            return False


def main():
    """Función principal de instalación."""
    try:
        print("🚀 Instalador de Dependencias para Testing de Producción SmarWatt")
        print("=" * 60)
        
        installer = DependencyInstaller()
        success = installer.run_installation()
        
        if success:
            print("\n🎉 Instalación completada exitosamente")
            print("▶️ Ahora puedes ejecutar los scripts de testing:")
            print("   python script_testing_produccion_completo.py")
            print("   python verificacion_endpoints_problematicos.py")
            sys.exit(0)
        else:
            print("\n⚠️ Instalación completada con errores")
            print("🔧 Revisa los mensajes de error arriba")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"❌ Error crítico: {e}")
        sys.exit(2)


if __name__ == "__main__":
    main()
