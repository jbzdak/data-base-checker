# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
from datetime import datetime, timedelta, date, time
import random

from sqlalchemy.exc import IntegrityError, ProgrammingError
from bdchecker.api import NewDatabaseTaskChecker
from bdcheckerapp.autograding.zaj6.tasks.utils import random_point_type, random_data_source
from .utils import Zaj7TaskChecker


class TaskChecker(NewDatabaseTaskChecker):

    display_stdout = True

    class TestSuite(Zaj7TaskChecker):

        _tested_object = Zaj7TaskChecker.dpdv

        def setUp(self):
            super().setUp()
            self.session.execute("TRUNCATE \"DATA_POINT_HISTORY\";")


        def test_insert_single_row(self):
            meas_date  =  datetime.now()
            data_point = self.dphc(point_type=random_point_type(self.session),
                                  data_source=random_data_source(self.session), value=5,
                                  date=meas_date)
            self.session.add(data_point)
            self.session.flush()
            data = list(self.session.query(self._tested_object))
            self.assertEqual(len(data), 1)
            item = data[0]
            self.assertEqual(data_point.point_type, item.point_type)
            self.assertEqual(data_point.data_source, item.data_source)
            self.assertEqual(meas_date.date(), item.date.date())
            self.assertEqual(1, item.aggregated)
            self.assertEqual(5, item.value)

        def test_insert_many_rows(self, pt=None, ds=None, value=None, do_checks=True, base_date=None):

            if base_date is None:
                base_date = date.today()

            meas_date  =  datetime.combine(base_date, time())

            if pt is None:
                pt = random_point_type(self.session)
            if ds is None:
                ds = random_data_source(self.session)
            if value is None:
                value = 5

            for ii in range(200):
                dp = self.dphc(point_type=pt,
                                  data_source=ds, value=value,
                                  date=meas_date + timedelta(minutes=ii)*5)
                self.session.add(dp)
            self.session.flush()

            if do_checks:
                data = list(self.session.query(self._tested_object))
                self.assertEqual(len(data), 1)
                item = data[0]
                self.assertEqual(pt, item.point_type)
                self.assertEqual(ds, item.data_source)
                self.assertEqual(meas_date.date(), item.date.date())
                self.assertEqual(200, item.aggregated)
                self.assertEqual(value, item.value)

        def test_multiple_datasets(self):

            self.test_insert_many_rows(1, 1, 5, do_checks=False)
            self.test_insert_many_rows(2, 1, 7, do_checks=False)

            data = list(self.session.query(self._tested_object))
            self.assertEqual(len(data), 2)
            item1 = filter(lambda x: x.point_type == 1, data).__next__()
            item2 = filter(lambda x: x.point_type == 2, data).__next__()

            self.assertEqual(item1.value, 5)
            self.assertEqual(item2.value, 7)

        def test_averaging(self):

            meas_date  =  datetime.combine(date.today(), time())

            pt = random_point_type(self.session)
            ds = random_data_source(self.session)

            values = []

            for ii in range(200):

                v = random.randint(0, 10)

                dp = self.dphc(point_type=pt,
                                  data_source=ds, value=v,
                                  date=meas_date + timedelta(minutes=ii)*5)
                values.append(v)
                self.session.add(dp)

            self.session.flush()

            data = list(self.session.query(self._tested_object))
            self.assertEqual(len(data), 1)
            item = data[0]

            mean = sum(values)/len(values)
            self.assertAlmostEqual(mean, item.value, places=2)

        def test_many_days(self):

            pt = random_point_type(self.session)
            ds = random_data_source(self.session)


            for day in range(1, 16):

                d = date(2012, 12, day)

                self.test_insert_many_rows(pt,ds, value=d.day, do_checks=False, base_date=d)

            self.session.flush()

            data = list(self.session.query(self._tested_object))
            self.assertEqual(len(data), 15)

            for row in data:
                self.assertAlmostEqual(row.date.day, row.value)





