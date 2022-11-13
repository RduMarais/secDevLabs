.SILENT:
.DEFAULT_GOAL := help

COLOR_RESET = \033[0m
COLOR_COMMAND = \033[36m
COLOR_YELLOW = \033[33m
COLOR_GREEN = \033[32m
COLOR_RED = \033[31m

PROJECT := A9 - Cimentech
PORT := 80

FLAG_ARG=$(flag)

## Installs a development environment
install: compose msg

## Composes project using docker-compose
compose: compose-down
	docker-compose -f deployments/docker-compose.yml -p secdevlabs up -d --build --force-recreate

## Down project using docker-compose
compose-down:
	docker-compose -f deployments/docker-compose.yml -p secdevlabs down -v --remove-orphans

## Prints initialization message after compose phase
msg:
	chmod +x deployments/check-init.sh
	./deployments/check-init.sh

## deploys CTF app with flag=XXXX
ctf: deploy-ctf msg
	echo "flag to use : ${FLAG_ARG}"

deploy-ctf:
	mkdir app/html/flag
	echo "flag = ${FLAG_ARG}" >> app/html/flag/flag.txt
	docker-compose -f deployments/docker-compose.yml -p secdevlabs_cimentech up -d --build --force-recreate

ctf-down:
	rm -r app/html/flag
	docker-compose -f deployments/docker-compose.yml -p secdevlabs_cimentech down -v --remove-orphans

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
