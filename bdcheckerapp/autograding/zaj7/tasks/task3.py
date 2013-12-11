# -*- coding: utf-8 -*-
from datetime import datetime, timedelta, date, time
import random

from sqlalchemy.exc import IntegrityError, ProgrammingError
from bdchecker.api import NewDatabaseTaskChecker
from bdcheckerapp.autograding.zaj6.tasks.utils import random_point_type, random_data_source
from .utils import Zaj7TaskChecker
from .task2 import TaskChecker as t2

class TaskChecker(NewDatabaseTaskChecker):

    display_stdout = True

    class TestSuite(t2.TestSuite):

        _tested_object = Zaj7TaskChecker.dpd
