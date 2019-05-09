# Makefile for the project

GREEN=\033[0;32m
RED=\033[0;31m
RESET=\033[0m

all: submodule-init gitlab-ci

dep:
	@echo -e "${GREEN}Checking for missing software...${RESET}"
	@which git || echo -e "${RED}ERROR: git is not installed.${RESET}"
	@which docker || echo -e "${RED}ERROR: docker is not installed.${RESET}"
	@which gitlab-runner || echo -e "${RED}ERROR: gitlab-runner is not installed.${RESET}"

docker-init: dep
	@echo -e "${GREEN}Pulling needed Docker images...${RESET}"
	sudo docker pull masashiy/ccg2lambda

submodule-init: dep
	@echo -e "${GREEN}Updating the submodules...${RESET}"
	git submodule init
	git submodule update

test-server: docker-init dep
	@echo -e "${GREEN}GitLab CI: test-server${RESET}"
	sudo gitlab-runner exec docker test-server

prepare-gitlab-ci: dep
	@echo -e "${GREEN}Preparing the environment for the GitLab CI scripts...${RESET}"
	mkdir -p /tmp/gitlab-cache

gitlab-ci: test-server
