#!/usr/bin/env bash

#################################################################
# Arguments for Airflow initialization
# So far there is only the SSH / MYSQL / SMTP connection to Jubail
#################################################################

## Defining SSH connection 
#airflow connections add  airflow_docker_ssh   --conn-type ssh \
#    --conn-host cgsb-build.abudhabi.nyu.edu \
#    --conn-login jr5241 \
#    --conn-port 4410 \
#    --conn-extra '{"key_file": "/home/airflow/.ssh/docker_rsa", "missing_host_key_policy": "AutoAddPolicy"}'

## Define jubail access
airflow connections add  airflow_docker_ssh   --conn-type ssh \
    --conn-host jubail.abudhabi.nyu.edu \
    --conn-login gencore \
    --conn-port 22 \
    --conn-extra '{"key_file": "/home/airflow/.ssh/id_rsa", "missing_host_key_policy": "AutoAddPolicy"}'

## Defining SMTP connection 

#airflow connections add airflow_docker_email --conn-type email \
#    --conn-host smtp.gmail.com \ 
#    --conn-login nyu10062@nyu.edu \ 
#    --conn-password jicbsgkxpnbtgdxa \ 
#    --conn-port 465

airflow connections add airflow_docker_email --conn-type email --conn-host smtp.gmail.com --conn-login nyu10062@nyu.edu --conn-password jicbsgkxpnbtgdxa --conn-port 465
## Defining Mysql Connection 
#airflow connections add airflow_docker_mysql --conn-type mysql \ 
#    --conn-login root \
#    --conn-password test \
#    --conn-host cgsb-build.abudhabi.nyu.edu \
#    --conn-port 13307 \
#    --conn-schema lims \
#    --conn-extra '{"ssl_mode": "DISABLED"}'

airflow connections add airflow_docker_mysql --conn-type mysql --conn-login root --conn-password test --conn-host cgsb-build.abudhabi.nyu.edu --conn-port 13307 --conn-schema lims --conn-extra '{"ssl_mode": "DISABLED"}'
