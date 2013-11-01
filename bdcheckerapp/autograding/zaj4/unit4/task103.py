from .util import Zaj4askChecker, Zaj41TestSuite

class TaskChecker(Zaj4askChecker):

    task_no = 103
    display_stdout = False


    class TestSuite(Zaj41TestSuite):

        @classmethod
        def setUpClass(cls):
            super().setUpClass()
            cls.load_migration()

        def test_tables(self):
            expected = [
                "OSOBA", "TAG", "PRACA_DYPLOMOWA"
            ]

            self.assert_tables_are(expected, "Zbędne tabele w schemacie")

        def test_columns(self):
            expected = """
             gender
 id
 message
 name
 status
 surname
 tel_no
 type""".split()

            self.assert_table_columns("OSOBA", expected, "Zbędne kolumny w schemacie")




