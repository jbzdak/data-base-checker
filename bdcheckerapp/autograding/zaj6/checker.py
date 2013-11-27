
import importlib
from bdchecker.glue import BaseTaskCheckerAutograder

for idx in range(1, 4):
    module = "bdcheckerapp.autograding.zaj6.tasks.task{}".format(idx)
    imported = importlib.import_module(module)
    tc = imported.TaskChecker

    class Autograder(BaseTaskCheckerAutograder):

        NAME = "zaj6task{}".format(idx)
        TaskChecker = tc
