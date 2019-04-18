import os
import subprocess

PATH_TO_CCG2LAMBDA = "../../ccg2lambda"
PATH_TO_CANDC = "/app/parsers/" + "/candc-1.00"
PATH_TO_TMP = "tmp"
TEMPLATE = PATH_TO_CCG2LAMBDA + "/en/semantic_templates_en_event.yaml"


def _tmp_check():
    """
    Checks if the Tmp directory exists, creates it if not
    """
    if not os.path.isdir(PATH_TO_TMP):
        print("Creating temporary directory at :" + PATH_TO_TMP)
        os.mkdir(PATH_TO_TMP)


def cleanTmpDir():
    """
    Cleans all the temporary files in the Tmp folders
    """
    _tmp_check()

    if not len(os.listdir(PATH_TO_TMP)) == 0:
        for files in os.listdir(PATH_TO_TMP):
            os.remove(PATH_TO_TMP + "/" + files)


def _execute_cmd(cmd):
    """
    Executes the cmd in shell, Raises an exception if the cmd did not go well
    :param cmd: the command
    """
    returned_output = subprocess.call(cmd, shell = True)
    _output_checker(returned_output, cmd)


def _setup_checker():
    """
    Checks if everything is correctly installed
    """
    if not os.path.isdir(PATH_TO_CCG2LAMBDA):
        raise Exception(
            "ccg2lambda not found : Please install from : https://github.com/mynlp/ccg2lambda or follow the "
            "README.md on : https://github.com/CLOVIS-AI/ccg2lambda-qa-assistant")
    _tmp_check()


def _output_checker(returned_output, cmd):
    """
    Checks if the returned_output is 0 and raise an exception with the output if not
    :param returned_output: the output code of the cmd
    :param cmd: the command
    """
    if not returned_output == 0:
        print("Error while converting Natural to SPARQL : " + cmd)
        print("Code error : %d", returned_output)

        returned_output_msg = subprocess.check_output(cmd)
        raise Exception("Problem encountered while converting into SPARQL. output : " + returned_output_msg)


def _tokenizing(sentences):
    """
    Tokenizes the sentences using an english tokenizer
    :param sentences: the question or sentence in english to be parsed
    """
    cmd = 'echo "' + sentences + '" | sed -f ' + PATH_TO_CCG2LAMBDA + "/en/tokenizer.sed > " \
          + PATH_TO_TMP + "/sentences.tok;"
    _execute_cmd(cmd)


def _candc_conversion():
    """
    Converts the files in xml format after parsing them with c&c
    """
    if not os.path.isdir(PATH_TO_CANDC):
        print("Please ensure that ccg2lambda is correctly installed : https://github.com/mynlp/ccg2lambda")
        raise Exception(("Error while using candc : directory not found at " + PATH_TO_CANDC))

    cmd = "{0}/bin/candc --models {1}/models --candc-printer xml --input {2}/sentences.tok > {3}/sentences.candc.xml" \
        .format(PATH_TO_CANDC, PATH_TO_CANDC, PATH_TO_TMP, PATH_TO_TMP)
    _execute_cmd(cmd)

    cmd = "python {0}/en/candc2transccg.py {1}/sentences.candc.xml > {2}/sentences.xml".format(PATH_TO_CCG2LAMBDA,
                                                                                               PATH_TO_TMP, PATH_TO_TMP)
    _execute_cmd(cmd)


def _ccg2lambda_conversion():
    """
    Converts the sentences in the file sentences.sem.xml using ccg2lambda
    """
    cmd = "python {0}/scripts/semparse.py {1}/sentences.xml {2} {3}/sentences.sem.xml".format(PATH_TO_CCG2LAMBDA,
                                                                                              PATH_TO_TMP, TEMPLATE,
                                                                                              PATH_TO_TMP)
    _execute_cmd(cmd)


def visualize_semantic():
    """
    Creates a visualization of the file sentences.sem.xml as the file sentences.html
    """
    cmd = "python {0}/scripts/visualize.py {1}/sentences.sem.xml > {2}/sentences.html".format(PATH_TO_CCG2LAMBDA,
                                                                                              PATH_TO_TMP, PATH_TO_TMP)
    _execute_cmd(cmd)


def convert(sentences) -> bool:
    """
    WIP : Converts a given sentence in a SPARQL format request for wikidata using ccg2lambda

    :param sentences: a sentence in natural language in english
    :return: True if the conversion succeeded,False otherwise.
    """
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
