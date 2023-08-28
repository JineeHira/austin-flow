import os

TRAFFIC_API = os.getenv("TRAFFIC_API", "https://data.austintexas.gov/resource/dx9v-zd7x.csv")
CSV_DIR = os.getenv("CSV_DIR", "/Users/jinee.hira/Dropbox/virtual_envs/austin-flow/airflow/dags/data")

PSQL_DB = os.getenv("PSQL_DB", "airflow")
PSQL_USER = os.getenv("PSQL_USER", "airflow")
PSQL_PASSWORD = os.getenv("PSQL_PASSWORD", "airflow")
PSQL_PORT = os.getenv("PSQL_PORT", "5432")
PSQL_HOST = os.getenv("PSQL_HOST", "localhost")

