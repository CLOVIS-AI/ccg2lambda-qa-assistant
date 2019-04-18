import os
import subprocess
import sys

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

        returned_output_msg = subprocess.check_output(cmd)
        raise Exception("Problem encountered while converting into SPARQL. output : " + returned_output_msg)


def _tokenizing(sentences):
    cmd = 'echo "' + sentences + '" | sed -f ' + PATH_TO_CCG2LAMBDA + "/en/tokenizer.sed > " \
          + PATH_TO_TMP + "/sentences.tok;"
    _execute_cmd(cmd)


def _candc_conversion():
    if not os.path.isdir(PATH_TO_CANDC):
        print("Error while using candc : directory not found at " + PATH_TO_CANDC)
        print("Please ensure that ccg2lambda is correctly installed : https://github.com/mynlp/ccg2lambda")
        exit(1)

    cmd = "{0}/bin/candc --models {1}/models --candc-printer xml --input {2}/sentences.tok > {3}/sentences.candc.xml" \
        .format(PATH_TO_CANDC, PATH_TO_CANDC, PATH_TO_TMP, PATH_TO_TMP)
    _execute_cmd(cmd)

    cmd = "python {0}/en/candc2transccg.py {1}/sentences.candc.xml > {2}/sentences.xml".format(PATH_TO_CCG2LAMBDA,
                                                                                               PATH_TO_TMP, PATH_TO_TMP)
    _execute_cmd(cmd)


def _ccg2lambda_conversion():
    cmd = "python {0}/scripts/semparse.py {1}/sentences.xml {2} {3}/sentences.sem.xml".format(PATH_TO_CCG2LAMBDA,
                                                                                              PATH_TO_TMP, TEMPLATE,
                                                                                              PATH_TO_TMP)
    _execute_cmd(cmd)


def visualize_semantic():
    cmd = "python {0}/scripts/visualize.py {1}/sentences.sem.xml > {2}/sentences.html".format(PATH_TO_CCG2LAMBDA,
                                                                                              PATH_TO_TMP, PATH_TO_TMP)
    _execute_cmd(cmd)


def convert(sentences) -> bool:
    _setup_checker()

    try:
        # Converting the sentences in Jigg's XML
        _tokenizing(sentences)
        _candc_conversion()

        # Converting using ccg2lambda
        _ccg2lambda_conversion()

        # Create a visualization
        visualize_semantic()
    except Exception as error:
        print(error)
        return False
    return True

