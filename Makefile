# Makefile for the project

SHELL := /bin/bash

GREEN=\033[0;32m
RED=\033[0;31m
RESET=\033[0m

PYTHON_VERSION=3.6
CURRENT_PYTHON:=$(shell python3 --version | cut -d ' ' -f 2)

.PHONY: all
all: ccg2lambda local

.PHONY: dep
dep:
	@echo -e "${GREEN}Checking for missing software: basics...${RESET}"
	@which git

.PHONY: dep-ci
dep-ci: dep
	@echo -e "${GREEN}Checking for missing software: GitLab CI...${RESET}"
	@which docker
	@which gitlab-runner

.PHONY: dep-py
dep-py: dep
	@echo -e "${GREEN}Checking for missing software: Python tests...${RESET}"
	@which python3
	@python -c "from distutils.version import StrictVersion; print(StrictVersion('${CURRENT_PYTHON}') > StrictVersion('${PYTHON_VERSION}'))" | grep True || echo -e "${RED}Your version is too low, should at least use Python ${PYTHON_VERSION}.${RESET}"
	@which coqc

.PHONY: docker-init
docker-init: dep-ci
	@echo -e "${GREEN}Pulling needed Docker images...${RESET}"
	sudo docker pull masashiy/ccg2lambda

.PHONY: ccg2lambda
ccg2lambda: .gitmodules | dep
	# Tests if the submodule has been updated (new path, new sha1, missing)
	@if git submodule status | egrep -q '^[-]|^[+]' ; then \
    	echo -e "${GREEN}Updating the submodules...${RESET}"; \
    	echo "git submodule update --init"; \
        git submodule update --init; \
    fi

.PHONY: test-server-ci
test-server-ci: docker-init | dep
	@echo -e "${GREEN}GitLab CI: test-server${RESET}"
	sudo gitlab-runner exec docker test-server

.PHONY: gitlab-ci
gitlab-ci: test-server-ci

.PHONY: local
local: test-server-local

ccg2lambda/coqlib.glob: ccg2lambda/coqlib.v | ccg2lambda
	@echo -e "${GREEN}Compiling the Coq templates...${RESET}"
	coqc ccg2lambda/coqlib.v

server/venv:
	@echo -e "${GREEN}Creating the virtual environnment...${RESET}"
	python3 -m venv server/venv/

python-requirements: server/venv server/requirements.txt
	@echo -e "${GREEN}Installing dependencies (pip)...${RESET}"
	source server/venv/bin/activate; pip install --upgrade pip
	source server/venv/bin/activate; pip install -r server/requirements.txt
	source server/venv/bin/activate; pip install depccg
	touch python-requirements

server/model: server/venv | python-requirements
	@echo -e "${GREEN}Downloading english model for DepCCG...${RESET}"
	source server/venv/bin/activate; depccg_en download
	mv server/venv/lib/python*/site-packages/depccg/models/tri_headfirst.tar.gz server/model.tar.gz
	mkdir -p server/model
	tar -xzvf server/model.tar.gz -C server/model
	mv server/model/tri_headfirst/* server/model/

ccg2lambda/candc-1.00: ccg2lambda/en/install_candc.sh | ccg2lambda
	@echo -e "${GREEN}Installing C&C...${RESET}"
	cd ccg2lambda; ./en/install_candc.sh

.PHONY: spacy-en
spacy-en: ccg2lambda server/venv python-requirements
	@echo -e "${GREEN}Downloading the SpaCy English model...${RESET}"
	source server/venv/bin/activate; python -m spacy download en

.PHONY: test-server-local-unittest
test-server-local-unittest: ccg2lambda dep-py ccg2lambda/coqlib.glob server/model spacy-en python-requirements
	@echo -e "${GREEN}Running unittest...${RESET}"
	source server/venv/bin/activate; cd server/src; python -m unittest discover

.PHONY: test-server-local-lint
test-server-local-lint: ccg2lambda dep-py python-requirements
	@echo -e "${GREEN}Linting Python code (PEP8)...${RESET}"
	source server/venv/bin/activate; pycodestyle --show-source --show-pep8 --statistics --max-line-length=120 --benchmark server/src

.PHONY: test-server-local
test-server-local: test-server-local-unittest test-server-local-lint
