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
    global PATHS_READY, TEMPLATE
    if PATHS_READY:
        print("Paths are already ready; exiting init_paths function")
        return

    print("\nSearching for the tools...")
    print("Working directory is [", os.getcwd(), "]")
    print("Project root is [", PROJECT_ROOT, "]")
    print("Server project root is [", SERVER_ROOT, "]")

    if test_directory(PROJECT_ROOT):
        print(" › Found the project root")
    else:
        print(" › Cannot find the project root!")

    if test_directory(SERVER_ROOT):
        print(" › Found the server root")
    else:
        print(" › Cannot find the server root!")

    if test_file(TEMPLATE):
        print(" › Found the template file")
    else:
        print(" › Template file not found")
        raise Exception("Couldn't find the template file.")

    print("Done initializing.\n")
    PATHS_READY = True
