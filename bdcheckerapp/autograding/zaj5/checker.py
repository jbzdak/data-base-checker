
import importlib
from bdchecker.glue import BaseTaskCheckerAutograder

for idx in range(1, 2):
    module = "bdcheckerapp.autograding.zaj5.unit5.task{}".format(idx)
    imported = importlib.import_module(module)
    tc = imported.TaskChecker

    class Autograder(BaseTaskCheckerAutograder):

        NAME = "zaj5task{}".format(idx)
        TaskChecker = tc
