from pathlib import Path
from airflow.operators.bash_operator import BashOperator
from airflow.utils.task_group import TaskGroup

class XmakePipeline:
    def __init__(self):
        self.proj_dir = Path.home() / "XmacsLabs" / "mogan"

    def __call__(self):
        with TaskGroup(group_id='test') as tg1:
            t1 = BashOperator(
                task_id='config',
                cwd=str(self.proj_dir),
                bash_command='xmake config --yes',
            )
            t2 = BashOperator(
                task_id='build',
                cwd=str(self.proj_dir),
                bash_command='xmake build --yes --verbose --diagnosis --all',
            )
            t3 = BashOperator(
                task_id='test',
                cwd=str(self.proj_dir),
                bash_command='xmake run --yes --verbose --diagnosis --group=tests',
            )
            t1 >> t2 >> t3
        return tg1
