import os
import sys

PATH_TO_CCG2LAMBDA = "../../ccg2lambda"
PATH_TO_CANDC = PATH_TO_CCG2LAMBDA + "/candc-1.00"
PATH_TO_TMP = "./tmp"
TEMPLATE = PATH_TO_CCG2LAMBDA + "/en/semantic_templates_en_event.yaml"


class ConverterNaturalToSPARQL:

    def __init__(self, sentences):
        self._sentences = sentences

    def _candc_conversion(self):
        if not os.path.isdir(PATH_TO_CANDC):
            print("Error while using candc : directory not found at " + PATH_TO_CANDC)
            print("Please ensure that ccg2lambda is correctly installed : https://github.com/mynlp/ccg2lambda")
            exit(1)

        # Converting the sentences in Jigg's XML
        cmd = "echo " + "\"" + self._sentences + "\"" + " | sed -f " + PATH_TO_CCG2LAMBDA + "/en/tokenizer.sed > " \
              + PATH_TO_TMP + "/sentences.tok;"
        os.system(cmd)

        cmd = PATH_TO_CANDC + "/bin/candc --models /path/to/candc-1.00/models --candc-printer xml --input " \
              + PATH_TO_TMP + "/sentences.tok > " + PATH_TO_TMP + "/sentences.candc.xml"
        os.system(cmd)

        cmd = "python" + PATH_TO_CCG2LAMBDA + "/en/candc2transccg.py + " + PATH_TO_TMP + "/sentences.candc.xml > " \
              + PATH_TO_TMP + "/sentences.xml"

        os.system(cmd)

    def _ccg2lambda_conversion(self):
        cmd = "python " + PATH_TO_CCG2LAMBDA + "/scripts/semparse.py " + PATH_TO_TMP + "/sentences.xml " \
              + TEMPLATE + " " + PATH_TO_TMP + "/sentences.sem.xml"
        os.system(cmd)

    def Convert(self):
        if not os.path.isdir(PATH_TO_CCG2LAMBDA):
            print("ccg2lambda not found : Please install from : https://github.com/mynlp/ccg2lambda")
            sys.exit(1)

        if not os.path.isdir(PATH_TO_TMP):
            print("Creating temporary directory at :" + PATH_TO_TMP)
            os.system("mkdir " + PATH_TO_TMP)

        self._candc_conversion()
        self._ccg2lambda_conversion()


