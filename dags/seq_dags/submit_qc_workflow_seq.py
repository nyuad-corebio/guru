from jinja2 import Environment, BaseLoader
#import paramiko
from seq_dags.ssh_helpers import execute_ssh_command_return_stdout_stderr, initialize_ssh
import logging
from nyuad_cgsb_jira_client.jira_client import jira_client
from seq_dags.biosails_helpers import poll_biosails_submissions
from airflow.providers.ssh.hooks.ssh import SSHHook

logger = logging.getLogger('submit_qc_workflow')
logger.setLevel(logging.DEBUG)

run_qc_workflow_command = """
#!/usr/bin/env bash

{% if dag_run.conf["scratch_dir"] %}
echo "Scratch Dir: {{ dag_run.conf["scratch_dir"] }}"
cd {{ dag_run.conf["scratch_dir"] }}/Unaligned
{% else %}
echo "There is no scratch dir specified. Exiting"
exit 256
{% endif %}

{% if dag_run.conf["qc_workflow"] %}
echo "Rendering: {{ dag_run.conf["qc_workflow"] }}"
cp {{ dag_run.conf["qc_workflow"] }} ./
sed -i  s/NCS-NUM/{{ dag_run.conf["jira_ticket"]}}/g {{ dag_run.conf["scratch_dir"] }}/Unaligned/qc*yml
module load gencore/1
module load gencore_biosails
biox run -w {{ dag_run.conf["scratch_dir"] }}/Unaligned/qc*yml -o qc.sh
hpcrunner.pl submit_jobs --infile qc.sh --project {{dag_run.conf["jira_ticket"]}}-qc
{% else %}
echo "There is no QC Workflow specified. Exiting"
exit 0
{% endif %}
"""


def submit_qc_workflow_to_slurm(ds, **kwargs):
    """ If there is a QC Workflow
    render it using biox, and submit it to slurm with hpcrunner
    Then poll the job to check when its done
    """

    if not kwargs['dag_run'].conf['qc_workflow']:
        return
    else:

        #Defining SSH connection
        ssh_hook = SSHHook(ssh_conn_id='guru_ssh')
        ssh = ssh_hook.get_conn()
        sftp = ssh.open_sftp()
    # File existence check
   # sftp = ssh.open_sftp()

        rtemplate = Environment(loader=BaseLoader).from_string(run_qc_workflow_command)
        rendered_run_qc_workflow_command = rtemplate.render(dag_run=kwargs['dag_run'])
        agg_output = False
        error = False
        ssh.close
        try:
            agg_output = execute_ssh_command_return_stdout_stderr(ssh, rendered_run_qc_workflow_command, logger)
        except Exception as e:
            error = e

        if agg_output:
            from pprint import pprint
            pprint(agg_output)
            poll_biosails_submissions(ssh, sftp, agg_output, kwargs)
        else:
            raise Exception('No output from biosails submission found!')


