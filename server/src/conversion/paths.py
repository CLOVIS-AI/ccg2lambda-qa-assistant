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

CCG2LAMBDA = "../../../ccg2lambda"
CANDC = "/app/parsers/candc-1.00"
TMP = "tmp"
TEMPLATE = "../res/parser/semantic_templates_en_qa.yaml"
PATHS_READY = False


def test_directory(path):
    """
    Checks if a directory exists, and is not empty.
    :param path: The path to that directory (absolute or relative)
    :return: True if the directory exists & is not empty, False otherwise.
    """
    path = os.path.abspath(path)
    if os.path.isdir(path):
        if len(os.listdir(path)) > 0:
            print("Found [", path, "], and it is not empty.")
            return True
        else:
            print("Found [", path, "], but it is empty!")
            return False
    else:
        print("Directory not found [", path, "]")
        return False


def test_file(path):
    """
    Checks if a file exists.
    :param path: The path to that file (absolute or relative)
    :return: True if the file exists, False otherwise.
    """
    path = os.path.abspath(path)
    if os.path.isfile(path):
        print("Found file [", path, "]")
        return True
    else:
        print("File not found [", path, "]")
        return False


def init_paths():
    """
    Searches for the tools in known location and finds their paths,
    or reports if they are missing.
    Searches in the submodule or in a Docker container.
    """
    global PATHS_READY, CANDC, CCG2LAMBDA, TEMPLATE
    if PATHS_READY:
        print("Paths are already ready; exiting init_paths function")
        return

    print("\nSearching for the tools...")
    print("Working directory is [", os.getcwd(), "]")
    if test_file(CCG2LAMBDA + "/README.md"):
        print(" › ccg2lambda is installed correctly (submodule)")

        if test_directory(CCG2LAMBDA + "/candc-1.00"):
            print(" › C&C is installed correctly")
            CANDC = CCG2LAMBDA + "/candc-1.00"
        else:
            print(" › C&C is not installed")
            raise Exception("Couldn't find C&C. Since you installed ccg2lambda as a submodule, "
                            "check that you installed C&C correctly according to ccg2lambda's documentation.")
    else:
        print(" › ccg2lambda is not installed as a submodule")

        if test_directory("/app"):
            print(" › ccg2lambda is installed correctly (Docker)")
            CCG2LAMBDA = "/app"
        else:
            print(" › ccg2lambda is not installed as a Docker directory")
            raise Exception("Couldn't find ccg2lambda. Tried submodule installation & Docker installation.")

        if test_directory("/app/parsers/candc-1.00"):
            print(" › C&C is installed correctly")
            CANDC = "/app/parsers/candc-1.00"
        else:
            print(" › C&C is not installed")
            raise Exception("Couldn't find C&C. Expected to find it in the Docker container.")

    if test_file(TEMPLATE):
        print(" › Found the template file")
    else:
        print(" › Template file not found")
        raise Exception("Couldn't find the template file.")

    print("Done initializing.\n")
    PATHS_READY = True
