
from sqlalchemy.exc import IntegrityError
from .util import Zaj3TestSuite, Zaj23askChecker


class TaskChecker(Zaj23askChecker):

    task_no = 5

    display_stdout = True

    class TestSuite(Zaj3TestSuite):


        def test_create_employees(self):
            for _ in range(5):
                st = self.create_pracownik()
                self.session.add(st)
                self.session.flush()

        def test_empty_name(self):
            def fun():
                student = self.create_pracownik()
                student.name = None
                self.session.add(student)
                self.session.flush()
            self.assertRaises(IntegrityError, fun)

        def test_empty_surname(self):
            def fun():
                student = self.create_pracownik()
                student.surname = None
                self.session.add(student)
                self.session.flush()
            self.assertRaises(IntegrityError, fun)



        def test_gender(self):
            for ii in range(2, 10):
                def fun():
                    student = self.create_pracownik()
                    student.gender = ii
                    self.session.add(student)
                    self.session.flush()
                self.assertRaises(IntegrityError, fun)
                self.session.rollback()

        def test_tel_no_1(self):
            def fun():
                student = self.create_pracownik()
                student.tel_no = "foobar"
                self.session.add(student)
                self.session.flush()
            self.assertRaises(IntegrityError, fun)

        def test_tel_no_2(self):
            def fun():
                student = self.create_pracownik()
                student.tel_no = "22 432-12-12"
                self.session.add(student)
                self.session.flush()
            self.assertRaises(IntegrityError, fun)

        def test_tel_no_3(self):
            def fun():
                student = self.create_pracownik()
                student.tel_no = "22 4321-2-12"
                self.session.add(student)
                self.session.flush()
            self.assertRaises(IntegrityError, fun)

        def test_tel_no_4(self):
            def fun():
                student = self.create_pracownik()
                student.tel_no = "22 432-AA-BB"
                self.session.add(student)
                self.session.flush()
            self.assertRaises(IntegrityError, fun)

        def test_tel_no_5(self):
            def fun():
                student = self.create_pracownik()
                student.tel_no = "22234-12-12"
                self.session.add(student)
                self.session.flush()
            self.assertRaises(IntegrityError, fun)