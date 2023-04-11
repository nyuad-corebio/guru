from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import  DagRun
from airflow.operators.bash import BashOperator
from airflow.providers.ssh.operators.ssh import SSHOperator
from airflow.providers.ssh.hooks.ssh import SSHHook
from pprint import pprint

#source_file_path = '{{ dag_run.conf.name }}'   


dag = DAG('default_sequence', description='Default Sequence DAG',
          schedule_interval=None,
          start_date=datetime(2023, 4, 1), catchup=False)
ssh_hook = SSHHook(ssh_conn_id='airflow_docker_ssh')
ssh_hook.no_host_key_check = True


def print_hello(ds=None, **kwargs):
    dag_run = kwargs['dag_run']
    # print(ds)
    return 'Hello world from first Airflow DAG! \'{{ dag_run.conf["jira_ticket"] if dag_run else "qqqq" }}\' {{ dag_run.conf["miso"] }}"  end'

	 

Initiate_task = PythonOperator(task_id='Initiate_task', python_callable=print_hello, dag=dag)

# rsync_archive_to_scratch_task = BashOperator(
#     task_id="rsync_archive_to_scratch_task",
#     bash_command='echo "Here is the message:  to {{ dag_run.conf["projname"] }}"',
# )


rsync_work_to_scratch_command = """
        mkdir -p {{ dag_run.conf["scratch_dir"] }}
        rsync -av "{{ dag_run.conf["work_dir"] }}/" "{{ dag_run.conf["scratch_dir"] }}/"
"""

rsync_work_to_scratch_task = SSHOperator(
    task_id='rsync_work_to_scratch',
    ssh_hook=ssh_hook,
    command=rsync_work_to_scratch_command,
    dag=dag
)



miso_samplesheet_generate_task = BashOperator(
    task_id="miso_samplesheet_generate_task",
#    bash_command='echo "Here is the message:  {{ dag_run.conf["miso_id"] }} to {{ dag_run.conf["work_dir"] }}"',
    bash_command='echo "Here is the message: {{ dag_run.conf["work_dir"]  }} to {{ dag_run.conf["reverse_id"]  }} to {{ dag_run.conf["scratch_dir"] }} to {{ dag_run.conf["archive_dir"] }} to  {{ dag_run.conf["projname"] }}  to  {{ dag_run.conf["miso_id"] }} to {{ dag_run.conf["jira_ticket"] }} to {{ dag_run.conf["workflow"] }} to {{ dag_run.conf["adpone"] }} to {{ dag_run.conf["adptwo"] }} to {{ dag_run.conf["email_id"] }}"',
)

ensure_samplesheet_task = BashOperator(
    task_id="ensure_samplesheet_task",
    bash_command='echo "Here is the message: \'{{ dag_run.conf["name"] if dag_run else "qqqq" }}\' {{ dag_run.conf["miso"] }}"',
)

demux_reverse_complement_task = BashOperator(
    task_id="demux_reverse_complement_task",
    bash_command='echo "Here is the message: \'{{ dag_run.conf["name"] if dag_run else "qqqq" }}\' {{ dag_run.conf["miso"] }}"',
)

adapter_string_replace_task = BashOperator(
    task_id="adapter_string_replace_task",
    bash_command='echo "Here is the message: \'{{ dag_run.conf["name"] if dag_run else "qqqq" }}\' {{ dag_run.conf["miso"] }}"',
)


archive_run_dir_task = BashOperator(
    task_id="archive_run_dir_task",
    bash_command='echo "Here is the message: \'{{ dag_run.conf["name"] if dag_run else "qqqq" }}\' {{ dag_run.conf["miso"] }}"',
)


#rsync_archive_to_scratch_task >> miso_samplesheet_generate_task >> ensure_samplesheet_task >> demux_reverse_complement_task >> adapter_string_replace_task  >> adapter_string_replace_task >> validate_samplenames_task >> demultiplex_task >> demultiplex_task >> submit_qc_workflow_task >> email_sent_task >> archive_run_dir_task
#rsync_archive_to_scratch_task >> [miso_samplesheet_generate_task,ensure_samplesheet_task,demux_reverse_complement_task,adapter_string_replace_task,adapter_string_replace_task,validate_samplenames_task,demultiplex_task,submit_qc_workflow_task,email_sent_task,archive_run_dir_task]

Initiate_task >> rsync_work_to_scratch_task >> miso_samplesheet_generate_task
