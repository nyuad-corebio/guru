#!/bin/bash
#To stop and delete all docker volumes, containers, network etc.. 
docker compose down
docker volume rm $(docker volume ls -q)
docker system prune -f -a
