#!/usr/bin/make -f

.DEFAULT_GOAL := help

.PHONY: env-start env-stop install-test-dependencies test help
.PHONY: deploy

ROOT_FOLDER := $(shell pwd)
DOCKER_COMPOSE_FILE := $(ROOT_FOLDER)/docker/docker-compose.yml
DOCKER_PROJECT_NAME := postoffice_django
PACKAGE_NAME := postoffice-django

env-start: ## Start project containers defined in docker-compose
	docker-compose -p $(DOCKER_PROJECT_NAME) -f $(DOCKER_COMPOSE_FILE) up -d
	docker-compose -p $(DOCKER_PROJECT_NAME) -f $(DOCKER_COMPOSE_FILE) exec -T app pip install --disable-pip-version-check -r /src/requirements/base.txt

env-stop: ## Stop project containers defined in docker-compose
	docker-compose -p $(DOCKER_PROJECT_NAME) -f $(DOCKER_COMPOSE_FILE) stop

bash: ## Open a bash shell in project's main container
	docker-compose -p $(DOCKER_PROJECT_NAME) -f $(DOCKER_COMPOSE_FILE) exec app bash

env-install-test-dependencies: ## Install all test dependencies
	docker-compose -p $(DOCKER_PROJECT_NAME) -f $(DOCKER_COMPOSE_FILE) exec -T app pip install --disable-pip-version-check -r /src/requirements/test.txt

install-test-dependencies:  ## Install test dependencies locally. Make sure to have a virtualenv configured.
	pip install -r requirements/test.txt

env-test:
	docker-compose -p $(DOCKER_PROJECT_NAME) -f $(DOCKER_COMPOSE_FILE) exec -T app python runtests.py

test: ## Run the test suite. Make sure you run make env-start first.
	python runtests.py

deploy: ## Tag and push a version. Usage: make distribute VERSION=1.0.0
	@[ "${VERSION}" ] && git tag "$(VERSION)" && git push --tags \
	|| ( echo "VERSION is not set. Usage: make deploy VERSION=1.0.0"; exit 1 )

help: ## Display this help text
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
