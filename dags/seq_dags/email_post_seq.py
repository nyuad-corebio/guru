import argparse
import io
import logging
import os
import sys
import smtplib
from email.message import EmailMessage
from airflow.hooks.base import BaseHook
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from airflow.providers.ssh.hooks.ssh import SSHHook
from nyuad_cgsb_jira_client.jira_client import jira_client


def generate_email_task(ds, **kwargs):
    dag_run = kwargs['dag_run']
    work_dir = dag_run.conf['work_dir']
    scratch_dir = dag_run.conf['scratch_dir']
    email_id = dag_run.conf['email_id']
    miso_id = dag_run.conf['miso_id']
    jira_ticket = dag_run.conf['jira_ticket']

    # Defining the path
    file_path = f"{scratch_dir}/Unaligned/data/processed/{jira_ticket}.html"
    # Trimming the basename which is required in sending email
    file_path_file = os.path.basename(file_path)


    #Defining SSH connection
    ssh_hook = SSHHook(ssh_conn_id='guru_ssh')
    ssh = ssh_hook.get_conn()

    # File existence check
    sftp = ssh.open_sftp()
    try:
        sftp.stat(file_path)
    except FileNotFoundError:
        raise AirflowException(f"The file {file_path_file} does not exist on ")

    # Open and saving the file as object
    remote_file = sftp.open(file_path, 'rb')
    file_bytes = remote_file.read()
    file_obj = io.BytesIO(file_bytes)

    # Closing connection
    remote_file.close()
    sftp.close()
    ssh.close()

    # SMTP configuration begins
    subject = f"Processing sequencing run {jira_ticket} / Miso ID {miso_id}"
    body = (f"Your recent run {jira_ticket} / Miso ID {miso_id} has successfully completed. \n\n"
                 f"Run Path:- {scratch_dir}/Unaligned\n"
                 "MultiQC Summary report is attached.\n\n"
                 "\n"
                 "Regards\n")
    attachments = [(file_path_file, file_obj)]

    # Set the SMTP Connection ID
    smtp_conn_id = 'guru_email'
    smtp_hook = BaseHook.get_connection(smtp_conn_id)

    # SMTP credentials
    smtp_server = smtp_hook.host
    smtp_port = smtp_hook.port
    smtp_username = smtp_hook.login
    smtp_password = smtp_hook.password

    # Compose the template
    msg = MIMEMultipart()
    msg['From'] = "Sequencing Run Notification"
    to = (f"{email_id}")
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(body))

    # Attaching file from object and assign to msg.attach variable 
    for filename, file_obj in attachments:
        attachment = MIMEApplication(file_obj.read(), _subtype='html')
        attachment.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(attachment)

    # Initiate the send
    with smtplib.SMTP_SSL(smtp_server, smtp_port)as server:
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, to.split(','), msg.as_string())

def email_jira_ticket_success(context):
    run_id = context['run_id']
    miso_id = context['dag_run'].conf['miso_id']
    jira_ticket = context['dag_run'].conf['jira_ticket']
    scratch_dir = context['dag_run'].conf['scratch_dir']
    comment = (f"Your recent run {jira_ticket} / Miso ID {miso_id} has successfully completed.\n\n"
                 "\n"
                 "Run Path"
                 "{code}"
                 f"{scratch_dir}/Unaligned/\n"
                 "{code}"
                 "\n"
                 "Regards,\n")
    jira_client.add_comment(jira_ticket, comment)

    #Define the variables for jira attachment
    file_path = f"{scratch_dir}/{jira_ticket}.html"
    file_path_file = os.path.basename(file_path)

    #Defining SSH connection
    ssh_hook = SSHHook(ssh_conn_id='guru_ssh')
    ssh = ssh_hook.get_conn()

#   Here copy the file from remote server and write as open file
    sftp = ssh.open_sftp()
    file_path = f"{scratch_dir}/Unaligned/data/processed/{jira_ticket}.html"
    file_obj = io.BytesIO()
    sftp.getfo(file_path, file_obj)
    sftp.close()

#   Seek the value to 0'th index
    file_obj.seek(0)
    jira_client.add_attachment(jira_ticket, attachment=file_obj, filename=file_path.split('/')[-1])

    sftp.close()
    ssh.close()
    return

def run_post_email_task(ds, **kwargs):
    generate_email_task(ds, **kwargs)
    email_jira_ticket_success(kwargs)

