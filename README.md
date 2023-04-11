# GURU: Genomics seqUencing Run AUtomation

## Trying GURU



### Docker setup is needed 

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

``` bash
cat .env
### Airflow variables
AIRFLOW_UID=<Airflow USER ID - Default is 50000>
AIRFLOW_URL=<IP Address or Hostname of the host machine>
AIRFLOW_PORT=8080

### SSH Connection variables
AIRFLOW_CONN_MY_SSH_CONN=ssh://user@host:port?key_file=/home/airflow/.ssh/id_rsa&missing_host_key_policy=AutoAddPolicy&conn_name=my_ssh_conn

### Mysql Connection variables
AIRFLOW_CONN_MY_MYSQL_CONN=mysql://user:password@host:port/database_name?conn_name=my_mysql_conn

### Email Connection variables
AIRFLOW_CONN_MY_EMAIL_CONN=smtp://user:password@smtp.gmail.com:587/?conn_name=my_email_conn


### Jira variables
CONSUMER_KEY=<key_name>
JIRA_SERVER=<URL or IP Address>
OAUTH_TOKEN=<token>
OAUTH_TOKEN_SECRET=<token_secret>
```

*** Update airflow connection params ***


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



To access  [http://localhost](http://localhost)
and use the credentials **airflow**/**airflow**.


