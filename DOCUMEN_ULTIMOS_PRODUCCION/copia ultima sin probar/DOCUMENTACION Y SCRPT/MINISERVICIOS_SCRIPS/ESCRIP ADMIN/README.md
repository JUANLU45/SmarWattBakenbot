# 🎯 SCRIPTS DE TESTING - PANEL DE ADMINISTRACIÓN

Suite completa de scripts para probar todos los endpoints del panel de administración de SmarWatt.

## 📁 Archivos Incluidos

### 🚀 Script Principal
- **`run_all_admin_tests.py`** - Ejecutor principal que corre todos los tests

### 🧪 Scripts de Testing
- **`test_admin_panel_endpoints.py`** - Test completo de endpoints administrativos
- **`test_market_data.py`** - Test específico de consulta de mercado
- **`generate_test_data.py`** - Generador de datos de prueba realistas

### 🔧 Archivos de Soporte
- **`auth_helper.py`** - Helper de autenticación Firebase
- **`firebase-adminsdk-fbsvc-key.json`** - Credenciales Firebase

## 🎯 ENDPOINTS PROBADOS

### 🔐 Endpoints Administrativos (Requieren permisos admin)
1. **POST** `/admin/tariffs/add` - Subir tarifa individual
2. **POST** `/admin/tariffs/batch-add` - Subir tarifas en lote

### 📊 Endpoints Públicos
3. **GET** `/tariffs/market-data` - Consultar tarifas del mercado

## 🚀 EJECUCIÓN RÁPIDA

```bash
# Ejecutar todos los tests
python run_all_admin_tests.py
```

## 📋 EJECUCIÓN INDIVIDUAL

```bash
# Solo generar datos de prueba
python generate_test_data.py

# Solo test de mercado (público)
python test_market_data.py

# Solo endpoints admin (requiere permisos)
python test_admin_panel_endpoints.py
```

## 🔐 CONFIGURACIÓN DE PERMISOS

Los tests que requieren permisos administrativos utilizan:
- **Token Admin**: Configurado en `auth_helper.py`
- **Validación**: Decorator `@admin_required` en la API
- **Seguridad**: Auditoría completa de acciones administrativas

## 📊 DATOS DE PRUEBA

### ✅ Características de los Datos
- **Realistas**: Basados en el mercado eléctrico español 2025
- **Identificables**: Todos incluyen `DELETEME` para fácil limpieza
- **Completos**: Incluyen todos los campos opcionales y obligatorios
- **Diversos**: Diferentes tipos de tarifa (PVPC, Fixed, Indexed)

### 📁 Archivos JSON Generados
- `sample_single_tariff.json` - Tarifa individual completa
- `sample_batch_tariffs.json` - Lote de 8 tarifas para batch
- `sample_minimal_tariff.json` - Solo campos obligatorios

## 🧹 LIMPIEZA AUTOMÁTICA

### ⚠️ Importante
Los scripts intentan limpiar automáticamente los datos de prueba, pero se recomienda:

1. **Verificación manual** después de los tests
2. **Buscar tarifas** con `DELETEME` en el nombre
3. **Eliminar manualmente** si persisten en el sistema

### 🔍 Identificadores de Limpieza
- Nombres de proveedor: `TEST_*_DELETEME`
- Nombres de tarifa: `* - DELETEME`
- Notas: Contienen `BORRAR DESPUÉS DEL TEST`

## 📊 INTERPRETACIÓN DE RESULTADOS

### ✅ Éxito (Status 200/201)
- Endpoint funcional
- Permisos correctos
- Datos procesados correctamente

### ❌ Error 400
- Datos inválidos
- Campos obligatorios faltantes
- Formato incorrecto

### ❌ Error 403
- Sin permisos administrativos
- Token inválido
- Usuario no autorizado

### ❌ Error 500
- Error interno del servidor
- Problemas de base de datos
- Fallos en procesamiento

## 🎯 URLs DE ENDPOINTS

### 🌐 Producción
- **Base URL**: `https://energy-ia-api-1010012211318.europe-west1.run.app`
- **Admin Individual**: `POST /admin/tariffs/add`
- **Admin Batch**: `POST /admin/tariffs/batch-add`
- **Mercado**: `GET /tariffs/market-data`

### 🏠 Desarrollo Local
- **Base URL**: `http://localhost:8081`
- **Endpoints**: Mismas rutas que producción

## 📋 CAMPOS DE TARIFA

### 🔴 Obligatorios
- `supplier_name` - Nombre de la compañía
- `tariff_name` - Nombre de la tarifa
- `tariff_type` - Tipo (PVPC, Fixed, Indexed)
- `fixed_term_price` - Precio término fijo (€/mes)
- `variable_term_price` - Precio término variable (€/kWh)

### 🟡 Opcionales (20+ campos)
- Precios por períodos (P1, P2, P3)
- Precios de gas
- Permanencia y penalizaciones
- Descuentos y promociones
- Energía verde
- Valoraciones y reseñas
- Información de contacto
- Códigos regulatorios

## 🔄 INTEGRACIÓN CON CI/CD

Los scripts están diseñados para integrarse en pipelines:

```bash
# Verificación pre-despliegue
python run_all_admin_tests.py
if [ $? -eq 0 ]; then
    echo "✅ Admin tests passed - Safe to deploy"
else
    echo "❌ Admin tests failed - Block deployment"
    exit 1
fi
```

## 🐛 TROUBLESHOOTING

### Problema: Error de autenticación
**Solución**: Verificar credenciales Firebase y permisos admin

### Problema: Error de conexión
**Solución**: Comprobar URL de API y conectividad de red

### Problema: Datos no se limpian
**Solución**: Ejecutar consulta manual y eliminar tarifas con `DELETEME`

### Problema: Tests fallan intermitentemente
**Solución**: Verificar límites de rate limiting y timeouts

## 📞 SOPORTE

Para problemas con los scripts:
1. Verificar logs de ejecución
2. Comprobar estado de la API
3. Validar permisos y credenciales
4. Revisar documentación en `ENDOPOIN_PANEL_ADMIN.MD`

---
**📅 Actualizado**: 21 de Julio 2025  
**🔧 Versión**: 1.0  
**🎯 Estado**: Completamente funcional y listo para producción
