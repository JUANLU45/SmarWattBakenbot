# 🔐 CONFIGURACIÓN DE SECRETS - GITHUB ACTIONS

# INSTRUCCIONES EXACTAS PARA CERO FALLOS

## 📋 **SECRETS REQUERIDOS EN GITHUB**

Ir a: **GitHub Repository → Settings → Secrets and variables → Actions**

### **🔑 SECRETS OBLIGATORIOS:**

```bash
# 1. GOOGLE CLOUD SERVICE ACCOUNT (CRÍTICO)
GCP_SA_KEY
# Valor: Todo el JSON del service account firebase-adminsdk-fbsvc@smatwatt.iam.gserviceaccount.com
# Formato: JSON completo (desde { hasta })

# 2. APIS Y TOKENS
GEMINI_API_KEY=AIzaSyCONKtpEAWHM5xtq-C3YTX8xsmFnHo0goE
OPENWEATHER_API_KEY=8f91cb80de36de44e701ff196ea256e8
ESIOS_API_TOKEN=ac5c7863608aae858a07e6e31cc9497275ecbe4a5d57f6fa769abd9bee350c94

# 3. CLAVES DE SEGURIDAD
SECRET_KEY_IA=MTvrA_NDjZ11l6wCEFcxVr6A7R1iI8AAeyQG6oRUv2I
SECRET_KEY=MTvrA_NDjZ11l6wCEFcxVr6A7R1iI8AAeyQG6oRUv2I
INTERNAL_SERVICE_TOKEN=MTvrA_NDjZ11l6wCEFcxVr6A7R1iI8AAeyQG6oRUv2I

# 4. URLS DE MICROSERVICIOS
EXPERT_BOT_API_URL=https://expert-bot-api-1010012211318.europe-west1.run.app
ENERGY_IA_API_URL=https://energy-ia-api-1010012211318.europe-west1.run.app
```

---

## 🎯 **PASOS PARA CONFIGURAR (PASO A PASO)**

### **1. 🔐 Obtener Service Account Key:**

```bash
# En Google Cloud Console:
# IAM & Admin → Service Accounts
# Buscar: firebase-adminsdk-fbsvc@smatwatt.iam.gserviceaccount.com
# Actions → Manage Keys → Add Key → Create New Key → JSON
# Descargar el archivo JSON completo
```

### **2. 📝 Configurar en GitHub:**

1. **Ir a tu repositorio GitHub**
2. **Settings** → **Secrets and variables** → **Actions**
3. **New repository secret** para cada secret:

```
Nombre: GCP_SA_KEY
Valor: [TODO EL CONTENIDO DEL JSON descargado]

Nombre: GEMINI_API_KEY
Valor: AIzaSyCONKtpEAWHM5xtq-C3YTX8xsmFnHo0goE

Nombre: OPENWEATHER_API_KEY
Valor: 8f91cb80de36de44e701ff196ea256e8

... (continuar con todos los secrets)
```

### **3. ✅ Verificar configuración:**

Una vez configurados TODOS los secrets, el workflow se ejecutará automáticamente cuando hagas push a master.

---

## 🚀 **FUNCIONAMIENTO AUTOMÁTICO**

### **📊 Flujo completo:**

1. **Haces push** a branch `master`
2. **GitHub Actions detecta** cambios en `energy_ia_api_COPY/` o `expert_bot_api_COPY/`
3. **Despliega automáticamente** solo los servicios modificados
4. **Ejecuta health checks** para verificar que funcionan
5. **Te notifica** el resultado

### **⏱️ Tiempos esperados:**

- **Detección de cambios:** 10 segundos
- **Deploy por microservicio:** 3-5 minutos
- **Health checks:** 30 segundos
- **Total:** 4-6 minutos máximo

### **🔔 Resultado:**

```
✅ Energy IA API desplegado exitosamente
🔗 URL: https://energy-ia-api-1010012211318.europe-west1.run.app
⏰ Timestamp: 2025-08-06 15:30:45

✅ Expert Bot API desplegado exitosamente
🔗 URL: https://expert-bot-api-1010012211318.europe-west1.run.app
⏰ Timestamp: 2025-08-06 15:32:15
```

---

## 🛡️ **CARACTERÍSTICAS DE SEGURIDAD**

### **✅ Configuración verificada:**

- **Service Account correcto:** firebase-adminsdk-fbsvc@smatwatt.iam.gserviceaccount.com
- **Región correcta:** europe-west1
- **Proyecto correcto:** smatwatt
- **Recursos exactos:** 4Gi memory, 2 CPU, 5 max instances
- **Secrets montados:** expert-bot-api-sa-key, firebase-adminsdk-key
- **Variables de entorno:** Todas las 25+ variables incluidas

### **🔒 Seguridad empresarial:**

- **Secrets nunca expuestos** en logs
- **Autenticación por Service Account** verificada
- **Health checks automáticos** antes de confirmar deploy
- **Rollback disponible** en caso de fallos

---

## ⚠️ **TROUBLESHOOTING**

### **❌ Si falla el deploy:**

```bash
# 1. Verificar que todos los secrets están configurados
# 2. Verificar que el Service Account tiene permisos
# 3. Revisar logs en: GitHub → Actions → [último workflow]
# 4. Verificar que las URLs de los microservicios son correctas
```

### **🔍 Debug común:**

```yaml
# Si necesitas debug, añadir este step temporal:
- name: 🐛 Debug variables
  run: |
    echo "Project: ${{ env.GCP_PROJECT_ID }}"
    echo "Region: ${{ env.GCP_REGION }}"
    echo "Branch: ${{ github.ref }}"
    # NUNCA imprimir secrets por seguridad
```

---

**🎯 RESULTADO FINAL:**
**PUSH → 4 MINUTOS → DESPLEGADO AUTOMÁTICAMENTE**
**CERO INTERVENCIÓN MANUAL REQUERIDA**
