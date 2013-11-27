# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError, ProgrammingError
from bdchecker.api import NewDatabaseTaskChecker
from bdcheckerapp.autograding.zaj6.tasks.utils import Zaj6TaskChecker


class TaskChecker(NewDatabaseTaskChecker):

    display_stdout = True

    class TestSuite(Zaj6TaskChecker):


        _tested_object = Zaj6TaskChecker.dphcv

        def test_view_1(self):
            try:
                meas_date  =  datetime.now()
                self.session.add(self.dphc(point_type=1, data_source=1, value=5, date=meas_date))
                self.session.commit()
                self.session.add(self.dphc(point_type=1, data_source=1, value=6, date=meas_date))
                self.session.commit()
                data = list(self.session.query(self._tested_object.value))
                self.assertEqual(1, len(data))
                self.assertEqual(data[0][0], 6)
            finally:
                self.session.execute("TRUNCATE \"DATA_POINT_HISTORY\";")
                self.session.execute("TRUNCATE \"DATA_POINT_CURRENT\";")
                self.session.commit()

        def test_view_2(self):

            meas_date  =  datetime.now()
            self.session.add(self.dphc(point_type=1, data_source=1, value=5, date=meas_date))
            self.session.add(self.dphc(point_type=1, data_source=405036284, value=6, date=meas_date))
            self.session.flush()
            data = list(self.session.query(self._tested_object.value))
            self.assertEqual(2, len(data))

        def test_view_3(self):

            meas_date  =  datetime.now()
            self.session.add(self.dphc(point_type=1, data_source=1, value=5, date=meas_date))
            self.session.add(self.dphc(point_type=2, data_source=1, value=6, date=meas_date))
            self.session.flush()
            data = list(self.session.query(self._tested_object.value))
            self.assertEqual(2, len(data))


        def test_view_4(self):

            meas_date  =  datetime.now()
            self.session.add(self.dphc(point_type=1, data_source=1, value=5, date=meas_date))
            self.session.add(self.dphc(point_type=2, data_source=1, value=6, date=meas_date))
            self.session.flush()
            data = list(self.session.query(self._tested_object.value))
            self.assertEqual(2, len(data))