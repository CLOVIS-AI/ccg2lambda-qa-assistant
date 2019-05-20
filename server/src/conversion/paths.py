###########################################################
#                                                         #
#      Contains the paths to the different external       #
#      tools used by this project.                        #
#                                                         #
###########################################################

import os

# Note that the paths written here are for initialization
# purpose only, and should not be used as-is; when the
# package is loaded they are updated to follow the real
# paths of the tools.
from qalogging import verbose, info, warning, error

PROJECT_ROOT: str = os.path.abspath("../../")
SERVER_ROOT: str = PROJECT_ROOT + "/server"
TEMPLATE: str = SERVER_ROOT + "/res/parser/semantic_templates_en_qa.yaml"
MODEL: str = SERVER_ROOT + "/model"

PATHS_READY = False


def test_directory(path, allow_empty=False):
    """
    Checks if a directory exists, and is not empty.
    :param allow_empty: Report a success even if the directory is empty
    :param path: The path to that directory (absolute or relative)
    :return: True if the directory exists & is not empty, False otherwise.
    """
    path = os.path.abspath(path)
    if os.path.isdir(path):
        if len(os.listdir(path)) > 0:
            verbose("Found [", path, "], and it is not empty.")
            return True
        else:
            verbose("Found [", path, "], but it is empty!")
            return allow_empty
    else:
        warning("Directory not found [", path, "]")
        return False


def test_file(path):
    """
    Checks if a file exists.
    :param path: The path to that file (absolute or relative)
    :return: True if the file exists, False otherwise.
    """
    path = os.path.abspath(path)
    if os.path.isfile(path):
        verbose("Found file [", path, "]")
        return True
    else:
        warning("File not found [", path, "]")
        return False


def init_paths():
    """
    Searches for the tools in known location and finds their paths,
    or reports if they are missing.
    Searches in the submodule or in a Docker container.
    """
    global PATHS_READY, TEMPLATE
    if PATHS_READY:
        verbose("Paths are already ready; exiting init_paths function")
        return

    info("\nSearching for the tools...")
    verbose("Working directory is [", os.getcwd(), "]")
    verbose("Project root is [", PROJECT_ROOT, "]")
    verbose("Server project root is [", SERVER_ROOT, "]")

    if test_directory(PROJECT_ROOT):
        verbose(" › Found the project root")
    else:
        error(" › Cannot find the project root!")

    if test_directory(SERVER_ROOT):
        verbose(" › Found the server root")
    else:
        error(" › Cannot find the server root!")

    if test_file(TEMPLATE):
        verbose(" › Found the template file")
    else:
        error(" › Template file not found")
        raise Exception("Couldn't find the template file.")

    verbose("Done initializing paths.\n")
    PATHS_READY = True
