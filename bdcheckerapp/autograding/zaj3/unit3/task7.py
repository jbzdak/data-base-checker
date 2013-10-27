import random
from sqlalchemy.orm import Query
from units.unit3.meta.orm import PracaDyplomowa
from sqlalchemy.exc import IntegrityError

from .util import NewDatabaseTaskChecker, Zaj3TestSuite, Zaj23askChecker


class TaskChecker(Zaj23askChecker):

    task_no = 7

    display_stdout = True

    class TestSuite(Zaj3TestSuite):

        def test_create_prace_dyplomowe(self):
            studenci = [self.create_student() for _ in range(4)]
            pracownicy = [self.create_pracownik() for _ in range(4)]
            for s in studenci:
                self.session.add(s)
            for p in pracownicy:
                self.session.add(p)
            self.session.flush()
            for ii in range(2):
                pd_list, student = self.create_praca_dyplomowa(studenci,
                                                               pracownicy)

                studenci.remove(student)
                for pd in pd_list:
                    self.session.add(pd)
                    self.session.flush()

        def test_praca_dyplomowa_student_fk(self):
            student = self.create_student()
            self.session.add(student)
            pracownik = self.create_pracownik()
            self.session.add(pracownik)
            self.session.flush()
            def fun():
                pd_list, _ = self.create_praca_dyplomowa([student], [pracownik])
                pd_list[0].student_id = random.choice(list(range(10000)))
                self.session.add(pd_list[0])
                self.session.flush()
            self.assertRaises(IntegrityError, fun)

        def test_praca_dyplomowa_pracownik_fk(self):
            student = self.create_student()
            self.session.add(student)
            pracownik = self.create_pracownik()
            self.session.add(pracownik)
            self.session.flush()
            def fun():
                pd_list, _ = self.create_praca_dyplomowa([student], [pracownik])
                pd_list[0].promotor_id = random.choice(list(range(10000)))
                self.session.add(pd_list[0])
                self.session.flush()
            self.assertRaises(IntegrityError, fun)

        def test_praca_dyplomowa_cascades_student(self):
            student = self.create_student()
            self.session.add(student)
            pracownik = self.create_pracownik()
            self.session.add(pracownik)
            self.session.flush()
            pd_list, _ = self.create_praca_dyplomowa([student], [pracownik])
            for pd in pd_list:
                self.session.add(pd)
                self.session.flush()
            # self.session.expunge()

            self.session.delete(student)
            self.session.flush()
            self.session.expire_all()

            prace_dyplomowe = list(Query(PracaDyplomowa, self.session).filter(
                PracaDyplomowa.student_id == student.id
            ))

            self.assertEqual(len(prace_dyplomowe), 0, "Po usunięciu studenta w bazie danych dalej są jego prace dyplomowe")

        def test_praca_dyplomowa_cascades_pracownik(self):
            student = self.create_student()
            self.session.add(student)
            pracownik = self.create_pracownik()
            self.session.add(pracownik)
            self.session.flush()
            pd_list, _ = self.create_praca_dyplomowa([student], [pracownik])
            for pd in pd_list:
                self.session.add(pd)
                self.session.flush()

            self.session.delete(pracownik)
            self.session.flush()
            self.session.expire_all()

            prace_dyplomowe = list(Query(PracaDyplomowa, self.session).filter(
                PracaDyplomowa.student_id == student.id
            ))

            for pd in prace_dyplomowe:
                self.assertIsNone(pd.promotor_id, "Kolumna pracownik_id po usunięciu pracownika powinna być nullem")