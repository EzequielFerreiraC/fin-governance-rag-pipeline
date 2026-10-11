from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
import time

# Default arguments for the DAG
# These arguments will be applied to all tasks in the DAG unless overridden individually.
default_args = {
    "owner": "data_engineering_team",
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}


def _mock_download_bacen_regulation():
    """Mock function to simulate downloading a BACEN regulation."""
    print("Downloading BACEN regulation...")
    time.sleep(2)
    fictional_file = "resolucao_cmn_4893_cybersecurity.pdf"
    print("Downloaded BACEN regulation:", fictional_file)

    return fictional_file


with DAG(
    dag_id="dag_bacen_ingestion_bronze",
    default_args=default_args,
    description="Capture daily BACEN regulations",
    schedule_interval="@daily",
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=["gov", "ingestion", "bronze"],
) as dag:
    start_process = EmptyOperator(task_id="start")

    download_data = PythonOperator(
        task_id="extract_bacen_api",
        python_callable=_mock_download_bacen_regulation,
    )

    move_to_datalake = BashOperator(
        task_id="load_to_bronze",
        bash_command="echo \"Moving file {{ ti.xcom_pull(task_ids='extract_bacen_api') }} to Bronze storage\"",
    )

    start_process >> download_data >> move_to_datalake
