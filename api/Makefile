.ONESHELL:
SHELL := /bin/bash

.SILENT:

%:
	@:

export SERVICE_NAME=eventhub-api

ifndef PROMETHEUS_MULTIPROC_DIR
	export PROMETHEUS_MULTIPROC_DIR=${PWD}/.prometheus
endif

ifndef SERVICE_PORT
	export SERVICE_PORT=5000
endif

ifndef PROMETHEUS_PORT
	export PROMETHEUS_PORT=8001
endif

DEFAULT_GOAL := help
.PHONY: help
help:
	awk 'BEGIN {FS = ":.*?## "} /^[%a-zA-Z0-9_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: install
install: ## Create poetry environment and install all dependencies.
	poetry config virtualenvs.in-project true --local
	poetry env use 3.11
	poetry install

.PHONY: style-check
style-check: ## Run style checks.
	printf "Style Checking with Flake8, Black and Isort\n"
	poetry run black --check .
	poetry run flake8 .
	poetry run isort --check-only --diff .

.PHONY: static-check
static-check: ## Run strict typing checks.
	printf "Static Checking with Mypy\n"
	poetry run mypy .

.PHONY: restyle
restyle: ## Reformat code with black and isort.
	poetry run black .
	poetry run isort --atomic .

.PHONY: clean-prometheus-dir
clean-prometheus-dir: ## Clean Prometheus multiprocess directory, if exists.
	mkdir -p $(PROMETHEUS_MULTIPROC_DIR)
	rm -rf $(PROMETHEUS_MULTIPROC_DIR)/*

.PHONY: tests
tests: clean-prometheus-dir ## Run tests.
	printf "Tests with Pytest\n"
ifeq (plain, $(filter plain,$(MAKECMDGOALS)))
	PYTHONPATH=. pytest tests -s
else
	PYTHONPATH=. poetry run pytest -s
endif

.PHONY: battery
battery: style-check static-check tests ## Run all checks and tests
	printf "\nPassed all checks and tests...\n"

.PHONY: run
run: clean-prometheus-dir ## Run service with dev configuration.
ifeq (plain, $(filter plain,$(MAKECMDGOALS)))
	$(SHELL) serve.sh
else
	poetry run $(SHELL) serve.sh
endif
