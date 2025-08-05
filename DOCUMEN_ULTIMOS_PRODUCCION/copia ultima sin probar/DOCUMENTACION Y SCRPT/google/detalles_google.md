IPS\BOT APY> gcloud config list project
[core]
project = smatwatt

Your active configuration is: [default]
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\Y DOCUMENTACION\MINISERVICIOS_SCRIPS\BOT APY> gcloud projects describe smatwatt

createTime: '2025-06-04T00:08:18.079295Z'
labels:
firebase: enabled
firebase-core: disabled
generative-language: enabled
lifecycleState: ACTIVE
name: SmatWatt
projectId: smatwatt
projectNumber: '1010012211318'
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\Y DOCUMENTACION\MINISERVICIOS_SCRIPS\BOT APY>
tbot\servicios\Y DOCUMENTACION\MINISERVICIOS_SCRIPS\BOT APY> gcloud services list --enabled --filter="bigquery" --format="table(name,title)"
NAME
TITLE
projects/1010012211318/services/bigquery.googleapis.com
projects/1010012211318/services/bigqueryconnection.googleapis.com
projects/1010012211318/services/bigquerydatapolicy.googleapis.com
projects/1010012211318/services/bigquerydatatransfer.googleapis.com
projects/1010012211318/services/bigquerymigration.googleapis.com
projects/1010012211318/services/bigqueryreservation.googleapis.com
projects/1010012211318/services/bigquerystorage.googleapis.com
projects/1010012211318/services/cloudtrace.googleapis.com
projects/1010012211318/services/dataform.googleapis.com
projects/1010012211318/services/dataplex.googleapis.com
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\Y DOCUMENTACION\MINISERVICIOS_SCRIPS\BOT APY>

RIPS\BOT APY> gcloud alpha bq datasets list
ID LOCATION
smatwatt:smartwatt_data EU
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\Y DOCUMENTACION\MINISERVICIOS_SCRIPS\BOT APY>
aset=smartwatt_data
DATASET_ID TABLE_ID CREATION_TIME EXPIRATION_TIME TYPE
smartwatt_data ai_ab_testing 2025-07-15T13:25:23 TABLE
smartwatt_data ai_business_metrics 2025-07-17T14:54:21 TABLE
smartwatt_data ai_predictions 2025-07-17T14:54:20 TABLE
smartwatt_data ai_prompt_optimization 2025-07-15T13:25:23 TABLE
smartwatt_data ai_sentiment_analysis 2025-07-14T13:19:35 TABLE
smartwatt_data ai_user_patterns 2025-07-14T13:19:35 TABLE
smartwatt_data async_tasks 2025-07-17T14:54:21 TABLE
smartwatt_data consumption_log 2025-06-16T10:46:56 TABLE
smartwatt_data conversations_log 2025-06-16T10:46:09 TABLE
smartwatt_data electricity_consumption_log 2025-06-07T17:23:47 TABLE
smartwatt_data feedback_log 2025-06-16T10:46:29 TABLE
smartwatt_data market_electricity_tariffs 2025-06-10T00:50:49 TABLE
smartwatt_data ml_training_20250711_062334 2025-07-11T04:23:37 TABLE
smartwatt_data model_feedback_log 2025-06-07T17:23:48 TABLE
smartwatt_data recommendation_log 2025-06-10T00:22:50 TABLE
smartwatt_data uploaded_documents_log 2025-06-16T10:46:45 TABLE
smartwatt_data user_profiles_enriched 2025-06-10T00:23:31 TABLE
smartwatt_data worker_metrics 2025-07-17T14:54:22 TABLE
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\Y DOCUMENTACION\MINISERVICIOS_SCRIPS\BOT APY>
IPS\BOT APY> gcloud iam service-accounts list
DISPLAY NAME EMAIL
DISABLED
App Engine default service account <smatwatt@appspot.gserviceaccount.com>
False
Default compute service account <1010012211318-compute@developer.gserviceaccount.com> False
SmarWatt <smarwatt@smatwatt.iam.gserviceaccount.com>
False
SmarWatt GitHub Actions Deployer <smwatt-gha-deployer@smatwatt.iam.gserviceaccount.com> False
GitHub Actions (JUANLU45/SmatWatt) <github-action-998093375@smatwatt.iam.gserviceaccount.com> False
Cuenta de Servicio para Expert Bot API <expert-bot-api-sa@smatwatt.iam.gserviceaccount.com> False
firebase-adminsdk <firebase-adminsdk-fbsvc@smatwatt.iam.gserviceaccount.com> False
SmarWatt Blog API Service Account <smarwatt-blog-api@smatwatt.iam.gserviceaccount.com> False
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\Y DOCUMENTACION\MINISERVICIOS_SCRIPS\BOT APY>

S C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\Y DOCUMENTACION\MINISERVICIOS_SCRIPS\BOT APY> gcloud iam service-accounts describe <firebase-adminsdk-fbsvc@smatwatt.iam.gserviceaccount.com>
description: Firebase Admin SDK Service Agent
displayName: firebase-adminsdk
email: <firebase-adminsdk-fbsvc@smatwatt.iam.gserviceaccount.com>
etag: MDEwMjE5MjA=
name: projects/smatwatt/serviceAccounts/firebase-adminsdk-fbsvc@smatwatt.iam.gserviceaccount.com
oauth2ClientId: '116550293443112934262'
projectId: smatwatt
uniqueId: '116550293443112934262'
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\Y DOCUMENTACION\MINISERVICIOS_SCRIPS\BOT APY>
table(bindings.role)" --filter="bindings.members:firebase-adminsdk-fbsvc@smatwatt.iam.gserviceaccount.com"
ROLE
roles/bigquery.dataEditor
roles/bigquery.dataViewer
roles/bigquery.user
roles/cloudfunctions.admin
roles/firebase.sdkAdminServiceAgent
roles/iam.serviceAccountTokenCreator
roles/secretmanager.secretAccessor
roles/storage.admin
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\Y DOCUMENTACION\MINISERVICIOS_SCRIPS\BOT APY>
IPS\BOT APY> gcloud alpha bq tables describe feedback_log --dataset=smartwatt_data
clustering:
fields:

- user_id
- recommendation_type
  creationTime: '1750070789936'
  etag: FFJUyhOWkGN9Qptv5oRIkg==
  id: smatwatt:smartwatt_data.feedback_log
  kind: bigquery#table
  lastModifiedTime: '1750070789936'
  location: EU
  numActiveLogicalBytes: '0'
  numActivePhysicalBytes: '0'
  numBytes: '0'
  numCurrentPhysicalBytes: '0'
  numLongTermBytes: '0'
  numLongTermLogicalBytes: '0'
  numLongTermPhysicalBytes: '0'
  numRows: '0'
  numTimeTravelPhysicalBytes: '0'
  numTotalLogicalBytes: '0'
  numTotalPhysicalBytes: '0'
  partitionDefinition:
  partitionedColumn:
- field: submitted_at
  schema:
  fields:
- mode: REQUIRED
  name: feedback_id
  type: STRING
- mode: REQUIRED
  name: user_id
  type: STRING
- mode: REQUIRED
  name: recommendation_type
  type: STRING
- mode: REQUIRED
  name: feedback_useful
  type: BOOLEAN
- name: comments
  type: STRING
- mode: REQUIRED
  name: submitted*at
  type: TIMESTAMP
  selfLink: <https://bigquery.googleapis.com/bigquery/v2/projects/smatwatt/datasets/smartwatt_data/tables/feedback_log>
  tableReference:
  datasetId: smartwatt_data
  projectId: smatwatt
  tableId: feedback_log
  timePartitioning:
  field: submitted_at
  type: DAY
  type: TABLE
  PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\Y DOCUMENTACION\MINISERVICIOS_SCRIPS\BOT APY>
  S C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\Y DOCUMENTACION\MINISERVICIOS_SCRIPS\BOT APY> gcloud run services describe expert-bot-api --region=europe-west1 --format="export" | findstr /i "env\|GCP*\|GOOGLE*\|BQ*"
  PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\Y DOCUMENTACION\MINISERVICIOS_SCRIPS\BOT APY>

AME CREATED REPLICATION_POLICY LOCATIONS
firebase-adminsdk-key 2025-07-20T17:58:54 automatic -
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\Y DOCUMENTACION\MINISERVICIOS_SCRIPS\BOT APY>

IPS\BOT APY> gcloud secrets list --filter="name~firebase"
NAME CREATED REPLICATION_POLICY LOCATIONS
firebase-adminsdk-key 2025-07-20T17:58:54 automatic -
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\Y DOCUMENTACION\MINISERVICIOS_SCRIPS\BOT APY> gcloud secrets versions list firebase-adminsdk-key
NAME STATE CREATED DESTROYED
1 enabled 2025-07-20T17:58:57 -
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\Y DOCUMENTACION\MINISERVICIOS_SCRIPS\BOT APY>
IPS\BOT APY> gcloud secrets versions list firebase-adminsdk-key
NAME STATE CREATED DESTROYED
1 enabled 2025-07-20T17:58:57 -
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\Y DOCUMENTACION\MINISERVICIOS_SCRIPS\BOT APY> gcloud alpha bq tables describe feedback_log --dataset=smartwatt_data --format="value(schema.fields[].name)"
feedback_id;user_id;recommendation_type;feedback_useful;comments;submitted_at
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\Y DOCUMENTACION

-----------ESQUEMAS TABLAS-----------------

S C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\DOCUMENTACION Y SCRPT\MINISERVICIOS_SCRIPS\ENERGYA API> gcloud alpha bq tables describe consumption_log --dataset=smartwatt_data --format="value(schema.fields[].name)"
consumption_id;user_id;timestamp_utc;kwh_consumed;estimated_cost;potencia_contratada_kw;tariff_name_at_time;source
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\DOCUMENTACION Y SCRPT\MINISERVICIOS_SCRIPS\ENERGYA API> gcloud alpha bq tables describe recommendation_log --dataset=smartwatt_data --format="value(schema.fields[].name)"
recommendation_id;user_id;timestamp_utc;input_avg_kwh;input_peak_percent;input_contracted_power_kw;input_num_inhabitants;input_home_type;recommended_provider;recommended_tariff_name;estimated_annual_saving;estimated_annual_cost;reference_tariff_name;reference_annual_cost
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\DOCUMENTACION Y SCRPT\MINISERVICIOS_SCRIPS\ENERGYA API> gcloud alpha bq tables describe uploaded_documents_log --dataset=smartwatt_data --format="value(schema.fields[].name)"
document_id;user_id;upload_timestamp;original_filename;mime_type;gcs_path;extracted_data_kwh_ref;extracted_data_cost_ref;extracted_data_power_ref;extracted_data_tariff_name_ref
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\DOCUMENTACION Y SCRPT\MINISERVICIOS_SCRIPS\ENERGYA API>
hema.fields[].name)"
user_id;last_update_timestamp;avg_kwh_last_year;peak_percent_avg;contracted_power_kw;num_inhabitants;home_type;heating_type;has_ac;has_pool;is_teleworker;post_code_prefix;has_solar_panels
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\DOCUMENTACION Y SCRPT\MINISERVICIOS_SCRIPS\ENERGYA API>
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\DOCUMENTACION Y SCRPT\MINISERVICIOS_SCRIPS\ENERGYA API> gcloud alpha bq tables describe market_electricity_tariffs --dataset=smartwatt_data --format="value(schema.fields[].name)"
update_timestamp;is_pvpc;is_active;fixed_monthly_fee;tariff_name;kwh_price_flat;kwh_price_peak;power_price_per_kw_per_month;tariff_id;tariff_type;kwh_price_valley;provider_name
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\DOCUMENTACION Y SCRPT\MINISERVICIOS_SCRIPS\ENERGYA API>
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\DOCUMENTACION Y SCRPT\MINISERVICIOS_SCRIPS\ENERGYA API> gcloud alpha bq tables describe electricity_consumption_log --dataset=smartwatt_data --format="value(schema.fields[].name)"
consumption_id;user_id;timestamp_utc;kwh_consumed;estimated_cost;tariff_type_at_time;source
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\DOCUMENTACION Y SCRPT\MINISERVICIOS_SCRIPS\ENERGYA API>
mated_cost;tariff_type_at_time;source
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\DOCUMENTACION Y SCRPT\MINISERVICIOS_SCRIPS\ENERGYA API> gcloud alpha bq tables describe model_feedback_log --dataset=smartwatt_data --format="value(schema.fields[].name)"
feedback_id;user_id;recommendation_type;feedback_useful;comments;submitted_at
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\DOCUMENTACION Y SCRPT\MINISERVICIOS_SCRIPS\ENERGYA API>

conversations_log
Esta es una tabla particionada. Learn more
Esquema
Detalles
Vista previa
Explorador de tablas
vista previa
Estadísticas
Linaje
Perfil de datos
Calidad de los datos
Filtro
Nombre del campo
Tipo
Modo
Clave
Intercalación
Valor predeterminado
Etiquetas de políticas
Políticas de datos
Descripción
conversation_id
STRING REQUIRED - - -

-

-
-

message_id
STRING REQUIRED - - -

-

-
-

user_id
STRING REQUIRED - - -

-

-
-

timestamp_utc
TIMESTAMP REQUIRED - - -

-

-
-

sender
STRING REQUIRED - - -

-

-
-

message_text
STRING REQUIRED - - -

-

-
-

intent_detected
STRING NULLABLE - - -

-

-
-

bot_action
STRING NULLABLE - - -

-

-
-

sentiment
STRING NULLABLE - - -

-

-
-

deleted
BOOLEAN NULLABLE - - -

-

-

Indica si la conversación está eliminada (soft delete)
deleted_at
TIMESTAMP NULLABLE - - -

-

-

Timestamp de cuando se eliminó la conversación
c

onversations_log
Esta es una tabla particionada. Learn more
Esquema
Detalles
Vista previa
Explorador de tablas
vista previa
Estadísticas
Linaje
Perfil de datos
Calidad de los datos
Filtro
Nombre del campo
Tipo
Modo
Clave
Intercalación
Valor predeterminado
Etiquetas de políticas
Políticas de datos
Descripción
conversation_id
STRING REQUIRED - - -

-

-
-

message_id
STRING REQUIRED - - -

-

-
-

user_id
STRING REQUIRED - - -

-

-
-

timestamp_utc
TIMESTAMP REQUIRED - - -

-

-
-

sender
STRING REQUIRED - - -

-

-
-

message_text
STRING REQUIRED - - -

-

-
-

intent_detected
STRING NULLABLE - - -

-

-
-

bot_action
STRING NULLABLE - - -

-

-
-

sentiment
STRING NULLABLE - - -

-

-
-

deleted
BOOLEAN NULLABLE - - -

-

-

Indica si la conversación está eliminada (soft delete)
deleted_at
TIMESTAMP NULLABLE - - -

-
