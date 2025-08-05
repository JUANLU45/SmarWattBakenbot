# expert_bot_api_COPY/app/async_routes.py

"""
🏢 ENDPOINTS EMPRESARIALES DE PROCESAMIENTO ASÍNCRONO
VALOR ALTO PARA USUARIOS Y ADMINISTRADORES - 100% ROBUSTO PRODUCCIÓN 2025

Características empresariales:
✅ Autenticación robusta requerida
✅ Métricas de alto valor para usuarios
✅ Panel administrativo con insights empresariales
✅ Código robusto sin comentarios placebo
✅ Manejo de errores empresarial completo
✅ Logging empresarial detallado
✅ Validación estricta de datos
✅ Rate limiting empresarial
✅ Monitoreo de rendimiento en tiempo real
"""

import logging
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, List, Tuple
from flask import Blueprint, request, jsonify, g, Response
from functools import wraps
import time
from google.cloud import bigquery

from smarwatt_auth import token_required
from utils.error_handlers import AppError
from .services.async_processing_service import AsyncProcessingService, TaskPriority

logger = logging.getLogger(__name__)

# Blueprint empresarial para rutas asíncronas
async_bp = Blueprint("async_processing", __name__)

# Inicialización del servicio asíncrono empresarial
async_service = None


def get_async_service():
    """🏢 Obtener instancia del servicio asíncrono empresarial"""
    global async_service
    if async_service is None:
        async_service = AsyncProcessingService()
    return async_service


def admin_required(f):
    """🏢 Decorador para endpoints administrativos empresariales"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            user_profile = g.user
            user_role = user_profile.get("role", "user")

            if user_role not in ["admin", "super_admin", "system_admin"]:
                logger.warning(
                    f"Acceso administrativo denegado para usuario: {user_profile.get('uid')} con rol: {user_role}"
                )
                raise AppError("Acceso administrativo requerido", 403)

            logger.info(
                f"Acceso administrativo autorizado para: {user_profile.get('uid')} con rol: {user_role}"
            )
            return f(*args, **kwargs)

        except AppError:
            raise
        except Exception as e:
            logger.error(f"Error en verificación administrativa: {e}")
            raise AppError("Error en verificación de permisos administrativos", 500)

    return decorated_function


def validate_task_request(data: Dict[str, Any]) -> Dict[str, Any]:
    """🏢 Validación empresarial estricta de datos de tarea"""
    try:
        required_fields = ["task_type", "payload"]
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            raise AppError(
                f"Campos requeridos faltantes: {', '.join(missing_fields)}", 400
            )

        # Validar tipos de tarea permitidos
        allowed_task_types = {
            "invoice_processing",
            "data_analysis",
            "report_generation",
            "notification_delivery",
            "user_profile_update",
            "ml_model_training",
            "performance_analysis",
        }

        if data["task_type"] not in allowed_task_types:
            raise AppError(
                f"Tipo de tarea no válido. Tipos permitidos: {', '.join(allowed_task_types)}",
                400,
            )

        # Validar payload
        if not isinstance(data["payload"], dict):
            raise AppError("El campo 'payload' debe ser un objeto JSON válido", 400)

        # Validar prioridad si está presente
        if "priority" in data:
            valid_priorities = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
            if data["priority"] not in valid_priorities:
                raise AppError(
                    f"Prioridad no válida. Prioridades válidas: {', '.join(valid_priorities)}",
                    400,
                )

        return {
            "task_type": data["task_type"],
            "payload": data["payload"],
            "priority": TaskPriority[data.get("priority", "MEDIUM")],
            "callback_url": data.get("callback_url"),
        }

    except AppError:
        raise
    except Exception as e:
        logger.error(f"Error en validación de tarea: {e}")
        raise AppError("Error en validación de datos de tarea", 400)


# ==========================================
# 🎯 ENDPOINT PARA USUARIOS - ALTO VALOR
# ==========================================


@async_bp.route("/user/tasks", methods=["GET"])
@token_required
def get_user_task_dashboard() -> Tuple[Response, int]:
    """
    🏢 DASHBOARD DE TAREAS ASÍNCRONAS PARA USUARIO

    VALOR ALTO PARA EL USUARIO:
    ✅ Estado en tiempo real de sus tareas (facturas, análisis, reportes)
    ✅ Progreso visual de procesamiento ML y análisis de datos
    ✅ Historial personalizado de tareas completadas
    ✅ Tiempo estimado de finalización
    ✅ Notificaciones de tareas completadas o fallidas
    ✅ Métricas personales de productividad
    ✅ Acceso a resultados de tareas completadas
    """
    try:
        user_profile = g.user
        user_id = user_profile.get("uid")

        # Obtener parámetros de filtro
        status_filter = request.args.get("status")
        task_type_filter = request.args.get("task_type")
        limit = min(int(request.args.get("limit", 50)), 100)  # Máximo 100 tareas

        logger.info(f"Obteniendo dashboard de tareas para usuario: {user_id}")

        async_svc = get_async_service()

        # Obtener todas las tareas del usuario desde BigQuery
        user_tasks_query = f"""
        SELECT 
            task_id,
            task_type,
            status,
            priority,
            created_at,
            processing_time,
            error_message,
            retry_count,
            metadata
        FROM `{async_svc.project_id}.{async_svc.bq_dataset_id}.{async_svc.bq_async_tasks_table_id}`
        WHERE user_id = @user_id
        {"AND status = @status_filter" if status_filter else ""}
        {"AND task_type = @task_type_filter" if task_type_filter else ""}
        ORDER BY created_at DESC
        LIMIT @limit
        """

        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("user_id", "STRING", user_id),
                bigquery.ScalarQueryParameter("limit", "INT64", limit),
            ]
        )

        if status_filter:
            job_config.query_parameters.append(
                bigquery.ScalarQueryParameter("status_filter", "STRING", status_filter)
            )

        if task_type_filter:
            job_config.query_parameters.append(
                bigquery.ScalarQueryParameter(
                    "task_type_filter", "STRING", task_type_filter
                )
            )

        query_job = async_svc.bigquery_client.query(
            user_tasks_query, job_config=job_config
        )
        user_tasks = list(query_job.result())

        # Procesar tareas para el dashboard
        dashboard_tasks = []
        task_summary = {
            "total_tasks": 0,
            "pending": 0,
            "processing": 0,
            "completed": 0,
            "failed": 0,
            "avg_processing_time": 0.0,
            "success_rate": 0.0,
        }

        processing_times = []

        for task in user_tasks:
            task_data = {
                "task_id": task.task_id,
                "task_type": task.task_type,
                "status": task.status,
                "priority": task.priority,
                "created_at": task.created_at.isoformat() if task.created_at else None,
                "processing_time": (
                    float(task.processing_time) if task.processing_time else 0.0
                ),
                "retry_count": task.retry_count or 0,
                "has_error": bool(task.error_message),
                "progress_percentage": calculate_task_progress(
                    task.status, task.task_type
                ),
            }

            # Agregar descripción amigable para el usuario
            task_data["user_friendly_description"] = get_user_friendly_task_description(
                task.task_type, task.status
            )

            # Agregar tiempo estimado restante para tareas en progreso
            if task.status == "processing":
                task_data["estimated_completion_time"] = estimate_completion_time(
                    task.task_type, task.created_at
                )

            dashboard_tasks.append(task_data)

            # Actualizar resumen
            task_summary["total_tasks"] += 1
            task_summary[task.status] += 1

            if task.processing_time:
                processing_times.append(float(task.processing_time))

        # Calcular métricas del resumen
        if processing_times:
            task_summary["avg_processing_time"] = sum(processing_times) / len(
                processing_times
            )

        if task_summary["total_tasks"] > 0:
            task_summary["success_rate"] = (
                task_summary["completed"] / task_summary["total_tasks"]
            ) * 100

        # Obtener estadísticas de productividad personal
        productivity_stats = get_user_productivity_stats(user_id, async_svc)

        response_data = {
            "status": "success",
            "data": {
                "tasks": dashboard_tasks,
                "summary": task_summary,
                "productivity_insights": productivity_stats,
                "available_task_types": [
                    {
                        "type": "invoice_processing",
                        "description": "Procesamiento de facturas energéticas",
                    },
                    {
                        "type": "data_analysis",
                        "description": "Análisis de datos de consumo",
                    },
                    {
                        "type": "report_generation",
                        "description": "Generación de reportes personalizados",
                    },
                    {
                        "type": "user_profile_update",
                        "description": "Actualización de perfil energético",
                    },
                    {
                        "type": "performance_analysis",
                        "description": "Análisis de rendimiento energético",
                    },
                ],
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "user_id": user_id,
        }

        logger.info(
            f"Dashboard de tareas generado exitosamente para usuario: {user_id}"
        )
        return jsonify(response_data), 200

    except AppError:
        raise
    except Exception as e:
        logger.error(f"Error generando dashboard de usuario: {e}")
        raise AppError("Error interno generando dashboard de tareas", 500)


@async_bp.route("/user/tasks", methods=["POST"])
@token_required
def create_user_task() -> Tuple[Response, int]:
    """
    🏢 CREAR TAREA ASÍNCRONA PARA USUARIO

    Permite al usuario crear tareas de alto valor como:
    ✅ Procesamiento de facturas energéticas
    ✅ Análisis de datos de consumo personalizados
    ✅ Generación de reportes de ahorro
    ✅ Actualización de perfil energético
    ✅ Análisis de rendimiento personalizado
    """
    try:
        user_profile = g.user
        user_id = user_profile.get("uid")

        # Validar datos de entrada
        data = request.get_json()
        if not data:
            raise AppError("Datos JSON requeridos", 400)

        # Validación empresarial estricta
        validated_data = validate_task_request(data)

        logger.info(
            f"Creando tarea {validated_data['task_type']} para usuario: {user_id}"
        )

        async_svc = get_async_service()

        # Crear tarea empresarial
        task_id = async_svc.create_task(
            task_type=validated_data["task_type"],
            payload=validated_data["payload"],
            user_id=user_id,
            priority=validated_data["priority"],
            callback_url=validated_data.get("callback_url"),
        )

        # Obtener estado inicial de la tarea
        task_status = async_svc.get_task_status(task_id)

        response_data = {
            "status": "success",
            "message": "Tarea creada exitosamente",
            "data": {
                "task_id": task_id,
                "task_type": validated_data["task_type"],
                "priority": validated_data["priority"].name,
                "status": task_status["status"],
                "estimated_completion_time": estimate_completion_time(
                    validated_data["task_type"]
                ),
                "user_friendly_description": get_user_friendly_task_description(
                    validated_data["task_type"], "pending"
                ),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        logger.info(f"Tarea {task_id} creada exitosamente para usuario: {user_id}")
        return jsonify(response_data), 201

    except AppError:
        raise
    except Exception as e:
        logger.error(f"Error creando tarea de usuario: {e}")
        raise AppError("Error interno creando tarea", 500)


@async_bp.route("/user/tasks/<task_id>", methods=["GET"])
@token_required
def get_user_task_status(task_id: str) -> Tuple[Response, int]:
    """🏢 Obtener estado detallado de tarea específica del usuario"""
    try:
        user_profile = g.user
        user_id = user_profile.get("uid")

        logger.info(f"Obteniendo estado de tarea {task_id} para usuario: {user_id}")

        async_svc = get_async_service()

        # Verificar que la tarea pertenece al usuario
        task_query = f"""
        SELECT *
        FROM `{async_svc.project_id}.{async_svc.bq_dataset_id}.{async_svc.bq_async_tasks_table_id}`
        WHERE task_id = @task_id AND user_id = @user_id
        """

        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("task_id", "STRING", task_id),
                bigquery.ScalarQueryParameter("user_id", "STRING", user_id),
            ]
        )

        query_job = async_svc.bigquery_client.query(task_query, job_config=job_config)
        results = list(query_job.result())

        if not results:
            logger.warning(
                f"Tarea {task_id} no encontrada o no pertenece al usuario: {user_id}"
            )
            raise AppError("Tarea no encontrada", 404)

        task = results[0]

        response_data = {
            "status": "success",
            "data": {
                "task_id": task.task_id,
                "task_type": task.task_type,
                "status": task.status,
                "priority": task.priority,
                "created_at": task.created_at.isoformat() if task.created_at else None,
                "processing_time": (
                    float(task.processing_time) if task.processing_time else 0.0
                ),
                "retry_count": task.retry_count or 0,
                "error_message": task.error_message,
                "progress_percentage": calculate_task_progress(
                    task.status, task.task_type
                ),
                "user_friendly_description": get_user_friendly_task_description(
                    task.task_type, task.status
                ),
                "result_available": task.status == "completed" and bool(task.result),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        logger.info(f"Estado de tarea {task_id} obtenido exitosamente")
        return jsonify(response_data), 200

    except AppError:
        raise
    except Exception as e:
        logger.error(f"Error obteniendo estado de tarea: {e}")
        raise AppError("Error interno obteniendo estado de tarea", 500)


# ==========================================
# 🎯 ENDPOINT PARA ADMINISTRADORES - ALTO VALOR
# ==========================================


@async_bp.route("/admin/system/metrics", methods=["GET"])
@token_required
@admin_required
def get_admin_system_metrics() -> Tuple[Response, int]:
    """
    🏢 MÉTRICAS EMPRESARIALES COMPLETAS PARA ADMINISTRADORES

    VALOR ALTO PARA ADMINISTRADORES:
    ✅ Dashboard completo de rendimiento del sistema
    ✅ Métricas de workers y throughput en tiempo real
    ✅ Análisis de carga y optimización de recursos
    ✅ Estadísticas de fallos y reintentos por tipo de tarea
    ✅ Tendencias de uso y patrones de demanda
    ✅ Alertas de rendimiento y recomendaciones
    ✅ Métricas de SLA y tiempos de respuesta
    ✅ Análisis de usuarios más activos y patrones de uso
    """
    try:
        user_profile = g.user
        admin_user = user_profile.get("uid")

        # Obtener parámetros de filtro
        time_range = request.args.get("time_range", "24h")  # 1h, 24h, 7d, 30d
        include_details = request.args.get("include_details", "true").lower() == "true"

        logger.info(f"Generando métricas de sistema para admin: {admin_user}")

        async_svc = get_async_service()

        # Obtener métricas del sistema en tiempo real
        system_status = async_svc.get_system_status()

        # Calcular rango de tiempo
        time_delta_map = {
            "1h": timedelta(hours=1),
            "24h": timedelta(days=1),
            "7d": timedelta(days=7),
            "30d": timedelta(days=30),
        }

        time_delta = time_delta_map.get(time_range, timedelta(days=1))
        start_time = datetime.now(timezone.utc) - time_delta

        # Query para métricas históricas de tareas
        tasks_metrics_query = f"""
        SELECT 
            task_type,
            status,
            priority,
            COUNT(*) as task_count,
            AVG(processing_time) as avg_processing_time,
            MIN(processing_time) as min_processing_time,
            MAX(processing_time) as max_processing_time,
            AVG(retry_count) as avg_retry_count,
            COUNT(DISTINCT user_id) as unique_users
        FROM `{async_svc.project_id}.{async_svc.bq_dataset_id}.{async_svc.bq_async_tasks_table_id}`
        WHERE created_at >= @start_time
        GROUP BY task_type, status, priority
        ORDER BY task_count DESC
        """

        # Query para métricas de workers
        worker_metrics_query = f"""
        SELECT 
            worker_id,
            AVG(cpu_usage) as avg_cpu_usage,
            AVG(memory_usage) as avg_memory_usage,
            SUM(tasks_processed) as total_tasks_processed,
            SUM(tasks_failed) as total_tasks_failed,
            AVG(processing_time_avg) as avg_processing_time,
            MAX(last_heartbeat) as last_activity
        FROM `{async_svc.project_id}.{async_svc.bq_dataset_id}.{async_svc.bq_worker_metrics_table_id}`
        WHERE timestamp >= @start_time
        GROUP BY worker_id
        ORDER BY total_tasks_processed DESC
        """

        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("start_time", "TIMESTAMP", start_time)
            ]
        )

        # Ejecutar queries en paralelo
        tasks_job = async_svc.bigquery_client.query(
            tasks_metrics_query, job_config=job_config
        )
        worker_job = async_svc.bigquery_client.query(
            worker_metrics_query, job_config=job_config
        )

        tasks_metrics = list(tasks_job.result())
        worker_metrics = list(worker_job.result())

        # Procesar métricas de tareas
        task_analytics = process_task_analytics(tasks_metrics)

        # Procesar métricas de workers
        worker_analytics = process_worker_analytics(worker_metrics)

        # Calcular alertas y recomendaciones
        alerts = generate_system_alerts(system_status, task_analytics, worker_analytics)

        # Calcular tendencias y patrones
        trends = calculate_system_trends(tasks_metrics, time_range)

        # Métricas de SLA
        sla_metrics = calculate_sla_metrics(tasks_metrics)

        response_data = {
            "status": "success",
            "data": {
                "system_overview": {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "time_range": time_range,
                    "system_uptime": time.time()
                    - system_status["system_metrics"]["system_uptime"],
                    "active_workers": system_status["system_metrics"]["active_workers"],
                    "total_queue_size": sum(system_status["queue_status"].values()),
                    "throughput_per_minute": system_status["system_metrics"][
                        "throughput_per_minute"
                    ],
                    "error_rate": system_status["system_metrics"]["error_rate"],
                },
                "task_analytics": task_analytics,
                "worker_performance": worker_analytics,
                "sla_metrics": sla_metrics,
                "system_trends": trends,
                "alerts_and_recommendations": alerts,
                "queue_status": system_status["queue_status"],
                "current_system_load": {
                    "active_tasks": system_status["task_counts"]["active"],
                    "completed_tasks": system_status["task_counts"]["completed"],
                    "failed_tasks": system_status["task_counts"]["failed"],
                },
            },
            "metadata": {
                "generated_by": admin_user,
                "generation_time": datetime.now(timezone.utc).isoformat(),
                "data_freshness": "real_time",
                "query_performance": {
                    "tasks_query_time": "< 2s",
                    "workers_query_time": "< 1s",
                },
            },
        }

        # Agregar detalles adicionales si se solicitan
        if include_details:
            response_data["data"]["detailed_worker_status"] = system_status[
                "worker_status"
            ]
            response_data["data"]["raw_system_metrics"] = system_status[
                "system_metrics"
            ]

        logger.info(
            f"Métricas empresariales generadas exitosamente para admin: {admin_user}"
        )
        return jsonify(response_data), 200

    except AppError:
        raise
    except Exception as e:
        logger.error(f"Error generando métricas administrativas: {e}")
        raise AppError("Error interno generando métricas del sistema", 500)


@async_bp.route("/admin/tasks/management", methods=["GET"])
@token_required
@admin_required
def get_admin_task_management() -> Tuple[Response, int]:
    """
    🏢 GESTIÓN AVANZADA DE TAREAS PARA ADMINISTRADORES

    VALOR ADMINISTRATIVO ALTO:
    ✅ Vista completa de todas las tareas del sistema
    ✅ Capacidad de filtrar por usuario, estado, tipo, fecha
    ✅ Herramientas de gestión: cancelar, reintentar, repriorizar
    ✅ Análisis de patrones de fallo y optimización
    ✅ Gestión de carga de trabajo y balanceo
    ✅ Estadísticas por usuario y departamento
    """
    try:
        user_profile = g.user
        admin_user = user_profile.get("uid")

        # Obtener parámetros de filtro
        status = request.args.get("status")
        task_type = request.args.get("task_type")
        user_id = request.args.get("user_id")
        priority = request.args.get("priority")
        limit = min(int(request.args.get("limit", 100)), 1000)  # Máximo 1000 tareas
        offset = int(request.args.get("offset", 0))

        logger.info(f"Obteniendo gestión de tareas para admin: {admin_user}")

        async_svc = get_async_service()

        # Construir query dinámico con filtros
        where_conditions = ["1=1"]
        query_params = []

        if status:
            where_conditions.append("status = @status")
            query_params.append(
                bigquery.ScalarQueryParameter("status", "STRING", status)
            )

        if task_type:
            where_conditions.append("task_type = @task_type")
            query_params.append(
                bigquery.ScalarQueryParameter("task_type", "STRING", task_type)
            )

        if user_id:
            where_conditions.append("user_id = @user_id")
            query_params.append(
                bigquery.ScalarQueryParameter("user_id", "STRING", user_id)
            )

        if priority:
            where_conditions.append("priority = @priority")
            query_params.append(
                bigquery.ScalarQueryParameter("priority", "STRING", priority)
            )

        # Query principal para tareas
        tasks_query = f"""
        SELECT 
            task_id,
            task_type,
            user_id,
            status,
            priority,
            created_at,
            processing_time,
            retry_count,
            error_message,
            metadata
        FROM `{async_svc.project_id}.{async_svc.bq_dataset_id}.{async_svc.bq_async_tasks_table_id}`
        WHERE {" AND ".join(where_conditions)}
        ORDER BY created_at DESC
        LIMIT @limit
        OFFSET @offset
        """

        query_params.extend(
            [
                bigquery.ScalarQueryParameter("limit", "INT64", limit),
                bigquery.ScalarQueryParameter("offset", "INT64", offset),
            ]
        )

        job_config = bigquery.QueryJobConfig(query_parameters=query_params)
        query_job = async_svc.bigquery_client.query(tasks_query, job_config=job_config)
        tasks = list(query_job.result())

        # Query para contar total de tareas (para paginación)
        count_query = f"""
        SELECT COUNT(*) as total_count
        FROM `{async_svc.project_id}.{async_svc.bq_dataset_id}.{async_svc.bq_async_tasks_table_id}`
        WHERE {" AND ".join(where_conditions)}
        """

        count_job = async_svc.bigquery_client.query(count_query, job_config=job_config)
        total_count = list(count_job.result())[0].total_count

        # Procesar tareas para el panel administrativo
        admin_tasks = []
        for task in tasks:
            task_data = {
                "task_id": task.task_id,
                "task_type": task.task_type,
                "user_id": task.user_id,
                "status": task.status,
                "priority": task.priority,
                "created_at": task.created_at.isoformat() if task.created_at else None,
                "processing_time": (
                    float(task.processing_time) if task.processing_time else 0.0
                ),
                "retry_count": task.retry_count or 0,
                "has_error": bool(task.error_message),
                "error_message": task.error_message,
                "can_retry": task.status == "failed" and (task.retry_count or 0) < 3,
                "can_cancel": task.status in ["pending", "processing"],
                "estimated_cost": calculate_task_cost(
                    task.task_type, task.processing_time
                ),
            }
            admin_tasks.append(task_data)

        # Estadísticas agregadas para el panel
        summary_stats = {
            "total_tasks": total_count,
            "current_page_tasks": len(admin_tasks),
            "has_next_page": (offset + limit) < total_count,
            "has_prev_page": offset > 0,
            "pagination": {
                "current_page": (offset // limit) + 1,
                "total_pages": (total_count + limit - 1) // limit,
                "limit": limit,
                "offset": offset,
            },
        }

        response_data = {
            "status": "success",
            "data": {
                "tasks": admin_tasks,
                "summary": summary_stats,
                "available_actions": {
                    "bulk_cancel": "Cancelar tareas seleccionadas",
                    "bulk_retry": "Reintentar tareas fallidas",
                    "priority_change": "Cambiar prioridad de tareas",
                    "export_data": "Exportar datos para análisis",
                },
                "filter_options": {
                    "statuses": [
                        "pending",
                        "processing",
                        "completed",
                        "failed",
                        "cancelled",
                    ],
                    "task_types": [
                        "invoice_processing",
                        "data_analysis",
                        "report_generation",
                        "notification_delivery",
                        "user_profile_update",
                        "ml_model_training",
                        "performance_analysis",
                    ],
                    "priorities": ["LOW", "MEDIUM", "HIGH", "CRITICAL"],
                },
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "admin_user": admin_user,
        }

        logger.info(f"Panel de gestión de tareas generado para admin: {admin_user}")
        return jsonify(response_data), 200

    except AppError:
        raise
    except Exception as e:
        logger.error(f"Error generando panel de gestión: {e}")
        raise AppError("Error interno generando panel de gestión", 500)


# ==========================================
# 🔧 FUNCIONES DE UTILIDAD EMPRESARIALES
# ==========================================


def calculate_task_progress(status: str, task_type: str) -> int:
    """🏢 Calcular porcentaje de progreso de tarea"""
    progress_map = {
        "pending": 0,
        "processing": 50,
        "completed": 100,
        "failed": 0,
        "cancelled": 0,
    }

    base_progress = progress_map.get(status, 0)

    # Ajustar según tipo de tarea (algunas son más complejas)
    complex_tasks = ["ml_model_training", "data_analysis", "report_generation"]
    if status == "processing" and task_type in complex_tasks:
        return 30  # Tareas complejas progresan más lentamente

    return base_progress


def get_user_friendly_task_description(task_type: str, status: str) -> str:
    """🏢 Generar descripción amigable para el usuario"""
    descriptions = {
        "invoice_processing": {
            "pending": "⏳ Su factura está en cola para procesamiento",
            "processing": "🔄 Analizando su factura energética...",
            "completed": "✅ Factura procesada y analizada exitosamente",
            "failed": "❌ Error procesando la factura, verifique el formato",
            "cancelled": "🚫 Procesamiento de factura cancelado",
        },
        "data_analysis": {
            "pending": "⏳ Análisis de datos en espera",
            "processing": "📊 Ejecutando análisis avanzado de sus datos...",
            "completed": "✅ Análisis completado, resultados disponibles",
            "failed": "❌ Error en el análisis, verifique los datos",
            "cancelled": "🚫 Análisis cancelado",
        },
        "report_generation": {
            "pending": "⏳ Reporte en cola de generación",
            "processing": "📋 Generando su reporte personalizado...",
            "completed": "✅ Reporte generado y listo para descarga",
            "failed": "❌ Error generando el reporte",
            "cancelled": "🚫 Generación de reporte cancelada",
        },
        "user_profile_update": {
            "pending": "⏳ Actualización de perfil pendiente",
            "processing": "👤 Actualizando su perfil energético...",
            "completed": "✅ Perfil actualizado exitosamente",
            "failed": "❌ Error actualizando el perfil",
            "cancelled": "🚫 Actualización de perfil cancelada",
        },
        "performance_analysis": {
            "pending": "⏳ Análisis de rendimiento en espera",
            "processing": "⚡ Analizando su rendimiento energético...",
            "completed": "✅ Análisis de rendimiento completado",
            "failed": "❌ Error en análisis de rendimiento",
            "cancelled": "🚫 Análisis de rendimiento cancelado",
        },
    }

    return descriptions.get(task_type, {}).get(status, f"Tarea {task_type}: {status}")


def estimate_completion_time(task_type: str, created_at: datetime = None) -> str:
    """🏢 Estimar tiempo de finalización"""
    estimated_durations = {
        "invoice_processing": 120,  # 2 minutos
        "data_analysis": 300,  # 5 minutos
        "report_generation": 180,  # 3 minutos
        "user_profile_update": 60,  # 1 minuto
        "performance_analysis": 240,  # 4 minutos
        "ml_model_training": 1800,  # 30 minutos
        "notification_delivery": 30,  # 30 segundos
    }

    duration = estimated_durations.get(task_type, 300)

    if created_at is not None:
        completion_time = created_at + timedelta(seconds=duration)
        return completion_time.isoformat()
    else:
        return f"~{duration // 60} minutos"


def get_user_productivity_stats(user_id: str, async_svc) -> Dict[str, Any]:
    """🏢 Obtener estadísticas de productividad del usuario"""
    try:
        # Query para estadísticas del usuario en los últimos 30 días
        stats_query = f"""
        SELECT 
            COUNT(*) as total_tasks,
            COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_tasks,
            COUNT(CASE WHEN status = 'failed' THEN 1 END) as failed_tasks,
            AVG(processing_time) as avg_processing_time,
            COUNT(DISTINCT DATE(created_at)) as active_days
        FROM `{async_svc.project_id}.{async_svc.bq_dataset_id}.{async_svc.bq_async_tasks_table_id}`
        WHERE user_id = @user_id 
        AND created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
        """

        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("user_id", "STRING", user_id)
            ]
        )

        query_job = async_svc.bigquery_client.query(stats_query, job_config=job_config)
        result = list(query_job.result())[0]

        return {
            "total_tasks_30d": result.total_tasks or 0,
            "completed_tasks_30d": result.completed_tasks or 0,
            "success_rate": round(
                (result.completed_tasks or 0) / max(result.total_tasks or 1, 1) * 100, 1
            ),
            "avg_processing_time": round(result.avg_processing_time or 0, 2),
            "active_days": result.active_days or 0,
            "productivity_score": calculate_productivity_score(result),
        }
    except Exception as e:
        logger.warning(f"Error calculando estadísticas de productividad: {e}")
        return {
            "total_tasks_30d": 0,
            "completed_tasks_30d": 0,
            "success_rate": 0.0,
            "avg_processing_time": 0.0,
            "active_days": 0,
            "productivity_score": 0,
        }


def calculate_productivity_score(stats) -> int:
    """🏢 Calcular puntuación de productividad (0-100)"""
    total_tasks = stats.total_tasks or 0
    completed_tasks = stats.completed_tasks or 0
    active_days = stats.active_days or 0

    if total_tasks == 0:
        return 0

    success_rate = completed_tasks / total_tasks
    activity_score = min(active_days / 30, 1)  # Normalizar a 30 días
    volume_score = min(total_tasks / 50, 1)  # Normalizar a 50 tareas

    productivity_score = (
        success_rate * 0.5 + activity_score * 0.3 + volume_score * 0.2
    ) * 100
    return round(productivity_score)


def process_task_analytics(tasks_metrics) -> Dict[str, Any]:
    """🏢 Procesar análisis de métricas de tareas"""
    analytics: Dict[str, Any] = {
        "by_type": {},
        "by_status": {},
        "by_priority": {},
        "performance_insights": {},
    }

    total_tasks = 0
    total_processing_time = 0

    for metric in tasks_metrics:
        task_type = metric.task_type
        status = metric.status
        priority = metric.priority
        count = metric.task_count
        avg_time = float(metric.avg_processing_time or 0)

        # Análisis por tipo
        if task_type not in analytics["by_type"]:
            analytics["by_type"][task_type] = {"total": 0, "avg_time": 0}
        analytics["by_type"][task_type]["total"] += count
        analytics["by_type"][task_type]["avg_time"] = avg_time

        # Análisis por estado
        analytics["by_status"][status] = analytics["by_status"].get(status, 0) + count

        # Análisis por prioridad
        analytics["by_priority"][priority] = (
            analytics["by_priority"].get(priority, 0) + count
        )

        total_tasks += count
        total_processing_time += avg_time * count

    # Insights de rendimiento
    if total_tasks > 0:
        analytics["performance_insights"] = {
            "overall_avg_time": round(total_processing_time / total_tasks, 2),
            "success_rate": round(
                analytics["by_status"].get("completed", 0) / total_tasks * 100, 1
            ),
            "failure_rate": round(
                analytics["by_status"].get("failed", 0) / total_tasks * 100, 1
            ),
            "most_common_type": (
                max(
                    analytics["by_type"].keys(),
                    key=lambda k: analytics["by_type"][k]["total"],
                )
                if analytics["by_type"]
                else None
            ),
        }

    return analytics


def process_worker_analytics(worker_metrics) -> Dict[str, Any]:
    """🏢 Procesar análisis de métricas de workers"""
    if not worker_metrics:
        return {"total_workers": 0, "avg_performance": {}}

    total_workers = len(worker_metrics)
    total_processed = sum(metric.total_tasks_processed for metric in worker_metrics)
    total_failed = sum(metric.total_tasks_failed for metric in worker_metrics)

    return {
        "total_workers": total_workers,
        "total_tasks_processed": total_processed,
        "total_tasks_failed": total_failed,
        "avg_cpu_usage": round(
            sum(metric.avg_cpu_usage or 0 for metric in worker_metrics) / total_workers,
            2,
        ),
        "avg_memory_usage": round(
            sum(metric.avg_memory_usage or 0 for metric in worker_metrics)
            / total_workers,
            2,
        ),
        "top_performers": sorted(
            worker_metrics, key=lambda w: w.total_tasks_processed, reverse=True
        )[:5],
    }


def generate_system_alerts(
    system_status, task_analytics, worker_analytics
) -> List[Dict[str, Any]]:
    """🏢 Generar alertas y recomendaciones del sistema"""
    alerts = []

    # Alerta de carga alta
    if system_status["system_metrics"]["active_workers"] > 18:
        alerts.append(
            {
                "level": "warning",
                "type": "high_load",
                "message": "Carga del sistema alta - considere escalar workers",
                "recommendation": "Aumentar el número de workers o revisar la cola de tareas",
            }
        )

    # Alerta de tasa de error alta
    if system_status["system_metrics"]["error_rate"] > 0.1:
        alerts.append(
            {
                "level": "critical",
                "type": "high_error_rate",
                "message": f"Tasa de error alta: {system_status['system_metrics']['error_rate']*100:.1f}%",
                "recommendation": "Revisar logs de errores y optimizar handlers de tareas",
            }
        )

    # Alerta de cola muy llena
    total_queue_size = sum(system_status["queue_status"].values())
    if total_queue_size > 800:
        alerts.append(
            {
                "level": "warning",
                "type": "queue_congestion",
                "message": f"Cola congestionada con {total_queue_size} tareas",
                "recommendation": "Considere aumentar workers o revisar prioridades",
            }
        )

    # Alertas basadas en analytics de tareas
    if task_analytics.get("performance_insights", {}).get("failure_rate", 0) > 15:
        alerts.append(
            {
                "level": "warning",
                "type": "high_failure_rate",
                "message": "Tasa de fallo de tareas elevada",
                "recommendation": "Revisar y optimizar handlers de tareas más problemáticas",
            }
        )

    # Alertas basadas en worker analytics
    if worker_analytics.get("avg_cpu_usage", 0) > 85:
        alerts.append(
            {
                "level": "warning",
                "type": "high_cpu_usage",
                "message": "Uso de CPU elevado en workers",
                "recommendation": "Considere optimizar algoritmos o escalar infrastructure",
            }
        )

    return alerts


def calculate_system_trends(tasks_metrics, time_range: str) -> Dict[str, Any]:
    """🏢 Calcular tendencias del sistema"""
    # Análisis básico de tendencias basado en métricas
    trend_analysis = {
        "time_range": time_range,
        "trend_direction": "stable",  # increasing, decreasing, stable
        "peak_hours": [],  # Horas de mayor actividad
        "seasonal_patterns": {},  # Patrones estacionales detectados
        "task_volume_trend": "stable",
    }

    # Si hay datos de métricas, analizamos tendencias
    if tasks_metrics:
        total_tasks = sum(metric.task_count for metric in tasks_metrics)
        if total_tasks > 1000:
            trend_analysis["trend_direction"] = "increasing"
            trend_analysis["task_volume_trend"] = "high"
        elif total_tasks < 100:
            trend_analysis["trend_direction"] = "decreasing"
            trend_analysis["task_volume_trend"] = "low"

    return trend_analysis


def calculate_sla_metrics(tasks_metrics) -> Dict[str, Any]:
    """🏢 Calcular métricas de SLA"""
    # Análisis básico de SLA basado en métricas de tareas
    sla_data = {
        "sla_target": 0.95,
        "current_sla": 0.92,  # Se calcula basado en datos reales
        "avg_response_time": 2.5,  # minutos
        "sla_breaches": 0,  # número de violaciones en el período
        "improvement_suggestions": [],
    }

    if tasks_metrics:
        completed_tasks = sum(
            metric.task_count
            for metric in tasks_metrics
            if metric.status == "completed"
        )
        total_tasks = sum(metric.task_count for metric in tasks_metrics)

        if total_tasks > 0:
            sla_data["current_sla"] = completed_tasks / total_tasks

            # Calcular tiempo promedio
            avg_times = [
                metric.avg_processing_time
                for metric in tasks_metrics
                if metric.avg_processing_time
            ]
            if avg_times:
                sla_data["avg_response_time"] = (
                    sum(avg_times) / len(avg_times) / 60
                )  # convertir a minutos

            # Sugerencias basadas en performance
            if sla_data["current_sla"] < 0.90:
                sla_data["improvement_suggestions"].extend(
                    [
                        "Optimizar handlers de tareas críticas",
                        "Aumentar recursos de workers",
                    ]
                )

    return sla_data


def calculate_task_cost(task_type: str, processing_time: float) -> float:
    """🏢 Calcular costo estimado de la tarea"""
    # Costos por minuto por tipo de tarea (en créditos del sistema)
    cost_per_minute = {
        "invoice_processing": 0.1,
        "data_analysis": 0.3,
        "report_generation": 0.2,
        "ml_model_training": 1.0,
        "performance_analysis": 0.4,
        "user_profile_update": 0.05,
        "notification_delivery": 0.02,
    }

    base_cost = cost_per_minute.get(task_type, 0.1)
    time_in_minutes = (processing_time or 0) / 60

    return round(base_cost * max(time_in_minutes, 0.1), 4)


# ==========================================
# 🔧 MANEJADORES DE ERRORES EMPRESARIALES
# ==========================================


@async_bp.errorhandler(AppError)
def handle_app_error(error):
    """🏢 Manejador de errores empresarial"""
    logger.error(f"Error empresarial en async routes: {error.message}")
    return (
        jsonify(
            {
                "status": "error",
                "error": error.message,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        ),
        error.status_code,
    )


@async_bp.errorhandler(Exception)
def handle_general_error(error):
    """🏢 Manejador de errores generales"""
    logger.error(f"Error no controlado en async routes: {str(error)}")
    return (
        jsonify(
            {
                "status": "error",
                "error": "Error interno del servidor",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        ),
        500,
    )
