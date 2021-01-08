#!/usr/bin/make -f

.DEFAULT_GOAL := help

.PHONY: env-start env-stop install-test-dependencies test help

ROOT_FOLDER := $(shell pwd)
DOCKER_COMPOSE_FILE := $(ROOT_FOLDER)/docker/docker-compose.yml
DOCKER_PROJECT_NAME := postoffice_django

env-start: ## Start project containers defined in docker-compose
	docker-compose -p $(DOCKER_PROJECT_NAME) -f $(DOCKER_COMPOSE_FILE) up -d

env-stop: ## Stop project containers defined in docker-compose
	docker-compose -p $(DOCKER_PROJECT_NAME) -f $(DOCKER_COMPOSE_FILE) stop

install-test-dependencies:  ## Install test dependencies locally. Make sure to have a virtualenv configured.
	pip install -r requirements/test.txt

test: ## Run the test suite. Make sure you run make env-start first.
	python runtests.py

help: ## Display this help text
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
