# GURU: Genomics seqUencing Run AUtomation

## Trying GURU


### Standalone setup

Installation using pip based setup as follows:- 

``` bash

cat pip-requirements.txt
apache-airflow                      
apache-airflow-client               
apache-airflow-providers-common-sql 
apache-airflow-providers-ftp        
apache-airflow-providers-http       
apache-airflow-providers-imap       
apache-airflow-providers-mysql      
apache-airflow-providers-sqlite     
apache-airflow-providers-ssh        
```

``` bash
pip3 install -r pip-requirements.txt
```



### Docker setup 


The simplest way to get GURU up and running quickly is to use
[Docker](https://www.docker.com/) compose. 

#### Prerequisites

Install required dependencies:

1. [Install Docker Latest Version V23.0.2+](https://docs.docker.com/engine/install/)
2. Linux Server preferred



Clone the repository and switch to the working directory.


```
git clone https://github.com/nyuad-corebio/sequencer-automation
cd sequencer-automation
```

You are now ready to run GURU.

#### Setting up the environment

Specifying the environment variables. 

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


