from airflow.utils.task_group import TaskGroup
from airflow.operators.empty import EmptyOperator


class GitCloneTG:
    def __init__(self):
        pass

    def __call__(self):
        with TaskGroup(group_id='group1') as tg1:
            t1 = EmptyOperator(task_id='task1')
            t2 = EmptyOperator(task_id='task2')

            t1 >> t2
        return tg1