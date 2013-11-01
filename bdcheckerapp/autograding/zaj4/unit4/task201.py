from .util import Zaj4askChecker, Zaj42TestSuite

class TaskChecker(Zaj4askChecker):

    task_no = 201
    display_stdout = False

    class TestSuite(Zaj42TestSuite):

        ROLLBACK = True

        def test_move(self):

            orig_cols = [
                self.OldPracownik.name,
                self.OldPracownik.surname,
                self.OldPracownik.gender,
                self.OldPracownik.tel_no
            ]

            original = list(self.session.query(*orig_cols).order_by(*orig_cols).all())

            self.close_session()
            self.load_migration()
            self.reset_session()

            migrated = list(self.session.query(*orig_cols).order_by(*orig_cols).all())

            self.assertEqual(original, migrated, "Niepoprawna migracja pracowników do nowego schematu")

