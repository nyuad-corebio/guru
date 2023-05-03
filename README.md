# GURU: Genomics seqUencing Run aUtomation

## Contents

- [Introduction](#introduction)
    - [Key facts](#key-facts)
    - [Technologies Used](#technologies-used)
- [Installation](#installation)
    - [Installing from Docker](#installing-from-docker)
    - [Installing from PyPI](#installing-from-pypi)
- [Usage](#usage)
- [Contact](#contact)
- [Citation](#citation)
- [Acknowledgements](#acknowledgements)
- [Other Useful Links](#other-useful-links)

## Introduction

Managing and maintaining a genomics infrastructure requires a multi-layered approach. Typically, that involves a Laboratory Information Management System (LIMS), the Sequencing Instrumentation, the computational Infrastructure to store and process the data, as well as any other additional layers such as project management software (e.g. JIRA). In a production environment, all of these layers need to efficiently communicate and integrate with each other, which can be a complicated task. In addition, the approach needs to be descriptive and yet flexible enough to accommodate new additions to the existing layers. Our solution, GURU (Genomics seqUencing Run aUtomation) addresses this need. GURU is implemented using Apache Airflow that allows for the authoring, scheduling and monitoring of workflows, or DAGs (Directed Acyclic Graph). Specific DAGs have been implemented to handle various sequencing runs, from SingleCell applications, to RNA/DNA sequencing, Short reads vs Long reads, archiving of sequencing runs, initiating specific types of analysis (QC/WGS/WES/RNAseq/ATAC/CHiP etc.), as well as automatically communicate to end-users regarding the status of their samples/runs. GURU has been containerized using Docker to enable easy deployment across various configurations.

<img src="/img/guru_title.png"  align="center" />

### Key facts 

- Customized user interface plugins using Apache Flask Web Framework, ensuring DAGs are bound to their respective plugins. 
- Airflow models (Dagbags) are used to enable the communication with the Airflow plugins, thus avoiding RESTAPIs.
- Commands are launched directly on the computational environment (Server/HPC/Cloud), and their status is monitored, meaning that GURU can be deployed anywhere and does not have to be deployed in the same  computational infrastructure where the data processing happens.
- Integration with JIRA (or other issue tracking systems) is achieved using a RESTAPI. The same approach can be implemented for any other additional layers of communication. 
- Integration with Bioinformatics Workflow Management Systems such as BioSAILs ensures more complex analyses can be supported (other WMS can also be supported e.g. Nextflow, CWL, Snakemake).

### Technologies Used

- Apache Airflow
- Docker
- Python
- Shell Scripting
- Python Flask Wtforms
- Jira (v6.3.12)


#### Important Note
- The jira we used the version is an outdated one and the integration is based on RESTAPI with Oauthv1. If you require assistance with other project management software or latest jira version, then we will help. 
- LIMS we used miso lims software and if you need assistance with other lims integration, we will help. 

## Installation

You can install GURU using [pip](https://pip.pypa.io/en/stable/) or  [docker](https://www.docker.com/). The simplest way to get GURU up and running quickly is to use Docker. 


### Installing from Docker
 
#### Prerequisites

1. [Install Docker Latest Version V23.0.2+](https://docs.docker.com/engine/install/)
2. Miso Lims ( Optional:- iskylims or other LIMS tools )
3. Jira ( Optional:- redmine or other project management softwares )

#### Cloning the repository

```
git clone https://github.com/nyuad-corebio/guru
cd guru
```

#### Setting up the environment

Defining the environment variables. 
Note:- Jira is optional, if you are not using customize the .env file accordingly.
Note:- Since the jira integration is based on Oauthv1, using a private key. You should place key name "jira.pem" in "keys" folder.

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

To invoke the the docker based installation, issue below commands.

``` bash
docker compose up --build -d
docker compose restart
```

Verify the services
``` bash
docker compose ps 
```

Validate the logs 
``` bash
docker compose logs -f 
```

To access Airflow User Interface [http://IP-address:8080](http://IP-address:8080)
and use the credentials **airflow**/**airflow**.

Note:- 
- If you run this service on a server, specify the (IP-address or hostname):8080 on the browser. 
- If you run this service on laptop, specify localhost:8080 on the browser

### Installing from PyPI

Installation using pip based setup as follows:- 

#### Cloning the repository

```
git clone https://github.com/nyuad-corebio/guru
cd guru
```

Define the environment variable in your .bashrc or .zshrc of you favourite shell.
Note:- Jira is optional, if you are not using customize the environment file accordingly.

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

Install jira module ( Optional )
Note:- Since the jira integration is based on Oauthv1, using a private key. You should place key name "jira.pem" in ~/.ssh/ path. 

``` bash
cd pkgs
sh pip_jira.sh
```

Initialize airflow db and this will create airflow.cfg in the AIRFLOW_HOME directory which defined as variable.

``` bash
airflow db init
```

Create user account named airflow with admin privileges.

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

To access Airflow User Interface [http://IP-address:8080](http://IP-address:8080)
and use the credentials **airflow**/**airflow**.

Note:- 
- If you run this service on a server, specify the (IP-address or hostname):8080 on the browser. 
- If you run this service on laptop, specify localhost:8080 on the browser

## Usage

- **DAGs**: Once login to Airflow UI, you may see the Airflow dags as below.

<img src="/img/guru_dag.png"  align="left"/>

- **User Interface**: Navigate to "Demultiplex Runs" tab to see the appropriate custom UI input for the Airflow Dags.  

<img src="/img/guru_ui_tab.png"  align="left"  />

- **Sequence Run**: Select "Default Sequence Run" from "Demultiplex Runs" tab. 

<img src="/img/guru_ui_template.png"  align="left" />

- **Sequence Run Summary**: Here is the summary  sequence run as per our setup.

<img src="/img/guru_ui_summary.png"  align="left" />

- `Project Name:-` Specify small description of the Project for eg:- Run for jacob for single cell.
- `Miso ID:-` We used Miso Lims for the sample tracking and the samplesheet information associated with the sequencing is fetching from Miso Mysql database based on Run ID( Miso Run ID validation is enabled ).
- `Reverse Complement:-` Specify "yes" or "no", as it will do reverse completement for Index2 sequencing. 
- `Email Address:-` You can specify email address one by one with comma seperated ( Email address syntax validation is enabled ).
- `Jira Ticket:-` We used jira for updating the status of the run and currently we are running an outdated version of jira v6.3.12 and this is integrated via Oauth keys with the airflow. 
- `Workflow:-` We used our custom developed workflow management system for the processing of QC/QT workflow. You can choose snakemake or nextflow or other WMS. Here we specified the path of the directory and where we choose the appropriate yaml files to proceed further.
- `Adapter Sequence 1:-` Sequence of adapter to be trimmed for read1
- `Adapter Sequence 2:-` Sequence of adapter to be trimmed for read2
- `Working Directory:-` Specifying the directory where you have the raw files which to be sequenced. 

- **Run Status**: If you choose "Check Run Status", you may see the status of Airlfow Dagruns started progressing.. 

<img src="/img/guru_dag_run.png"  align="left" />

- **10X Run**: Select "10X Sequence Run" from "Demultiplex Runs" tab.

<img src="/img/guru_ui_10xui.png"  align="left" />

- `10X Workflow:-` Here you can choose the 10X workflows by choosing the appropriate radio button.

- **10X Run Summary**: Similarly if you fill and submit the  "10X Sequence Run". You may see the status of Dagruns.

<img src="/img/guru_ui_10x.png"  align="left" />

## Contact

For any query or feedback related to GURU by posting a [Github issue](https://github.com/nyuad-corebio/guru/issues).

## Citation

If you use GURU in your research or publications, please cite our [Github page](https://github.com/nyuad-corebio/guru).


## Acknowledgements

This work was supported by Tamkeen under the NYU Abu Dhabi Research Institute Award to the NYUAD Center for Genomics and Systems Biology (ADHPG-CGSB). We would also like to acknowledge the High Performance Computing department at NYU Abu Dhabi for the computational resources and their continuous support.

## Other Useful Links

- [CGSB Webpage](https://cgsb.abudhabi.nyu.edu) : for news and updates
- [Biosails](https://www.biorxiv.org/content/biorxiv/early/2019/01/02/509455.full.pdf)
- [Airflow](https://airflow.apache.org/) 
- [Miso Lims](https://github.com/miso-lims/miso-lims)
- [Docker](https://www.docker.com/)