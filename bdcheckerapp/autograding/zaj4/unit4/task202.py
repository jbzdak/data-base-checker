from .util import Zaj4askChecker, Zaj41TestSuite

__author__ = 'jb'

class TaskChecker(Zaj4askChecker):

    task_no = 202
    display_stdout = False


    class TestSuite(Zaj41TestSuite):
        def test_move_praca_dyplomowa(self):

            original = list(self.session.execute("""
SELECT pd.tytul, pd.type, s.name, p.surname
    FROM "PRACA_DYPLOMOWA" pd, "STUDENT" s, "PRACOWNIK" p
    WHERE pd.student_id = s.id AND pd.promotor_id = p.id
    ORDER BY pd.tytul, pd.type, s.name, p.surname;
            """))

            self.close_session()
            self.load_migration()
            self.reset_session()

            migrated = list(self.session.execute("""
SELECT pd.tytul, pd.type, s.name, p.surname
    FROM "PRACA_DYPLOMOWA" pd, "STUDENT" s, "PRACOWNIK" p
    WHERE pd.student_id = s.id AND pd.promotor_id = p.id
    ORDER BY pd.tytul, pd.type, s.name, p.surname;
            """))

            self.assertEqual(original, migrated, "Test w którym wybieram dane z tabel STUDDENT i PRACOWNIK oraz PRACA_DYPLOMOWA")

            migrated_2 = list(self.session.execute("""
SELECT pd.tytul, pd.type, s.name, p.surname
    FROM "PRACA_DYPLOMOWA" pd, "OSOBA" s, "OSOBA" p
    WHERE pd.student_id = s.id AND pd.promotor_id = p.id
    ORDER BY pd.tytul, pd.type, s.name, p.surname;
            """))

            self.assertEqual(original, migrated_2, "Test w którym wybieram dane z tabeli OSOBA i PRACA_DYPLOMOWA")


