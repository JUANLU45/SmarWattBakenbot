smartwatt_data.recommendation_log'); print('CAMPOS REALES recommendation_log:'); [print(f'  {field.name}') for field in table.schema]"
CAMPOS REALES recommendation_log:
  recommendation_id
  user_id
  timestamp_utc
  input_avg_kwh
  input_peak_percent
  input_contracted_power_kw
  input_num_inhabitants
  input_home_type
  recommended_provider
  recommended_tariff_name
  estimated_annual_saving
  estimated_annual_cost
  reference_tariff_name
  reference_annual_cost
  consumption_kwh
  timestamp
  record_date
  total_savings
  annual_cost
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\DOCUMENTACION Y SCRPT\MINISERVICIOS_SCRIPS\ESCRIP ADMIN>

e}, Ahorro: {row.estimated_annual_saving}, Costo: {row.estimated_annual_cost}') for row in results]"
DATOS MÁS RECIENTES EN LA TABLA:
ID: 90ffa42a-6..., Usuario: 56bE1dNrje..., Fecha: 2025-07-14 19:16:28.036832+00:00, Proveedor: Red Eléctrica de España (REE), Tarifa: PVPC - Tarifa Regulada, Ahorro: 0, Costo: 342.69
ID: 70c876c3-7..., Usuario: Yoy2orAwZP..., Fecha: 2025-06-17 21:42:50.761881+00:00, Proveedor: PVPC Comercializador, Tarifa: Tarifa Regulada PVPC, Ahorro: 0, Costo: 615.3
ID: c3611fec-3..., Usuario: Yoy2orAwZP..., Fecha: 2025-06-17 21:27:59.471673+00:00, Proveedor: PVPC Comercializador, Tarifa: Tarifa Regulada PVPC, Ahorro: 0, Costo: 615.3
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\DOCUMENTACION Y SCRPT\MINISERVICIOS_SCRIPS\ESCRIP ADMIN>

ud import bigquery; client = bigquery.Client(project='smatwatt'); table = client.get_table('smatwatt.smartwatt_data.ai_sentiment_analysis'); print('CAMPOS REALES ai_sentiment_analysis:'); [print(f'  {field.name} - {field.field_type} ({field.mode})') for field in table.schema]"          
CAMPOS REALES ai_sentiment_analysis:
  interaction_id - STRING (REQUIRED)            
  conversation_id - STRING (REQUIRED)
  user_id - STRING (REQUIRED)
  message_text - STRING (REQUIRED)
  sentiment_score - FLOAT (REQUIRED)
  sentiment_label - STRING (REQUIRED)
  confidence - FLOAT (REQUIRED)
  emotional_indicators - JSON (NULLABLE)
  analyzed_at - TIMESTAMP (REQUIRED)
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\DOCUMENTACION Y SCRPT\MINISERVICIOS_SCRIPS\ESCRIP ADMIN>

CAMPOS REALES conversations_log:'); [print(f'  {field.name} - {field.field_type} ({field.mode})') for field in table.schema]"        
CAMPOS REALES conversations_log:
  conversation_id - STRING (REQUIRED)
  message_id - STRING (REQUIRED)
  user_id - STRING (REQUIRED)
  timestamp_utc - TIMESTAMP (REQUIRED)
  sender - STRING (REQUIRED)
  message_text - STRING (REQUIRED)
  intent_detected - STRING (NULLABLE)
  bot_action - STRING (NULLABLE)
  sentiment - STRING (NULLABLE)
  deleted - BOOLEAN (NULLABLE)
  deleted_at - TIMESTAMP (NULLABLE)
  response_text - STRING (NULLABLE)
  context_completeness - INTEGER (NULLABLE)     
  response_time_ms - INTEGER (NULLABLE)
  session_info - JSON (NULLABLE)
  metadata - JSON (NULLABLE)
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\DOCUMENTACION Y SCRPT\MINISERVICIOS_SCRIPS\ESCRIP ADMIN>cd "c:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\energy_ia_api_COPY" && gcloud alpha bq tables describe market_electricity_tariffs --dataset=smartwatt_data --project=smatwatt
creationTime: '1749516649526'
etag: 2a+R1vguSgQmg17/7aTi1Q==
id: smatwatt:smartwatt_data.market_electricity_tariffs
kind: bigquery#table
lastModifiedTime: '1752224803491'
location: EU
numActiveLogicalBytes: '161'     
numActivePhysicalBytes: '2756'   
numBytes: '161'
numCurrentPhysicalBytes: '2756'  
numLongTermBytes: '0'
numLongTermLogicalBytes: '0'     
numLongTermPhysicalBytes: '0'    
numRows: '1'
numTimeTravelPhysicalBytes: '0'  
numTotalLogicalBytes: '161'      
numTotalPhysicalBytes: '2756'    
schema:
  fields:
  - mode: NULLABLE
    name: update_timestamp       
    type: TIMESTAMP
  - mode: NULLABLE
    name: is_pvpc
    type: BOOLEAN
  - mode: NULLABLE
    name: is_active
    type: BOOLEAN
  - mode: NULLABLE
    name: fixed_monthly_fee      
    type: FLOAT
  - mode: NULLABLE
    name: tariff_name
    type: STRING
  - mode: NULLABLE
    name: kwh_price_flat
    type: FLOAT
  - mode: NULLABLE
    name: kwh_price_peak
    type: FLOAT
  - mode: NULLABLE
    name: power_price_per_kw_per_month
    type: FLOAT
  - mode: NULLABLE
    name: tariff_id
    type: STRING
  - mode: NULLABLE
    name: tariff_type
    type: STRING
  - mode: NULLABLE
    name: kwh_price_valley       
    type: FLOAT
  - mode: NULLABLE
    name: provider_name
    type: STRING
selfLink: https://bigquery.googleapis.com/bigquery/v2/projects/smatwatt/datasets/smartwatt_data/tables/market_electricity_tariffs   
tableReference:
  datasetId: smartwatt_data      
  projectId: smatwatt
  tableId: market_electricity_tariffs
type: TABLE
PS C:\Smarwatt_2\SmarWatt_2\backend\sevicio chatbot\servicios\energy_ia_api_COPY>