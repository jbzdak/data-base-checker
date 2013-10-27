__author__ = 'jb'

from .util import NewDatabaseTaskChecker, Zaj3TestSuite, Zaj23askChecker


class TaskChecker(Zaj23askChecker):

    task_no = 2

    display_stdout = True

    class TestSuite(Zaj3TestSuite):

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




