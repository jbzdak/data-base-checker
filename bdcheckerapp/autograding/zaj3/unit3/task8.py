import random
from sqlalchemy.orm import Query
from sqlalchemy.sql import Delete
from units.unit3.meta.orm import PracaDyplomowa, Tag, Student, Pracownik

__author__ = 'jb'
from sqlalchemy.exc import IntegrityError

__author__ = 'jb'

from .util import NewDatabaseTaskChecker, Zaj3TestSuite, Zaj23askChecker


class TaskChecker(Zaj23askChecker):

    task_no = 8

    display_stdout = True

    class TestSuite(Zaj3TestSuite):

        def test_can_delete_from_tag_if_db_empty(self):
            self.session.query(Student).delete()
            self.session.query(Pracownik).delete()
            self.session.flush()
            self.session.query(Tag).delete()
            self.session.flush()


        def test_drop_tag_if_student(self):
            student = self.create_student()
            self.session.add(student)
            self.session.flush()
            def fun():
                self.session.query(Tag).delete()
                self.session.flush()
            self.assertRaises(IntegrityError, fun)

        def test_drop_tag_if_praca_dyplomowa(self):
            student = self.create_student()
            self.session.add(student)
            pracownik = self.create_pracownik()
            self.session.add(pracownik)
            self.session.flush()
            pd_list, _ = self.create_praca_dyplomowa([student], [pracownik])
            for pd in pd_list:
                self.session.add(pd)
                self.session.flush()
            def fun():
                self.session.query(Tag).delete()
                self.session.flush()
            self.assertRaises(IntegrityError, fun)
