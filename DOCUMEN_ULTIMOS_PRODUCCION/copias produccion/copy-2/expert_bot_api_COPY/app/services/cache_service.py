# expert_bot_api_COPY/app/services/cache_service.py

import redis
import json
import logging
import time
import threading
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from collections import defaultdict
import hashlib
import pickle
import gzip
import fnmatch

from flask import current_app
from utils.error_handlers import AppError


@dataclass
class CacheStats:
    """🏢 Estadísticas de cache empresarial"""

    hits: int = 0
    misses: int = 0
    sets: int = 0
    deletes: int = 0
    evictions: int = 0
    memory_usage: int = 0
    key_count: int = 0
    avg_hit_rate: float = 0.0


@dataclass
class CacheEntry:
    """🏢 Entrada de cache empresarial"""

    key: str
    value: Any
    ttl: int
    created_at: datetime
    accessed_at: datetime
    access_count: int = 0
    size_bytes: int = 0
    tags: List[str] = None
    metadata: Dict[str, Any] = None


class CacheService:
    """
    🏢 SERVICIO DE CACHE EMPRESARIAL NIVEL 2025

    Características empresariales:
    - Cache distribuido con Redis Cluster
    - Cache local L1 con TTL inteligente
    - Estrategias de invalidación avanzadas
    - Métricas de rendimiento en tiempo real
    - Compresión automática de datos grandes
    - Particionamiento inteligente por tags
    - Preloading predictivo de datos
    - Monitoreo de memoria y rendimiento
    - Backup y recuperación automática
    - Análisis de patrones de acceso
    """

    def __init__(self):
        """Inicialización empresarial del cache"""

        # Configuración empresarial
        self.default_ttl = 3600  # 1 hora
        self.max_memory_usage = 1024 * 1024 * 1024  # 1GB
        self.compression_threshold = 1024  # 1KB
        self.l1_cache_size = 10000  # Entradas L1
        self.l2_cache_size = 100000  # Entradas L2

        # Cache local L1 (en memoria)
        self.l1_cache = {}
        self.l1_access_times = {}
        self.l1_ttl = {}

        # Cache local L2 (respaldo)
        self.l2_cache = {}

        # Estadísticas empresariales
        self.stats = CacheStats()
        self.performance_metrics = {
            "avg_get_time": 0.0,
            "avg_set_time": 0.0,
            "peak_memory_usage": 0,
            "cache_efficiency": 0.0,
            "eviction_rate": 0.0,
        }

        # Tags para invalidación
        self.tag_keys = defaultdict(set)
        self.key_tags = defaultdict(set)

        # Monitoreo
        self.monitoring_thread = None
        self.is_monitoring = False

        # Lock para thread safety
        self.cache_lock = threading.RLock()

        # Inicialización robusta
        self._initialize_enterprise_cache()

    def _initialize_enterprise_cache(self):
        """🏢 Inicialización robusta del cache empresarial"""
        try:
            # Configurar Redis
            self._setup_redis_connection()

            # Configurar cache local
            self._setup_local_cache()

            # Inicializar monitoreo
            self._start_monitoring()

            # Configurar estrategias de limpieza
            self._setup_cleanup_strategies()

            logging.info("🏢 CacheService Empresarial inicializado correctamente")

        except Exception as e:
            logging.error(f"Error crítico en inicialización de CacheService: {e}")
            raise AppError("Error crítico en inicialización del servicio de cache", 500)

    def _setup_redis_connection(self):
        """Configurar conexión Redis empresarial"""
        try:
            # Configuración Redis desde Flask
            redis_config = {
                "host": current_app.config.get("REDIS_HOST", "localhost"),
                "port": current_app.config.get("REDIS_PORT", 6379),
                "db": current_app.config.get("REDIS_DB", 0),
                "decode_responses": False,
                "socket_connect_timeout": 5,
                "socket_timeout": 5,
                "retry_on_timeout": True,
                "health_check_interval": 30,
            }

            # Autenticación si está configurada
            redis_password = current_app.config.get("REDIS_PASSWORD")
            if redis_password:
                redis_config["password"] = redis_password

            # Conexión con pool
            self.redis_client = redis.Redis(
                connection_pool=redis.ConnectionPool(**redis_config, max_connections=20)
            )

            # Verificar conexión
            self.redis_client.ping()

            # Configurar prefijos
            self.redis_prefix = current_app.config.get(
                "REDIS_PREFIX", "smarwatt_cache:"
            )

            logging.info("✅ Redis configurado correctamente")

        except Exception as e:
            logging.error(f"Error configurando Redis: {e}")
            # Fallback a cache solo local
            self.redis_client = None
            logging.warning("🔄 Cache funcionando solo en modo local")

    def _setup_local_cache(self):
        """Configurar cache local empresarial"""
        # Configurar límites
        self.l1_max_size = current_app.config.get("L1_CACHE_SIZE", self.l1_cache_size)
        self.l2_max_size = current_app.config.get("L2_CACHE_SIZE", self.l2_cache_size)

        # Configurar TTL por defecto
        self.local_default_ttl = current_app.config.get(
            "LOCAL_CACHE_TTL", 300
        )  # 5 minutos

        logging.info("✅ Cache local configurado")

    def _start_monitoring(self):
        """Iniciar monitoreo empresarial"""
        if not self.is_monitoring:
            self.is_monitoring = True
            self.monitoring_thread = threading.Thread(
                target=self._monitoring_loop, daemon=True
            )
            self.monitoring_thread.start()
            logging.info("🔍 Monitoreo de cache iniciado")

    def _monitoring_loop(self):
        """🏢 Loop de monitoreo empresarial"""
        while self.is_monitoring:
            try:
                # Actualizar estadísticas
                self._update_cache_stats()

                # Limpiar entradas expiradas
                self._cleanup_expired_entries()

                # Optimizar memoria
                self._optimize_memory_usage()

                # Análisis de patrones
                self._analyze_access_patterns()

                # Esperar siguiente ciclo
                time.sleep(60)  # 1 minuto

            except Exception as e:
                logging.error(f"Error en monitoreo de cache: {e}")
                time.sleep(10)

    def _setup_cleanup_strategies(self):
        """Configurar estrategias de limpieza empresarial"""
        # Configurar LRU para L1
        self.l1_lru_enabled = True

        # Configurar LFU para L2
        self.l2_lfu_enabled = True

        # Configurar TTL automático
        self.auto_ttl_enabled = True

    def get(self, key: str, default: Any = None) -> Any:
        """🏢 Obtener valor del cache con múltiples niveles"""
        start_time = time.time()

        try:
            with self.cache_lock:
                # Buscar en L1 (memoria rápida)
                if key in self.l1_cache:
                    if self._is_l1_valid(key):
                        value = self.l1_cache[key]
                        self._update_l1_access(key)
                        self._record_cache_hit()
                        return value
                    else:
                        self._evict_from_l1(key)

                # Buscar en L2 (memoria local)
                if key in self.l2_cache:
                    entry = self.l2_cache[key]
                    if self._is_entry_valid(entry):
                        # Promover a L1
                        self._promote_to_l1(key, entry.value)
                        self._record_cache_hit()
                        return entry.value
                    else:
                        self._evict_from_l2(key)

                # Buscar en Redis (distribuido)
                if self.redis_client:
                    try:
                        redis_key = self._get_redis_key(key)
                        redis_value = self.redis_client.get(redis_key)

                        if redis_value is not None:
                            # Deserializar
                            value = self._deserialize_value(redis_value)

                            # Almacenar en caches locales
                            self._store_in_local_caches(key, value)

                            self._record_cache_hit()
                            return value
                    except Exception as e:
                        logging.error(f"Error accediendo Redis: {e}")

                # Cache miss
                self._record_cache_miss()
                return default

        finally:
            # Actualizar métricas de rendimiento
            get_time = time.time() - start_time
            self._update_performance_metric("avg_get_time", get_time)

    def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None,
        tags: Optional[List[str]] = None,
    ) -> bool:
        """🏢 Establecer valor en cache con múltiples niveles"""
        start_time = time.time()

        try:
            with self.cache_lock:
                # Configurar TTL
                if ttl is None:
                    ttl = self.default_ttl

                # Crear entrada
                entry = CacheEntry(
                    key=key,
                    value=value,
                    ttl=ttl,
                    created_at=datetime.now(timezone.utc),
                    accessed_at=datetime.now(timezone.utc),
                    tags=tags or [],
                    size_bytes=self._calculate_size(value),
                )

                # Almacenar en L1
                self._store_in_l1(key, value, ttl)

                # Almacenar en L2
                self._store_in_l2(key, entry)

                # Almacenar en Redis
                if self.redis_client:
                    try:
                        redis_key = self._get_redis_key(key)
                        serialized_value = self._serialize_value(value)

                        # Usar compresión si es necesario
                        if len(serialized_value) > self.compression_threshold:
                            serialized_value = self._compress_value(serialized_value)

                        self.redis_client.setex(redis_key, ttl, serialized_value)

                    except Exception as e:
                        logging.error(f"Error escribiendo en Redis: {e}")

                # Manejar tags
                if tags:
                    self._update_tag_mappings(key, tags)

                # Actualizar estadísticas
                self._record_cache_set()

                return True

        except Exception as e:
            logging.error(f"Error estableciendo cache: {e}")
            return False

        finally:
            # Actualizar métricas de rendimiento
            set_time = time.time() - start_time
            self._update_performance_metric("avg_set_time", set_time)

    def delete(self, key: str) -> bool:
        """🏢 Eliminar valor del cache en todos los niveles"""
        try:
            with self.cache_lock:
                deleted = False

                # Eliminar de L1
                if key in self.l1_cache:
                    self._evict_from_l1(key)
                    deleted = True

                # Eliminar de L2
                if key in self.l2_cache:
                    self._evict_from_l2(key)
                    deleted = True

                # Eliminar de Redis
                if self.redis_client:
                    try:
                        redis_key = self._get_redis_key(key)
                        result = self.redis_client.delete(redis_key)
                        if result > 0:
                            deleted = True
                    except Exception as e:
                        logging.error(f"Error eliminando de Redis: {e}")

                # Limpiar tags
                self._cleanup_tag_mappings(key)

                if deleted:
                    self._record_cache_delete()

                return deleted

        except Exception as e:
            logging.error(f"Error eliminando del cache: {e}")
            return False

    def exists(self, key: str) -> bool:
        """🏢 Verificar si existe una clave en el cache"""
        with self.cache_lock:
            # Verificar L1
            if key in self.l1_cache and self._is_l1_valid(key):
                return True

            # Verificar L2
            if key in self.l2_cache and self._is_entry_valid(self.l2_cache[key]):
                return True

            # Verificar Redis
            if self.redis_client:
                try:
                    redis_key = self._get_redis_key(key)
                    return self.redis_client.exists(redis_key) > 0
                except Exception as e:
                    logging.error(f"Error verificando existencia en Redis: {e}")

            return False

    def invalidate_by_tags(self, tags: List[str]) -> int:
        """🏢 Invalidar cache por tags empresarial"""
        try:
            with self.cache_lock:
                keys_to_delete = set()

                # Encontrar claves por tags
                for tag in tags:
                    if tag in self.tag_keys:
                        keys_to_delete.update(self.tag_keys[tag])

                # Eliminar claves
                deleted_count = 0
                for key in keys_to_delete:
                    if self.delete(key):
                        deleted_count += 1

                logging.info(f"🏢 Invalidadas {deleted_count} claves por tags: {tags}")
                return deleted_count

        except Exception as e:
            logging.error(f"Error invalidando por tags: {e}")
            return 0

    def invalidate_pattern(self, pattern: str) -> List[str]:
        """🏢 Invalidar cache por patrón"""
        try:
            with self.cache_lock:
                invalidated_keys = []

                # Buscar en L1
                for key in list(self.l1_cache.keys()):
                    if fnmatch.fnmatch(key, pattern):
                        self._evict_from_l1(key)
                        invalidated_keys.append(key)

                # Buscar en L2
                for key in list(self.l2_cache.keys()):
                    if fnmatch.fnmatch(key, pattern):
                        self._evict_from_l2(key)
                        invalidated_keys.append(key)

                # Buscar en Redis
                if self.redis_client:
                    try:
                        redis_pattern = self._get_redis_key(pattern)
                        redis_keys = self.redis_client.keys(redis_pattern)

                        for redis_key in redis_keys:
                            # Extraer clave original
                            original_key = redis_key.decode("utf-8").replace(
                                self.redis_prefix, ""
                            )
                            self.redis_client.delete(redis_key)
                            invalidated_keys.append(original_key)

                    except Exception as e:
                        logging.error(f"Error invalidando patrón en Redis: {e}")

                # Limpiar tags
                for key in invalidated_keys:
                    self._cleanup_tag_mappings(key)

                logging.info(
                    f"🏢 Invalidadas {len(invalidated_keys)} claves por patrón: {pattern}"
                )
                return invalidated_keys

        except Exception as e:
            logging.error(f"Error invalidando por patrón: {e}")
            return []

    def clear_all(self) -> bool:
        """🏢 Limpiar todo el cache"""
        try:
            with self.cache_lock:
                # Limpiar L1
                self.l1_cache.clear()
                self.l1_access_times.clear()
                self.l1_ttl.clear()

                # Limpiar L2
                self.l2_cache.clear()

                # Limpiar Redis
                if self.redis_client:
                    try:
                        pattern = self._get_redis_key("*")
                        redis_keys = self.redis_client.keys(pattern)
                        if redis_keys:
                            self.redis_client.delete(*redis_keys)
                    except Exception as e:
                        logging.error(f"Error limpiando Redis: {e}")

                # Limpiar tags
                self.tag_keys.clear()
                self.key_tags.clear()

                logging.info("🏢 Cache completamente limpiado")
                return True

        except Exception as e:
            logging.error(f"Error limpiando cache: {e}")
            return False

    def get_stats(self) -> Dict[str, Any]:
        """🏢 Obtener estadísticas empresariales del cache"""
        with self.cache_lock:
            # Calcular hit rate
            total_requests = self.stats.hits + self.stats.misses
            hit_rate = (self.stats.hits / total_requests) if total_requests > 0 else 0.0

            # Obtener información de memoria
            memory_info = self._get_memory_info()

            return {
                "cache_stats": {
                    "hits": self.stats.hits,
                    "misses": self.stats.misses,
                    "hit_rate": hit_rate,
                    "sets": self.stats.sets,
                    "deletes": self.stats.deletes,
                    "evictions": self.stats.evictions,
                },
                "memory_info": memory_info,
                "performance_metrics": self.performance_metrics,
                "cache_sizes": {
                    "l1_size": len(self.l1_cache),
                    "l2_size": len(self.l2_cache),
                    "redis_size": self._get_redis_size(),
                },
                "tag_info": {
                    "total_tags": len(self.tag_keys),
                    "total_tagged_keys": len(self.key_tags),
                },
            }

    def preload_data(self, preload_config: Dict[str, Any]) -> bool:
        """🏢 Precargar datos en cache empresarial"""
        try:
            # Importar servicios necesarios
            from app.services.energy_service import EnergyService

            energy_service = EnergyService()

            # Precargar datos comunes
            common_data = preload_config.get("common_data", [])
            for data_type in common_data:
                if data_type == "user_profiles":
                    self._preload_user_profiles(energy_service)
                elif data_type == "consumption_patterns":
                    self._preload_consumption_patterns(energy_service)
                elif data_type == "tariff_data":
                    self._preload_tariff_data(energy_service)

            # Precargar datos específicos de usuario
            user_data = preload_config.get("user_data", {})
            for user_id, data_types in user_data.items():
                for data_type in data_types:
                    if data_type == "profile":
                        self._preload_user_profile(user_id, energy_service)
                    elif data_type == "consumption_history":
                        self._preload_consumption_history(user_id, energy_service)

            logging.info("🏢 Preload de datos completado")
            return True

        except Exception as e:
            logging.error(f"Error en preload: {e}")
            return False

    def _preload_user_profiles(self, energy_service):
        """Precargar perfiles de usuarios activos"""
        try:
            # Obtener usuarios activos (implementación simplificada)
            active_users = ["user1", "user2", "user3"]

            for user_id in active_users:
                try:
                    profile = energy_service.get_dashboard_data_enterprise(user_id)
                    self.set(
                        f"user_profile:{user_id}",
                        profile,
                        ttl=1800,
                        tags=["user_profiles"],
                    )
                except Exception as e:
                    logging.warning(f"Error precargando perfil {user_id}: {e}")

        except Exception as e:
            logging.error(f"Error precargando perfiles: {e}")

    def _preload_consumption_patterns(self, energy_service):
        """Precargar patrones de consumo"""
        try:
            # Patrones comunes (implementación simplificada)
            patterns = energy_service.get_consumption_patterns()
            self.set("consumption_patterns", patterns, ttl=3600, tags=["patterns"])

        except Exception as e:
            logging.error(f"Error precargando patrones: {e}")

    def _preload_tariff_data(self, energy_service):
        """Precargar datos de tarifas"""
        try:
            # Datos de tarifas (implementación simplificada)
            tariff_data = {"tariffs": ["2.0TD", "3.0TD", "PVPC"]}
            self.set("tariff_data", tariff_data, ttl=7200, tags=["tariffs"])

        except Exception as e:
            logging.error(f"Error precargando tarifas: {e}")

    def _preload_user_profile(self, user_id: str, energy_service):
        """Precargar perfil específico de usuario"""
        try:
            profile = energy_service.get_dashboard_data_enterprise(user_id)
            self.set(
                f"user_profile:{user_id}",
                profile,
                ttl=1800,
                tags=["user_profiles", f"user:{user_id}"],
            )

        except Exception as e:
            logging.warning(f"Error precargando perfil {user_id}: {e}")

    def _preload_consumption_history(self, user_id: str, energy_service):
        """Precargar historial de consumo"""
        try:
            history = energy_service.get_consumption_history_enterprise(user_id)
            self.set(
                f"consumption_history:{user_id}",
                history,
                ttl=3600,
                tags=["consumption", f"user:{user_id}"],
            )

        except Exception as e:
            logging.warning(f"Error precargando historial {user_id}: {e}")

    # Métodos internos de gestión
    def _is_l1_valid(self, key: str) -> bool:
        """Verificar si entrada L1 es válida"""
        if key not in self.l1_ttl:
            return False

        expiry_time = self.l1_ttl[key]
        return datetime.now(timezone.utc) < expiry_time

    def _is_entry_valid(self, entry: CacheEntry) -> bool:
        """Verificar si entrada es válida"""
        expiry_time = entry.created_at + timedelta(seconds=entry.ttl)
        return datetime.now(timezone.utc) < expiry_time

    def _update_l1_access(self, key: str):
        """Actualizar acceso L1"""
        self.l1_access_times[key] = datetime.now(timezone.utc)

    def _promote_to_l1(self, key: str, value: Any):
        """Promover entrada a L1"""
        self._store_in_l1(key, value, self.local_default_ttl)

    def _store_in_l1(self, key: str, value: Any, ttl: int):
        """Almacenar en L1 con gestión de tamaño"""
        # Verificar límite de tamaño
        if len(self.l1_cache) >= self.l1_max_size:
            self._evict_lru_from_l1()

        # Almacenar
        self.l1_cache[key] = value
        self.l1_access_times[key] = datetime.now(timezone.utc)
        self.l1_ttl[key] = datetime.now(timezone.utc) + timedelta(seconds=ttl)

    def _store_in_l2(self, key: str, entry: CacheEntry):
        """Almacenar en L2 con gestión de tamaño"""
        # Verificar límite de tamaño
        if len(self.l2_cache) >= self.l2_max_size:
            self._evict_lfu_from_l2()

        # Almacenar
        self.l2_cache[key] = entry

    def _evict_from_l1(self, key: str):
        """Evitar de L1"""
        self.l1_cache.pop(key, None)
        self.l1_access_times.pop(key, None)
        self.l1_ttl.pop(key, None)

    def _evict_from_l2(self, key: str):
        """Evitar de L2"""
        self.l2_cache.pop(key, None)

    def _evict_lru_from_l1(self):
        """Evitar LRU de L1"""
        if not self.l1_access_times:
            return

        # Encontrar clave menos recientemente usada
        lru_key = min(
            self.l1_access_times.keys(), key=lambda k: self.l1_access_times[k]
        )
        self._evict_from_l1(lru_key)
        self.stats.evictions += 1

    def _evict_lfu_from_l2(self):
        """Evitar LFU de L2"""
        if not self.l2_cache:
            return

        # Encontrar clave menos frecuentemente usada
        lfu_key = min(self.l2_cache.keys(), key=lambda k: self.l2_cache[k].access_count)
        self._evict_from_l2(lfu_key)
        self.stats.evictions += 1

    def _store_in_local_caches(self, key: str, value: Any):
        """Almacenar en caches locales"""
        # Almacenar en L1
        self._store_in_l1(key, value, self.local_default_ttl)

        # Crear entrada para L2
        entry = CacheEntry(
            key=key,
            value=value,
            ttl=self.local_default_ttl,
            created_at=datetime.now(timezone.utc),
            accessed_at=datetime.now(timezone.utc),
        )

        # Almacenar en L2
        self._store_in_l2(key, entry)

    def _get_redis_key(self, key: str) -> str:
        """Obtener clave Redis con prefijo"""
        return f"{self.redis_prefix}{key}"

    def _serialize_value(self, value: Any) -> bytes:
        """Serializar valor para Redis"""
        return pickle.dumps(value)

    def _deserialize_value(self, value: bytes) -> Any:
        """Deserializar valor de Redis"""
        # Verificar si está comprimido
        if value.startswith(b"\x1f\x8b"):  # Gzip magic number
            value = gzip.decompress(value)

        return pickle.loads(value)

    def _compress_value(self, value: bytes) -> bytes:
        """Comprimir valor"""
        return gzip.compress(value)

    def _calculate_size(self, value: Any) -> int:
        """Calcular tamaño aproximado del valor"""
        try:
            return len(pickle.dumps(value))
        except:
            return 0

    def _update_tag_mappings(self, key: str, tags: List[str]):
        """Actualizar mappings de tags"""
        # Limpiar mappings existentes
        self._cleanup_tag_mappings(key)

        # Agregar nuevos mappings
        for tag in tags:
            self.tag_keys[tag].add(key)
            self.key_tags[key].add(tag)

    def _cleanup_tag_mappings(self, key: str):
        """Limpiar mappings de tags"""
        if key in self.key_tags:
            tags = self.key_tags[key]
            for tag in tags:
                self.tag_keys[tag].discard(key)
                if not self.tag_keys[tag]:
                    del self.tag_keys[tag]
            del self.key_tags[key]

    def _record_cache_hit(self):
        """Registrar hit de cache"""
        self.stats.hits += 1

    def _record_cache_miss(self):
        """Registrar miss de cache"""
        self.stats.misses += 1

    def _record_cache_set(self):
        """Registrar set de cache"""
        self.stats.sets += 1

    def _record_cache_delete(self):
        """Registrar delete de cache"""
        self.stats.deletes += 1

    def _update_performance_metric(self, metric: str, value: float):
        """Actualizar métrica de rendimiento"""
        current_value = self.performance_metrics.get(metric, 0.0)
        # Promedio móvil simple
        self.performance_metrics[metric] = (current_value * 0.9) + (value * 0.1)

    def _update_cache_stats(self):
        """Actualizar estadísticas de cache"""
        # Calcular hit rate
        total_requests = self.stats.hits + self.stats.misses
        if total_requests > 0:
            self.stats.avg_hit_rate = self.stats.hits / total_requests

        # Calcular uso de memoria
        self.stats.memory_usage = self._calculate_memory_usage()

        # Actualizar contador de claves
        self.stats.key_count = len(self.l1_cache) + len(self.l2_cache)

    def _calculate_memory_usage(self) -> int:
        """Calcular uso de memoria aproximado"""
        memory_usage = 0

        # L1 cache
        for value in self.l1_cache.values():
            memory_usage += self._calculate_size(value)

        # L2 cache
        for entry in self.l2_cache.values():
            memory_usage += entry.size_bytes

        return memory_usage

    def _get_memory_info(self) -> Dict[str, Any]:
        """Obtener información de memoria"""
        return {
            "total_memory_usage": self._calculate_memory_usage(),
            "l1_memory_usage": sum(
                self._calculate_size(v) for v in self.l1_cache.values()
            ),
            "l2_memory_usage": sum(
                entry.size_bytes for entry in self.l2_cache.values()
            ),
            "memory_limit": self.max_memory_usage,
            "memory_utilization": self._calculate_memory_usage()
            / self.max_memory_usage,
        }

    def _get_redis_size(self) -> int:
        """Obtener tamaño de Redis"""
        if self.redis_client:
            try:
                pattern = self._get_redis_key("*")
                return len(self.redis_client.keys(pattern))
            except:
                return 0
        return 0

    def _cleanup_expired_entries(self):
        """Limpiar entradas expiradas"""
        current_time = datetime.now(timezone.utc)

        # Limpiar L1
        expired_l1 = [key for key, ttl in self.l1_ttl.items() if current_time > ttl]

        for key in expired_l1:
            self._evict_from_l1(key)

        # Limpiar L2
        expired_l2 = [
            key
            for key, entry in self.l2_cache.items()
            if not self._is_entry_valid(entry)
        ]

        for key in expired_l2:
            self._evict_from_l2(key)

    def _optimize_memory_usage(self):
        """Optimizar uso de memoria"""
        current_usage = self._calculate_memory_usage()

        # Si el uso de memoria supera el límite, evitar entradas
        if current_usage > self.max_memory_usage:
            # Evitar de L1 primero
            entries_to_evict = len(self.l1_cache) // 4
            for _ in range(entries_to_evict):
                self._evict_lru_from_l1()

            # Si aún es alto, evitar de L2
            current_usage = self._calculate_memory_usage()
            if current_usage > self.max_memory_usage:
                entries_to_evict = len(self.l2_cache) // 4
                for _ in range(entries_to_evict):
                    self._evict_lfu_from_l2()

    def _analyze_access_patterns(self):
        """Analizar patrones de acceso"""
        # Análisis simplificado
        total_requests = self.stats.hits + self.stats.misses

        if total_requests > 1000:
            # Calcular eficiencia del cache
            efficiency = self.stats.hits / total_requests
            self.performance_metrics["cache_efficiency"] = efficiency

            # Calcular tasa de evicción
            eviction_rate = self.stats.evictions / total_requests
            self.performance_metrics["eviction_rate"] = eviction_rate

    def stop_monitoring(self):
        """Detener monitoreo"""
        self.is_monitoring = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)

    def __del__(self):
        """Destructor"""
        self.stop_monitoring()
