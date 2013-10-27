from . import task1, task2, task3, task4, task5, task6, task7, task8

from .util import Zaj23askChecker


class TaskChecker(Zaj23askChecker):

    task_no = 9

    display_stdout = False

    class TestSuite(
        task1.TaskChecker.TestSuite,
        task2.TaskChecker.TestSuite,
        task3.TaskChecker.TestSuite,
        task4.TaskChecker.TestSuite,
        task5.TaskChecker.TestSuite,
        task6.TaskChecker.TestSuite,
        task7.TaskChecker.TestSuite,
        task8.TaskChecker.TestSuite,
        ):
        pass

