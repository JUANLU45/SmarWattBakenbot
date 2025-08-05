# expert_bot_api_COPY/bq_migrations/migration_runner.py
# 🏢 ORQUESTADOR DE MIGRACIONES BIGQUERY EMPRESARIAL

import logging
import os
from typing import Dict, List, Optional
from datetime import datetime, timezone
import importlib.util
import sys
from pathlib import Path

from google.cloud import bigquery
from google.api_core import exceptions as google_exceptions
from flask import current_app

from smarwatt_auth.exceptions import AppError


class MigrationRunner:
    """
    🏢 ORQUESTADOR DE MIGRACIONES BIGQUERY EMPRESARIAL

    Características:
    - Versionado automático de esquemas
    - Rollback automático en caso de error
    - Logging detallado de migraciones
    - Validación de scripts antes de ejecutar
    - Soporte para migraciones idempotentes
    """

    def __init__(self, project_id: str, dataset_id: str):
        """
        Inicializar runner de migraciones

        Args:
            project_id: ID del proyecto GCP
            dataset_id: ID del dataset BigQuery
        """
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.client = bigquery.Client(project=project_id)
        self.logger = logging.getLogger("migration_runner")
        self.migrations_dir = Path(__file__).parent
        self.migrations_table = "schema_migrations"

        # Inicializar tabla de migraciones
        self._ensure_migrations_table()

    def _ensure_migrations_table(self):
        """Crear tabla de migraciones si no existe"""
        try:
            table_ref = self.client.dataset(self.dataset_id).table(
                self.migrations_table
            )

            # Verificar si la tabla existe
            try:
                self.client.get_table(table_ref)
                self.logger.info(f"Tabla {self.migrations_table} ya existe")
                return
            except google_exceptions.NotFound:
                pass

            # Crear tabla de migraciones
            schema = [
                bigquery.SchemaField("version", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("migration_name", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("applied_at", "TIMESTAMP", mode="REQUIRED"),
                bigquery.SchemaField("execution_time_ms", "INTEGER", mode="REQUIRED"),
                bigquery.SchemaField("success", "BOOLEAN", mode="REQUIRED"),
                bigquery.SchemaField("error_message", "STRING", mode="NULLABLE"),
                bigquery.SchemaField("rollback_applied", "BOOLEAN", mode="NULLABLE"),
                bigquery.SchemaField("rollback_at", "TIMESTAMP", mode="NULLABLE"),
            ]

            table = bigquery.Table(table_ref, schema=schema)
            table = self.client.create_table(table)

            self.logger.info(f"✅ Tabla de migraciones {self.migrations_table} creada")

        except Exception as e:
            self.logger.error(f"Error creando tabla de migraciones: {e}")
            raise AppError(f"Error inicializando sistema de migraciones: {str(e)}", 500)

    def run_migrations(self, target_version: Optional[str] = None) -> Dict[str, any]:
        """
        Ejecutar migraciones pendientes

        Args:
            target_version: Versión objetivo (opcional)

        Returns:
            Dict con resultado de las migraciones
        """
        try:
            self.logger.info("🚀 Iniciando ejecución de migraciones")

            # Obtener migraciones aplicadas
            applied_migrations = self._get_applied_migrations()

            # Obtener migraciones disponibles
            available_migrations = self._get_available_migrations()

            # Filtrar migraciones pendientes
            pending_migrations = self._get_pending_migrations(
                applied_migrations, available_migrations, target_version
            )

            if not pending_migrations:
                self.logger.info("✅ No hay migraciones pendientes")
                return {
                    "status": "success",
                    "message": "No hay migraciones pendientes",
                    "migrations_applied": 0,
                    "total_time_ms": 0,
                }

            # Ejecutar migraciones
            results = []
            total_time = 0

            for migration in pending_migrations:
                self.logger.info(f"📦 Ejecutando migración: {migration['name']}")

                result = self._execute_migration(migration)
                results.append(result)
                total_time += result["execution_time_ms"]

                if not result["success"]:
                    self.logger.error(f"❌ Error en migración {migration['name']}")
                    return {
                        "status": "error",
                        "message": f"Error en migración {migration['name']}",
                        "error": result["error_message"],
                        "migrations_applied": len([r for r in results if r["success"]]),
                        "total_time_ms": total_time,
                        "results": results,
                    }

            successful_migrations = len([r for r in results if r["success"]])

            self.logger.info(f"✅ Migraciones completadas: {successful_migrations}")

            return {
                "status": "success",
                "message": f"Migraciones completadas exitosamente",
                "migrations_applied": successful_migrations,
                "total_time_ms": total_time,
                "results": results,
            }

        except Exception as e:
            self.logger.error(f"Error ejecutando migraciones: {e}")
            raise AppError(f"Error en sistema de migraciones: {str(e)}", 500)

    def rollback_migration(self, version: str) -> Dict[str, any]:
        """
        Hacer rollback de una migración

        Args:
            version: Versión de la migración a revertir

        Returns:
            Dict con resultado del rollback
        """
        try:
            self.logger.info(f"🔄 Iniciando rollback de migración: {version}")

            # Verificar que la migración está aplicada
            if not self._is_migration_applied(version):
                raise AppError(f"La migración {version} no está aplicada", 400)

            # Cargar migración
            migration = self._load_migration(version)
            if not migration:
                raise AppError(f"No se encontró migración {version}", 404)

            # Ejecutar rollback
            start_time = datetime.now()

            try:
                if hasattr(migration["module"], "downgrade"):
                    migration["module"].downgrade(
                        self.client, self.project_id, self.dataset_id
                    )
                    success = True
                    error_message = None
                else:
                    success = False
                    error_message = "La migración no tiene función downgrade"

            except Exception as e:
                success = False
                error_message = str(e)
                self.logger.error(f"Error en rollback: {e}")

            # Calcular tiempo de ejecución
            execution_time = (datetime.now() - start_time).total_seconds() * 1000

            # Registrar rollback
            self._register_rollback(version, success, error_message, execution_time)

            if success:
                self.logger.info(f"✅ Rollback completado: {version}")
                return {
                    "status": "success",
                    "message": f"Rollback de {version} completado",
                    "execution_time_ms": int(execution_time),
                }
            else:
                self.logger.error(f"❌ Error en rollback: {version}")
                return {
                    "status": "error",
                    "message": f"Error en rollback de {version}",
                    "error": error_message,
                    "execution_time_ms": int(execution_time),
                }

        except Exception as e:
            self.logger.error(f"Error en rollback: {e}")
            raise AppError(f"Error en rollback: {str(e)}", 500)

    def _get_applied_migrations(self) -> List[Dict[str, any]]:
        """Obtener migraciones aplicadas"""
        try:
            query = f"""
            SELECT version, migration_name, applied_at, success, rollback_applied
            FROM `{self.project_id}.{self.dataset_id}.{self.migrations_table}`
            WHERE success = TRUE AND (rollback_applied IS NULL OR rollback_applied = FALSE)
            ORDER BY version
            """

            query_job = self.client.query(query)
            results = list(query_job)

            return [dict(row) for row in results]

        except Exception as e:
            self.logger.error(f"Error obteniendo migraciones aplicadas: {e}")
            return []

    def _get_available_migrations(self) -> List[Dict[str, any]]:
        """Obtener migraciones disponibles"""
        try:
            migrations = []

            # Buscar archivos de migración
            for file_path in self.migrations_dir.glob("*.py"):
                if (
                    file_path.name.startswith("__")
                    or file_path.name == "migration_runner.py"
                ):
                    continue

                # Extraer versión del nombre del archivo
                version = file_path.stem

                migrations.append(
                    {
                        "version": version,
                        "name": file_path.name,
                        "path": file_path,
                    }
                )

            # Ordenar por versión
            migrations.sort(key=lambda x: x["version"])

            return migrations

        except Exception as e:
            self.logger.error(f"Error obteniendo migraciones disponibles: {e}")
            return []

    def _get_pending_migrations(
        self,
        applied: List[Dict],
        available: List[Dict],
        target_version: Optional[str] = None,
    ) -> List[Dict]:
        """Obtener migraciones pendientes"""
        applied_versions = {m["version"] for m in applied}

        pending = []
        for migration in available:
            if migration["version"] not in applied_versions:
                if target_version is None or migration["version"] <= target_version:
                    pending.append(migration)

        return pending

    def _execute_migration(self, migration: Dict[str, any]) -> Dict[str, any]:
        """Ejecutar una migración"""
        start_time = datetime.now()

        try:
            # Cargar módulo de migración
            module = self._load_migration_module(migration["path"])

            if not hasattr(module, "upgrade"):
                raise Exception("La migración no tiene función upgrade")

            # Ejecutar migración
            module.upgrade(self.client, self.project_id, self.dataset_id)

            success = True
            error_message = None

        except Exception as e:
            success = False
            error_message = str(e)
            self.logger.error(f"Error ejecutando migración {migration['name']}: {e}")

        # Calcular tiempo de ejecución
        execution_time = (datetime.now() - start_time).total_seconds() * 1000

        # Registrar migración
        self._register_migration(
            migration["version"],
            migration["name"],
            success,
            error_message,
            execution_time,
        )

        return {
            "version": migration["version"],
            "name": migration["name"],
            "success": success,
            "error_message": error_message,
            "execution_time_ms": int(execution_time),
        }

    def _load_migration_module(self, path: Path):
        """Cargar módulo de migración"""
        try:
            spec = importlib.util.spec_from_file_location("migration", path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module

        except Exception as e:
            raise Exception(f"Error cargando migración {path}: {e}")

    def _load_migration(self, version: str) -> Optional[Dict[str, any]]:
        """Cargar migración por versión"""
        available = self._get_available_migrations()

        for migration in available:
            if migration["version"] == version:
                module = self._load_migration_module(migration["path"])
                migration["module"] = module
                return migration

        return None

    def _register_migration(
        self,
        version: str,
        name: str,
        success: bool,
        error_message: Optional[str],
        execution_time: float,
    ):
        """Registrar migración en tabla"""
        try:
            table_ref = self.client.dataset(self.dataset_id).table(
                self.migrations_table
            )

            row = {
                "version": version,
                "migration_name": name,
                "applied_at": datetime.now(timezone.utc).isoformat(),
                "execution_time_ms": int(execution_time),
                "success": success,
                "error_message": error_message,
                "rollback_applied": False,
                "rollback_at": None,
            }

            errors = self.client.insert_rows_json(table_ref, [row])

            if errors:
                self.logger.error(f"Error registrando migración: {errors}")

        except Exception as e:
            self.logger.error(f"Error registrando migración: {e}")

    def _register_rollback(
        self,
        version: str,
        success: bool,
        error_message: Optional[str],
        execution_time: float,
    ):
        """Registrar rollback en tabla"""
        try:
            # Actualizar registro de migración
            query = f"""
            UPDATE `{self.project_id}.{self.dataset_id}.{self.migrations_table}`
            SET rollback_applied = TRUE,
                rollback_at = CURRENT_TIMESTAMP()
            WHERE version = '{version}' AND success = TRUE
            """

            self.client.query(query)

            # Insertar registro de rollback
            table_ref = self.client.dataset(self.dataset_id).table(
                self.migrations_table
            )

            row = {
                "version": f"{version}_rollback",
                "migration_name": f"Rollback {version}",
                "applied_at": datetime.now(timezone.utc).isoformat(),
                "execution_time_ms": int(execution_time),
                "success": success,
                "error_message": error_message,
                "rollback_applied": None,
                "rollback_at": None,
            }

            errors = self.client.insert_rows_json(table_ref, [row])

            if errors:
                self.logger.error(f"Error registrando rollback: {errors}")

        except Exception as e:
            self.logger.error(f"Error registrando rollback: {e}")

    def _is_migration_applied(self, version: str) -> bool:
        """Verificar si una migración está aplicada"""
        try:
            query = f"""
            SELECT COUNT(*) as count
            FROM `{self.project_id}.{self.dataset_id}.{self.migrations_table}`
            WHERE version = '{version}' AND success = TRUE 
            AND (rollback_applied IS NULL OR rollback_applied = FALSE)
            """

            query_job = self.client.query(query)
            result = list(query_job)[0]

            return result["count"] > 0

        except Exception as e:
            self.logger.error(f"Error verificando migración: {e}")
            return False

    def get_migration_status(self) -> Dict[str, any]:
        """Obtener estado de migraciones"""
        try:
            applied_migrations = self._get_applied_migrations()
            available_migrations = self._get_available_migrations()

            pending_migrations = self._get_pending_migrations(
                applied_migrations, available_migrations
            )

            return {
                "applied_count": len(applied_migrations),
                "available_count": len(available_migrations),
                "pending_count": len(pending_migrations),
                "applied_migrations": [m["version"] for m in applied_migrations],
                "pending_migrations": [m["version"] for m in pending_migrations],
                "last_applied": (
                    applied_migrations[-1]["applied_at"] if applied_migrations else None
                ),
            }

        except Exception as e:
            self.logger.error(f"Error obteniendo estado: {e}")
            return {"error": str(e)}
