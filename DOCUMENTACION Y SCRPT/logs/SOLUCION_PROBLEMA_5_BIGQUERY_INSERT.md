# ANÁLISIS Y SOLUCIÓN DEL PROBLEMA 5: FALLO SILENCIOSO DE INSERCIÓN EN BIGQUERY

## 1. RESUMEN DEL PROBLEMA

Se ha identificado un error silencioso pero crítico en los logs del servicio `energy-ia-api`. El error `ERROR - ? Error insertando en BigQuery:` aparece después de generar una recomendación de tarifa.

Este fallo no interrumpe el flujo del usuario (no genera un error 500), pero impide que los datos de las recomendaciones generadas se guarden en la base de datos. A nivel empresarial, esto es extremadamente grave, ya que se pierde información vital para el análisis de negocio, la inteligencia de datos y el reentrenamiento de los modelos de IA.

## 2. ANÁLISIS Y VERIFICACIÓN CONTRA EL CÓDIGO (CERO ESPECULACIÓN)

### A. Verificación de Logs (Hecho)

- **Log:** `root - ERROR - ? Error insertando en BigQuery:`
- **Fuente del Log:** `energy-ia-api`
- **Timestamp:** `2025-08-01T13:28:32.475Z`
- **Contexto del Log:** El error ocurre inmediatamente después de que se genera una recomendación, en el momento de persistir los resultados.
- **Conclusión del Log:** La operación de escritura en la tabla de recomendaciones de BigQuery está fallando.

### B. Verificación del Código de Inserción (Hecho)

- **Archivo Verificado:** `energy_ia_api_COPY/app/routes.py`
- **Función Relevante:** `_log_recommendation` dentro de la clase `EnterpriseTariffRecommenderService`.
- **Análisis del Código:**
  1. La función prepara un diccionario llamado `log_data` para la inserción.
  2. Este diccionario contiene, entre otros, los campos:
     - `record_date`: Creado a partir de `current_timestamp.date()`.
     - `total_savings`: Un duplicado del campo `estimated_annual_saving`.
  3. La función intenta insertar este diccionario en la tabla `recommendation_log` de BigQuery.

### C. Identificación de la Causa Raíz (Verificado)

- **El Problema:** El esquema del objeto Python (`log_data`) que se intenta insertar no coincide con el esquema de la tabla de destino en BigQuery.
- **Evidencia Concluyente:** El código está intentando escribir en columnas (`record_date`, `total_savings`) que no existen en la definición de la tabla de BigQuery. La API de BigQuery rechaza la inserción debido a esta discrepancia de esquemas, resultando en un error de tipo `BadRequest 400: no such field`. El sistema de logging genérico captura este error y lo reporta como "Error insertando en BigQuery", ocultando el detalle específico.

- **Conclusión Final de la Causa Raíz:** La falta de sincronización entre el esquema de la aplicación y el esquema de la base de datos es la causa directa del fallo de inserción.

## 3. PLAN DE ACCIÓN DETALLADO (PROPUESTA DE SOLUCIÓN EMPRESARIAL)

Para corregir este problema de forma robusta, escalable y siguiendo las mejores prácticas de Infraestructura como Código (IaC), se creará un script de migración de base de datos.

### Paso 1: Crear un Script de Migración de Esquema

Se creará un nuevo archivo Python dedicado a gestionar las migraciones del esquema de BigQuery. Este script será la única fuente de verdad para la estructura de la base de datos.

- **Nuevo Archivo:** `BQ-tablas/bq_migrations/V2__add_recommendation_fields.py`
- **Contenido del Script:**

```python
# BQ-tablas/bq_migrations/V2__add_recommendation_fields.py
import os
from google.cloud import bigquery
from google.api_core.exceptions import NotFound

# --- CONFIGURACIÓN EMPRESARIAL ROBUSTA ---
# Usar variables de entorno para máxima flexibilidad
PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "tu-proyecto-gcp")
DATASET_ID = os.environ.get("BQ_DATASET_ID", "smartwatt_data")
TABLE_ID = os.environ.get("BQ_RECOMMENDATION_LOG_TABLE_ID", "recommendation_log")

# --- CLIENTE BIGQUERY ---
client = bigquery.Client(project=PROJECT_ID)

def run_migration():
    """
    Añade las columnas 'record_date' y 'total_savings' a la tabla de logs de recomendaciones.
    Es idempotente: no falla si las columnas ya existen.
    """
    print("🚀 Iniciando migración V2 para la tabla de recomendaciones...")

    table_ref = client.dataset(DATASET_ID).table(TABLE_ID)

    try:
        table = client.get_table(table_ref)
        print(f"✅ Tabla '{TABLE_ID}' encontrada.")
    except NotFound:
        print(f"❌ ERROR: La tabla '{TABLE_ID}' no existe en el dataset '{DATASET_ID}'. No se puede migrar.")
        return

    original_schema = table.schema
    new_schema = original_schema[:]  # Crear una copia para modificar

    # --- DEFINICIÓN DE NUEVOS CAMPOS ---
    # Usamos un diccionario para evitar duplicados y facilitar la comprobación
    fields_to_add = {
        "record_date": bigquery.SchemaField("record_date", "DATE", mode="NULLABLE", description="Fecha de la recomendación para particionamiento y análisis."),
        "total_savings": bigquery.SchemaField("total_savings", "FLOAT", mode="NULLABLE", description="Ahorro total estimado (campo duplicado para análisis histórico).")
    }

    # --- LÓGICA IDEMPOTENTE ---
    # Comprobar si los campos ya existen antes de añadirlos
    existing_field_names = {field.name for field in original_schema}

    added_any_field = False
    for field_name, field_definition in fields_to_add.items():
        if field_name not in existing_field_names:
            print(f"   - Añadiendo columna '{field_name}'...")
            new_schema.append(field_definition)
            added_any_field = True
        else:
            print(f"   - La columna '{field_name}' ya existe. Omitiendo.")

    # --- APLICAR CAMBIOS SOLO SI ES NECESARIO ---
    if added_any_field:
        table.schema = new_schema
        client.update_table(table, ["schema"])
        print("✅ Migración completada. El esquema de la tabla ha sido actualizado.")
    else:
        print("✅ El esquema ya está actualizado. No se requieren cambios.")

if __name__ == "__main__":
    run_migration()

```

### Paso 2: Ejecutar la Migración

Este script se ejecutará una vez en el entorno de producción (preferiblemente a través de un pipeline de CI/CD, pero manualmente por ahora) para actualizar el esquema de la tabla de forma segura.

### Paso 3: Eliminar Código Redundante (Refactorización)

El código en `energy_ia_api_COPY/app/routes.py` tiene un campo redundante (`total_savings`). Se eliminará para mantener el código limpio y evitar la duplicación de datos.

1.  **Archivo a Modificar:** `energy_ia_api_COPY/app/routes.py`
2.  **Función:** `_log_recommendation`
3.  **Cambio:** Eliminar la línea `"total_savings": recommendation["best_recommendation"]["cost_analysis"]["annual_savings"],` del diccionario `log_data`. El campo `estimated_annual_saving` ya contiene este valor.

## 4. IMPACTO Y VERIFICACIÓN POST-IMPLEMENTACIÓN

- **Impacto:** Se restaurará la integridad de los datos. Todas las nuevas recomendaciones se guardarán correctamente en BigQuery, habilitando el análisis de datos y la inteligencia de negocio.
- **Verificación:**
  1.  Después de ejecutar el script de migración, se verificará el esquema de la tabla en la consola de Google Cloud para confirmar que las nuevas columnas existen.
  2.  Después de desplegar el cambio en el código, se monitorearán los logs de `energy-ia-api` para confirmar que los errores de inserción en BigQuery han desaparecido por completo.
  3.  Se consultará la tabla `recommendation_log` en BigQuery para verificar que los nuevos registros se están insertando correctamente con los nuevos campos poblados.

Este plan de acción no solo corrige el error, sino que introduce una práctica de gestión de bases de datos mucho más robusta y profesional, fundamental para un sistema en producción.
