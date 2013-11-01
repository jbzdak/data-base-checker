from .util import Zaj4askChecker, Zaj41TestSuite

from . import task103, task100

class TaskChecker(Zaj4askChecker):

    task_no = 104
    display_stdout = False


    class TestSuite(Zaj41TestSuite):


        def test_mega(self):
            orig_cols = [
                self.OldPracownik.name,
                self.OldPracownik.surname,
                self.OldPracownik.gender,
                self.OldPracownik.tel_no
            ]

            original_osoby = list(self.session.query(*orig_cols).order_by(*orig_cols).all())

            original_prace = list(self.session.execute("""
SELECT pd.tytul, pd.type, s.name, p.surname
    FROM "PRACA_DYPLOMOWA" pd, "STUDENT" s, "PRACOWNIK" p
    WHERE pd.student_id = s.id AND pd.promotor_id = p.id
    ORDER BY pd.tytul, pd.type, s.name, p.surname;
            """))

            self.close_session()
            self.load_migration()
            self.reset_session()

            migrated_cols = [
                self.Osoba.name,
                self.Osoba.surname,
                self.Osoba.gender,
                self.Osoba.tel_no
            ]

            migrated_osoby = list(
                self.session.query(*migrated_cols)
                .filter(self.Osoba.type == self.PRACOWNIK_TYPE)
                .order_by(*migrated_cols).all()
            )

            self.assertEqual(original_osoby, migrated_osoby)

            migrated_prace = list(self.session.execute("""
SELECT pd.tytul, pd.type, s.name, p.surname
    FROM "PRACA_DYPLOMOWA" pd, "OSOBA" s, "OSOBA" p
    WHERE pd.student_id = s.id AND pd.promotor_id = p.id
        AND s.type = 'type:stud' AND p.type = 'type:prac'
    ORDER BY pd.tytul, pd.type, s.name, p.surname;
            """))

            self.assertEqual(original_prace, migrated_prace)

            task103.TaskChecker.TestSuite.test_tables(self)
            task103.TaskChecker.TestSuite.test_columns(self)

            task100.TaskChecker.TestSuite.test_check_gender_contrtaint_pracownik(self)
            self.reset_session()
            task100.TaskChecker.TestSuite.test_check_gender_constraint_student(self)
            self.reset_session()
            task100.TaskChecker.TestSuite.test_check_insert_pracownik(self)
            self.reset_session()