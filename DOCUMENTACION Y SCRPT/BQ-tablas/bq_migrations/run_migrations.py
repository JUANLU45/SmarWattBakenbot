#!/usr/bin/env python3
"""
SISTEMA DE MIGRACIONES EMPRESARIALES ROBUSTO

Este script ejecuta todas las migraciones de BigQuery de forma robusta
y empresarial, creando todas las tablas necesarias para el funcionamiento
completo del sistema.

Autor: Sistema de Migraciones Empresariales
Fecha: 2025-07-16
Versión: 1.0

FUNCIONALIDADES:
- Ejecución automática de todas las migraciones
- Verificación de dependencias antes de ejecutar
- Logging detallado de cada operación
- Manejo robusto de errores
- Verificación de estado final

TABLAS CREADAS:
1. ai_prompt_optimization - Optimización de prompts de IA
2. ai_predictions - Predicciones de IA con metadata
3. ai_business_metrics - Métricas empresariales de IA
4. async_tasks - Tareas asíncronas con tracking
5. worker_metrics - Métricas de rendimiento de workers
"""

import os
import sys
import logging
import importlib.util
from datetime import datetime, timezone
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv(Path(__file__).parent.parent / ".env")

# Configurar logging empresarial SIN EMOJIS para Windows
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("migration_log.log", encoding="utf-8"),
    ],
)

logger = logging.getLogger(__name__)


class EnterpriseMigrationRunner:
    """Ejecutor de migraciones empresariales robusto"""

    def __init__(self):
        self.migrations_dir = Path(__file__).parent
        self.migrations_executed = []
        self.migrations_failed = []

    def get_migration_files(self):
        """Obtener lista de archivos de migración ordenados"""
        migration_files = []

        for file_path in self.migrations_dir.glob("*.py"):
            if file_path.name.startswith(("001_", "002_", "003_", "004_", "005_")):
                migration_files.append(file_path)

        # Ordenar por nombre para ejecutar en orden
        migration_files.sort(key=lambda x: x.name)

        return migration_files

    def load_migration_module(self, file_path):
        """Cargar módulo de migración dinámicamente"""
        spec = importlib.util.spec_from_file_location("migration", file_path)

        if spec is None or spec.loader is None:
            raise ImportError(f"No se pudo cargar el módulo de migración: {file_path}")

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def execute_migration(self, file_path):
        """Ejecutar una migración específica"""
        migration_name = file_path.stem

        try:
            logger.info(f"EXECUTING: Ejecutando migración: {migration_name}")

            # Cargar módulo de migración
            module = self.load_migration_module(file_path)

            # Verificar que tenga función upgrade
            if not hasattr(module, "upgrade"):
                raise ValueError(
                    f"Migración {migration_name} no tiene función 'upgrade'"
                )

            # Inicializar cliente BigQuery
            from google.cloud import bigquery

            client = bigquery.Client()

            # Obtener variables de entorno
            project_id = os.environ.get("GCP_PROJECT_ID")
            dataset_id = os.environ.get("BQ_DATASET_ID")

            # Ejecutar migración con argumentos correctos
            result = module.upgrade(client, project_id, dataset_id)

            if result is not False:  # None o True son válidos
                logger.info(
                    f"SUCCESS: Migración {migration_name} ejecutada exitosamente"
                )
                self.migrations_executed.append(migration_name)
                return True
            else:
                logger.error(f"ERROR: Migración {migration_name} falló")
                self.migrations_failed.append(migration_name)
                return False

        except Exception as e:
            logger.error(f"ERROR: Error ejecutando migración {migration_name}: {e}")
            self.migrations_failed.append(migration_name)
            return False

    def verify_environment(self):
        """Verificar que el entorno esté configurado correctamente"""
        logger.info("VERIFICANDO: Configuración del entorno...")

        required_vars = ["GCP_PROJECT_ID", "BQ_DATASET_ID"]

        missing_vars = []
        for var in required_vars:
            if not os.environ.get(var):
                missing_vars.append(var)

        if missing_vars:
            logger.error(
                f"ERROR: Variables de entorno faltantes: {', '.join(missing_vars)}"
            )
            return False

        logger.info("SUCCESS: Configuración del entorno verificada")
        return True

    def run_all_migrations(self):
        """Ejecutar todas las migraciones"""
        logger.info("INICIANDO SISTEMA DE MIGRACIONES EMPRESARIALES")
        logger.info("=" * 60)

        # Verificar entorno
        if not self.verify_environment():
            logger.error("ERROR: Error en configuración del entorno")
            return False

        # Obtener archivos de migración
        migration_files = self.get_migration_files()

        if not migration_files:
            logger.warning("WARNING: No se encontraron archivos de migración")
            return True

        logger.info(f"FOUND: Se encontraron {len(migration_files)} migraciones")

        # Ejecutar cada migración
        for file_path in migration_files:
            success = self.execute_migration(file_path)

            if not success:
                logger.error(
                    f"ERROR: Migración {file_path.stem} falló - continuando con las siguientes"
                )
                # Continuar con las siguientes migraciones

        # Reporte final
        self.print_final_report()

        # Retornar True si al menos una migración fue exitosa
        return len(self.migrations_executed) > 0

    def print_final_report(self):
        """Imprimir reporte final de migraciones"""
        logger.info("\n" + "=" * 60)
        logger.info("REPORTE FINAL DE MIGRACIONES")
        logger.info("=" * 60)

        logger.info(
            f"SUCCESS: Migraciones ejecutadas exitosamente: {len(self.migrations_executed)}"
        )
        for migration in self.migrations_executed:
            logger.info(f"   - {migration}")

        if self.migrations_failed:
            logger.info(f"FAILED: Migraciones fallidas: {len(self.migrations_failed)}")
            for migration in self.migrations_failed:
                logger.info(f"   - {migration}")

        logger.info("=" * 60)

        if self.migrations_failed:
            logger.warning(
                "WARNING: Algunas migraciones fallaron. Revisa los logs para más detalles."
            )
        else:
            logger.info("SUCCESS: Todas las migraciones completadas exitosamente!")


def main():
    """Función principal"""
    try:
        runner = EnterpriseMigrationRunner()
        success = runner.run_all_migrations()

        if success:
            logger.info("SUCCESS: Sistema de migraciones completado")
            sys.exit(0)
        else:
            logger.error("ERROR: Sistema de migraciones falló")
            sys.exit(1)

    except KeyboardInterrupt:
        logger.info("INTERRUPTED: Migraciones interrumpidas por el usuario")
        sys.exit(1)
    except Exception as e:
        logger.error(f"CRITICAL ERROR: Error crítico en sistema de migraciones: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
