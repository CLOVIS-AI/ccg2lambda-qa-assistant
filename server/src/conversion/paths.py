import os

PATH_TO_CCG2LAMBDA = "../../../ccg2lambda"
PATH_TO_CANDC = "/app/parsers/candc-1.00"
PATH_TO_TMP = "tmp"
TEMPLATE = PATH_TO_CCG2LAMBDA + "/en/semantic_templates_en_event.yaml"
PATHS_READY = False


def test_directory(path):
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
    path = os.path.abspath(path)
    if os.path.isfile(path):
        print("Found file [", path, "]")
        return True
    else:
        print("File not found [", path, "]")
        return False


def init_paths():
    global PATHS_READY, PATH_TO_CANDC, PATH_TO_CCG2LAMBDA, TEMPLATE
    if PATHS_READY:
        print("Paths are already ready; exiting init_paths function")
        return

    print("\nSearching for the tools...")
    print("Working directory is [", os.getcwd(), "]")
    if test_file(PATH_TO_CCG2LAMBDA + "/README.md"):
        print(" › ccg2lambda is installed correctly (submodule)")

        if test_directory(PATH_TO_CCG2LAMBDA + "/candc-1.00"):
            print(" › C&C is installed correctly")
            PATH_TO_CANDC = PATH_TO_CCG2LAMBDA + "/candc-1.00"
        else:
            print(" › C&C is not installed")
            raise Exception("Couldn't find C&C. Since you installed ccg2lambda as a submodule, "
                            "check that you installed C&C correctly according to ccg2lambda's documentation.")

        if test_file(TEMPLATE):
            print(" › Found the template file")
        else:
            print(" › Template file not found")
            raise Exception("Couldn't find the template file.")
    else:
        print(" › ccg2lambda is not installed as a submodule")

        if test_directory("/app"):
            print(" › ccg2lambda is installed correctly (Docker)")
            PATH_TO_CCG2LAMBDA = "/app"
        else:
            print(" › ccg2lambda is not installed as a Docker directory")
            raise Exception("Couldn't find ccg2lambda. Tried submodule installation & Docker installation.")

        if test_directory("/app/parsers/candc-1.00"):
            print(" › C&C is installed correctly")
            PATH_TO_CANDC = "/app/parsers/candc-1.00"
        else:
            print(" › C&C is not installed")
            raise Exception("Couldn't find C&C. Expected to find it in the Docker container.")

        if test_file(PATH_TO_CCG2LAMBDA + "/en/semantic_templates_en_event.yaml"):
            print(" › Template found")
            TEMPLATE = PATH_TO_CCG2LAMBDA + "/en/semantic_templates_en_event.yaml"
        else:
            print(" › Template not found")
            raise Exception("Couldn't find the template.")
    print("Done initializing.\n")
    PATHS_READY = True
