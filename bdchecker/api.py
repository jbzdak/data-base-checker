from operator import itemgetter
import re
from sqlalchemy.orm import sessionmaker
from bdchecker.unit_util import get_bd_checker

__author__ = 'jb'

import uuid
import settings
from .db_utils import *
import os
import unittest
import io

import logging

logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

@contextmanager
def capture():
    import sys
    from io import StringIO
    # oldout, olderr = sys.stdout, sys.stderr
    out=[StringIO()]
    handler = logging.StreamHandler(out[0])
    logging.getLogger('sqlalchemy.engine').addHandler(handler)
    try:
        # sys.stdout, sys.stderr = out
        yield out
    finally:
        logging.getLogger('sqlalchemy.engine').removeHandler(handler)
        out[0] = out[0].getvalue()
        out[0] = re.sub(r"\\\\n", "\\n", out[0])

class BaseTaskChecker(object):

    TestSuite = None

    display_failure_cause = True

    display_stdout = False

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.args = args
        self.kwargs = kwargs

    def create_test_suite(self):
        suite = self.TestSuite
        suite.args = self.args
        suite.kwargs = self.kwargs
        return suite

    def dispose_test_suite(self, suite):
        pass

    def grade_result(self, result):
        if result.wasSuccessful():
            return True, 10
        else:
            return False, 2

    def perform_grading(self, result):
        passes, mark = self.grade_result(result)
        return passes, mark, result

    def perform_test(self):

        Suite = self.create_test_suite()

        try:
            with capture() as captured_streams:
                suite = unittest.TestLoader().loadTestsFromTestCase(Suite)
                stream = io.StringIO()
                result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)

            passes, mark, result = self.perform_grading(result)

            if not self.display_failure_cause:
                return passes, mark, ''

            if self.display_stdout:
                stream.write("=" * 30)
                stream.write("\ncaptured stdout\n")
                stream.write("=" * 30 + "\n")
                stream.write(captured_streams[0])
                stream.write("=" * 30)
                stream.write("\nend captured stdout\n")
                stream.write("=" * 30 + "\n")

            if not getattr(self.data_package, 'uses_versioned_api', False):
                stream.write("\n\n")
                stream.write("=" * 30)
                stream.write("\nPobierz nową wersję oprogramowania "
                             "do sprawdzania zadań ze strony: "
                             "https://bitbucket.org/jbzdak/bazy_danych_checker")

            stream.seek(0)
            return passes, mark, stream.read()
        except Exception as e:
            logging.exception("While executing tests")
        finally:
            self.dispose_test_suite(Suite)


class DatabaseTaskChecker(BaseTaskChecker):

    engine = None

    def create_test_suite(self):
        suite = super(DatabaseTaskChecker, self).create_test_suite()
        suite.engine = self.engine
        suite.session = sessionmaker(bind=self.engine)()
        return suite

    def dispose_test_suite(self, suite):
        suite.session.close()


class NewDatabaseTaskChecker(BaseTaskChecker):

    ECHO = False
    DISPOSE = True

    def create_test_suite(self):
        self.db_name = str(uuid.uuid4())
        self.db_pass = self.db_name
        create_role(self.db_name, self.db_pass)
        create_database(self.db_name, self.db_name)
        self.engine = settings.create_engine_for(self.db_name,
                                                 self.db_pass, self.db_name,
                                                 self.ECHO)

        suite = super().create_test_suite()

        suite.db_name = self.db_name
        suite.engine = self.engine

        return suite

    def dispose_test_suite(self, suite):

        self.engine.dispose()
        if self.DISPOSE:
            try:
                drop_database(self.db_name)
            finally:
                drop_role(self.db_name)

        return


class BDTester(unittest.TestCase):
    def assertListEqual(self, list1, list2, msg=None):
        if max(len(list1), len(list2)) >= 100:
            self.assertTrue(list1 == list2, msg)
        super(BDTester, self).assertListEqual(list1, list2, msg)

class SessionTest(BDTester):

    ROLLBACK = True

    HAS_TABLE_QUERY = "SELECT COUNT(*) FROM pg_tables WHERE tablename = :table"

    SELECT_TABLES_QUERY = "select tablename from pg_tables " \
                          "WHERE schemaname = 'public' ORDER BY tablename;"

    SELECT_COLUMNS_QUERY = """
SELECT column_name
    FROM information_schema.columns
    WHERE table_name = :table AND table_schema=:schema
    ORDER BY column_name;
    """

    def assert_has_table(self, table_name, msg = None):
        if msg is None:
            msg = u"Table {} not found".format(table_name)
        self.assertEqual(
            self.session.execute(self.HAS_TABLE_QUERY, {'table' : table_name}).scalar(), 1, msg
        )

    def assert_tables_are(self, table_list, msg=None):
        """

        :param table_list:
        :param msg:
        """
        self.assertEqual(
            list(map(itemgetter(0), self.session.execute(self.SELECT_TABLES_QUERY))),
            sorted(table_list),
            msg

        )

    def assert_table_columns(self, table, columns, msg=None, schema='public'):
        rs = self.session.execute(self.SELECT_COLUMNS_QUERY,
                                  {'table': table, 'schema': schema})
        self.assertEqual(
            list(map(itemgetter(0), rs)),
            sorted(columns),
            msg
        )

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self.session = None

    def reset_session(self):
        if self.session:
            self.session.close()
        self.session = self.sessionmaker()

    def close_session(self):
        self.session.close()
        self.session = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.sessionmaker = sessionmaker(bind=cls.engine)

    def setUp(self):
        self.reset_session()

    def tearDown(self):
        if self.ROLLBACK:
            self.session.rollback()
        else:
            self.session.commit()

        self.session.close()

