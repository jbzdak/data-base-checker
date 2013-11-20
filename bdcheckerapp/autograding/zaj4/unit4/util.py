
from ...zaj3.unit3.util import *
from .orm import singletable


class Zaj4askChecker(NewDatabaseTaskChecker):

    ECHO = True
    unit_no = 4
    display_stdout = True

    def create_test_suite(self):
        suite = super().create_test_suite()
        return suite


class Zaj4TestSuite(SessionTest):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        load_script(
            os.path.join(os.path.dirname(__file__), "create-schema.sql"),
            cls.db_name, cls.db_name)

        session = cls.sessionmaker()
        try:
            studenci = [create_student() for _ in range(random.randint(50, 75))]
            pracownicy = [create_pracownik() for _ in range(random.randint(10, 20))]
            for s in studenci:
                session.add(s)
            for p in pracownicy:
                session.add(p)
            session.flush()
            for ii in range(20):
                pd_list, student = create_praca_dyplomowa(studenci,
                                                                pracownicy)
                studenci.remove(student)
                for pd in pd_list:
                    session.add(pd)
                    session.flush()
            session.commit()
        finally:
            session.close()


STUDENT_TYPE = 'type:stud'

PRACOWNIK_TYPE = 'type:prac'

def random_osoba(*args):
    from .orm import singletable
    osoba = singletable.Osoba()
    osoba.gender = random.choice((0, 1))
    osoba.name = random_name()
    osoba.surname = random_surname()
    return osoba

def random_osoba_student(*args):
    osoba = random_osoba()
    osoba.type = STUDENT_TYPE
    osoba.message = random_sentence()
    osoba.status = random_status()
    return osoba

def random_osoba_pracownik(*args):
    osoba = random_osoba()
    osoba.type = PRACOWNIK_TYPE
    osoba.tel_no = random_tel_no()
    return osoba


class Zaj41TestSuite(Zaj4TestSuite):

    STUDENT_TYPE = STUDENT_TYPE
    PRACOWNIK_TYPE = PRACOWNIK_TYPE

    random_osoba_student = random_osoba_student
    random_osoba_pracownik = random_osoba_pracownik

    OldPracownik = singletable.Pracownik
    OldStudent = singletable.Student
    Osoba = singletable.Osoba

    @classmethod
    def load_migration(cls):
        if not "script" in cls.kwargs:
            raise ValueError("Proszę podać skrypt stawiający bazę danych jako argument --script")
        try:
            load_result = load_script(StringIO(cls.kwargs['script']), cls.db_name, cls.db_name)
            pattern = '='*30 + '\nPSQL output\n' + '='*30 + '\n'
            cls.additional_output_list.append(pattern + load_result.decode('utf-8') + pattern)
        except SubprocessError as e:
            pattern = '='*30 + '\nPSQL error\n' + '='*30 + '\n'
            cls.additional_output_list.append(pattern + e.output.decode('utf-8') + pattern)


class Zaj42TestSuite(Zaj4TestSuite):

    create_student = create_student
    create_pracownik = create_pracownik


    STUDENT_TYPE = STUDENT_TYPE
    PRACOWNIK_TYPE = PRACOWNIK_TYPE

    OldPracownik = singletable.Pracownik
    OldStudent = singletable.Student

    @classmethod
    def load_migration(cls):
        if not "script" in cls.kwargs:
            raise ValueError("Proszę podać skrypt stawiający bazę danych jako argument --script")
        try:
            load_result = load_script(StringIO(cls.kwargs['script']), cls.db_name, cls.db_name)
            pattern = '='*30 + '\nPSQL output\n' + '='*30 + '\n'
            cls.additional_output_list.append(pattern + load_result.decode('utf-8') + pattern)
        except SubprocessError as e:
            pattern = '='*30 + '\nPSQL error\n' + '='*30 + '\n'
            cls.additional_output_list.append(pattern + e.output.decode('utf-8') + pattern)

