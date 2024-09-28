#!bin/bash -e
dokcer compose down
docker rmi -f costom_llm-multiagent
docker compose up