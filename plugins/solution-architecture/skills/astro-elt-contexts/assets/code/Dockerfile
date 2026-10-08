FROM quay.io/astronomer/astro-runtime:13.2.0

USER astro
RUN python -m venv "${AIRFLOW_HOME}/dbt_venv" \
    && "${AIRFLOW_HOME}/dbt_venv/bin/pip" install --no-cache-dir dbt-postgres dbt-sqlserver
