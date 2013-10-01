# -*- coding: utf-8 -*-
from configparser import ConfigParser
from grading.autograding import Autograder


class ConfigFileBackedAudograder(Autograder):

    CONFIG_FILE = None

    def __init__(self):
        self.cf = ConfigParser()
        self.cf.read(self.CONFIG_FILE)

    @property
    def description(self):
        return self.cf.get(self.NAME, "description", fallback=self.DESCRIPTION)


