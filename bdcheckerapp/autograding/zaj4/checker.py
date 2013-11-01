# -*- coding: utf-8 -*-

import importlib
from bdchecker.glue import BaseTaskCheckerAutograder

tasks = [100, 101, 102, 103, 104, 200, 201, 202, 203]

for idx in tasks:
    module = "bdcheckerapp.autograding.zaj4.unit4.task{}".format(idx)
    imported = importlib.import_module(module)
    tc = imported.TaskChecker

    class Autograder(BaseTaskCheckerAutograder):

        NAME = "zaj3task{}".format(idx)
        TaskChecker = tc
