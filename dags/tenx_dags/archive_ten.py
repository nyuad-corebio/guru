import paramiko
import argparse
import logging
import os
import sys
from tenx_dags.ssh_helpers import execute_ssh_command
from airflow.providers.ssh.hooks.ssh import SSHHook


logger = logging.getLogger('archive_tar_archive-3')
logger.setLevel(logging.DEBUG)


def generate_archive_scratch_dir_command(scratch_dir):
    dirname = os.path.dirname(scratch_dir)

    archive_dir = scratch_dir.replace('scratch', 'archive')
    archive_dir = os.path.dirname(archive_dir)
    # tar_name = os.path.basename(scratch_dir) + '.tar'
    tar_name = os.path.basename(scratch_dir)

    # TODO Really should have profiles that say where to ssh to
    return 'rsync -av  {}/{} {}/'.format(dirname, tar_name, archive_dir)


def archive_scratch_dir_folder(ds, **kwargs):
    #Defining SSH connection 
    ssh_hook = SSHHook(ssh_conn_id='guru_ssh')
    ssh = ssh_hook.get_conn()

    scratch_dir = kwargs['dag_run'].conf['scratch_dir']
    scratch_dir = scratch_dir.rstrip('/')

    command = generate_archive_scratch_dir_command(scratch_dir)
    status = execute_ssh_command(ssh, command, logger, None)
    ssh.close()

    if status:
        return
    else:
        raise Exception
    

