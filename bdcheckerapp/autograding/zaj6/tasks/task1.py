# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
from datetime import datetime
from sqlalchemy.exc import IntegrityError, ProgrammingError
from bdchecker.api import NewDatabaseTaskChecker
from bdcheckerapp.autograding.zaj6.tasks.utils import Zaj6TaskChecker


class TaskChecker(NewDatabaseTaskChecker):

    display_stdout = True

    class TestSuite(Zaj6TaskChecker):

        def test_has_table_dph(self):
            self.assert_has_table("DATA_POINT_HISTORY", "Tabela \"DATA_POINT_HISTORY\" nie istnieje")

        def test_has_table_pt(self):
            self.assert_has_table("POINT_TYPE", "Tabela \"POINT_TYPE\" nie istnieje")

        def test_has_table_ds(self):
            self.assert_has_table("DATA_SOURCE", "Tabela \"DATA_SOURCE\" nie istnieje")

        def test_foreign_keys_ok(self):
            self.session.add(self.dph(point_type=1, data_source=1, value=5, date=datetime.now()))
            self.session.flush()

        def test_foreign_keys_invalid(self):
            self.session.add(self.dph(point_type=-1, data_source=-1, value=5, date=datetime.now()))

            with self.assertRaises(IntegrityError):
                self.session.flush()
