#!/usr/bin/env bash
set -x -e
cd /opt/airflow/pkgs/nyuad-cgsb-jira-client
pip install --ignore-installed .
