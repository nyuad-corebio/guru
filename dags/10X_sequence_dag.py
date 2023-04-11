from datetime import datetime
from airflow import DAG
from airflow.providers.ssh.operators.ssh import SSHOperator
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.ssh.hooks.ssh import SSHHook

#Loading python dag run scripts  
from tenx_dags.archive_ten  import archive_scratch_dir_folder
from tenx_dags.demultiplex_ten import run_demultiplex_task
from tenx_dags.email_pre_ten import run_pre_email_task
from tenx_dags.email_post_ten import run_post_email_task

#Loading jira module 
from nyuad_cgsb_jira_client.jira_client import jira_client


#source_file_path = '{{ dag_run.conf.name }}'   

dag = DAG('10X_sequence', description='10X Sequence DAG',
          schedule_interval=None,
          start_date=datetime(2023, 4, 1), catchup=False)
ssh_hook = SSHHook(ssh_conn_id='airflow_docker_ssh')
ssh_hook.no_host_key_check = True

def print_hello(ds=None, **kwargs):
    dag_run = kwargs['dag_run']
    pprint(dag_run)
    return 'Hello world from first Airflow DAG! {{ dag_run.conf["scratch_dir"] }} end'


rsync_archive_to_scratch_task = BashOperator(
    task_id="rsync_archive_to_scratch_task",
    bash_command='echo "Here is the message: {{ dag_run.conf["work_dir"]  }}  to {{ dag_run.conf["jira_ticket"] }}"',
)


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

# miso_samplesheet_generate_task = BashOperator(
#     task_id="miso_samplesheet_generate_task",
#     bash_command='echo "Here is the message: {{ dag_run.conf["work_dir"]  }}  to {{ dag_run.conf["scratch_dir"] }} to {{ dag_run.conf["archive_dir"] }} to {{ dag_run.conf["projname"] }}  to {{ dag_run.conf["workflow"] }} to  {{ dag_run.conf["miso_id"] }} to {{ dag_run.conf["jira_ticket"] }} to {{ dag_run.conf["email_id"] }}"',
# )

miso_samplesheet_generate_command = """
        rsync -av /scratch/gencore/workflows/latest/miso_samplesheet_gen10X.py "{{ dag_run.conf["scratch_dir"] }}/"
        cd "{{ dag_run.conf["scratch_dir"] }}/"
        module load python/3.9.0
        python miso_samplesheet_gen10X.py {{ dag_run.conf["miso_id"]}}
"""

miso_samplesheet_generate_task = SSHOperator(
    task_id='miso_samplesheet_generate',
    ssh_hook=ssh_hook,
    command=miso_samplesheet_generate_command,
    retries=2,
    retry_delay=60,
    dag=dag
)

demultiplex_task = PythonOperator(
    task_id='demultiplex',
    retries=1,
    python_callable=run_demultiplex_task,
    provide_context=True,
    dag=dag
)

email_pre_sent_task = PythonOperator(
    task_id='email_pre_sent',
    retries=1,
    python_callable=run_pre_email_task,
    dag=dag
)

archive_scratch_folder_task = PythonOperator(
    task_id='archive_run_dir',
    retries=2,
    python_callable=archive_scratch_dir_folder,
    dag=dag
)

email_post_sent_task = PythonOperator(
    task_id='email_post_sent',
    retries=1,
    python_callable=run_post_email_task,
    dag=dag
)

#rsync_archive_to_scratch_task >> miso_samplesheet_generate_task >> ensure_samplesheet_task >> demux_reverse_complement_task >> adapter_string_replace_task  >> adapter_string_replace_task >> validate_samplenames_task >> demultiplex_task >> demultiplex_task >> submit_qc_workflow_task >> email_sent_task >> archive_run_dir_task
#rsync_archive_to_scratch_task >> [miso_samplesheet_generate_task,ensure_samplesheet_task,demux_reverse_complement_task,adapter_string_replace_task,adapter_string_replace_task,validate_samplenames_task,demultiplex_task,submit_qc_workflow_task,email_sent_task,archive_run_dir_task]

rsync_work_to_scratch_task >> email_pre_sent_task  >> miso_samplesheet_generate_task >> demultiplex_task >> email_post_sent_task >> archive_scratch_folder_task
