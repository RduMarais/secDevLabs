.SILENT:
.DEFAULT_GOAL := help

COLOR_RESET = \033[0m
COLOR_COMMAND = \033[36m
COLOR_YELLOW = \033[33m
COLOR_GREEN = \033[32m
COLOR_RED = \033[31m

PROJECT := A6 - Stegonography
PORT := 10006

FLAG_ARG=$(flag)

## Installs a development environment
install: env compose msg

## Composes project using docker-compose
compose: compose-down
	docker-compose -f deployments/docker-compose.yml -p secdevlabs up -d --build --force-recreate

## Down project using docker-compose
compose-down:
	docker-compose -f deployments/docker-compose.yml -p secdevlabs down -v --remove-orphans

## Generate new environment variables for Stegonography app
env:
	chmod +x deployments/generate-env.sh
	./deployments/generate-env.sh

## Deploys CTF infra with flag=XXX
ctf: deploy-ctf msg
	echo "flag to use : ${FLAG_ARG}"

deploy-ctf:
	# sed is used in a distribution-independant manner
	sed -i'.bak' -e 's/<h1 class="h3 mb-0 text-gray-800">Dashboard<\/h1>/<h1 class="h3 mb-0 text-gray-800">${FLAG_ARG}<\/h1>/g' app/static/views/admin.html
	docker-compose -f deployments/docker-compose.yml -p secdevlabs up -d --build --force-recreate

ctf-down:
	mv app/static/views/admin.html.bak app/static/views/admin.html
	docker-compose -f deployments/docker-compose.yml -p secdevlabs down -v --remove-orphans

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
