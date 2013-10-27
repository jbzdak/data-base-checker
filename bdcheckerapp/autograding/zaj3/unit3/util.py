from io import StringIO
from operator import attrgetter
import os
from sqlalchemy.orm import sessionmaker
from bdchecker import db_utils
from bdchecker.api import NewDatabaseTaskChecker, SessionTest
from units.unit3.meta.orm import Base
from bdchecker.db_utils import load_script
from units.unit3.meta.data import TAGS, TITLE
from units.unit3.meta.orm import Student, Pracownik, PracaDyplomowa
import random

DIRNAME = os.path.split(__file__)[0]

NAMES = []
SURNAMES = []

__SENTENCES="""
The approval contracts the degree.
The shake orchestrates the bizarre twist.
The blue son confers the leather.
The industry prepares the responsible relation.
The company communicates the design.
The pain surpasss the special place.
The goofy paste persuades the view.
The request spearheads the effect.
The glamorous disgust strategizes the person.
The motion entertains the chief butter.
The vigorous base originates the side.
The skinny thought restores the division.
The behavior employs the placid secretary.
The hellish copper eliminates the answer.
The zany body addresss the polish.
The far-flung stage augments the feeling.
The country uphelds the thing.
The authority stages the sort.
The organisation simulates the unsuitable size.
The fact straightens the man.
The stimulating act detects the rain.
The intelligent sort discriminates the limit.
The mushy rain sorts the room.
The division leads the average laugh.
The adjustment applys the structure.
The perfect bit recognizes the family.
The macabre structure installs the current.
The mysterious paste transports the manager.
The itchy form launchs the rate.
The agreement tests the body.
The rhythm diversifys the uninterested impulse.
The quality collates the owner.
The daughter uncovers the river.
The oil combines the slip.
The shame filters the distance.
The decision distributes the concerned stretch.
The wandering roll details the opinion.
The draconian print prepares the sea.
The point raises the walk.
The music aides the obtainable bit.
The surprise photographs the wine.
The late paper mobilizes the part.
The week facilitates the motion.
The literate record displays the debt.
The unique attraction conducts the vessel.
The field exercises the kind fight.
The blood heads the theory.
The twist schedules the uninterested belief.
The six sign conserves the quality.
The sense uncovers the part.
The company quotes the tough night.
The mind integrates the numberless credit.
The back saves the roll.
The brass equips the phobic offer.
The minute recruits the stretch.
The spooky profit controls the meat.
The meal narrates the rabid work.
The profit instructs the necessary river.
The madly rice commences the place.
The smoke estimates the experience.
The needy part contracts the noise.
The shocking change oversaws the profit.
The womanly country approves the stretch.
The attraction discriminates the many vessel.
The act enlarges the upbeat order.
The religion increases the fight.
The punishment attracts the expert.
"""

SENTENCES = __SENTENCES.split('\n')

del __SENTENCES

with open(os.path.join(DIRNAME, "data", "imiona_all.txt")) as f:
    for line in f:
        NAMES.append(line.strip())

with open(os.path.join(DIRNAME, "data", "nazwiska.txt")) as f:
    for line in f:
        SURNAMES.append(line.strip())


class Zaj23askChecker(NewDatabaseTaskChecker):

    ECHO = True

    unit_no = 3

    display_stdout = True


def random_name():
    return random.choice(NAMES)


def random_surname():
    return random.choice(SURNAMES)


def random_sentence():
    return random.choice(SENTENCES)


def random_status():
    return random.choice(list(filter(lambda x:x.key.startswith("status"), TAGS))).key


def random_tel_no():
    return "22 234-{}{}-{}{}".format(*[
        random.choice(list(range(10))) for _ in range(4)
    ])

def create_student(*args):
    st = Student()
    st.name = random.choice(NAMES)
    st.surname = random.choice(SURNAMES)
    st.message = random.choice(SENTENCES)
    st.status = random_status()
    st.gender = random.choice([0, 1])
    return st

def create_pracownik(*args):
    pr = Pracownik()
    pr.name = random.choice(NAMES)
    pr.surname = random.choice(SURNAMES)
    pr.gender = random.choice([0, 1])
    pr.tel_no = random_tel_no()
    return pr

def create_praca_dyplomowa(studenci, pracownicy):
    pd_list = []
    typy = map(attrgetter("key"),
            filter(lambda x: x.key.startswith("praca:"), TAGS))
    student = random.choice(studenci)


    for type in typy:
        pd = PracaDyplomowa()
        pd.type = type
        pd.tytul = random.choice(TITLE)
        pracownik = random.choice(pracownicy)
        pd.student_id = student.id
        pd.promotor_id = pracownik.id
        pd_list.append(pd)

    return pd_list, student


class Zaj3TestSuite(SessionTest):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        if not "script" in cls.kwargs:
            raise ValueError("Proszę podać skrypt stawiający bazę danych jako argument --script")
        load_script(StringIO(cls.kwargs['script']), cls.db_name, cls.db_name)

    create_student = create_student

    create_pracownik = create_pracownik

    def create_praca_dyplomowa(self, studenci, pracownicy):
        pd_list = []
        typy = map(attrgetter("key"),
                filter(lambda x: x.key.startswith("praca:"), TAGS))
        student = random.choice(studenci)


        for type in typy:
            pd = PracaDyplomowa()
            pd.type = type
            pd.tytul = random.choice(TITLE)
            pracownik = random.choice(pracownicy)
            pd.student_id = student.id
            pd.promotor_id = pracownik.id
            pd_list.append(pd)

        return pd_list, student


def set_up_engine(engine):
    Base.metadata.create_all(engine)

    sess = sessionmaker(bind=engine)

    session = sess()
    try:
        for t in TAGS:
            session.add(t)
        session.flush()
        pracownicy = []
        studenci = []
        for ii in range(50):
            prac = create_pracownik()
            pracownicy.append(prac)
            session.add(prac)
        for ii in range(50):
            stud = create_student()
            studenci.append(stud)
            session.add(stud)
        session.flush()
        for ii in range(25):
            stud = studenci.pop()
            for p in create_praca_dyplomowa([stud], pracownicy)[0]:
                session.add(p)
        session.commit()


    finally:
        session.close()