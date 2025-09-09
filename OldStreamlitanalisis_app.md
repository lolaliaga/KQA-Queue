# 📌 Análisis del script `app.py`

## 1. Librerías usadas

-   **Streamlit (`st`)** → interfaz web interactiva.
-   **Pandas (`pd`)** → manejo de DataFrames y datos tabulares.
-   **Requests** → para hacer requests HTTP a Google Sheets.
-   **Google Auth (`Credentials`)** → autenticación con Google Service
    Account (para hojas privadas).
-   **OS, IO, Time, Quote** → utilidades de sistema, buffer de strings,
    backoff en requests, y encoding de nombres de hojas.

## 2. Fuentes de datos

El código usa **Google Sheets** como base de datos.\
- **Public Lessons** → se accede vía export en CSV con `gid`. -
**Ratings y QA** → se accede vía API de Sheets con autenticación. -
**Replacements** → otra hoja separada (cancelaciones/reemplazos de
clases).

Constantes que guardan los IDs: - `LESSONS_SS`, `RATING_LATAM_SS`,
`RATING_BRAZIL_SS`, `QA_LATAM_SS`, `QA_BRAZIL_SS`, `REPL_SS`. - Cada uno
tiene asociado un `gid` o un `sheet_name`.

## 3. Funciones clave

-   `get_creds()` → obtiene credenciales desde `st.secrets` o
    `os.environ`.
-   `api_retry()` → retry con **backoff exponencial** para llamadas
    HTTP.
-   `fetch_csv(ss_id, gid)` → descarga CSV público y lo convierte en
    DataFrame.
-   `fetch_values(ss_id, sheet_name)` → obtiene un `range` de Google
    Sheets API.
-   `load_public_lessons()` → carga clases públicas y las normaliza
    (Tutor, Fecha, Curso, Link...).
-   `load_rating()` → trae ratings QA por tutor (últimos 90 días,
    promedio, etc.).
-   `load_qa()` → carga las evaluaciones QA de lecciones.
-   `load_replacements()` → trae reemplazos/postergaciones.
-   `build_df()` → función central que:
    1.  Junta **públicos + ratings + QA + replacements**.
    2.  Une todo en un solo DataFrame homogéneo.
    3.  Añade columna **Source** = "Public" o "QA".
    4.  Hace un merge para rellenar datos faltantes.
    5.  Devuelve el DataFrame final.

## 4. UI en Streamlit

-   **Filtros en sidebar**:
    -   Checkboxes para mostrar u ocultar *public lessons* y *QA
        lessons*.
    -   Rango de fechas para cada tipo de lección.
    -   Multiselect para cualquier columna (dinámico).
    -   Opción para ocultar filas con `#N/A`.
-   **Tabla principal**:
    -   Se filtra el `DataFrame` con las condiciones seleccionadas.
    -   Se muestra con `st.dataframe`.
    -   Descarga en CSV disponible con `st.download_button`.

## 5. Lógica de filtrado

-   Se construyen dos máscaras:

    -   `mask_public` → según fecha de la lección.
    -   `mask_qa` → según fecha de evaluación QA.

-   Luego:

    ``` python
    mask = mask_public | mask_qa
    ```

    (las une con OR lógico).

-   A esa máscara se le aplican los filtros extra (Tutor, Región, etc.).

-   Finalmente se muestra `dff = df[mask]`.

## 6. Salida

-   Dashboard con **todas las clases** (LATAM y Brasil).
-   Incluye:
    -   Nombre de tutor, grupo, curso, módulo, link.
    -   Rating (con varios KPIs).
    -   QA score y marker.
    -   Info de replacements.
-   Datos filtrables y descargables.

------------------------------------------------------------------------

✅ En resumen:\
Este código construye un **pipeline ETL sencillo en Streamlit** → baja
datos desde Google Sheets, los combina, los limpia y genera un
**dashboard interactivo de QA y lecciones**.
