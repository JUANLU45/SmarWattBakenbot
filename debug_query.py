#!/usr/bin/env python3
# Script para analizar la query SQL y encontrar el error exacto

query = """        SELECT 
            conversation_id,
            message_text,
            response_text,
            context_completeness,
            response_time_ms,
            timestamp_utc
        FROM `project.dataset.table`
        WHERE user_id = @user_id 
          AND (deleted IS NULL OR deleted = false)
        ORDER BY timestamp_utc DESC
        LIMIT @limit"""

lines = query.split("\n")
for i, line in enumerate(lines):
    print(f'{i+1:2}: "{line}"')

# Analizar línea por línea para encontrar "deleted at [11:16]"
target_line = lines[9]  # Línea 10 (índice 9) tiene el WHERE deleted
print(f'\nLínea 10: "{target_line}"')
print(f"Longitud: {len(target_line)}")

# Buscar la posición exacta donde BigQuery encuentra el error
if len(target_line) > 15:
    print(f'Posición 16: "{target_line[15]}"')
    print(f'Substring desde pos 11: "{target_line[10:20]}"')

# El error "deleted at [11:16]" sugiere que BigQuery está interpretando
# "deleted" como si fuera seguido de "at" en algún lugar
print(f'\nBuscando "deleted" en la query:')
for i, line in enumerate(lines):
    if "deleted" in line:
        pos = line.find("deleted")
        print(f'Línea {i+1}, posición {pos}: "{line.strip()}"')
