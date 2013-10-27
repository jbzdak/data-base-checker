import hashlib
from sqlalchemy.sql.expression import text

__author__ = 'jb'

import importlib
from .database.functions import check_password
from .db_utils import  connect
from .database import functions


def get_bd_checker(unit_no, task_no):
    module = importlib.import_module("units.unit{}.task{}".format(unit_no,
                                                                  task_no))
    return getattr(module, "TaskChecker")

DETAIL_QUERY = """
SELECT unit, task, MAX(grade)/2 AS task_grade FROM grade AS gsubs
    WHERE gsubs.user_id = :user_id GROUP BY unit, task ORDER BY unit, task
"""

GROSS_QUERY = """
SELECT unit, SUM(task_grade) FROM (
    SELECT task, unit, MAX(grade)/2 AS task_grade FROM grade AS gsubs
        WHERE gsubs.user_id = :user_id GROUP BY unit, task
        ORDER BY unit, task
    ) AS grade_select
    GROUP BY unit
"""

def _wrap_rs(rs):
    return [
        "\t".join([str(cell) for cell in row]) for row in rs
    ]


def get_results(settings, user_id):
    with connect(settings.ENGINE) as conn:
        return _wrap_rs(
            conn.execute(text(DETAIL_QUERY),  user_id=user_id)
        )


def get_results_gross(settings, user_id):
    with connect(settings.ENGINE) as conn:
        return _wrap_rs(
            conn.execute(text(GROSS_QUERY),  user_id=user_id)
        )


def execute_test_checker(data_package):

    # check_password(data_package.user_id_1, data_package.user_pass_1, data_package.unit_no)
    # check_password(data_package.user_id_2, data_package.user_pass_2, data_package.unit_no)

    CheckerClass = get_bd_checker(data_package.unit_no, data_package.task_no)
    checker = CheckerClass(data_package)
    return checker.perform_test()


class Executor(object):

    def __init__(self, settings):
        self.instance = settings.INSTANCE
        self.settings = settings

    def execute_test_checker(self, package, uses_versioned_api=False):

        from bdchecker.api import DataPackage
        pack = DataPackage(**package)
        pack.instance = self.instance

        if not pack.unit_no in self.settings.ALLOWED_UNITS:
            raise ValueError("Nie można jeszcze wykonać zdań z zajęć {}".format(pack.unit_no))

        pack.uses_versioned_api = uses_versioned_api

        return execute_test_checker(pack)

    def set_password(self, user_id, supervisor_password, new_password):

        functions.set_password(user_id, supervisor_password, new_password)
        return None

    def show_marks(self, user_id, password, details = False):
        check_password(user_id, password)
        if details:
            return get_results(self.settings, user_id)
        return get_results_gross(self.settings, user_id)

    def version(self):
        return self.settings.VERSION

