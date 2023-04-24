# GURU: Genomics seqUencing Run aUtomation


## Contents

- [Introduction](#introduction)
- [Installation](#installation)
    - [Installing from PyPI](#installing-from-pypi)
    - [Installing from Docker](#installing-from-docker)
- [Contact](#contact)

## Introduction

Managing and maintaining a genomics infrastructure requires a multi-layered approach. Typically, that involves a Laboratory Information Management System (LIMS), the Sequencing Instrumentation, the computational Infrastructure to store and process the data, as well as any other additional layers such as project management software (e.g. JIRA). In a production environment, all of these layers need to efficiently communicate and integrate with each other, which can be a complicated task. In addition, the approach needs to be descriptive and yet flexible enough to accommodate new additions to the existing layers. Our solution, GURU (Genomics seqUencing Run aUtomation) addresses this need. GURU is implemented using Apache Airflow that allows for the authoring, scheduling and monitoring of workflows, or DAGs (Directed Acyclic Graph). Specific DAGs have been implemented to handle various sequencing runs, from SingleCell applications, to RNA/DNA sequencing, Short reads vs Long reads, archiving of sequencing runs, initiating specific types of analysis (QC/WGS/WES/RNAseq/ATAC/CHiP etc.), as well as automatically communicate to end-users regarding the status of their samples/runs. GURU has been containerized using Docker to enable easy deployment across various configurations.


### Key facts 

- Customized user interface plugins using Apache Flask Web Framework, ensuring DAGs are bound to their respective plugins. 
- Airflow models (Dagbags) are used to enable the communication with the Airflow plugins, thus avoiding RESTAPIs.
- Commands are launched directly on the computational environment (Server/HPC/Cloud), and their status is monitored, meaning that GURU can be deployed anywhere and does not have to be deployed in the same ( computational infrastructure where the data processing happens.
- Integration with JIRA (or other issue tracking systems) is achieved using a RESTAPI. The same approach can be implemented for any other additional layers of communication. 
- Integration with Bioinformatics Workflow Management Systems such as BioSAILs ensures more complex analyses can be supported (other WMS can also be supported e.g. Nextflow, CWL, Snakemake).


## Installation

Here are the different ways that you can launch GURU. 
Note:- You can customize the configuration as per your requirements. 

### Installing from PyPI

Installation using pip based setup as follows:- 

Clone the repository and switch to the working directory.

```
git clone https://github.com/nyuad-corebio/guru
cd guru
```

Define the environment variable in your .bashrc or .zshrc of you favourite shell.
Note:- Jira is optional, if you are not using customize the code accordingly.

``` bash
### Airflow variables
export AIRFLOW_HOME=<Path-to-airflow-home>
export AIRFLOW_URL=<IP Address or Hostname of the host machine>
export AIRFLOW_PORT=8080
###Jira env variables
export CONSUMER_KEY=<key_name>
export JIRA_SERVER=<URL or IP Address>
export OAUTH_TOKEN=<token>
export OAUTH_TOKEN_SECRET=<token_secret>
```


Install the prerequisite python packages using below command

``` bash
pip3 install -r pip-requirements.txt
```

Install jira module 

``` bash
cd pkgs
sh pip_jira.sh
```

Initialize airflow db and this will create airflow.cfg in the AIRFLOW_HOME directory which defined as variable.

``` bash
airflow db init
```



Create user account

``` bash
airflow users create \
--username airflow \
--password airflow \
--firstname <first-name> \
--lastname <lastname> \
--role Admin \
--email <specify-email>
```

Update the airflow connection parameters for ssh, smtp and mysql.
Note:- Modify the ssh key path, user credentails etc.
``` bash
sh scripts/airflow_conn.sh
```

Launch below two commands on each terminal or you can run as a background one after the other. 

``` bash
airflow scheduler
airflow webserver
```

To access  [http://IP-address:8080](http://IP-address:8080)
and use the credentials **airflow**/**airflow**.

### Installing from Docker


The simplest way to get GURU up and running quickly is to use
[Docker](https://www.docker.com/) compose. 

#### Prerequisites

Install required dependencies:

1. [Install Docker Latest Version V23.0.2+](https://docs.docker.com/engine/install/)



Clone the repository and switch to the working directory.

```
git clone https://github.com/nyuad-corebio/guru
cd guru
```

You are now ready to run GURU.

#### Setting up the environment

Defining the environment variables. 
Note:- Jira is optional, if you are not using customize the code accordingly.

``` bash
cat .env
### Airflow variables
AIRFLOW_UID=<Airflow USER ID - Default is 50000>
AIRFLOW_URL=<IP Address or Hostname of the host machine>
AIRFLOW_PORT=8080

### Jira variables
CONSUMER_KEY=<key_name>
JIRA_SERVER=<URL or IP Address>
OAUTH_TOKEN=<token>
OAUTH_TOKEN_SECRET=<token_secret>
```

***Update airflow connection params***


To bring up the environment, install the pre-requisites above and run the
following commands.


Using docker compose command:
``` bash
docker compose up --build -d
sleep 60
docker compose restart
```

Verify the service using 
```
docker compose logs -f 
```



To access  [http://IP-address:8080](http://IP-address:8080)
and use the credentials **airflow**/**airflow**.


## Contact

If you have any questions, please contact [here](nyuad.cgsb.cb@nyu.edu).

- [CGSB Webpage](https://cgsb.abudhabi.nyu.edu) : for news and updates