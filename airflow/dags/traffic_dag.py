from datetime import datetime, timedelta

from airflow import DAG
from airflow.models import Variable
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}
with DAG(
    'traffic_report',
    default_args=default_args,
    description='Schedule Data Ingestion',
    schedule_interval="@daily",
    start_date=days_ago(6),
    catchup=True
) as dag:

    # Task to install required packages
    t0_install_packages = BashOperator(
        task_id='install_required_packages',
        bash_command='pip install sodapy'  
    )

    t1 = BashOperator(
        task_id='import_data_to_csv',
        bash_command='python /opt/airflow/dags/data_ingestion.py --date {{ ds }}'
    )
    
    t2 = BashOperator(
        task_id='export_data_to_db',
        bash_command='python /opt/airflow/dags/data_to_db.py '
                     '--date {{ ds }} --connection %s' % Variable.get("data_dev_connection")
    )

    # Set task dependencies
    t0_install_packages >> t1 >> t2
