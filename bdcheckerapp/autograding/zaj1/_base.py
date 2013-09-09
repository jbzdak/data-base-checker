# coding=utf-8

from bdcheckerapp.autograding._autograding import SQLAutograder

class Zaj1BaseAutograder(SQLAutograder):

    EXPECTED_SQL = None

    def autograde(self, current_grade, model_instance):
        super(Zaj1BaseAutograder, self).autograde(current_grade, model_instance)

