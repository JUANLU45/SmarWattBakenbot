#!/usr/bin/env python3
"""
🚀 EJECUTOR PRINCIPAL - TESTS PANEL ADMINISTRACIÓN
================================================

Ejecuta todos los tests del panel de administración en orden.
Incluye generación de datos, pruebas de endpoints y limpieza.

ORDEN DE EJECUCIÓN:
1. Generar datos de prueba
2. Test de consulta de mercado (público)
3. Test completo de endpoints admin
4. Resumen final
"""

import subprocess
import sys
import os
from datetime import datetime, timezone


class AdminTestsRunner:
    """Ejecutor de todos los tests administrativos"""
    
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.results = {}
        
    def run_script(self, script_name: str, description: str) -> bool:
        """Ejecutar un script de Python y capturar el resultado"""
        print(f"\n🚀 EJECUTANDO: {description}")
        print("=" * 60)
        
        script_path = os.path.join(self.script_dir, script_name)
        
        if not os.path.exists(script_path):
            print(f"❌ ERROR: Script no encontrado: {script_path}")
            return False
        
        try:
            # Ejecutar el script
            result = subprocess.run(
                [sys.executable, script_path],
                cwd=self.script_dir,
                capture_output=False,  # Mostrar output en tiempo real
                text=True
            )
            
            success = result.returncode == 0
            print(f"\n📊 RESULTADO: {'✅ ÉXITO' if success else '❌ FALLO'}")
            return success
            
        except Exception as e:
            print(f"❌ ERROR EJECUTANDO {script_name}: {e}")
            return False
    
    def run_all_tests(self):
        """Ejecutar toda la suite de tests administrativos"""
        print("🎯 SUITE COMPLETA DE TESTS - PANEL DE ADMINISTRACIÓN")
        print("=" * 65)
        print(f"🕐 Inicio: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print(f"📁 Directorio: {self.script_dir}")
        
        # Test 1: Generar datos de prueba
        self.results['data_generation'] = self.run_script(
            "generate_test_data.py",
            "Generación de datos de prueba realistas"
        )
        
        # Test 2: Consulta de mercado (público)
        self.results['market_data'] = self.run_script(
            "test_market_data.py", 
            "Test de consulta de datos de mercado"
        )
        
        # Test 3: Endpoints administrativos completos
        self.results['admin_endpoints'] = self.run_script(
            "test_admin_panel_endpoints.py",
            "Test completo de endpoints administrativos"
        )
        
        # Resumen final
        self.print_final_summary()
    
    def print_final_summary(self):
        """Imprimir resumen final de toda la suite"""
        print(f"\n" + "="*65)
        print(f"📊 RESUMEN FINAL - SUITE PANEL ADMINISTRACIÓN")
        print(f"=" * 65)
        
        print(f"🕐 Finalizado: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
        
        total_tests = len(self.results)
        passed_tests = sum(self.results.values())
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        
        print(f"\n📋 RESULTADOS POR COMPONENTE:")
        print(f"   1. Generación de datos: {'✅ PASS' if self.results.get('data_generation') else '❌ FAIL'}")
        print(f"   2. Consulta de mercado: {'✅ PASS' if self.results.get('market_data') else '❌ FAIL'}")
        print(f"   3. Endpoints admin: {'✅ PASS' if self.results.get('admin_endpoints') else '❌ FAIL'}")
        
        print(f"\n📊 ESTADÍSTICAS GLOBALES:")
        print(f"   ✅ Componentes exitosos: {passed_tests}/{total_tests}")
        print(f"   ❌ Componentes fallidos: {total_tests - passed_tests}/{total_tests}")
        print(f"   📈 Tasa de éxito global: {success_rate:.1f}%")
        
        # Estado del sistema
        if success_rate == 100:
            print(f"\n🎉 SISTEMA ADMINISTRATIVO COMPLETAMENTE FUNCIONAL")
            print(f"   ✅ Todos los endpoints están operativos")
            print(f"   ✅ Panel de administración listo para producción")
            
        elif success_rate >= 66:
            print(f"\n⚠️ SISTEMA ADMINISTRATIVO PARCIALMENTE FUNCIONAL")
            print(f"   🔍 Revisar componentes fallidos")
            print(f"   ⚡ Algunos endpoints pueden requerir atención")
            
        else:
            print(f"\n🚨 PROBLEMAS CRÍTICOS EN SISTEMA ADMINISTRATIVO")
            print(f"   ❌ Múltiples componentes fallando")
            print(f"   🔧 Revisión completa requerida")
        
        # Recomendaciones
        print(f"\n💡 RECOMENDACIONES:")
        
        if not self.results.get('data_generation'):
            print(f"   🔧 Revisar generador de datos de prueba")
            
        if not self.results.get('market_data'):
            print(f"   🔧 Verificar endpoint de consulta de mercado")
            print(f"   🔍 Comprobar conectividad con Energy-IA-API")
            
        if not self.results.get('admin_endpoints'):
            print(f"   🔧 Revisar permisos de administrador")
            print(f"   🔍 Verificar autenticación admin")
            print(f"   📋 Comprobar endpoints POST /admin/tariffs/*")
        
        if all(self.results.values()):
            print(f"   🚀 Sistema listo para implementar frontend de administración")
            print(f"   📋 Documentación completa disponible en archivos MD")
        
        print(f"\n📁 ARCHIVOS GENERADOS:")
        if self.results.get('data_generation'):
            print(f"   - sample_single_tariff.json (datos tarifa individual)")
            print(f"   - sample_batch_tariffs.json (datos lote tarifas)")
            print(f"   - sample_minimal_tariff.json (datos mínimos)")
        
        print(f"\n🧹 LIMPIEZA:")
        print(f"   ⚠️ Eliminar manualmente tarifas con 'DELETEME' del sistema")
        print(f"   🗑️ Los datos de prueba están marcados para fácil identificación")


if __name__ == "__main__":
    print("🎯 INICIANDO SUITE COMPLETA DE TESTS ADMINISTRATIVOS")
    print("=" * 60)
    
    runner = AdminTestsRunner()
    runner.run_all_tests()
    
    # Código de salida basado en resultados
    if all(runner.results.values()):
        print(f"\n✅ SUITE COMPLETADA EXITOSAMENTE")
        sys.exit(0)
    else:
        print(f"\n❌ SUITE COMPLETADA CON FALLOS")
        sys.exit(1)
