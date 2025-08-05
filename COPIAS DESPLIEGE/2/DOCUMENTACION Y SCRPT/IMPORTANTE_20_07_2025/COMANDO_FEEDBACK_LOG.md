# 🔍 COMANDO PARA OBTENER CAMPOS DE FEEDBACK_LOG

## 📊 OBTENER CAMPOS REALES DE LA TABLA

```bash
gcloud alpha bq tables describe feedback_log --dataset=smartwatt_data --format="value(schema.fields[].name)" --project=smatwatt
```

## 📋 OBTENER CAMPOS CON TIPOS Y MODOS

```bash
gcloud alpha bq tables describe feedback_log --dataset=smartwatt_data --format="table(schema.fields[].name, schema.fields[].type, schema.fields[].mode)" --project=smatwatt
```

## 🐍 COMANDO PYTHON PARA ANÁLISIS COMPLETO

```bash
cd "c:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios" && python -c "
from google.cloud import bigquery
client = bigquery.Client(project='smatwatt')
table = client.get_table('smatwatt.smartwatt_data.feedback_log')
print('CAMPOS REALES feedback_log:')
print([field.name for field in table.schema])
print('TIPOS:', [field.field_type for field in table.schema])
print('MODOS:', [field.mode for field in table.schema])
"
```

**🎯 EJECUTA EL COMANDO Y PEGA AQUÍ EL RESULTADO PARA CONTINUAR LA VERIFICACIÓN COMPLETA**
