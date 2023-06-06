from datetime import datetime
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from pipelines.git import GitSyncPipeline
from pipelines.xmake import XmakePipeline

default_args = {
    'owner': 'da',
    'start_date': datetime(2023, 6, 1, 0, 0, 0),
}

with DAG(dag_id='mogan_build_and_test', schedule="@hourly", max_active_runs=1, default_args=default_args) as dag:
    git_clone = GitSyncPipeline()
    build_and_test = XmakePipeline()
    task = BashOperator(
        task_id='show_xmake_version',
        bash_command='xmake --version | head -n 1',
    )
    
    git_clone() >> task >> build_and_test()
