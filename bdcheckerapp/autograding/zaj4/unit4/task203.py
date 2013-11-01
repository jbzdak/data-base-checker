from .util import Zaj4askChecker, Zaj41TestSuite

__author__ = 'jb'


class TaskChecker(Zaj4askChecker):

    task_no = 203
    display_stdout = False


    class TestSuite(Zaj41TestSuite):

        @classmethod
        def setUpClass(cls):
            super().setUpClass()
            cls.load_migration()

        def test_tables(self):
            expected = [
                "OSOBA", "TAG", "PRACA_DYPLOMOWA", "PRACOWNIK", "STUDENT"
            ]

            self.assert_tables_are(expected, "Niepotrzebne tabele")

        def test_columns_osoba(self):
            expected = """
             gender
 id
 name
surname""".split()

            self.assert_table_columns("OSOBA", expected, "Niepotrzebne kolumny w tabeli osoba")

        def test_columns_student(self):
            expected = """
             gender
 id
 name
 message
 status
surname""".split()

            self.assert_table_columns("STUDENT", expected, "Niepotrzebne kolumny w tabeli student")

        def test_columns_pracownik(self):
            expected = """
             gender
 id
 name
 tel_no
surname""".split()

            self.assert_table_columns("PRACOWNIK", expected, "Niepotrzebne kolumny w tableli pracownik")