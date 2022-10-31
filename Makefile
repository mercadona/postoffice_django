#!/usr/bin/make -f

.DEFAULT_GOAL := help

.PHONY: env-start env-stop install-test-dependencies test help
.PHONY: deploy

ROOT_FOLDER := $(shell pwd)
DOCKER_COMPOSE_FILE := $(ROOT_FOLDER)/docker/docker-compose.yml
DOCKER_PROJECT_NAME := postoffice_django
PACKAGE_NAME := postoffice-django
APP_SERVICE := app

install-test-requirements: ## Install all test dependencies
	docker-compose -p $(DOCKER_PROJECT_NAME) -f $(DOCKER_COMPOSE_FILE) exec -T ${APP_SERVICE} pip install --disable-pip-version-check -r /src/requirements/test.txt

test:
	docker-compose -p $(DOCKER_PROJECT_NAME) -f $(DOCKER_COMPOSE_FILE) exec -T ${APP_SERVICE} python runtests.py

build: ## Build project image
	docker-compose -p $(DOCKER_PROJECT_NAME) -f $(DOCKER_COMPOSE_FILE) build --no-cache --pull

env-start: ## Start project containers defined in docker-compose
	docker-compose -p $(DOCKER_PROJECT_NAME) -f $(DOCKER_COMPOSE_FILE) up -d
	docker-compose -p $(DOCKER_PROJECT_NAME) -f $(DOCKER_COMPOSE_FILE) exec -T ${APP_SERVICE} pip install --disable-pip-version-check -r /src/requirements/base.txt

env-stop: ## Stop project containers defined in docker-compose
	docker-compose -p $(DOCKER_PROJECT_NAME) -f $(DOCKER_COMPOSE_FILE) stop

env-destroy: ## Destroy all project containers
	docker-compose -p $(DOCKER_PROJECT_NAME) -f $(DOCKER_COMPOSE_FILE) down -v --rmi all --remove-orphans

env-recreate: build env-start  ## Force building project image and start all containers again

env-reset: destroy-containers env-start ## Destroy project containers and start them again

destroy-containers: ## Destroy project containers
	docker-compose -p $(DOCKER_PROJECT_NAME) -f $(DOCKER_COMPOSE_FILE) down -v

bash: ## Open a bash shell in project's main container
	docker-compose -p $(DOCKER_PROJECT_NAME) -f $(DOCKER_COMPOSE_FILE) exec app bash

view-logs: ## Display interactive logs of all project containers
	docker-compose -p $(DOCKER_PROJECT_NAME) -f $(DOCKER_COMPOSE_FILE) logs -f

deploy: ## Tag and push a version. Usage: make distribute VERSION=1.0.0
	@[ "${VERSION}" ] && git tag "$(VERSION)" && git push --tags \
	|| ( echo "VERSION is not set. Usage: make deploy VERSION=1.0.0"; exit 1 )

help: ## Display this help text
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
