
from .util import Zaj3TestSuite, Zaj23askChecker


class TaskChecker(Zaj23askChecker):

    task_no = 4

    display_stdout = True

    class TestSuite(Zaj3TestSuite):


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
