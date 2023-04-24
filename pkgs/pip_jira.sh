#!/usr/bin/env bash
################
#This script install the jira custom module with Oauthv1 authentication.
#OAUTH credentials and private key we specified in .env and private key specified in keys directory
################
set -x -e
cd nyuad-cgsb-jira-client
pip install --ignore-installed .
