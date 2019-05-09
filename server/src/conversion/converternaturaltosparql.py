import os
import subprocess

from conversion.paths import TMP, CCG2LAMBDA, CANDC, TEMPLATE, init_paths, RTE, TEMPLATE_QA, SENTENCES_TXT


def clean_tmp_dir() -> None:
    """
    Cleans all the temporary files in the Tmp folders
    """
    if not len(os.listdir(TMP)) == 0:
        for files in os.listdir(TMP):
            os.remove(TMP + "/" + files)


def _execute_cmd(cmd: str) -> None:
    """
    Executes the cmd in shell, Raises an exception if the cmd did not go well
    :param cmd: the command
    """
    returned_output = subprocess.call(cmd, shell=True)
    __check_output(returned_output, cmd)


def __check_output(returned_output: int, cmd: str) -> None:
    """
    Checks if the returned_output is 0 and raise an exception with the output if not
    :param returned_output: the output code of the cmd
    :param cmd: the command
    """
    if not returned_output == 0:
        print("Error while converting Natural to SPARQL : " + cmd)
        print("Code error : %d", returned_output)

        raise Exception("Problem encountered while converting into SPARQL. output : " + cmd)


def _tokenizing(sentences: str) -> None:
    """
    Tokenizes the sentences using an english tokenizer
    :param sentences: the question or sentence in english to be parsed
    """
    cmd = 'echo "' + sentences + '" | sed -f ' + CCG2LAMBDA + "/en/tokenizer.sed > " \
          + TMP + "/sentences.tok;"
    _execute_cmd(cmd)


def _candc_conversion() -> None:
    """
    Converts the files in xml format after parsing them with c&c
    """
    cmd = "{0}/bin/candc --models {0}/models --candc-printer xml --input {1}/sentences.tok > {1}/sentences.candc.xml" \
        .format(CANDC, TMP)
    _execute_cmd(cmd)

    cmd = "python3 {0}/en/candc2transccg.py {1}/sentences.candc.xml > {1}/sentences.xml" \
        .format(CCG2LAMBDA, TMP)
    _execute_cmd(cmd)


def _ccg2lambda_conversion() -> None:
    """
    Converts the sentences in the file sentences.sem.xml using ccg2lambda
    """
    cmd = "python3 {0}/scripts/semparse.py {1}/sentences.xml {2} {1}/sentences.sem.xml" \
        .format(CCG2LAMBDA, TMP, TEMPLATE)
    _execute_cmd(cmd)


def visualize_semantic() -> None:
    """
    Creates a visualization of the file sentences.sem.xml as the file sentences.html
    """
    cmd = "python3 {0}/scripts/visualize.py {1}/sentences.sem.xml > {1}/sentences.html" \
        .format(CCG2LAMBDA, TMP)
    _execute_cmd(cmd)


def _execute_rte_script(text: str) -> None:
    """
    Executes the rte_en_qa.sh script from DepCCG.
    :param text: The input on which DepCCG runs.
    """
    sentences = open(SENTENCES_TXT, "w+")
    sentences.write(text)
    sentences.close()

    working_dir = os.getcwd()
    os.chdir(CCG2LAMBDA)
    result = subprocess.Popen([RTE, SENTENCES_TXT, TEMPLATE_QA], shell=False, stdout=subprocess.PIPE)
    __check_output(result.returncode, str(result.communicate()[0].decode()))
    os.chdir(working_dir)


def convert_qa(question: str) -> None:
    init_paths()

    _execute_rte_script(question)

    # TODO: Return something useful


def convert(sentences: str) -> bool:
    """
    WIP : Converts a given sentence in a SPARQL format request for wikidata using ccg2lambda

    :param sentences: a sentence in natural language in english
    :return: True if the conversion succeeded,False otherwise.
    """
    init_paths()

    # Converting the sentences in Jigg's XML
    _tokenizing(sentences)
    _candc_conversion()

    # Converting using ccg2lambda
    _ccg2lambda_conversion()

    # Create a visualization
    visualize_semantic()
    return True
