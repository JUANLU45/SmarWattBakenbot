# Instrucciones Críticas para la Reparación del Despliegue Automático (CI/CD)

Ha habido un error en la configuración de los secretos de GitHub que ha provocado el fallo de los despliegues automáticos. Sigue estas instrucciones para corregirlo de forma definitiva.

El error se debe a la inclusión de los caracteres `<` y `>` en las URLs de los servicios.

## Acción Requerida: Corregir los Secretos en GitHub

Ve a tu repositorio de GitHub → **Settings** → **Secrets and variables** → **Actions**.

Busca los siguientes dos secretos y actualiza su valor para que **NO** contengan los caracteres `<` y `>`:

1.  **`EXPERT_BOT_API_URL`**
    -   **Valor INCORRECTO:** `<https://expert-bot-api-1010012211318.europe-west1.run.app>`
    -   **Valor CORRECTO:** `https://expert-bot-api-1010012211318.europe-west1.run.app`

2.  **`ENERGY_IA_API_URL`**
    -   **Valor INCORRECTO:** `<https://energy-ia-api-1010012211318.europe-west1.run.app>`
    -   **Valor CORRECTO:** `https://energy-ia-api-1010012211318.europe-west1.run.app`

**El resto de los secretos que configuraste son correctos.** Solo es necesario modificar estos dos.

## Siguientes Pasos

Una vez que hayas guardado los cambios en estos dos secretos, puedes volver a la pestaña "Actions" de tu repositorio, seleccionar el workflow que falló y hacer clic en **"Re-run all jobs"**.

Con los secretos corregidos, el despliegue se completará con éxito.
