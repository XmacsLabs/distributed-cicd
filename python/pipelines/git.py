from airflow.utils.task_group import TaskGroup
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python import BranchPythonOperator
from pathlib import Path


class GitSyncPipeline:
    def __init__(self):
        self.proj_dir = Path.home() / "XmacsLabs" / "mogan"

    def clone_or_pull(self) -> callable:
        def _inner(**kwargs):
            if Path(self.proj_dir).exists():
                return "git_sync.git_pull"
            else:
                return "git_sync.git_clone"
        return _inner

    def __call__(self):
        with TaskGroup(group_id='git_sync') as tg1:
            cond = BranchPythonOperator(task_id=f"clone_or_pull",
                                        python_callable=self.clone_or_pull()
                                        )

            t1 = BashOperator(
                task_id='mkdir',
                bash_command='mkdir -p ~/XmacsLabs/',
            )
            t2 = BashOperator(
                task_id='git_clone',
                bash_command='git clone https://gitee.com/XmacsLabs/mogan.git ~/XmacsLabs/mogan',
            )
            t3 = BashOperator(
                task_id='git_pull',
                cwd=str(self.proj_dir),
                bash_command='git pull',
            )
            t1 >> cond >> [t2, t3]

        return tg1