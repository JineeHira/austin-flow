import os

app_token = os.getenv("SOCRATA_APP_TOKEN")
username = os.getenv("SOCRATA_USERNAME")
password = os.getenv("SOCRATA_PASSWORD")

CSV_DIR = os.getenv("CSV_DIR", "/opt/airflow/dags/data")

PSQL_DB = os.getenv("PSQL_DB", "airflow")
PSQL_USER = os.getenv("PSQL_USER", "airflow")
PSQL_PASSWORD = os.getenv("PSQL_PASSWORD", "airflow")
PSQL_PORT = os.getenv("PSQL_PORT", "5432")
PSQL_HOST = os.getenv("PSQL_HOST", "localhost")
