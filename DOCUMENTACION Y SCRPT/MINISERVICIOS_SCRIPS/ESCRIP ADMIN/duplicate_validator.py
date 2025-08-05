#!/usr/bin/env python3
"""
🔒 VALIDADOR ANTIDUPLICADOS ROBUSTO - SMARWATT
==============================================

Sistema empresarial para prevenir duplicados en tarifas eléctricas.
Compatible 100% con backend existente, sin modificar estructura.

CARACTERÍSTICAS:
- Validación pre-inserción BigQuery
- Sistema robusto contra fallos
- Compatible con datos parciales
- Limpieza automática de testing
- Manejo de errores empresarial

AUTOR: Sistema SmarWatt
FECHA: 21 julio 2025
"""

import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timezone
from google.cloud import bigquery
from google.cloud.exceptions import NotFound, GoogleCloudError


class TariffDuplicateValidator:
    """Validador robusto antiduplicados para tarifas eléctricas"""

    def __init__(self, project_id: str, dataset_id: str, table_id: str):
        """
        Inicializar validador con configuración BigQuery

        Args:
            project_id: ID del proyecto GCP
            dataset_id: ID del dataset BigQuery
            table_id: ID de la tabla de tarifas
        """
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.table_id = table_id
        self.full_table_id = f"{project_id}.{dataset_id}.{table_id}"

        try:
            self.bq_client = bigquery.Client()
            self.logger = logging.getLogger(f"{self.__class__.__name__}")
            self.logger.info("✅ Validador antiduplicados inicializado correctamente")
        except Exception as e:
            self.logger = logging.getLogger(f"{self.__class__.__name__}")
            self.logger.error(f"❌ Error inicializando BigQuery client: {str(e)}")
            self.bq_client = None

    def generate_unique_identifier(self, tariff_data: Dict[str, Any]) -> str:
        """
        Generar identificador único basado en campos obligatorios
        ROBUSTO: Funciona aunque falten campos opcionales

        Args:
            tariff_data: Datos de la tarifa

        Returns:
            str: Identificador único normalizado
        """
        try:
            # CAMPOS OBLIGATORIOS del backend (verificados)
            supplier = str(tariff_data.get("supplier_name", "")).strip().upper()
            tariff = str(tariff_data.get("tariff_name", "")).strip().upper()
            tariff_type = str(tariff_data.get("tariff_type", "")).strip().upper()

            # Validar que existan los campos mínimos
            if not supplier or not tariff or not tariff_type:
                raise ValueError(
                    "Campos obligatorios faltantes para generar identificador"
                )

            # Normalizar para evitar diferencias por espacios/mayúsculas
            unique_id = f"{supplier}||{tariff}||{tariff_type}"

            self.logger.debug(f"🔑 ID generado: {unique_id}")
            return unique_id

        except Exception as e:
            self.logger.error(f"❌ Error generando ID único: {str(e)}")
            raise

    def check_tariff_exists(
        self, tariff_data: Dict[str, Any]
    ) -> Tuple[bool, Optional[str]]:
        """
        Verificar si tarifa ya existe en BigQuery
        ROBUSTO: Maneja errores de conexión y tabla inexistente

        Args:
            tariff_data: Datos de la tarifa a verificar

        Returns:
            Tuple[bool, Optional[str]]: (existe, error_msg)
        """
        if not self.bq_client:
            return False, "Cliente BigQuery no disponible"

        try:
            unique_id = self.generate_unique_identifier(tariff_data)

            # Query optimizada para verificar existencia
            query = f"""
            SELECT COUNT(*) as count
            FROM `{self.full_table_id}`
            WHERE UPPER(TRIM(supplier_name)) = @supplier
              AND UPPER(TRIM(tariff_name)) = @tariff_name
              AND UPPER(TRIM(tariff_type)) = @tariff_type
            LIMIT 1
            """

            # Parámetros seguros para evitar inyección SQL
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter(
                        "supplier",
                        "STRING",
                        str(tariff_data.get("supplier_name", "")).strip().upper(),
                    ),
                    bigquery.ScalarQueryParameter(
                        "tariff_name",
                        "STRING",
                        str(tariff_data.get("tariff_name", "")).strip().upper(),
                    ),
                    bigquery.ScalarQueryParameter(
                        "tariff_type",
                        "STRING",
                        str(tariff_data.get("tariff_type", "")).strip().upper(),
                    ),
                ]
            )

            # Ejecutar query con timeout
            query_job = self.bq_client.query(query, job_config=job_config)
            results = list(query_job.result(timeout=30))

            exists = results[0].count > 0 if results else False

            if exists:
                self.logger.warning(f"⚠️ Tarifa duplicada encontrada: {unique_id}")
            else:
                self.logger.debug(f"✅ Tarifa nueva verificada: {unique_id}")

            return exists, None

        except NotFound:
            # Tabla no existe - asumir que no hay duplicados
            self.logger.info(
                f"📋 Tabla {self.full_table_id} no encontrada - asumir nueva"
            )
            return False, None

        except GoogleCloudError as e:
            error_msg = f"Error BigQuery: {str(e)}"
            self.logger.error(f"❌ {error_msg}")
            return False, error_msg

        except Exception as e:
            error_msg = f"Error verificando existencia: {str(e)}"
            self.logger.error(f"❌ {error_msg}")
            return False, error_msg

    def validate_required_fields(
        self, tariff_data: Dict[str, Any]
    ) -> Tuple[bool, List[str]]:
        """
        Validar que existan los campos mínimos obligatorios
        ROBUSTO: Solo valida lo ESTRICTAMENTE necesario del backend

        Args:
            tariff_data: Datos de la tarifa

        Returns:
            Tuple[bool, List[str]]: (es_válido, campos_faltantes)
        """
        # CAMPOS OBLIGATORIOS verificados en routes.py
        required_fields = [
            "supplier_name",
            "tariff_name",
            "tariff_type",
            "fixed_term_price",
            "variable_term_price",
        ]

        missing_fields = []

        for field in required_fields:
            value = tariff_data.get(field)

            # Validar existencia y no vacío
            if value is None or (isinstance(value, str) and not value.strip()):
                missing_fields.append(field)
            # Validar precios numéricos
            elif field in ["fixed_term_price", "variable_term_price"]:
                try:
                    float(value)
                except (ValueError, TypeError):
                    missing_fields.append(f"{field} (debe ser numérico)")

        is_valid = len(missing_fields) == 0

        if not is_valid:
            self.logger.warning(f"⚠️ Campos faltantes: {missing_fields}")
        else:
            self.logger.debug("✅ Campos obligatorios validados")

        return is_valid, missing_fields

    def validate_single_tariff(self, tariff_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validación completa de tarifa individual
        ROBUSTO: Devuelve estado detallado sin fallar

        Args:
            tariff_data: Datos de la tarifa

        Returns:
            Dict con resultado de validación
        """
        result = {
            "is_valid": False,
            "is_duplicate": False,
            "missing_fields": [],
            "error_message": None,
            "can_proceed": False,
            "unique_id": None,
        }

        try:
            # 1. Validar campos obligatorios
            fields_valid, missing_fields = self.validate_required_fields(tariff_data)
            result["missing_fields"] = missing_fields

            if not fields_valid:
                result["error_message"] = (
                    f"Campos obligatorios faltantes: {missing_fields}"
                )
                return result

            # 2. Generar ID único
            try:
                result["unique_id"] = self.generate_unique_identifier(tariff_data)
            except Exception as e:
                result["error_message"] = f"Error generando ID: {str(e)}"
                return result

            # 3. Verificar duplicados
            is_duplicate, duplicate_error = self.check_tariff_exists(tariff_data)
            result["is_duplicate"] = is_duplicate

            if duplicate_error:
                # Error de conexión - permitir continuar con advertencia
                result["error_message"] = f"Advertencia: {duplicate_error}"
                result["can_proceed"] = True  # Sistema robusto continúa
                self.logger.warning(
                    f"⚠️ Error verificando duplicados pero continuando: {duplicate_error}"
                )
            elif is_duplicate:
                # Duplicado confirmado - bloquear
                result["error_message"] = f"Tarifa duplicada: {result['unique_id']}"
                result["can_proceed"] = False
            else:
                # Todo OK - proceder
                result["can_proceed"] = True
                result["is_valid"] = True

        except Exception as e:
            result["error_message"] = f"Error validación: {str(e)}"
            self.logger.error(f"❌ Error en validación: {str(e)}")

        return result

    def validate_batch_tariffs(self, tariffs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validar lote de tarifas
        ROBUSTO: Procesa las válidas aunque algunas fallen

        Args:
            tariffs: Lista de tarifas a validar

        Returns:
            Dict con resumen de validación batch
        """
        result = {
            "total_tariffs": len(tariffs),
            "valid_tariffs": [],
            "invalid_tariffs": [],
            "duplicate_tariffs": [],
            "errors": [],
            "can_proceed_count": 0,
        }

        unique_ids_in_batch = set()

        for i, tariff in enumerate(tariffs):
            tariff_result = self.validate_single_tariff(tariff)

            # Verificar duplicados dentro del mismo batch
            if (
                tariff_result.get("unique_id")
                and tariff_result["unique_id"] in unique_ids_in_batch
            ):
                result["duplicate_tariffs"].append(
                    {
                        "index": i,
                        "tariff": tariff,
                        "error": f"Duplicado dentro del lote: {tariff_result['unique_id']}",
                    }
                )
                continue

            if tariff_result["can_proceed"]:
                result["valid_tariffs"].append(
                    {
                        "index": i,
                        "tariff": tariff,
                        "unique_id": tariff_result["unique_id"],
                    }
                )
                result["can_proceed_count"] += 1

                if tariff_result.get("unique_id"):
                    unique_ids_in_batch.add(tariff_result["unique_id"])

            elif tariff_result["is_duplicate"]:
                result["duplicate_tariffs"].append(
                    {
                        "index": i,
                        "tariff": tariff,
                        "error": tariff_result["error_message"],
                    }
                )
            else:
                result["invalid_tariffs"].append(
                    {
                        "index": i,
                        "tariff": tariff,
                        "error": tariff_result["error_message"],
                    }
                )

            if tariff_result.get("error_message"):
                result["errors"].append(
                    f"Tarifa {i+1}: {tariff_result['error_message']}"
                )

        self.logger.info(
            f"📊 Batch validado: {result['can_proceed_count']}/{result['total_tariffs']} tarifas válidas"
        )

        return result

    def cleanup_test_data(self) -> Dict[str, Any]:
        """
        Limpiar datos de testing con marcador DELETEME
        ROBUSTO: Informa errores pero no falla

        Returns:
            Dict con resultado de limpieza
        """
        if not self.bq_client:
            return {"success": False, "error": "Cliente BigQuery no disponible"}

        try:
            # Query para eliminar datos de testing
            delete_query = f"""
            DELETE FROM `{self.full_table_id}`
            WHERE supplier_name LIKE '%DELETEME%'
               OR tariff_name LIKE '%DELETEME%'
               OR supplier_name LIKE '%TEST_%'
               OR tariff_name LIKE '%TEST_%'
            """

            self.logger.info("🧹 Iniciando limpieza de datos de testing...")

            query_job = self.bq_client.query(delete_query)
            result = query_job.result(timeout=60)

            # Obtener número de filas eliminadas
            deleted_rows = query_job.num_dml_affected_rows or 0

            self.logger.info(
                f"✅ Limpieza completada: {deleted_rows} registros eliminados"
            )

            return {
                "success": True,
                "deleted_rows": deleted_rows,
                "message": f"Eliminados {deleted_rows} registros de testing",
            }

        except NotFound:
            return {
                "success": True,
                "deleted_rows": 0,
                "message": "Tabla no encontrada - sin datos para limpiar",
            }

        except Exception as e:
            error_msg = f"Error en limpieza: {str(e)}"
            self.logger.error(f"❌ {error_msg}")
            return {"success": False, "error": error_msg, "deleted_rows": 0}

    def get_validation_summary(self, validation_result: Dict[str, Any]) -> str:
        """
        Generar resumen legible de validación

        Args:
            validation_result: Resultado de validate_single_tariff o validate_batch_tariffs

        Returns:
            str: Resumen formateado
        """
        if "total_tariffs" in validation_result:
            # Resultado batch
            summary = f"""
🔍 RESUMEN VALIDACIÓN BATCH:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Total tarifas: {validation_result['total_tariffs']}
✅ Válidas: {validation_result['can_proceed_count']}
❌ Inválidas: {len(validation_result['invalid_tariffs'])}
🔄 Duplicadas: {len(validation_result['duplicate_tariffs'])}
"""
            if validation_result["errors"]:
                summary += f"\n⚠️ Errores principales:\n"
                for error in validation_result["errors"][:5]:  # Mostrar máximo 5
                    summary += f"  • {error}\n"

        else:
            # Resultado individual
            status = "✅ VÁLIDA" if validation_result["is_valid"] else "❌ INVÁLIDA"
            summary = f"""
🔍 VALIDACIÓN TARIFA: {status}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🆔 ID único: {validation_result.get('unique_id', 'N/A')}
🔄 Duplicada: {'Sí' if validation_result['is_duplicate'] else 'No'}
✅ Puede proceder: {'Sí' if validation_result['can_proceed'] else 'No'}
"""
            if validation_result["missing_fields"]:
                summary += f"📋 Campos faltantes: {', '.join(validation_result['missing_fields'])}\n"
            if validation_result["error_message"]:
                summary += f"❌ Error: {validation_result['error_message']}\n"

        return summary
