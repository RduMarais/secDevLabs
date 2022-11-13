.SILENT:
.DEFAULT_GOAL := help

GO ?= go
GOROOT ?= $(shell $(GO) env GOROOT)
GOPATH ?= $(shell $(GO) env GOPATH)
GOBIN ?= $(GOPATH)/bin

COLOR_RESET = \033[0m
COLOR_COMMAND = \033[36m
COLOR_YELLOW = \033[33m
COLOR_GREEN = \033[32m
COLOR_RED = \033[31m

PROJECT := A1 - CopyNPaste API
PORT := 10001
SLEEPUNTILAPPSTARTS := 45

FLAG_ARG=$(flag)

## Test the application
test: go test ./...

## Run project using docker-compose
compose: compose-down
	docker-compose -f deployments/docker-compose.yml -p secdevlabs up -d --build --force-recreate

## Down project using docker-compose
compose-down:
	docker-compose -f deployments/docker-compose.yml -p secdevlabs down -v --remove-orphans

exploit:
	chmod +x deployments/exploit.sh
	./deployments/exploit.sh

## Deploys CTF infra with flag=XXX
ctf: deploy-ctf msg
	echo "flag to use : ${FLAG_ARG}"
	curl -i -s -k -X $$'POST' -H $$'Host: localhost:10001' -H $$'Content-Type: application/json' --data-binary $$'{\"user\":\"${FLAG_ARG}\",\"pass\":\"${FLAG_ARG}\",\"passcheck\":\"${FLAG_ARG}\"}' $$'http://localhost:10001/register'

deploy-ctf:
	docker-compose -f deployments/docker-compose.yml -p secdevlabs_copy_paste down -v 
	docker-compose -f deployments/docker-compose.yml -p secdevlabs_copy_paste up -d --build --force-recreate

ctf-down:
	docker-compose -f deployments/docker-compose.yml -p secdevlabs_copy_paste down -v --remove-orphans

validate:


## Installs a development environment using docker-compose
install: compose msg

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
