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

PROJECT_ROOT = "../../"
SERVER_ROOT = PROJECT_ROOT + "server/"
CCG2LAMBDA = PROJECT_ROOT + "ccg2lambda"
CANDC = "/app/parsers/candc-1.00"
DEPCCG = PROJECT_ROOT + "depccg"
TMP = "tmp"
TEMPLATE = "../res/parser/simple_templates_qa.yaml"
RTE = ""
PARSER_LOCATION_FILE = ""
PATHS_READY = False


def test_directory(path, allow_empty=False):
    """
    Checks if a directory exists, and is not empty.
    :param allow_empty: Are empty directories successful or not?
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
            return allow_empty
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
    global PATHS_READY, CANDC, CCG2LAMBDA, TEMPLATE, RTE, PARSER_LOCATION_FILE
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

    if test_directory(DEPCCG):
        print(" › Found depccg")
    else:
        print(" › depccg not found")
        raise Exception("Couldn't find depccg; expected to find it as a submodule.")

    if test_directory(TMP, allow_empty=True):
        print(" › Found the temporary directory")
    else:
        print(" › Creating the temporary directory...", end='')
        os.mkdir(TMP)
        print(" Done.")

    RTE = CCG2LAMBDA + "/en/rte_en_qa.sh"
    if test_file(RTE):
        print(" › Found the rte_en_qa script")
    else:
        print(" › rte_en_qa not found")
        raise Exception("Couldn't find the rte_en_qa script.")

    PARSER_LOCATION_FILE = CCG2LAMBDA + "/en/parser_location.txt"
    print("Writing depccg's location to [", os.path.abspath(PARSER_LOCATION_FILE), "]")

    parser_location = open(PARSER_LOCATION_FILE, "w+")
    parser_location.write("depccg:" + os.path.abspath(DEPCCG))
    parser_location.close()
    if test_file(PARSER_LOCATION_FILE):
        print(" › Successfully created the parser_location file")
    else:
        print(" › parser_location not found, but I just created it!")
        raise Exception("Couldn't find the parser_location file.")

    print("Done initializing.\n")
    PATHS_READY = True
