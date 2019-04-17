import subprocess
import sys
import os

PATH_TO_CCG2LAMBDA = "../../ccg2lambda"
PATH_TO_CANDC = PATH_TO_CCG2LAMBDA + "/candc-1.00"
PATH_TO_TMP = "./tmp"
TEMPLATE = PATH_TO_CCG2LAMBDA + "/en/semantic_templates_en_event.yaml"


def _tmp_check():
    if not os.path.isdir(PATH_TO_TMP):
        print("Creating temporary directory at :" + PATH_TO_TMP)
        os.mkdir(PATH_TO_TMP)


def cleanTmpDir():
    _tmp_check()

    if not len(os.listdir(PATH_TO_TMP)) == 0:
        for files in os.listdir(PATH_TO_TMP):
            os.remove(PATH_TO_TMP + "/" + files)


def _execute_cmd(cmd):
    returned_output = subprocess.call(cmd, shell = True)
    _output_checker(returned_output, cmd)


def _setup_checker():
    if not os.path.isdir(PATH_TO_CCG2LAMBDA):
        print("ccg2lambda not found : Please install from : https://github.com/mynlp/ccg2lambda or follow the "
              "README.md on : https://github.com/CLOVIS-AI/ccg2lambda-qa-assistant")
        sys.exit(1)
    _tmp_check()


def _output_checker(returned_output, cmd):
    if not returned_output == 0:
        print("Error while converting Natural to SPARQL : " + cmd)
        print("Code error : %d", returned_output)
        exit(1)


def _tokenizing(sentences):
    cmd = "echo " + "\"" + sentences + "\"" + " | sed -f " + PATH_TO_CCG2LAMBDA + "/en/tokenizer.sed > " \
          + PATH_TO_TMP + "/sentences.tok;"
    _execute_cmd(cmd)


def _candc_conversion():
    if not os.path.isdir(PATH_TO_CANDC):
        print("Error while using candc : directory not found at " + PATH_TO_CANDC)
        print("Please ensure that ccg2lambda is correctly installed : https://github.com/mynlp/ccg2lambda")
        exit(1)

    cmd = PATH_TO_CANDC + "/bin/candc --models " + PATH_TO_CANDC + "/models --candc-printer xml --input " \
          + PATH_TO_TMP + "/sentences.tok > " + PATH_TO_TMP + "/sentences.candc.xml"
    _execute_cmd(cmd)

    cmd = "python " + PATH_TO_CCG2LAMBDA + "/en/candc2transccg.py " + PATH_TO_TMP + "/sentences.candc.xml > " \
          + PATH_TO_TMP + "/sentences.xml"
    _execute_cmd(cmd)


def _ccg2lambda_conversion():
    cmd = "python " + PATH_TO_CCG2LAMBDA + "/scripts/semparse.py " + PATH_TO_TMP + "/sentences.xml " \
          + TEMPLATE + " " + PATH_TO_TMP + "/sentences.sem.xml"
    _execute_cmd(cmd)


def visualize_semantic():
    cmd = "python " + PATH_TO_CCG2LAMBDA + "/scripts/visualize.py " + PATH_TO_TMP + "/sentences.sem.xml > " \
          + PATH_TO_TMP + "/sentences.html"
    _execute_cmd(cmd)


def convert(sentences):
    _setup_checker()

    # Converting the sentences in Jigg's XML
    _tokenizing(sentences)
    _candc_conversion()

    # Converting using ccg2lambda
    _ccg2lambda_conversion()

    # Create a visualization
    visualize_semantic()
