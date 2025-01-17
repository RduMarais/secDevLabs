.SILENT:
.DEFAULT_GOAL := help

COLOR_RESET = \033[0m
COLOR_COMMAND = \033[36m
COLOR_YELLOW = \033[33m
COLOR_GREEN = \033[32m
COLOR_RED = \033[31m

PROJECT := A7 Gossip World
PORT := 10007
SLEEPUNTILAPPSTARTS := 45

FLAG_ARG=$(flag)

## Installs a development environment using docker-compose
install: compose msg 

## Runs project using docker-compose
compose: compose-down
	docker-compose -f deployments/docker-compose.yml -p secdevlabs up -d --build --force-recreate

## Down project using docker-compose
compose-down:
	docker-compose -f deployments/docker-compose.yml -p secdevlabs down -v --remove-orphans

## Deploys project and view docker logs
deploy: compose
	docker logs app-a7 -f


## Deploys CTF infra with flag=XXX
ctf: deploy-ctf msg
	echo "flag to use : ${FLAG_ARG}"
	screen -dm -S gossip_bot python app/util/bot_flag.py

test-ctf:
	echo "${FLAG_ARG}" > app/util/.flag.txt
	screen -dm -S gossip_bot python app/util/bot_flag.py

deploy-ctf:
	echo "${FLAG_ARG}" > app/util/.flag.txt
	docker-compose -f deployments/docker-compose.yml -p secdevlabs_gossip_world up -d --build --force-recreate

ctf-down:
	rm app/util/.flag.txt
	docker-compose -f deployments/docker-compose.yml -p secdevlabs_gossip_world down -v --remove-orphans

## Prints initialization message after compose phase
msg:
	chmod +x deployments/check-init.sh
	./deployments/check-init.sh

## Prints help message
help:
	printf "\n${COLOR_YELLOW}${PROJECT}\n------\n${COLOR_RESET}"
	awk '/^[a-zA-Z\-\_0-9\.%]+:/ { \
		helpMessage = match(lastLine, /^## (.*)/); \
		if (helpMessage) { \
			helpCommand = substr($$1, 0, index($$1, ":")); \
			helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
			printf "${COLOR_COMMAND}$$ make %s${COLOR_RESET} %s\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST) | sort
	printf "\n"
