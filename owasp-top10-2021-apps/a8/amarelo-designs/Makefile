.SILENT:
.DEFAULT_GOAL := help

COLOR_RESET = \033[0m
COLOR_COMMAND = \033[36m
COLOR_YELLOW = \033[33m
COLOR_GREEN = \033[32m
COLOR_RED = \033[31m

PROJECT := A8 - Amarelo Designs
PORT := 10008
SLEEPUNTILAPPSTARTS := 10

FLAG_FRONT_ARG=$(flag_front)
FLAG_BACK_ARG=$(flag_back)

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


## Deploys CTF infra with flag_front=XXX flag_back=XXX
ctf: deploy-ctf msg
	echo "flags to use : ${FLAG_FRONT_ARG} and ${FLAG_BACK_ARG}"

deploy-ctf:
	echo "${FLAG_BACK_ARG}" > app/flag.txt
	sed -i'.bak' -e 's/<h1 class="page-header">Dashboard<\/h1>/<h1 class="page-header">${FLAG_FRONT_ARG}<\/h1>/g' app/static/User/pages/index.html
	docker-compose -f deployments/docker-compose.yml -p secdevlabs up -d --build --force-recreate

ctf-down:
	rm app/flag.txt
	mv app/static/User/pages/index.html.bak app/static/User/pages/index.html
	docker-compose -f deployments/docker-compose.yml -p secdevlabs down -v --remove-orphans


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
