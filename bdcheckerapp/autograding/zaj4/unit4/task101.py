from .util import Zaj4askChecker, Zaj41TestSuite

class TaskChecker(Zaj4askChecker):

    task_no = 101
    display_stdout = False

    class TestSuite(Zaj41TestSuite):

        ROLLBACK = True

        def test_move_to_osoba(self):

            orig_cols = [
                self.OldPracownik.name,
                self.OldPracownik.surname,
                self.OldPracownik.gender,
                self.OldPracownik.tel_no
            ]

            original_pracownik = list(self.session.query(*orig_cols).order_by(*orig_cols).all())

            self.close_session()
            self.load_migration()
            self.reset_session()

            migrated_cols = [
                self.Osoba.name,
                self.Osoba.surname,
                self.Osoba.gender,
                self.Osoba.tel_no
            ]

            migrated_pracownik = list(
                self.session.query(*migrated_cols)
                .filter(self.Osoba.type == self.PRACOWNIK_TYPE)
                .order_by(*migrated_cols).all()
            )

            self.assertEqual(original_pracownik, migrated_pracownik, "DOkonuje zapyrania wybierającego pracowników ze starego i nowego scheamtu. Wyniki są różne, a powiny być takie same")



