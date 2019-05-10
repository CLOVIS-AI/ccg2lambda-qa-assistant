# Makefile for the project

SHELL := /bin/bash

GREEN=\033[0;32m
RED=\033[0;31m
RESET=\033[0m

PYTHON_VERSION=3.6
CURRENT_PYTHON:=$(shell python3 --version | cut -d ' ' -f 2)

all: submodule-init local

dep:
	@echo -e "${GREEN}Checking for missing software: basics...${RESET}"
	@which git

dep-ci: dep
	@echo -e "${GREEN}Checking for missing software: GitLab CI...${RESET}"
	@which docker
	@which gitlab-runner

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

ccg2lambda/coqlib.glob:
	@echo -e "${GREEN}Compiling the Coq templates...${RESET}"
	coqc ccg2lambda/coqlib.v

server/venv:
	@echo -e "${GREEN}Creating the virtual environnment...${RESET}"
	python3 -m venv server/venv/
	@echo -e "${GREEN}Installing dependencies (pip)...${RESET}"
	source server/venv/bin/activate; pip install -r server/requirements.txt
	source server/venv/bin/activate; pip install depccg

server/model: server/venv
	@echo -e "${GREEN}Downloading english model for DepCCG...${RESET}"
	source server/venv/bin/activate; depccg_en download
	mv server/venv/lib/python*/site-packages/depccg/models/tri_headfirst.tar.gz server/model.tar.gz
	mkdir -p server/model
	tar -xzvf server/model.tar.gz -C server/model
	mv server/model/tri_headfirst/* server/model/

ccg2lambda/candc-1.00: submodule-init
	@echo -e "${GREEN}Installing C&C...${RESET}"
	cd ccg2lambda; ./en/install_candc.sh

spacy-en: submodule-init server/venv
	@echo -e "${GREEN}Downloading the SpaCy English model...${RESET}"
	source server/venv/bin/activate; python -m spacy download en

test-server-local-unittest: submodule-init dep-py ccg2lambda/coqlib.glob server/model spacy-en
	@echo -e "${GREEN}Running unittest...${RESET}"
	source server/venv/bin/activate; cd server/src; python -m unittest discover

test-server-local-lint: submodule-init dep-py
	@echo -e "${GREEN}Linting Python code (PEP8)...${RESET}"
	source server/venv/bin/activate; pycodestyle --show-source --show-pep8 --statistics --max-line-length=120 --benchmark server/src

test-server-local: test-server-local-unittest test-server-local-lint
