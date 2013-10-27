# -*- coding: utf-8 -*-

import importlib
from bdchecker.glue import BaseTaskCheckerAutograder

for idx in range(1, 10):
    module = "bdcheckerapp.autograding.zaj3.unit3.task{}".format(idx)
    imported = importlib.import_module(module)
    tc = imported.TaskChecker

    class Autograder(BaseTaskCheckerAutograder):

        NAME = "zaj3task{}"
        TaskChecker = tc
