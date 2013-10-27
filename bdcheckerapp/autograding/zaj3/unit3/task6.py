from .util import Zaj3TestSuite, Zaj23askChecker


class TaskChecker(Zaj23askChecker):

    task_no = 6

    display_stdout = True

    class TestSuite(Zaj3TestSuite):

        def test_create_employees(self):
            for _ in range(3):
                st = self.create_pracownik()
                self.session.add(st)
                self.session.flush()

        def test_create_students(self):
            for _ in range(3):
                st = self.create_student()
                self.session.add(st)
                self.session.flush()

        def test_create_prace_dyplomowe(self):
            studenci = [self.create_student() for _ in range(100)]
            pracownicy = [self.create_pracownik() for _ in range(10)]
            for s in studenci:
                self.session.add(s)
            for p in pracownicy:
                self.session.add(p)
            self.session.flush()
            for ii in range(20):
                pd_list, student = self.create_praca_dyplomowa(studenci,
                                                                pracownicy)
                studenci.remove(student)
                for pd in pd_list:
                    self.session.add(pd)
                    self.session.flush()

