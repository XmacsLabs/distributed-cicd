from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from pipelines.git_clone import GitCloneTG

dag_args = {
    'owner': 'da',
    'depends_on_past': False,
    'start_date': datetime(2023, 6, 1, 0, 0, 0),
}

with DAG(dag_id='mogan_build_and_test', schedule="@hourly", default_args=dag_args) as dag:
    task = BashOperator(
        task_id='show_xmake_version',
        bash_command='xmake --version | head -n 1',
    )
    git_clone = GitCloneTG()
    
    task >> git_clone()
