FROM apache/airflow:2.5.3
USER root
#Setting Dubai TZ
ENV TZ=Asia/Dubai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
USER airflow
RUN echo "alias ll='ls -lah'" >> ~/.bashrc
#RUN echo "export CONSUMER_KEY=jira-cli" >> ~/.bashrc
#RUN echo "export JIRA_SERVER=https://cbi.abudhabi.nyu.edu/jira" >> ~/.bashrc
#RUN echo "export OAUTH_TOKEN=aqq77NdQrEPjV9GC6rSR4lwVqo4Sg4Vg" >> ~/.bashrc
#RUN echo "export OAUTH_TOKEN_SECRET=Vs7q0GZoS9MMO1mAfiIm440UsWS1Yvut" >> ~/.bashrc
ADD requirements.txt .
RUN pip install -r requirements.txt
ADD pkgs /opt/airflow/pkgs
USER root
RUN chmod -R 777 /opt/airflow/pkgs
USER airflow
WORKDIR /opt/airflow/pkgs
RUN sh pip_custom.sh
#RUN pip install -U pyjwt
RUN pip install -U  --force-reinstall PyJWT
WORKDIR /opt/airflow
