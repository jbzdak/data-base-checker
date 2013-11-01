from .util import Zaj4askChecker, Zaj41TestSuite

__author__ = 'jb'

class TaskChecker(Zaj4askChecker):

    task_no = 102
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
    FROM "PRACA_DYPLOMOWA" pd, "OSOBA" s, "OSOBA" p
    WHERE pd.student_id = s.id AND pd.promotor_id = p.id
        AND s.type = 'type:stud' AND p.type = 'type:prac'
    ORDER BY pd.tytul, pd.type, s.name, p.surname;
            """))

            self.assertEqual(original, migrated, "Dokonuje wyboru pracy dyplomowej i danych autora i promotora ze starego i nowego schematu. Wyniki są od siebie różne, a powinny być takie same. ")


