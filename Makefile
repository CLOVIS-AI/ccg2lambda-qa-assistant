# Makefile for the project

SHELL := /bin/bash

GREEN=\033[0;32m
RED=\033[0;31m
RESET=\033[0m

PYTHON_VERSION=3.6

all: submodule-init local

dep:
	@echo -e "${GREEN}Checking for missing software: basics...${RESET}"
	@which git

dep-ci: dep
	@echo -e "${GREEN}Checking for missing software: GitLab CI...${RESET}"
	@which docker
	@which gitlab-runner

dep-py: CURRENT_PYTHON:=$(shell python --version | cut -d ' ' -f 2)
dep-py: dep
	@echo -e "${GREEN}Checking for missing software: Python tests...${RESET}"
	@which python3
	@python -c "from distutils.version import StrictVersion; print(StrictVersion('${CURRENT_PYTHON}') > StrictVersion('${PYTHON_VERSION}'))" | grep True || echo -e "${RED}Your version is too low, should at least use Python ${PYTHON_VERSION}.${RESET}"
	@which coqc

docker-init: dep-ci
	@echo -e "${GREEN}Pulling needed Docker images...${RESET}"
	sudo docker pull masashiy/ccg2lambda

submodule-init: dep
	@echo -e "${GREEN}Updating the submodules...${RESET}"
	git submodule init
	git submodule update

test-server-ci: docker-init dep
	@echo -e "${GREEN}GitLab CI: test-server${RESET}"
	sudo gitlab-runner exec docker test-server

gitlab-ci: test-server-ci

local: test-server-local

coqc: ccg2lambda/coqlib.glob
	@echo -e "${GREEN}Compiling the Coq templates...${RESET}"
	coqc ccg2lambda/coqlib.v

venv: server/venv
	@echo -e "${GREEN}Creating the virtual environnment...${RESET}"
	python3 -m venv server/venv/

test-server-local: submodule-init dep-py coqc
	@echo -e "${GREEN}Activating the virtual environnment...${RESET}"
	@source server/venv/bin/activate; \
	cd server/src; \
	echo -e "${GREEN}Installing the dependencies (pip)...${RESET}"; \
	pip install -r ../requirements.txt; \
	echo -e "${GREEN}Unit tests...${RESET}"; \
	python3 -m unittest discover; \
	echo -e "${GREEN}Linting...${RESET}"; \
	pycodestyle --show-source --show-pep8 --statistics --max-line-length=120 --benchmark .;
