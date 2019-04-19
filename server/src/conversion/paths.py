import os

PATH_TO_CCG2LAMBDA = "../../../ccg2lambda"
PATH_TO_CANDC = "/app/parsers/candc-1.00"
PATH_TO_TMP = "tmp"
TEMPLATE = PATH_TO_CCG2LAMBDA + "/en/semantic_templates_en_event.yaml"
PATHS_READY = False


def init_paths():
    global PATHS_READY
    if PATHS_READY:
        print("Paths are already ready; exiting init_paths function")
        return

    print("Trying to find the different tools that are required...")
    print("Working directory is [", os.getcwd(), "]")
    if os.path.isfile(PATH_TO_CCG2LAMBDA + "/README.md"):
        print("ccg2lambda is installed as a submodule")
    else:
        print("ccg2lambda is not installed as a submodule, assuming we're in the Docker container")
    print("Done initializing.")
    PATHS_READY = True
    exit(1)
