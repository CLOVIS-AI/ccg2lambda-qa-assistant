import os
import subprocess

from conversion.paths import TMP, CCG2LAMBDA, CANDC, TEMPLATE, init_paths, RTE


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
    returned_output = subprocess.call(cmd, shell = True)
    _output_checker(returned_output, cmd)


def _output_checker(returned_output: int, cmd: str) -> None:
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


def _create_txt_document(text: str) -> None:
    cmd = "echo {0} > {1}/sentences.txt" \
        .format(text, TMP)
    _execute_cmd(cmd)


def _execute_rte_script() -> None:
    TMP_PATH_FROM_CCG = "../server/src/tmp"
    RES_PATH_FROM_CCG = "../server/res"
    cmd = "cd {0} && /en/rte_en_qa.sh {1}/sentences.txt {2}/parser/semantic_templates_en_qa.yaml" \
        .format(CCG2LAMBDA, TMP_PATH_FROM_CCG, RES_PATH_FROM_CCG)
    _execute_cmd(cmd)


def convertQA(question: str) -> None:
    init_paths()

    _create_txt_document(question)

    _execute_rte_script()


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
