
from datetime import datetime, timedelta

from airflow import DAG
from airflow.models import Variable
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}
with DAG(
    'data_migration',
    default_args=default_args,
    description='Data Migration',
    schedule_interval="@once",
    start_date=datetime.strptime("2023-08-30", '%Y-%m-%d'),
    catchup=False
) as dag:
    
    # Task to install required packages
    t0_packages = BashOperator(
        task_id='install_required_packages',
        bash_command='pip install sodapy'  
    )

    t1 = BashOperator(
        task_id='data_migration',
        bash_command='python /opt/airflow/dags/data_migration.py '
        '--connection %s' % Variable.get("data_dev_connection")
    )

    # Set task dependencies
    t0_packages >> t1