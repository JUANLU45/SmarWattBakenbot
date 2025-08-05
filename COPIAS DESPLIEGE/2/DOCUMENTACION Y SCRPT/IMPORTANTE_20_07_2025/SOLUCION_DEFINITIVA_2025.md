ser_profiles_enriched:
13 a bq tables describe user_profiles_enriched --dataset=smartwatt_data --format="table(schema.fields[].name, schema.fields[].type, schema.fields[].mode)" --project=smatwatt
NAME
['user_id', 'last_update_timestamp', 'avg_kwh_last_year', 'peak_percent_avg', 'contracted_power_kw', 'num_inhabitants', 'home_type', 'heating_type', 'has_ac', 'has_pool', 'is_teleworker', 'post_code_prefix', 'has_solar_panels', 'consumption_kwh', 'monthly_consumption_kwh', 'timestamp'] ['STRING', 'TIMESTAMP', 'NUMERIC', 'NUMERIC', 'NUMERIC', 'INTEGER', 'STRING', 'STRING', 'BOOLEAN', 'BOOLEAN', 'BOOLEAN', 'STRING', 'BOOLEAN', 'FLOAT', 'FLOAT', 'TIMESTAMP'] [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
. Esta es la colección. Bequery la que te he puesto arriba. Ahora hay que comprobar en los archivos de los mini servicios. Que los archivos que necesiten de esa colección coincidan todos los campos coincidan los nombres coincida. La colección. Y recuerda que aquí no se piensa ni se cree ni se imagina 1. Aquí se verifica todo, métetelo en tu \*\*\*\* cabeza y no se hace nada básico, se hace todo robusto y no se duplica nada antes. Antes de duplicar algo hay que verificar si existen todos los archivos de los dos miniservicios. Son órdenes estrictas. Sí en la verificación ves que algún otro archivo necesita de su uso hay que arreglarlo también si es necesario, sino no esto tiene que ser robusto. Y los endopoint también hay que verificarlos que que los que la llamen y los que suba los datos. Es decir, firedsStore se tiene que crear la misma colección exactamente igual. Que la que hay en byquery. Lo único que tiene que coger decir Store el nombre de usuario cuando se llame algún endopoint o algo no sé cómo está implementado hay que verificar cómo está implementado que creo que está perfecto eso. El nombre de usuario la tiene que coger lo tiene que coger y su email si lo necesita. De La colección sí firestore     users

displayName
"Tomates Juanlu"
(cadena)

email
"<tomatesjuanlu@gmail.com>"
(cadena)

messageUsage
(mapa) Así es como viene la colección de firestory en firebase. Pero una vez que coja el nombre de usuario. Pues lo tiene que implementar en todo. En todos los sitios. Con el lumbre normal que tienen todas las colecciones de para el usuario. Segundo lugar, no hagas nada, aquí primero se verifica, como estamos haciendo, verificar que todos los archivos necesarios utilicen los mismos campos, utilicen todo y cuando se verifique que no se utiliza. O algo que haya que arreglar, se verifica siempre primero, siempre se verifica primero aquí no hay que hacer nada pensando ni creyendo ni imaginando. Aquí se verifica todo primero que no esté implementado y entonces, si no está ahí es necesario, se arregla y se hace. Recuerda que la colección se tiene que crear igual en fines base firestore la misma que hay en. Query para sus datos para los datos de usuario. Necesito que leas todo este mensaje entero mucho al principio del tobote puesto todos los pues todos los campos de la colección. Y ahora me estás dando comando para volver a sacar los coma los campos del mensaje entero lo que tienes que hacer.
