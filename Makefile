# Makefile for the project

ELMO_DOWNLOAD=/tmp/elmo
PREVIOUS=$(pwd)

all: submodules elmo

submodules:
	git submodule init
	git submodule update

elmo:
	@echo "Downloading the English ELMo Model"
	@mkdir -p ${ELMO_DOWNLOAD}
	@cd ${ELMO_DOWNLOAD} \
	    && test ! -f lstm_parser_elmo_finetune.tar.gz \
	    && wget https://cl.naist.jp/~masashi-y/resources/depccg/lstm_parser_elmo_finetune.tar.gz \
	    || echo "Already downloaded, nothing to do"