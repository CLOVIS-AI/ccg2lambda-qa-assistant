# ccg2lambda QA Assistant

## Introduction

The goal of this project is to setup a pipeline to unify the ccg2lambda project in a single application.

Especially, this project will make it possible to use a single UI to ask a question, and get an answer back.

Here is a simplified version of the pipeline:

 1. The user writes a sentence in the UI (this project)
 1. The sentence is translated into CCG (by C&C or depccg)
 1. The result is translated into a logical formula (by ccg2lambda)
 1. The formula is parsed into Python objects (by nltk)
 1. The formula is translated into a SPARQL query (this project)
 1. The query is executed, the results are parsed back to text (this project)
 1. The result is displayed to the user in the UI (this project)

## Installation & usage

First, clone the project.

### Mandatory dependencies

You will need to install the following dependencies, all of which are Free and Open Source (FOSS). This project is based on [ccg2lambda](https://github.com/mynlp/ccg2lambda), which at the current time of writing is not compatible with Windows; therefore, we are not compatible with Windows systems either.

 - `python` (3.6 or higher) In particular, the project will use the Python version linked as '`python3`' on your path.
   - [Debian/Ubuntu package](https://packages.debian.org/stable/python3) Warning: at the time of writing this, the package is not up-to-date on Debian.
   - [Arch extra package](https://www.archlinux.org/packages/extra/x86_64/python/) is up-to-date
 - `git` is required because of the use of Git submodules.
   - [Debian/Ubuntu package](https://packages.debian.org/stable/git) is up-to-date
   - [Arch extra package](https://www.archlinux.org/packages/extra/x86_64/git/) is up-to-date
 - `coq` is required by ccg2lambda.
   - [Debian/Ubuntu package](https://packages.debian.org/stable/coq) is up-to-date
   - [Arch community package](https://www.archlinux.org/packages/community/x86_64/coq/) is up-to-date
 - `make`
   - [Debian/Ubuntu package](https://packages.debian.org/stable/make) is up-to-date
   - [Arch core package](https://www.archlinux.org/packages/core/x86_64/make/) is up-to-date

### Optional dependencies: GitLab CI

This project is integrated with GitLab's Continuous Integration tools. To run the pipeline on your computer, you will need the following dependencies:

 - `docker` to run the containers.
   - [Install on Debian](https://docs.docker.com/install/linux/docker-ce/debian/#install-docker-ce)
   - [Install on Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-docker-ce)
   - [Arch community package](https://www.archlinux.org/packages/community/x86_64/docker/)
 - `gitlab-runner` to run the CI suites.
   - [Install on Debian, Ubuntu, Mint, RHEL, CentOS, Fedora](https://docs.gitlab.com/runner/install/linux-repository.html#installing-the-runner)
   - [Arch community package](https://www.archlinux.org/packages/community/x86_64/gitlab-runner/)

### How to use the Makefile

This project is built around a Makefile, that handles every step of the building.

The Makefile will take care of installing the rest of the dependencies, and of compiling everything.

The main targets are:

 - `local` (by default) to compile & run the test suites locally
 - `gitlab-ci` to run the GitLab CI suites locally

Both require a working internet access (HTTPS & SSH).

For example: `make local gitlab-ci` will:
 - Download and update ccg2lambda
 - Compile the Coq library
 - Create the Python virtual environment
 - Download the models used by spaCy
 - Download the Python requirements (spaCy, DepCCG, Wikipedia...)
 - Install C&C
 - Run the unit tests of the project
 - And do everything again in the GitLab CI container
 - etc.

In particular, the Makefile is crafted to not do useless steps: all the downloads will not happen if the files are already downloaded, the requirements are only downloaded if they are not already, the library is only compiled if it's not already, etc. Therefore, it's much more efficient to always use the Makefile rather than try to do things by hand.

## What does this project do?

This project is split into multiple subprojects:

 - `server` is the main project. It also includes a simple Command Line Interface (CLI) for the project. [More information](server/README.md)
 - `google-assistant` handles the integration of the project into the Google Assistant. [More information](google-assistant/README.md)
 - `web` handles the integration of the project with a web interface. [More information](web/README.md)

For additional information on how to setup the different subprojects, read their README.md (linked above).