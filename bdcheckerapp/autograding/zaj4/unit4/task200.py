from sqlalchemy.exc import IntegrityError
from .orm.inherrits import Pracownik, Osoba
from .util import Zaj4askChecker, Zaj42TestSuite

class TaskChecker(Zaj4askChecker):

    task_no = 100
    display_stdout = False

    class TestSuite(Zaj42TestSuite):

        ROLLBACK = True

        @classmethod
        def setUpClass(cls):
            super().setUpClass()
            cls.load_migration()


        def test_create_students(self):
            for _ in range(100):
                st = self.create_student()
                self.session.add(st)
                self.session.flush()

        def test_student_has_id_after_insert(self):
            for _ in range(3):
                st = self.create_student()
                self.session.add(st)
                self.session.flush()
                self.assertIsNotNone(st.id)

                self.session.flush()

        def test_empty_name(self):
            def fun(*args):
                student = self.create_student()
                student.name = None
                self.session.add(student)
                self.session.flush()
            self.assertRaises(IntegrityError, fun, "Udało mi się wstawić studenta bez imienia")

        def test_empty_surname(self):
            def fun(*args):
                student = self.create_student()
                student.surname = None
                self.session.add(student)
                self.session.flush()
            self.assertRaises(IntegrityError, fun, "Udało mi się wstawić studenta bez nazwiska")


        def test_empty_message(self):
            def fun(*args):
                student = self.create_student()
                student.message = None
                self.session.add(student)
                self.session.flush()
            self.assertRaises(IntegrityError, fun, "Udało mi się wstawić studenta bez wiadomości")

        def test_gender(self):
            for ii in range(2, 10):
                def fun(*args):
                    student = self.create_student()
                    student.gender = ii
                    self.session.add(student)
                    self.session.flush()
                self.assertRaises(IntegrityError, fun, "Udało mi się wstaić studenta z niepoprawną płcią. ")
                self.session.rollback()

        def test_status_fk(self):
            def fun(*args):
                student = self.create_student()
                student.status = "foobaz"
                self.session.add(student)
                self.session.flush()
            self.assertRaises(IntegrityError, fun, "Udało mi się wstawić studenta z niepoprawnym statusem ")

        def test_create_employees(self):
            for _ in range(100):
                st = self.create_pracownik()
                self.session.add(st)
                self.session.flush()

        def test_pracownik_has_id_after_insert(self):
            for _ in range(3):
                st = self.create_pracownik()
                self.session.add(st)
                self.session.flush()
                self.assertIsNotNone(st.id)

        def test_empty_name_pracownik(self):
            def fun(*args):
                student = self.create_pracownik()
                student.name = None
                self.session.add(student)
                self.session.flush()
            self.assertRaises(IntegrityError, fun, "Udało mi się wstawić pracownika bez imienia")

        def test_empty_surname_pracownik(self):
            def fun(*args):
                student = self.create_pracownik()
                student.surname = None
                self.session.add(student)
                self.session.flush()
            self.assertRaises(IntegrityError, fun, "Udało mi się wstawić pracownika bez nazwiska")


        def test_gender_pracownik(self):
            for ii in range(2, 10):
                def fun(*args):
                    student = self.create_pracownik()
                    student.gender = ii
                    self.session.add(student)
                    self.session.flush()
                self.assertRaises(IntegrityError, fun, "Udao mi się stawić pracownika z niepoprawną płcią")
                self.session.rollback()

        def test_tel_no_1(self):
            def fun(*args):
                student = self.create_pracownik()
                student.tel_no = "foobar"
                self.session.add(student)
                self.session.flush()
            self.assertRaises(IntegrityError, fun, "Udało mi się wstawić pracownika z niepoprawnym telefonem")

        def test_tel_no_2(self):
            def fun(*args):
                student = self.create_pracownik()
                student.tel_no = "22 432-12-12"
                self.session.add(student)
                self.session.flush()
            self.assertRaises(IntegrityError, fun, "Udało mi się wstawić pracownika z niepoprawnym telefonem")

        def test_tel_no_3(self):
            def fun(*args):
                student = self.create_pracownik()
                student.tel_no = "22 4321-2-12"
                self.session.add(student)
                self.session.flush()
            self.assertRaises(IntegrityError, fun, "Udało mi się wstawić pracownika z niepoprawnym telefonem")

        def test_tel_no_4(self):
            def fun(*args):
                student = self.create_pracownik()
                student.tel_no = "22 432-AA-BB"
                self.session.add(student)
                self.session.flush()
            self.assertRaises(IntegrityError, fun, "Udało mi się wstawić pracownika z niepoprawnym telefonem")

        def test_tel_no_5(self):
            def fun(*args):
                student = self.create_pracownik()
                student.tel_no = "22234-12-12"
                self.session.add(student)
                self.session.flush()
            self.assertRaises(IntegrityError, fun, "Udało mi się wstawić pracownika z niepoprawnym telefonem")

        def test_inserts_into_student_inserts_into_osoba(self):
            s = self.create_student()
            self.session.add(s)
            self.session.flush()
            o = self.session.query(Osoba).filter(Osoba.id==s.id).first()
            self.assertEqual(o.name, s.name)
            self.assertEqual(s.surname, o.surname)
            self.assertEqual(s.gender, s.gender)

        def test_inserts_into_pracownik_inserts_into_osoba(self):
            s = self.create_pracownik()
            self.session.add(s)
            self.session.flush()
            o = self.session.query(Osoba).filter(Osoba.id==s.id).first()
            self.assertEqual(o.name, s.name)
            self.assertEqual(s.surname, o.surname)
            self.assertEqual(s.gender, s.gender)


