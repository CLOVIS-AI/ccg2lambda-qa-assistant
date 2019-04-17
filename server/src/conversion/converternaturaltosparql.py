import subprocess
import sys
import os

PATH_TO_CCG2LAMBDA = "../../ccg2lambda"
PATH_TO_CANDC = PATH_TO_CCG2LAMBDA + "/candc-1.00"
PATH_TO_TMP = "./tmp"
TEMPLATE = PATH_TO_CCG2LAMBDA + "/en/semantic_templates_en_event.yaml"


class ConverterNaturalToSPARQL:

    def __init__(self, sentences):
        self._sentences = sentences

    def _tmp_check(self):
        if not os.path.isdir(PATH_TO_TMP):
            print("Creating temporary directory at :" + PATH_TO_TMP)
            cmd = "mkdir " + PATH_TO_TMP
            returned_output = subprocess.call(cmd, shell=True)
            self._output_checker(returned_output, cmd)

    def cleanTmpDir(self):
        self._tmp_check()

        if not len(os.listdir(PATH_TO_TMP)) == 0:
            cmd = "rm -r " + PATH_TO_TMP + "/*"
            subprocess.call(cmd, shell=True)

    def _settup_checker(self):
        if not os.path.isdir(PATH_TO_CCG2LAMBDA):
            print("ccg2lambda not found : Please install from : https://github.com/mynlp/ccg2lambda or follow the "
                  "README.md on : https://github.com/CLOVIS-AI/ccg2lambda-qa-assistant")
            sys.exit(1)

        self._tmp_check()

    def _output_checker(self, returned_output, cmd):
        if not returned_output == 0:
            print("Error while converting Natural to SPARQL : " + cmd)
            print("Code error : %d", returned_output)
            exit(1)

    def _tokenizing(self):
        cmd = "echo " + "\"" + self._sentences + "\"" + " | sed -f " + PATH_TO_CCG2LAMBDA + "/en/tokenizer.sed > " \
              + PATH_TO_TMP + "/sentences.tok;"
        returned_output = subprocess.call(cmd, shell=True)
        self._output_checker(returned_output, cmd)

    def _candc_conversion(self):
        if not os.path.isdir(PATH_TO_CANDC):
            print("Error while using candc : directory not found at " + PATH_TO_CANDC)
            print("Please ensure that ccg2lambda is correctly installed : https://github.com/mynlp/ccg2lambda")
            exit(1)

        # Converting the sentences in Jigg's XML
        self._tokenizing()

        cmd = PATH_TO_CANDC + "/bin/candc --models " + PATH_TO_CANDC + "/models --candc-printer xml --input " \
              + PATH_TO_TMP + "/sentences.tok > " + PATH_TO_TMP + "/sentences.candc.xml"
        returned_output = subprocess.call(cmd, shell=True)
        self._output_checker(returned_output, cmd)

        cmd = "python " + PATH_TO_CCG2LAMBDA + "/en/candc2transccg.py " + PATH_TO_TMP + "/sentences.candc.xml > " \
              + PATH_TO_TMP + "/sentences.xml"
        returned_output = subprocess.call(cmd, shell=True)
        self._output_checker(returned_output, cmd)

    def _ccg2lambda_conversion(self):
        cmd = "python " + PATH_TO_CCG2LAMBDA + "/scripts/semparse.py " + PATH_TO_TMP + "/sentences.xml " \
              + TEMPLATE + " " + PATH_TO_TMP + "/sentences.sem.xml"
        returned_output = subprocess.call(cmd, shell=True)
        self._output_checker(returned_output, cmd)

    def visualize_semantic(self):
        cmd = "python " + PATH_TO_CCG2LAMBDA + "/scripts/visualize.py " + PATH_TO_TMP + "/sentences.sem.xml > " \
              + PATH_TO_TMP + "/sentences.html"
        returned_output = subprocess.call(cmd, shell=True)
        self._output_checker(returned_output, cmd)

    def convert(self):
        self._candc_conversion()
        self._ccg2lambda_conversion()
        self.visualize_semantic()
