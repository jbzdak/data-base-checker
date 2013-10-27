from sqlalchemy.exc import IntegrityError

__author__ = 'jb'

from .util import NewDatabaseTaskChecker, Zaj3TestSuite, Zaj23askChecker


class TaskChecker(Zaj23askChecker):

    task_no = 3

    display_stdout = True

    class TestSuite(Zaj3TestSuite):

        def test_create_students(self):
            for _ in range(3):
                st = self.create_student()
                self.session.add(st)
                self.session.flush()

        def test_empty_name(self):
            def fun():
                student = self.create_student()
                student.name = None
                self.session.add(student)
                self.session.flush()
            self.assertRaises(IntegrityError, fun)

        def test_empty_surname(self):
            def fun():
                student = self.create_student()
                student.surname = None
                self.session.add(student)
                self.session.flush()
            self.assertRaises(IntegrityError, fun)


        def test_empty_message(self):
            def fun():
                student = self.create_student()
                student.message = None
                self.session.add(student)
                self.session.flush()
            self.assertRaises(IntegrityError, fun)

        def test_gender(self):
            for ii in range(2, 10):
                def fun():
                    student = self.create_student()
                    student.gender = ii
                    self.session.add(student)
                    self.session.flush()
                self.assertRaises(IntegrityError, fun)
                self.session.rollback()

        def test_status_fk(self):
            def fun():
                student = self.create_student()
                student.status = "foobaz"
                self.session.add(student)
                self.session.flush()
            self.assertRaises(IntegrityError, fun)




