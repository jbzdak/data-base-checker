import random
from sqlalchemy.exc import IntegrityError
from .util import Zaj4askChecker, Zaj41TestSuite

class TaskChecker(Zaj4askChecker):

    task_no = 100
    display_stdout = False

    class TestSuite(Zaj41TestSuite):

        ROLLBACK = True

        @classmethod
        def setUpClass(cls):
            super().setUpClass()
            cls.load_migration()

        def test_check_has_osoba_table(self):
            self.assert_has_table("OSOBA")

        def test_check_insert_student(self):
            for _ in range(100):
                self.session.add(self.random_osoba_student())
                self.session.flush()

        def test_check_insert_pracownik(self):
            for _ in range(100):
                self.session.add(self.random_osoba_pracownik())
                self.session.flush()

        def test_check_gender_constraint_student(self):
            def test(*args):
                student = self.random_osoba_student()
                student.gender = random.randint(2, 1000)
                self.session.add(student)
                self.session.flush()
            self.assertRaises(IntegrityError, test, "Udało mi się dodać studenta z niepoprawną płcią")

        def test_check_gender_contrtaint_pracownik(self):
            def test(*args):
                student = self.random_osoba_pracownik()
                student.gender = random.randint(2, 1000)
                self.session.add(student)
                self.session.flush()
            self.assertRaises(IntegrityError, test, "Udało mi sie dodać pracownika z niepoprawną płcią")

        def test_check_status_constraint_student(self):
            def test(*args):
                os = self.random_osoba_student()
                os.status = "foobar"
                self.session.add(os)
                self.session.flush()
            self.assertRaises(IntegrityError, test, "Udało mi się dodać studenta z niepoprawnm statusem")

        def test_check_message_student(self):
            def test(*args):
                os = self.random_osoba_student()
                os.message = None
                self.session.add(os)
                self.session.flush()
            self.assertRaises(IntegrityError, test, "Udało mi się dodać studenta bez wiadomości")

        def test_check_status_student(self):
            def test(*args):
                os = self.random_osoba_student()
                os.message = None
                self.session.add(os)
                self.session.flush()
            self.assertRaises(IntegrityError, test, "Udało mi się dodać studenta bez statusu")

        def test_check_tel_no_pracownik(self):
            def test(*args):
                os = self.random_osoba_pracownik()
                os.tel_no = None
                self.session.add(os)
                self.session.flush()
            self.assertRaises(IntegrityError, test, "Udało mi się dodać pracownika bez telefonu")